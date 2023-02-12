import numpy as np
import matplotlib.pyplot as plt


path1 = np.loadtxt('map_data/garage_map_path1_2_csv.csv', delimiter=';')
print(path1)

plt.imshow(path1)
plt.show()