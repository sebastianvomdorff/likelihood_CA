import numpy as np
import matplotlib.pyplot as plt
from cellular_automaton import cellular_automaton
from count_to_likelihood_mapping import likelihood_mapping
from pedestrian_density_overlay import ped_density_overlay
from safety_eval import safety_eval
from map_tools import restore_map, slice_map_fov
from fixed_speed import fixed_speed_eval
from find_waypoint_at_time import find_waypoint_at_time

import config


def assess_freespace(
    lattice,
    ped_density_dist,
    trajectory_time,
    trajectory,
    likelihhood_bins,
    ego_x,
    ego_y,
    speed_list,
):
    if config.slicing:
        # cut out relevant part of map
        [
            map_slice,
            top,
            bottom,
            left,
            right,
        ] = slice_map_fov(lattice, ego_x, ego_y)
    else:
        map_slice = lattice

    # Propagate the occupied space with the cellular automaton
    if config.output:
        print(
            "Simulation horizon: ",
            config.sim_steps,
            "sim_steps *",
            config.dt,
            "ms =",
            config.simulation_horizon,
            "ms",
        )
    lattice_intermediate = cellular_automaton(map_slice.copy(), config.sim_steps_drive)
    if config.debug_lattice_intermediate:
        print(
            "Image shows the intermediate extrapolation after ",
            config.drive_time,
            "ms.",
        )
        plt.imshow(lattice_intermediate)
        plt.show()

    lattice_propagated = cellular_automaton(
        lattice_intermediate.copy(), config.sim_steps_brake
    )
    if config.debug_lattice_propagated:
        print(
            "Image shows the intermediate extrapolation after ",
            config.simulation_horizon,
            "ms.",
        )
        plt.imshow(lattice_propagated)
        plt.show()

    if config.slicing:
        # Restore relevant part of map
        memory = restore_map(
            lattice.copy(), lattice_intermediate, top, bottom, left, right
        )
        lattice_propagated = restore_map(
            lattice.copy(), lattice_propagated, top, bottom, left, right
        )
    else:
        memory = lattice_intermediate

    if config.v_ego_cut_off:
        v_ego_index = (np.abs(speed_list[:, 1] - config.v_vehicle)).argmin()
        lattice = np.where(lattice_propagated < v_ego_index, 0, lattice_propagated)
        if config.debug_cut_off:
            print(
                "The propagation map after removing all entries beyond the ego speed:"
            )
            plt.imshow(lattice_propagated)
            plt.show()

    # ca_prop = lattice_propagated.copy()
    # ca_prop[lattice_propagated == -1] = 200
    # ca_prop[ego_y, ego_x] = config.sim_steps
    # plt.imshow(ca_prop)
    # plt.show()
    # plt.savefig('/cellular_automaton_images/'+ str())
    # Calculate the likelihood distribution of pedestrians
    # considering their speed distribution
    if config.fixed_speed:
        ped_expct_lattice = fixed_speed_eval(lattice_propagated.copy(), speed_list)

    else:
        lattice_lklh_eval = likelihood_mapping(
            likelihhood_bins, lattice_propagated.copy()
        )
        # lkhl_dist_lattice = lattice_lklh_eval.copy()
        # lkhl_dist_lattice[ego_y, ego_x] = 2
        # plt.imshow(lkhl_dist_lattice)
        # plt.show()
        # plt.savefig('lklhd_dist_map_images/'+ str(trajectory_time) + "_wp_" + str(sim_time) + ".png")
        # Calculate the expected pedestrians per cell
        # considering the density distribution
        lattice_ped_eval = ped_density_overlay(
            lattice_lklh_eval.copy(), ped_density_dist
        )
        ped_expct_lattice = lattice_ped_eval.copy()
        ped_expct_lattice[ego_y, ego_x] = config.pedestrians_per_sqm

    total_collisions = np.sum(lattice_ped_eval[ego_y, ego_x]) * 4
    if config.output:
        print("Total collisions: ", total_collisions)

    if config.show_assessment:
        print(
            "Image shows the total expected pedestrians at the end of the simulation."
        )
        plt.imshow(ped_expct_lattice)
        plt.show()
    # plt.savefig('ped_expct_map_images/'+ str(trajectory_time) + "_wp_" + str(sim_time) + ".png")
    if config.output:
        print(
            "Closest waypoint at time: ",
            find_waypoint_at_time(
                trajectory, trajectory_time + (config.simulation_horizon / config.dt)
            ),
        )

    # Assess safety and record violations
    safety_violations = safety_eval(total_collisions)[0]

    if config.show_memory:
        plt.imshow(memory)
        plt.show()
    return memory, safety_violations
