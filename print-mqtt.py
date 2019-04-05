import datetime

from PIL import Image, ImageDraw, ImageFont

from brother_ql.raster import BrotherQLRaster
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send

import paho.mqtt.client as mqtt

# Settings
W, H = (236, 236)            # Label-size in pixel (may depend on the label model)
fontname = 'menlo.ttf'       # Font
img_fraction = 0.8           # use 80% of the max. size
model = 'QL-700'             # Printer model
label = 'd24'                # Label model
device = '/dev/usb/lp0'      # 
mqttip = '10.1.1.50'         # MQTT host

def do_print():
    # Generate text
    now = datetime.datetime.now()

    day = now.strftime('%d')       # 05
    month = now.strftime('%B')[:5] # first 5 characters of month 'Novem'
    year = now.strftime('%Y')      # 2019
    txt = day + '\n' + month + '\n' + year

    # Generate image
    img = Image.new('RGB', (W,H), color = 'white')
    draw = ImageDraw.Draw(img)

    fontsize = 1
    font = ImageFont.truetype(fontname, fontsize)
    (w, h) = draw.multiline_textsize(txt, font = font)
    while w < img_fraction * W and h < img_fraction * H:
        fontsize += 1
        font = ImageFont.truetype(fontname, fontsize)
        (w, h) = draw.multiline_textsize(txt, font = font)

    fontsize -= 1
    font = ImageFont.truetype(fontname, fontsize)

    draw.text(((W-w)/2,(H-h)/2), txt, font = font, fill = 'black', align = 'center') # place in center

    # Setup printer
    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = True

    convert(qlr, [img], label) # Convert
    send(qlr.data, device)     # Do the printing

# MQTT
def on_connect(client, userdata, flags, rc):
    print('connected')
    client.publish('dersimn/maintenance/LabelPrinter/online', 'true', retain=True)
    client.subscribe('dersimn/action/LabelPrinter/printdate')

def on_message(client, userdata, msg):
    print(msg.topic)
    if msg.topic == 'dersimn/action/LabelPrinter/printdate':
        do_print()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.will_set('dersimn/maintenance/LabelPrinter/online', 'false', retain=True)
client.connect(mqttip, 1883, 60)

client.loop_forever()