import numpy as np

# eliminates all speed bin entries which are not allowed to propagate in the given timestep


def eligible_speed_bins(speed_bins, time_step, SoL):
    # Check which speeds are eligible to propagate, create boolean filter
    condition_filter = np.logical_not(time_step % np.round(SoL / speed_bins[:, 0]))
    # Multiply speeds and likelihoods with boolean filter
    eligible_bins = np.multiply(speed_bins, condition_filter[:, np.newaxis])
    return eligible_bins


# bins = np.array([[10, 0.05], [5, 0.1], [3.333, 0.2], [2.5, 0.3], [2, 0.35]])

# for steps in range(10):
#     prop_speeds = eligible_speed_bins(bins, steps, 10)
#     print(prop_speeds)
