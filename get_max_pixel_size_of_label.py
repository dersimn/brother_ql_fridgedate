from brother_ql.labels import ALL_LABELS

def get_max_pixel_size_of_label(label):
    for i in ALL_LABELS:
        if i.identifier == label:
            return i.dots_printable