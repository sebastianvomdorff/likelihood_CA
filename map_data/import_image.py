from xxlimited import new
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


image = Image.open('map_data/garage_populated_orig.png')

# summarize some details about the image
print(image.format)
print(image.size)
print(image.mode)

array_conversion = np.asarray(image)

new_image = array_conversion[149:997, 608:1456]

print(new_image.shape)

plt.imshow(new_image)
plt.show()

free_space = 3

static_obstacle = 2

omitt = 1