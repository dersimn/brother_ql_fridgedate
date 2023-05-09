#!/usr/bin/env python3

import os
from io import BytesIO
import json
import base64
import paho.mqtt.client as mqtt
from PIL import Image
import re

from brother_ql.raster import BrotherQLRaster
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.devicedependent import label_type_specs, label_sizes, ROUND_DIE_CUT_LABEL

from helper.gen_img import gen_img
from helper.print_img import print_img
from helper.gen_date_string import gen_date_string
from helper.font_helpers import get_fonts


# Settings
DEFAULT_FONT    = os.getenv('DEAFULT_FONT_FILE', './fonts/VeraMoBd.ttf')
DEFAULT_SIZE    = float(os.getenv('IMG_SIZE', 0.8))
DEVICE          = os.getenv('USB_DEVICE', 'usb://0x04f9:0x2042/000H8Z154932')
MQTT_HOST       = os.getenv('MQTT_HOST',  '127.0.0.1')
MODEL           = os.getenv('MODEL', 'QL-700')
DEAFULT_LABEL   = os.getenv('DEAFULT_LABEL', 'd24')
MQTT_PREFIX     = os.getenv('MQTT_PREFIX', 'dersimn/LabelPrinter')

def image_to_base64_png(im):
    image_buffer = BytesIO()
    im.save(image_buffer, format="PNG")
    image_buffer.seek(0)
    b64_img = base64.b64encode(image_buffer.read())
    b64_img_str = str(b64_img, 'utf-8')
    return 'data:image/png;base64,' + b64_img_str

# MQTT
def on_connect(client, userdata, flags, rc):
    print('mqtt > connected')
    client.publish(MQTT_PREFIX+'/online', 'true', retain=True)

    client.publish(MQTT_PREFIX+'/status/fonts', json.dumps(get_fonts('./fonts')), retain=True)
    client.publish(MQTT_PREFIX+'/status/label-sizes', json.dumps([
        {
            'name': name,
            'friendly-name': label_type_specs[name]['name'], 
            'round': (label_type_specs[name]['kind'] in (ROUND_DIE_CUT_LABEL,)) # True if round label
        }
        for name in label_sizes
    ]), retain=True)

    client.subscribe(MQTT_PREFIX+'/set/print/text')
    client.subscribe(MQTT_PREFIX+'/set/print/image')

def on_disconnect(client, userdata, rc):
    if rc == 0:
        client.publish(MQTT_PREFIX+'/online', 'false', retain=True)

def on_message(client, userdata, msg):
    print('mqtt <', msg.topic)

    # Preview
    if msg.topic == (MQTT_PREFIX+'/set/print/text'):
        # Load JSON
        try:
            settings = json.loads(msg.payload)
        except ValueError as e:
            settings = {}

        text = settings.get('text', gen_date_string())
        label = settings.get('label', DEAFULT_LABEL)
        size = settings.get('size', DEFAULT_SIZE)
        font = settings.get('font', DEFAULT_FONT)

        # Generate Image
        img = gen_img(text, label, size, font)

        # Publish
        client.publish(MQTT_PREFIX+'/status/preview', json.dumps({
            'data': image_to_base64_png(img),
            'text': text,
            'label': label,
            'size': size,
            'font': font
        }))

    # Print Image
    if msg.topic == (MQTT_PREFIX+'/set/print/image'):
        # Load JSON
        try:
            obj = json.loads(msg.payload)

            b64_img = obj.get('data')
            label = obj.get('label', DEAFULT_LABEL)
        except ValueError as e:
            client.publish(MQTT_PREFIX+'/status/print/image', json.dumps({
                'status': 'error',
                'message': 'Invalid JSON sent.'
            }))
            return

        try:
            # Remove 'data:image/png;base64,' from beginning
            b64_img_data = re.sub('^data:image/.+;base64,', '', b64_img)

            # Load Image
            img = Image.open(BytesIO(base64.b64decode(b64_img_data)))

            # Setup Printer
            qlr = BrotherQLRaster(MODEL)
            qlr.exception_on_warning = True
            convert(qlr, [img], label, dither=True) # Convert
            status = send(qlr.data, DEVICE)         # Do the printing

            # Publish on success
            client.publish(MQTT_PREFIX+'/status/print/image', json.dumps({
                'status': 'success',
                'message': status,
                'data': b64_img
            }))
        except Exception as e:
            client.publish(MQTT_PREFIX+'/status/print/image', json.dumps({
                'status': 'error',
                'message': str(e)
            }))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.will_set(MQTT_PREFIX+'/online', 'false', retain=True)
client.connect(MQTT_HOST, 1883, 60)

client.loop_forever()
