# likelihood_CA

This version simply counts +1 in every cell if a neighboring cell has a higher count.
With knowledge about the simulation time, time step-width and the geometry of the lattice, each count can be mapped to an equivalent speed.
Utilizing a "survival function", 1-cdf (cumulative distribution function), a likelihood of a pedestrian having entered that cell can be mapped to the given speeds.

Multiplying the likelihood of a pedestrian having reached a cell with a distribution of expected pedestrians per area unit allows to estimate the occupancy of a cell as pedestrians/cell.
