from PIL import Image
from raycast import ray_cast
import matplotlib.pyplot as plt
import numpy as np


image = Image.open('map_data/garage_populated_orig.png')

# summarize some details about the image
print(image.format)
print(image.size)
print(image.mode)

array_conversion = np.asarray(image)

new_image = array_conversion[149:997, 608:1456]
new_image = new_image[:, :, 0].copy()

print(new_image.size)

print(new_image.shape)

plt.imshow(new_image)
plt.show()

free_space = 0

static_obstacle = -1

omitt = 1

normalized_img = new_image[::4, ::4]
normalized_img = normalized_img.astype(int)

print(normalized_img.shape)
normalized_img[normalized_img == 211] = free_space
normalized_img[normalized_img == 139] = free_space
normalized_img[normalized_img == 105] = static_obstacle
normalized_img[normalized_img == 46] = static_obstacle
normalized_img[normalized_img == 93] = static_obstacle
normalized_img[normalized_img == 99] = static_obstacle
normalized_img[normalized_img == 199] = static_obstacle

plt.imshow(normalized_img)
plt.show()

# save as npy for later import
np.save("map_data/garage_map_1", normalized_img)

# export to csv/txt based format with "," as separator
np.savetxt("map_data/garage_map_csv.csv", normalized_img, delimiter=",")

fov_map = ray_cast(normalized_img, 85, 94, static_obstacle)

plt.imshow(fov_map)
plt.show()
