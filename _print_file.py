from gen_img import gen_img
from print_img import print_img
from gen_date_string import gen_date_string


# Settings
fontname = 'VeraMoBd.ttf'    # Font
img_fraction = 0.8           # use 80% of the max. size
label = 'd24'                # Label model


# Debug print to file
img = gen_img(gen_date_string(), label, img_fraction, fontname)
img.save('_debug.png')