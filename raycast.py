# Execute 2D ray-casting/ray-tracing using the Bresenham algorithm

import numpy as np
import config


def ray_cast(map, ego_x, ego_y):
    [y_size, x_size] = map.shape
    x_start = ego_x - 1
    y_start = ego_y - 1

    # print("map_size: ", map.shape)

    # initialize field-of-view map with all cells as not considered yet ("2")
    fov = np.ones((y_size, x_size)) * 2

    # Mark the static structure as not visible ("0") in FOV map
    fov[map == config.cell_blocked] = 0

    # print("y, x start: ", y_start, x_start)
    # print("y, x size: ", y_size, x_size)
    # Set ego position as visible ("1")
    fov[y_start, x_start] = 1

    # Divide map in four quarters to speed up processing
    # Top left quarter
    for y_end in range(y_start):
        for x_end in range(x_start):
            if fov[y_end, x_end] == 2:
                visible = 1

                dx = abs(x_end - x_start)
                dy = -abs(y_end - y_start)
                error = dx + dy

                if x_start < x_end:
                    sx = 1
                else:
                    sx = -1

                if y_start < y_end:
                    sy = 1
                else:
                    sy = -1

                x = x_start
                y = y_start

                while (x != x_end) or (y != y_end):
                    fov[y, x] = visible
                    error2 = 2 * error
                    if error2 > dy:
                        error = error + dy
                        x = x + sx
                    if error2 < dx:
                        error = error + dx
                        y = y + sy
                    if map[y, x] == config.cell_blocked:
                        visible = 0

                fov[y_end, x_end] = visible

    # Top right quarter
    for y_end in range(y_start):
        for x_end in range(x_size - 1, x_start - 1, -1):
            if fov[y_end, x_end] == 2:
                visible = 1

                dx = abs(x_end - x_start)
                dy = -abs(y_end - y_start)
                error = dx + dy

                if x_start < x_end:
                    sx = 1
                else:
                    sx = -1

                if y_start < y_end:
                    sy = 1
                else:
                    sy = -1

                x = x_start
                y = y_start

                while (x != x_end) or (y != y_end):
                    fov[y, x] = visible
                    error2 = 2 * error
                    if error2 > dy:
                        error = error + dy
                        x = x + sx

                    if error2 < dx:
                        error = error + dx
                        y = y + sy

                    if map[y, x] == config.cell_blocked:
                        visible = 0

                fov[y_end, x_end] = visible

    # Bottom left quarter
    for y_end in range(y_size - 1, y_start - 1, -1):
        for x_end in range(x_start):
            if fov[y_end, x_end] == 2:
                visible = 1

                dx = abs(x_end - x_start)
                dy = -abs(y_end - y_start)
                error = dx + dy

                if x_start < x_end:
                    sx = 1
                else:
                    sx = -1

                if y_start < y_end:
                    sy = 1
                else:
                    sy = -1

                x = x_start
                y = y_start

                while (x != x_end) or (y != y_end):
                    fov[y, x] = visible
                    error2 = 2 * error
                    if error2 > dy:
                        error = error + dy
                        x = x + sx

                    if error2 < dx:
                        error = error + dx
                        y = y + sy

                    if map[y, x] == config.cell_blocked:
                        visible = 0

                fov[y_end, x_end] = visible

    # Bottom right quarter
    for y_end in range(y_size - 1, y_start - 1, -1):
        for x_end in range(x_size - 1, x_start - 1, -1):
            if fov[y_end, x_end] == 2:
                visible = 1

                dx = abs(x_end - x_start)
                dy = -abs(y_end - y_start)
                error = dx + dy

                if x_start < x_end:
                    sx = 1
                else:
                    sx = -1

                if y_start < y_end:
                    sy = 1
                else:
                    sy = -1

                x = x_start
                y = y_start

                while (x != x_end) or (y != y_end):
                    fov[y, x] = visible
                    error2 = 2 * error
                    if error2 > dy:
                        error = error + dy
                        x = x + sx

                    if error2 < dx:
                        error = error + dx
                        y = y + sy

                    if map[y, x] == config.cell_blocked:
                        visible = 0

                fov[y_end, x_end] = visible

    return fov
