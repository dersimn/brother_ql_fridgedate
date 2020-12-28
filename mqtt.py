#!/usr/bin/env python3

import os
from io import BytesIO
import json
import base64
import paho.mqtt.client as mqtt

from helper.gen_img import gen_img
from helper.print_img import print_img
from helper.gen_date_string import gen_date_string


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
    client.subscribe(MQTT_PREFIX+'/set/preview')
    client.subscribe(MQTT_PREFIX+'/set/print/text')
    client.subscribe(MQTT_PREFIX+'/set/print/image')

def on_disconnect(client, userdata, rc):
    if rc == 0:
        client.publish(MQTT_PREFIX+'/online', 'false', retain=True)

def on_message(client, userdata, msg):
    print('mqtt <', msg.topic)

    # Preview
    if msg.topic == (MQTT_PREFIX+'/set/preview'):
        # Load JSON
        try:
            settings = json.loads(msg.payload)
        except ValueError as e:
            settings = {}

        # Generate Image
        img = gen_img(
            settings.get('text', gen_date_string()), 
            settings.get('label', DEAFULT_LABEL), 
            settings.get('size', DEFAULT_SIZE), 
            settings.get('font', DEFAULT_FONT)
        )

        # Publish
        client.publish(MQTT_PREFIX+'/status/preview', json.dumps({'data': image_to_base64_png(img)}))

    # Print Text
    if msg.topic == (MQTT_PREFIX+'/set/print/text'):
        # Generate image
        img = gen_img(gen_date_string(), DEAFULT_LABEL, DEFAULT_SIZE, DEFAULT_FONT)
        # Print image
        print_img(img, MODEL, DEAFULT_LABEL, DEVICE)

    # Print Image
    #if msg.topic == (MQTT_PREFIX+'/set/print/image'):
        # ...

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.will_set(MQTT_PREFIX+'/online', 'false', retain=True)
client.connect(MQTT_HOST, 1883, 60)

client.loop_forever()
