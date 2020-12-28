#!/usr/bin/env python3

from helper.gen_img import gen_img
from helper.print_img import print_img
from helper.gen_date_string import gen_date_string


# Settings
fontname = './fonts/VeraMoBd.ttf'    # Font
img_fraction = 0.8           # use 80% of the max. size
model = 'QL-700'             # Printer model
label = 'd24'                # Label model
device = '/dev/usb/lp0'      #


# Generate image
img = gen_img(gen_date_string(), label, img_fraction, fontname)

# Print image
print_img(img, model, label, device)