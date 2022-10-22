def ped_density_overlay(likelihood_map, density_map):
    if likelihood_map.shape != density_map.shape:
        print("Density map does not match with CDF lattice dimensions!")
        return likelihood_map
    else:
        for i in range(likelihood_map.shape[0]):
            for k in range(likelihood_map.shape[1]):
                density_map[i, k] = density_map[i, k] * likelihood_map[i, k]
        return density_map
