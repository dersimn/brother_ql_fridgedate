from PIL import Image
from print_img import print_img


# Settings
model = 'QL-700'             # Printer model
label = 'd24'                # Label model
device = '/dev/usb/lp0'      #


# Load image from file
img = Image.open('print_img.png')

# Print image
print_img(img, model, label, device)