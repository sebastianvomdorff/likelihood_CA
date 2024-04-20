import config
import numpy as np
import matplotlib.pyplot as plt


def path_import(file):
    """This function imports a CSV file and
    interprets values >=1 as numbered waypoints.
    The coordinates of each waypoint are stored in the path array.
    It matches the patter, [waypoint_number, y, x]"""

    csv = np.loadtxt(file, delimiter=";")
    last_waypoint = int(np.max(csv))
    path = np.zeros([last_waypoint, 3])

    for i in range(0, last_waypoint):
        path[i, 0] = i + 1
        path[i, 1:3] = np.argwhere(csv == i + 1)
    return path


# Import map data
lattice = np.load(config.map_location)
lattice = lattice.astype(int)

plt.imshow(lattice)
plt.show()

path = path_import(config.path_location)
print(path)

path_in_map = lattice.copy()
for i in range(path.shape[0]):
    path_in_map[int(path[i, 1]), int(path[i, 2])] = 1

plt.imshow(path_in_map)
plt.show()
