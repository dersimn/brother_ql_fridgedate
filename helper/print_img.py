from brother_ql.raster import BrotherQLRaster
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send


def print_img(img, model, label, device):
    # Setup printer
    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = True

    convert(qlr, [img], label, dither=True) # Convert
    return send(qlr.data, device)                  # Do the printing
