import numpy as np
import matplotlib.pyplot as plt


paths = np.loadtxt('map_data/garage_map_paths_csv.csv', delimiter=';')
print(paths)

plt.imshow(paths)
plt.show()
