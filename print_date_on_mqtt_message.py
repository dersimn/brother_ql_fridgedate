#!/usr/bin/env python3

import os
import paho.mqtt.client as mqtt

from helper.gen_img import gen_img
from helper.print_img import print_img
from helper.gen_date_string import gen_date_string


# Settings
fontname     = os.getenv('FONT_FILE', 'VeraMoBd.ttf')
img_fraction = float(os.getenv('IMG_SIZE', 0.8))
device       = os.getenv('USB_DEVICE', '/dev/usb/lp0')
mqttip       = os.getenv('MQTT_HOST',  '127.0.0.1')
model        = os.getenv('BROTHER_MODEL')
label        = os.getenv('BROTHER_LABEL')


# MQTT
def on_connect(client, userdata, flags, rc):
    print('connected')
    client.publish('dersimn/maintenance/LabelPrinter/online', 'true', retain=True)
    client.subscribe('dersimn/action/LabelPrinter/printdate')

def on_disconnect(client, userdata, rc):
    if rc == 0:
        client.publish('dersimn/maintenance/LabelPrinter/online', 'false', retain=True)

def on_message(client, userdata, msg):
    print(msg.topic)
    if msg.topic == 'dersimn/action/LabelPrinter/printdate':
        # Generate image
        img = gen_img(gen_date_string(), label, img_fraction, fontname)
        # Print image
        print_img(img, model, label, device)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.will_set('dersimn/maintenance/LabelPrinter/online', 'false', retain=True)
client.connect(mqttip, 1883, 60)

client.loop_forever()