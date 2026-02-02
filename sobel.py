from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
from scipy.ndimage import gaussian_filter
import numpy as np


def downscale(img):
    orig_width = img.width
    orig_height = img.height

    new_width = orig_width // 8
    new_height = orig_height // 8

    small_img = img.resize((new_width, new_height), resample=Image.BOX)

    return small_img.resize((orig_width, orig_height), resample=Image.BOX)


img = np.array(Image.open("circle.jpg").convert("L")).astype(np.float32)

G_x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])

G_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

img_smoothed = gaussian_filter(img, sigma=1)

grad_x = ndimage.correlate(img_smoothed, G_x)
grad_y = ndimage.correlate(img_smoothed, G_y)

magnitude = np.sqrt(grad_x**2 + grad_y**2)

theta = (np.arctan2(grad_y, grad_x) + np.pi) / (2 * np.pi)

height, width = theta.shape

red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
yellow = [255, 255, 0]

print(magnitude.max())

colorized_theta = np.zeros((height, width, 3), dtype=np.uint8)

threshold = 8

for i in range(height):
    for j in range(width):
        if magnitude[i, j] < threshold:
            colorized_theta[i, j] = [0, 0, 0]  # Make it Black
            continue

        val = theta[i, j]
        if (0.3125 < val < 0.4375) or (0.8125 < val < 0.9375):
            colorized_theta[i, j] = green
        elif (0.1875 <= val <= 0.3125) or (0.6875 <= val <= 0.8125):
            colorized_theta[i, j] = blue
        elif (0.0625 < val < 0.1875) or (0.5625 < val < 0.6875):
            colorized_theta[i, j] = yellow
        else:
            colorized_theta[i, j] = red

new = Image.fromarray(colorized_theta)

downscaled = downscale(new)

downscaled.show()
