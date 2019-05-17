from PIL import Image, ImageDraw, ImageFont

from get_max_pixel_size_of_label import get_max_pixel_size_of_label


def gen_img(txt, label, img_fraction=0.8, fontname='VeraMoBd.ttf'):
    W, H = get_max_pixel_size_of_label(label)

    # Generate image
    img = Image.new('L', (W,H), color='white')
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

    return img
