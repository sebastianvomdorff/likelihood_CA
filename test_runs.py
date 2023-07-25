import config
import main
import csv
import time

start_time = time.time()

header = [
    "Test case",
    "Velocity type",
    "Vehicle velocity",
    "Pedestrian velocity",
    "Memory",
    "Ego velocity cut-off",
    "Pedestrian density",
]

with open("test_cases.csv", "w", encoding="UTF8") as test_cases:
    writer = csv.writer(test_cases)

    # write the header
    writer.writerow(header)


header2 = [
    "Safety violations",
    "Simulation loops",
    "Total collisions",
    "Simulation time",
]

with open("test_results.csv", "w", encoding="UTF8") as test_results:
    writer = csv.writer(test_results)

    # write the header
    writer.writerow(header2)

iteration = 0
sim_type = "Stochastic"
for config.v_vehicle in [5 / 3.6, 10 / 3.6]:
    print("Vehicle speed: ", config.v_vehicle)
    for ped_speed_stoch in [[1.65, 1.0], [1.3, 0.3], [1.0, 0.2]]:
        config.ped_speed_mean = ped_speed_stoch[0]
        config.ped_spd_std_dev = ped_speed_stoch[1]
        print("Pedestrian speed: ", ped_speed_stoch)
        for config.memory in [0, 1]:
            print("Using memory:", config.memory)
            for config.v_ego_cut_off in [0, 1]:
                print("Velocity cut-off: ", config.v_ego_cut_off)
                for config.pedestrians_per_sqm in [0.04, 0.005]:
                    print("Pedestrain density: ", config.pedestrians_per_sqm)
                    iteration = iteration + 1
                    print("Test case: ", iteration)

                    data = [
                        iteration,
                        sim_type,
                        config.v_vehicle,
                        ped_speed_stoch,
                        config.memory,
                        config.v_ego_cut_off,
                        config.pedestrians_per_sqm,
                    ]

                    with open("test_cases.csv", "a", encoding="UTF8") as test_cases:
                        writer = csv.writer(test_cases)

                        # write the header
                        writer.writerow(data)

                    main.main()


sim_type = "Fixed"
fixed_speed = 1
for config.v_vehicle in [5 / 3.6, 10 / 3.6]:
    print("Vehicle speed: ", config.v_vehicle)
    for config.ped_speed_fixed in [1, 1.5, 2.0]:
        print("Pedestrian speed: ", config.ped_speed_fixed)
        for config.memory in [0, 1]:
            print("Using memory:", config.memory)
            for config.v_ego_cut_off in [0, 1]:
                print("Velocity cut-off: ", config.v_ego_cut_off)
                for config.pedestrians_per_sqm in [0.04, 0.005]:
                    print("Pedestrain density: ", config.pedestrians_per_sqm)
                    iteration = iteration + 1
                    print("Test case: ", iteration)

                    data = [
                        iteration,
                        sim_type,
                        config.v_vehicle,
                        config.ped_speed_fixed,
                        config.memory,
                        config.v_ego_cut_off,
                        config.pedestrians_per_sqm,
                    ]

                    with open("test_cases.csv", "a", encoding="UTF8") as test_cases:
                        writer = csv.writer(test_cases)

                        # write the header
                        writer.writerow(data)

                    main.main()

end_time = time.time()

total_minutes_elapsed = (end_time - start_time) / 60

print("All simulation cases done in ", config.dt, "ms steps")
print("This took ", total_minutes_elapsed, "minutes.")
