from PIL import Image, ImageDraw, ImageFont
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


def asciify(img):
    ASCII = ["@", "Q", "O", "e", "o", "u", ";", ":", ".", " "]
    block = 8

    array = np.array(img)
    h, w = array.shape
    img = Image.new("L", (w, h), color=255)

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Menlo.ttc")

    for y in range(0, h, block):
        for x in range(0, w, block):
            y1, y2 = y, min(y + block, h)
            x1, x2 = x, min(x + block, w)

            block_pixels = array[y1:y2, x1:x2]
            avg = np.floor(np.mean(block_pixels))
            index = int(avg / 255 * (len(ASCII)))
            char = ASCII[index]

            draw.text((x, y), char, fill=0, font=font)

    return img


def main():
    img = Image.open("bird.jpg")
    img = downscale(img)
    img = img.convert("L")
    img = img.point(quantize_down)
    img = asciify(img)
    img.show()


if __name__ == "__main__":
    main()
