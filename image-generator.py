from PIL import Image


def test():
    im = Image.open("kolibri-os.png")
    return im


print(test())
