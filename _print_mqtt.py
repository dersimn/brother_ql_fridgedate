from gen_img import gen_img
from print_img import print_img
from gen_date_string import gen_date_string

import paho.mqtt.client as mqtt


# Settings
fontname = 'VeraMoBd.ttf'    # Font
img_fraction = 0.8           # use 80% of the max. size
model = 'QL-700'             # Printer model
label = 'd24'                # Label model
device = '/dev/usb/lp0'      # 
mqttip = '10.1.1.50'         # MQTT host


# MQTT
def on_connect(client, userdata, flags, rc):
    print('connected')
    client.publish('dersimn/maintenance/LabelPrinter/online', 'true', retain=True)
    client.subscribe('dersimn/action/LabelPrinter/printdate')

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