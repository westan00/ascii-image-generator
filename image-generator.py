from PIL import Image
import numpy as np


def downscale(img):
    orig_width = img.width
    orig_height = img.height

    new_width = orig_width // 8
    new_height = orig_height // 8

    small_img = img.resize((new_width, new_height), resample=Image.BILINEAR)

    return small_img.resize((orig_width, orig_height), resample=Image.NEAREST)


def quantize_down(val):
    return np.floor(val / 255 * 9) * (255 // 9)


def main():
    img = Image.open("bird.jpg")
    img = downscale(img)
    img = img.convert("L")
    img = img.point(quantize_down)
    img.show()


main()
