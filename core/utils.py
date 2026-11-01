import numpy as np
import math


def calculate_angle(a, b, c):
    # """
    # Teen points se beech wale point (b) ka angle nikalta hai.
    # Jaise: kandha (a), kohni (b), kalai (c) -> kohni ka angle.
    # """
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = abs(np.degrees(radians))
    if angle > 180:
        angle = 360 - angle
    return angle


def angle_from_vertical(top, bottom):
    """Do points ke beech ka angle seedhi (vertical) line se. 0 = bilkul seedha."""
    dx = top[0] - bottom[0]
    dy = top[1] - bottom[1]
    return abs(math.degrees(math.atan2(dx, -dy)))