import numpy as np
import matplotlib.pyplot as plt
from raycast import ray_cast
from cellular_automaton import cellular_automaton
from count_to_likelihood_mapping import likelihood_mapping
from pedestrian_density_overlay import ped_density_overlay
import config
import time


def drive_path(likelihhood_bins, ped_density_dist,  lattice, path, cell_speed):
    """ This function proceeds the vehicle along the path.
    The trajectory is generated and followed in intervals defined by the
    driving time until end"""
    global safety_violations
    safety_violations = 0
    trajectory = trajectory_generation(cell_speed, path)
    if config.output:
        print("Trajectory: ", trajectory)
    for trajectory_time in range(0, int(np.floor(trajectory[-1, 3])), int(config.drive_time)):
        proceed_trajectory(trajectory_time, trajectory, lattice, ped_density_dist, likelihhood_bins)
        # plt.savefig('path_images/' + str(trajectory_time) + '.png')
    print("Total safety violations: ", safety_violations)


def trajectory_generation(cell_speed, path):
    """ This function delivers the rounded time, when a cell is reached.
    The output array looks like [cell_number, y, x, time_stamp]"""

    time_stamps = path[:, 0]/cell_speed
    time_stamps = np.round(time_stamps, int(1/config.dt))
    path_size = path.shape
    trajectory = np.zeros([path_size[0], path_size[1]+1])
    trajectory[:, :-1] = path
    trajectory[:, -1] = time_stamps
    return trajectory


def proceed_trajectory(trajectory_time, trajectory, lattice, ped_density_dist, likelihhood_bins):
    # determine step of trajectory has been reached
    start_wp = find_waypoint_at_time(trajectory, trajectory_time)
    end_wp = find_waypoint_at_time(trajectory, trajectory_time + config.simulation_horizon)
    intermediate_wps = trajectory[start_wp:(end_wp + 1), 3]
    if config.output:
        print("Waypoints:", intermediate_wps)
        print("Trajectory step: ", start_wp)
        print("Trajectory time: ", trajectory_time)

    # determine own position
    ego_x = int(trajectory[start_wp, 2])
    ego_y = int(trajectory[start_wp, 1])
    if config.output:
        print("Ego position x, y: ", ego_x, ego_y)

    # cut out relevant part of map
    [map_slice, ego_x_adjusted, ego_y_adjusted] = slice_map(lattice.copy(), ego_x, ego_y)

    # Initialize map from point of view
    map_slice = init_map(map_slice, ego_x_adjusted, ego_y_adjusted)

    last_step = intermediate_wps[0]
    """
    # Extrapolate environmnent over given time horizon for each entered cell
    for step in intermediate_wps:
        sim_time = step - last_step
        map_slice = assess_freespace(map_slice, ped_density_dist, trajectory_time, sim_time, trajectory, likelihhood_bins, ego_x_adjusted, ego_y_adjusted)
        # plt.savefig('cellular_automaton_images/' + str(trajectory_time) + "_wp_" + str(step) + '.png')
        last_step = step
    """
    # Do the extrapolation in a single roll
    sim_time = config.simulation_horizon
    assess_freespace(map_slice, ped_density_dist, trajectory_time, sim_time, trajectory, likelihhood_bins, ego_x_adjusted, ego_y_adjusted)

def assess_freespace(lattice, ped_density_dist, trajectory_time, sim_time, trajectory, likelihhood_bins, ego_x, ego_y):
    # Propagate the occupied space with the cellular automaton
    sim_steps = int(sim_time/config.dt)
    if config.output:
        print("sim_time: ", sim_time)
    lattice_propagated = cellular_automaton(lattice.copy(), sim_steps)

    # ca_prop = lattice_propagated.copy()
    # ca_prop[lattice_propagated == -1] = 200
    # ca_prop[ego_y, ego_x] = config.sim_steps
    # plt.imshow(ca_prop)
    # plt.show()
    # plt.savefig('/cellular_automaton_images/'+ str())
    # Calculate the likelihood distribution of pedestrians
    # considering their speed distribution
    lattice_lklh_eval = likelihood_mapping(likelihhood_bins, lattice_propagated.copy())
    lkhl_dist_lattice = lattice_lklh_eval.copy()
    lkhl_dist_lattice[ego_y, ego_x] = 2
    # plt.imshow(lkhl_dist_lattice)
    # plt.show()
    # plt.savefig('lklhd_dist_map_images/'+ str(trajectory_time) + "_wp_" + str(sim_time) + ".png")
    # Calculate the expected pedestrians per cell
    # considering the density distribution
    lattice_ped_eval = ped_density_overlay(lattice_lklh_eval.copy(), slice_map(ped_density_dist, ego_x, ego_y)[0])
    ped_expct_lattice = lattice_ped_eval.copy()
    ped_expct_lattice[ego_y, ego_x] = 0.005
    if config.show_assessment:
        plt.imshow(ped_expct_lattice)
        plt.show()
    # plt.savefig('ped_expct_map_images/'+ str(trajectory_time) + "_wp_" + str(sim_time) + ".png")
    if config.output:
        print("Closest waypoint at time: ", find_waypoint_at_time(trajectory, trajectory_time + sim_time))

    total_collisions = np.sum(lattice_ped_eval[ego_y, ego_x])*4
    if config.output:
        print("collisions: ", total_collisions)
    collisions_per_second = safety_eval(total_collisions, sim_time)
    # print("Collisions per second: ", collisions_per_second)
    return lattice_propagated


def safety_eval(total_collisions, sim_time):
    global safety_violations
    if sim_time > 0:
        collisions_per_second = total_collisions / sim_time
        collisions_per_hour = collisions_per_second * 3600
    else:
        collisions_per_second = 0
        collisions_per_hour = 0

    safety_evaluation = "unsafe"
    if collisions_per_hour < config.safety_threshold:
        safety_evaluation = "safe"
    else:
        if config.output:
            print("Total estimated collisions: ", total_collisions, " in ", config.simulation_horizon, "seconds.")
            print("Equaling ", collisions_per_hour, " 1/hr.")
            print("The maneuver is ", safety_evaluation, " considering a threshold of ", config.safety_threshold, " 1/hr (ASIL C for random faults).")
        safety_violations = safety_violations + 1
        # time.sleep(2)

    return safety_evaluation, collisions_per_hour



def footprint_lookup(path, trajectory, time):
    """ returns the vehicles latest entered cells at a given time"""

    for i in (0, np.size(trajectory)[1]):
        if trajectory[i, 1] > time:
            latest = i-1
            break
    path_index = trajectory[latest, 0]
    ego_cells = np.where(path == path_index)
    return ego_cells


def find_waypoint_at_time(trajectory, time):
    """Returns the index of the trajectory waypoint that is closest to a given time.
    Note that the index starts counting from 0, while waypoints start at 1"""

    row_index = (np.abs(trajectory[:, 3] - time)).argmin()
    return row_index


def init_map(lattice, ego_x, ego_y):
    """This function calculates the field of view from a given position
    and initializes the blocked and empty cells.Cells outside the field
    of view that are not statically blocked are considered as occupied."""

    # Caluclate field of view in map from given ego positon
    fov_map = ray_cast(lattice, ego_x, ego_y)

    # Mark cells that are not blocked but outside of field of view as occupied
    lattice[lattice == config.cell_empty] = config.cell_occupied

    # Mark all cells within the FOV as empty
    lattice[fov_map == 1] = config.cell_empty

    if config.show_map_init:
        plot_lattice = lattice.copy()
        plot_lattice[lattice == config.sim_steps] = 3
        plot_lattice[ego_y, ego_x] = 2
        plt.imshow(plot_lattice)
        plt.show()

    return lattice


def slice_map(lattice, ego_x, ego_y):
    """Cuts out the relevant map area. Limits the considered map by the time
    the fastest human could travel over the projection horizon"""
    relevant_range = int(round((config.fastest_person + config.v_vehicle) * config.simulation_horizon / config.cell_size))
    top = max(ego_y - relevant_range + 1, 0)
    bottom = min(ego_y + relevant_range + 1, lattice.shape[0])
    left = max(ego_x - relevant_range + 1, 0)
    right = min(ego_x + relevant_range + 1, lattice.shape[1])

    slice = lattice[top:bottom, left:right]
    adjusted_x = ego_x - left
    adjusted_y = ego_y - top
    if config.output:
        print("Adjusted coordinates for map slice: ", adjusted_x, adjusted_y)
    return slice, adjusted_x, adjusted_y
