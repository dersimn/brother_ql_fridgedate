import json

from helper.font_helpers import get_fonts

FONTS = get_fonts('./fonts')

def list_fonts():
    for font_family_name in sorted(list(FONTS.keys())):
        for font_style in FONTS[font_family_name].keys():
            print(font_family_name, font_style)

def get_font_list():
    return {
        name: list(FONTS[name].keys())
        for name in sorted(list(FONTS.keys()))
    }

def get_font_path(font_family_name, font_style_name):
    try:
        if font_family_name is None or font_style_name is None:
            raise LookupError('Not enough arguments provided')
        font_path = FONTS[font_family_name][font_style_name]
    except KeyError:
        raise LookupError('Couln''t find the font & style')
    return font_path

if __name__ == '__main__':
    print('Available Fonts:')
    print(json.dumps(get_font_list()))
    print(json.dumps(FONTS))
    print('Get Front Path by Name:')
    print(get_font_path('Bitstream Vera Sans', 'Oblique'))
