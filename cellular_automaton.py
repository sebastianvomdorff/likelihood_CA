import math
import numpy as np
import config

def cellular_automaton(lattice, time_steps):

    # determine all cells distances in the range
    neighbors = np.arange(-config.neighborhood_range, config.neighborhood_range + 1)

    # Extract length and width of lattice
    rows_total = lattice.shape[0]
    columns_total = lattice.shape[1]

    # Get squareroot of 2
    sqrt2 = math.sqrt(2)

    for step in range(time_steps + 1):
        lattice_frozen = lattice.copy()

        # Move through the lattice
        if ((step % (sqrt2+1)) < 1):
            for row in range(rows_total):
                for column in range(columns_total):
                    if lattice_frozen[row, column] != config.cell_blocked:
                        lattice[row, column] = cell_update_moore(row, column, rows_total, columns_total, neighbors, lattice_frozen)
        else:
            for row in range(rows_total):
                for column in range(columns_total):
                    if lattice_frozen[row, column] != config.cell_blocked:
                        lattice[row, column] = cell_update_von_neumann(row, column, rows_total, columns_total, neighbors, lattice_frozen)

    return lattice


def cell_update_moore(row, column, rows_total, columns_total, neighbors, lattice_frozen):

    # create working copy from lattice
    current_cell = lattice_frozen[row, column].copy()
    propagation_flag = 0

    # Browse through cells of the Moore neighborhood and update cell
    for delta_row in neighbors:
        for delta_column in neighbors:
            current_neighbor = [row + delta_row, column + delta_column]
            # Check for boundaries of lattice
            if (current_neighbor[0] >= 0) and (current_neighbor[0] < rows_total):
                if (current_neighbor[1] >= 0) and (current_neighbor[1] < columns_total):
                    if lattice_frozen[current_neighbor[0], current_neighbor[1]] > current_cell:
                        propagation_flag = 1
    if propagation_flag == 1:
        current_cell = current_cell + 1
    return current_cell


def cell_update_moore_without(row, column, rows_total, columns_total, neighbors, lattice_frozen):

    # create working copy from lattice
    current_cell = lattice_frozen[row, column].copy()
    propagation_flag = 0

    # Browse through neighboring cells of the von Neumann neighborhood and update cell
    for delta_row in neighbors:
        for delta_column in neighbors:
            current_neighbor = [row + delta_row, column + delta_column]
            # Check for boundaries of lattice
            if (current_neighbor[0] >= 0) and (current_neighbor[0] < rows_total):
                if (current_neighbor[1] >= 0) and (current_neighbor[1] < columns_total):
                    # select von Neumann neighborhood cells in range
                    if (current_neighbor[0]) != row and (current_neighbor[1] != column):
                        if lattice_frozen[current_neighbor[0], current_neighbor[1]] > current_cell:
                            propagation_flag = 1
    if propagation_flag == 1:
        current_cell = current_cell + 1
    return current_cell


def cell_update_von_neumann(row, column, rows_total, columns_total, neighbors, lattice_frozen):

    # create working copy from lattice
    current_cell = lattice_frozen[row, column].copy()
    propagation_flag = 0

    # Browse through neighboring cells of the von Neumann neighborhood and update cell
    for delta_row in neighbors:
        for delta_column in neighbors:
            current_neighbor = [row + delta_row, column + delta_column]
            # Check for boundaries of lattice
            if (current_neighbor[0] >= 0) and (current_neighbor[0] < rows_total):
                if (current_neighbor[1] >= 0) and (current_neighbor[1] < columns_total):
                    # select von Neumann neighborhood cells in range
                    if (current_neighbor[0]) == row or (current_neighbor[1] == column):
                        if lattice_frozen[current_neighbor[0], current_neighbor[1]] > current_cell:
                            propagation_flag = 1
    if propagation_flag == 1:
        current_cell = current_cell + 1
    return current_cell
