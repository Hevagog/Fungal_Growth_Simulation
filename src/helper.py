import math
import numpy as np

#
SCALING_FACTOR = 1.e7


def calculate_points_on_line(origin_coordinates, tip_coordinates):
    # Bresenham's line algorithm. Returns a list of points on a line between two points.
    points = []
    x1, y1 = int(origin_coordinates[0]), int(origin_coordinates[1])
    x2, y2 = int(tip_coordinates[0]), int(tip_coordinates[1])

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    x, y = x1, y1
    x_inc = 1 if x2 > x1 else -1
    y_inc = 1 if y2 > y1 else -1

    if dx > dy:
        p = 2 * dy - dx
        for _ in range(dx):
            points.append((x, y))
            if p >= 0:
                y += y_inc
                p -= 2 * dx
            x += x_inc
            p += 2 * dy
    else:
        p = 2 * dx - dy
        for _ in range(dy):
            points.append((x, y))
            if p >= 0:
                x += x_inc
                p -= 2 * dy
            y += y_inc
            p += 2 * dx

    points.append((x, y))
    return points


@staticmethod
def l2_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


@staticmethod
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


@staticmethod
def cinera_extention_Rate(length):
    return 0.178 + 1/(77800 * math.exp(-0.195 * length)+3.92)


@staticmethod
def acutatum_extention_Rate(length):
    return 0.178 + 0.092/(9096 * math.exp(-0.326 * length) + 0.589)


@staticmethod
def stoloifenr_extention_Rate(length):
    return 0.58 + 1/(80.15 * math.exp(-0.236 * length)+1.202)


extention_functions = [cinera_extention_Rate,
                       acutatum_extention_Rate,
                       stoloifenr_extention_Rate]
