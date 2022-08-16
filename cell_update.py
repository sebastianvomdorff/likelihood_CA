import numpy as np


def cell_update_moore(row, column, rows_total, columns_total, neighbors, lattice_frozen):

    # create working copy from lattice
    current_cell = lattice_frozen[row, column].copy()

    # Browse through cells of the Moore neighborhood and update cell
    for delta_row in neighbors:
        for delta_column in neighbors:
            current_neighbor = [row + delta_row, column + delta_column]
            # Check for boundaries of lattice
            if (current_neighbor[0] >= 0) and (current_neighbor[0] < rows_total):
                if (current_neighbor[1] >= 0) and (current_neighbor[1] < columns_total):
                    if lattice_frozen[current_neighbor[0], current_neighbor[1]] > current_cell:
                        current_cell = current_cell + 1
    return current_cell


def cell_update_moore_without(row, column, rows_total, columns_total, neighbors, lattice_frozen):

    # create working copy from lattice
    current_cell = lattice_frozen[row, column].copy()

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
                            current_cell = current_cell + 1
    return current_cell


def cell_update_von_neumann(row, column, rows_total, columns_total, neighbors, lattice_frozen):

    # create working copy from lattice
    current_cell = lattice_frozen[row, column].copy()

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
                            current_cell = current_cell + 1
    return current_cell