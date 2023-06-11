import numpy as np
import matplotlib.pyplot as plt
from cellular_automaton import cellular_automaton
from count_to_likelihood_mapping import likelihood_mapping
from pedestrian_density_overlay import ped_density_overlay
from safety_eval import safety_eval
from map_tools import restore_map, slice_map_fov, footprint_lookup
from fixed_speed import fixed_speed_eval
from find_waypoint_at_time import find_waypoint_at_time

import config


def assess_freespace(
    original_lattice,
    ped_density_dist,
    trajectory_step,
    trajectory,
    likelihhood_bins,
    ego_x,
    ego_y,
    speed_list,
    start_wp_idx,
    end_wp_idx,
    footprint_map,
):
    fragment_time_steps = trajectory[start_wp_idx : (end_wp_idx + 1), 3]

    fragment_time_steps_relative = fragment_time_steps - fragment_time_steps[0]

    simulation_time_steps = fragment_time_steps_relative

    if simulation_time_steps[-1] < config.sim_steps:
        simulation_time_steps = np.append(simulation_time_steps, config.sim_steps)
    elif simulation_time_steps[-1] > config.sim_steps:
        simulation_time_steps[-1] = config.sim_steps

    insert_idx = np.where(
        (simulation_time_steps[:-1] < config.sim_steps_drive)
        & (simulation_time_steps[1:] > config.sim_steps_drive)
    )[0]
    simulation_time_steps = np.insert(
        simulation_time_steps, insert_idx + 1, config.sim_steps_drive
    )

    if config.output:
        print("Absolute time-steps in trajectory fragment: ", fragment_time_steps)
        print(
            "Relative time-steps in trajectory fragment: ", fragment_time_steps_relative
        )
        print("Relative time-steps for the simulation: ", simulation_time_steps)

    simulation_end_step = trajectory_step + config.sim_steps
    if config.output:
        print("Simulation end point: ", simulation_end_step)

    safety_violations = 0
    memory = original_lattice
    passed_sim_time = 0
    iteration_index = 1
    lattice_intermediate = original_lattice

    for timeframe in simulation_time_steps[1:]:
        print("debug timeframe: ", timeframe)
        ego_x = int(trajectory[iteration_index, 2])
        ego_y = int(trajectory[iteration_index, 1])

        single_cell_sim_steps = int(timeframe - passed_sim_time)
        if config.slicing:
            # cut out relevant part of map
            [
                lattice_intermediate,
                top,
                bottom,
                left,
                right,
            ] = slice_map_fov(lattice_intermediate, ego_x, ego_y)

        print("debug: ", passed_sim_time)
        # Propagate the occupied space with the cellular automaton
        if config.output:
            print(
                "Simulation horizon: ",
                timeframe,
                "sim_steps *",
                config.dt,
                "ms =",
                timeframe * config.dt,
                "ms",
            )
        lattice_intermediate = cellular_automaton(
            lattice_intermediate.copy(), single_cell_sim_steps
        )
        if config.debug_lattice_intermediate:
            print(
                "Image shows the intermediate extrapolation after ",
                timeframe * config.dt,
                "ms.",
            )
            plt.imshow(lattice_intermediate)
            plt.show()

        if config.slicing:
            # Restore relevant part of map
            lattice_intermediate = restore_map(
                original_lattice.copy(),
                lattice_intermediate.copy(),
                top,
                bottom,
                left,
                right,
            )

        if timeframe == config.sim_steps_drive:
            memory = lattice_intermediate

        if config.v_ego_cut_off:
            v_ego_index = (np.abs(speed_list[:, 1] - config.v_vehicle)).argmin()
            lattice = np.where(
                lattice_intermediate < v_ego_index, 0, lattice_intermediate
            )
            if config.debug_cut_off:
                print(
                    "The propagation map after removing all entries beyond the ego speed:"
                )
                plt.imshow(lattice_intermediate)
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
            lattice_ped_eval = fixed_speed_eval(lattice_intermediate.copy(), speed_list)

        else:
            lattice_lklh_eval = likelihood_mapping(
                likelihhood_bins, lattice_intermediate.copy()
            )
            # lkhl_dist_lattice = lattice_lklh_eval.copy()
            # lkhl_dist_lattice[ego_y, ego_x] = 2
            # plt.imshow(lkhl_dist_lattice)
            # plt.show()
            # plt.savefig('lklhd_dist_map_images/'+ str(trajectory_step) + "_wp_" + str(sim_time) + ".png")
            # Calculate the expected pedestrians per cell
            # considering the density distribution
            lattice_ped_eval = ped_density_overlay(
                lattice_lklh_eval.copy(), ped_density_dist
            )

        ped_expct_lattice = lattice_ped_eval.copy()
        ped_expct_lattice[ego_y, ego_x] = config.pedestrians_per_sqm

        collisions = np.sum(
            lattice_ped_eval[
                footprint_lookup(footprint_map, start_wp_idx + iteration_index)
            ]
        )
        if config.output:
            print("Collisions: ", collisions)

        if config.debug_show_intermediate_assessment:
            print(
                "Image shows the total expected pedestrians at the end of the simulation."
            )
            plt.imshow(ped_expct_lattice)
            plt.show()
        # plt.savefig('ped_expct_map_images/'+ str(trajectory_step) + "_wp_" + str(sim_time) + ".png")
        if config.output:
            print(
                "Closest waypoint at time: ",
                find_waypoint_at_time(
                    trajectory,
                    trajectory_step + (config.simulation_horizon / config.dt),
                ),
            )

        # Assess safety and record violations
        if safety_eval(collisions, single_cell_sim_steps)[0]:
            safety_violations = 1

        # Record passed sim-time
        passed_sim_time = timeframe
        iteration_index = iteration_index + 1

    if config.show_extrapolation:
        print(
            "Image shows the total extrapolation after ",
            timeframe * config.dt,
            "ms.",
        )
        plt.imshow(lattice_intermediate)
        plt.show()

    if config.show_assessment:
        print(
            "Image shows the total expected pedestrians at the end of the simulation."
        )
        plt.imshow(ped_expct_lattice)
        plt.show()

    if config.show_memory:
        plt.imshow(memory)
        plt.show()
    return memory, safety_violations, collisions
