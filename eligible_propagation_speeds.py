import numpy as np


def eligible_speed_bins(speed_bins, time_step, SoL):
    """eliminates all speed bin entries which are not allowed to propagate
    in the given timestep"""
    # Check which speeds are eligible to propagate, create boolean filter
    condition_filter = np.logical_not(time_step % np.round(SoL / speed_bins[:, 0]))
    # Multiply speeds and likelihoods with boolean filter
    eligible_bins = np.multiply(speed_bins, condition_filter[:, np.newaxis])
    return eligible_bins
