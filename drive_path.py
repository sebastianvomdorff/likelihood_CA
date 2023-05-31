import numpy as np
import matplotlib.pyplot as plt
from map_tools import init_map, merge_memory_map
from assess_freespace import assess_freespace
from find_waypoint_at_time import find_waypoint_at_time
import config


def drive_path(
    likelihhood_bins, ped_density_dist, lattice, path, cell_speed, speed_list
):
    """This function proceeds the vehicle along the path.
    The trajectory is generated and followed in intervals defined by the
    driving time until end"""
    safety_violations = 0
    simulation_loops = 0
    trajectory = trajectory_generation(cell_speed, path)
    memory = np.where(lattice == 0, config.sim_steps, lattice)
    if config.output:
        print("Trajectory: ", trajectory)
    for trajectory_step in range(0, int(trajectory[-1, 3]), config.sim_steps_drive):
        [memory, new_safety_violations] = proceed_trajectory(
            trajectory_step,
            trajectory,
            lattice,
            ped_density_dist,
            likelihhood_bins,
            speed_list,
            memory,
        )
        safety_violations = safety_violations + new_safety_violations
        simulation_loops = simulation_loops + 1
        # plt.savefig('path_images/' + str(trajectory_step) + '.png')
    print(
        "Total safety violations: ",
        safety_violations,
        " in ",
        simulation_loops,
        " simulation steps.",
    )


def trajectory_generation(cell_speed, path):
    """This function delivers the rounded time, when a cell is reached.
    The output array looks like [cell_number, y, x, reached at sim_step]"""

    reached_at_sim_step = (path[:, 0] - 1) / cell_speed
    reached_at_sim_step = np.round(reached_at_sim_step)
    path_size = path.shape
    trajectory = np.zeros([path_size[0], path_size[1] + 1])
    trajectory[:, :-1] = path
    trajectory[:, -1] = reached_at_sim_step
    return trajectory


def proceed_trajectory(
    trajectory_step,
    trajectory,
    lattice,
    ped_density_dist,
    likelihhood_bins,
    speed_list,
    memory,
):
    # determine step of trajectory that has been reached
    start_wp_idx = find_waypoint_at_time(trajectory, trajectory_step)
    end_wp_idx = find_waypoint_at_time(
        trajectory, trajectory_step + int(config.sim_steps)
    )

    if config.output:
        print(
            "Trajectory fragment starts at waypoint index: ",
            start_wp_idx,
            "and ends on wapoint index ",
            end_wp_idx,
        )
        print("Which corresponds to time step:", trajectory[end_wp_idx, 3])
        print("Simulation start step: ", trajectory_step)
        print("Trajectory time: ", trajectory_step * config.dt * config.t_atomic, "s")

    # determine own position
    ego_x = int(trajectory[start_wp_idx, 2])
    ego_y = int(trajectory[start_wp_idx, 1])
    if config.output:
        print("Ego position x, y: ", ego_x, ego_y)

    # Initialize map from point of view
    input_lattice = init_map(lattice.copy(), ego_x, ego_y)

    if config.memory:
        input_lattice = merge_memory_map(input_lattice, memory)

    [memory, safety_violations] = assess_freespace(
        input_lattice,
        ped_density_dist,
        trajectory_step,
        trajectory,
        likelihhood_bins,
        ego_x,
        ego_y,
        speed_list,
        start_wp_idx,
        end_wp_idx,
    )

    """# Extrapolate environmnent over given time horizon for each entered cell
    for step in intermediate_wps:
        sim_time = step - last_step
        map_slice = assess_freespace(
            map_slice,
            ped_density_dist,
            trajectory_step,
            sim_time,
            trajectory,
            likelihhood_bins,
            ego_x_adjusted,
            ego_y_adjusted,
        )
        # plt.savefig('cellular_automaton_images/' + str(trajectory_step) + "_wp_" + str(step) + '.png')
        last_step = step"""
    return memory, safety_violations
