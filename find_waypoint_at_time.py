import numpy as np


def find_waypoint_at_time(trajectory, time):
    """Returns the index of the trajectory waypoint that is closest to a given
    time. Note that the index starts counting from 0, while waypoints start
    at 1"""

    row_index = (np.abs(trajectory[:, 3] - time)).argmin()
    return row_index
