import config


def safety_eval(total_collisions, sim_steps):
    global safety_violations
    # calculate simulation time in seconds
    sim_time = sim_steps * config.dt * config.t_atomic
    if sim_time > 0:
        collisions_per_second = total_collisions / sim_time
        collisions_per_hour = collisions_per_second * 3600
    else:
        collisions_per_second = 0
        collisions_per_hour = 0

    if collisions_per_hour < config.safety_threshold:
        safety_violation = 0
        safety_evaluation = "safe"
    else:
        safety_violation = 1
        safety_evaluation = "unsafe"
    if config.output:
        print(
            "Total estimated collisions: ",
            total_collisions,
            " in ",
            sim_time,
            "seconds.",
        )
        print("This equals ", collisions_per_hour, " 1/hr collisions.")
        print(
            "The maneuver is ",
            safety_evaluation,
            " considering a threshold of ",
            config.safety_threshold,
            " 1/hr (ASIL C for random faults).",
        )
        # time.sleep(2)

    return safety_violation, safety_evaluation, collisions_per_hour
