import math


def from_rgb(rgb: tuple) -> str:
    """
    Translate rgb tuple into tkinter color string.
    """
    return "#%02x%02x%02x" % rgb


def interpolate(start: float, end: float, t: float) -> float:
    """
    Perform linear interpolation.
    :param start: the starting point.
    :param end: the ending point.
    :param t: the proportion to interpolate to.
    """
    return (1 - t) * start + t * end


def interpolate_color(start: tuple, end: tuple, n: float) -> tuple:
    """
    Perform linear interpolation on colors.
    :param start: starting rgb tuple.
    :param end: ending rgb tuple.
    :param n: proportion to interpolate to.
    """
    return int(interpolate(start[0], end[0], n)), int(interpolate(start[1], end[1], n)), int(interpolate(start[2],
                                                                                                         end[2], n))


def distance(point1: tuple, point2: tuple) -> float:
    """
    :return: the distance between point1 and point2.
    """
    return math.sqrt((point1[1] - point2[1]) ** 2 + (point1[0] - point2[0]) ** 2)


def closest_two_points(points1: tuple, points2: tuple) -> tuple:
    """
    :return: the closest two points (one from points1 and one from points2) and their corresponding indexes.
    (point1, point2, i, j)
    """
    closest_overall = points1[0], points2[0], 0, 0

    # Iterate through every combination of points1 with points2
    for point, i in zip(points1, range(0, len(points1))):
        closest = points2[0], 0
        for point2, j in zip(points2, range(0, len(points2))):
            if distance(point, point2) < distance(point, closest[0]):
                closest = point2, j
        if distance(closest[0], point) < distance(closest_overall[0], closest_overall[1]):
            closest_overall = point, closest[0], i, closest[1]

    return closest_overall


def offset(point: tuple, d_point: tuple) -> tuple:
    """
    :return: point offset by d_point.
    """
    return point[0] + d_point[0], point[1] + d_point[1]


def offset_on_angle(point: tuple, angle: float, radius: float) -> tuple:
    """
    :return: point offset by radius along angle.
    """
    return point[0] + math.cos(angle) * radius, point[1] + math.sin(angle) * radius


def add_bullets(text: tuple) -> str:
    """
    Create a new line preceded by a bullet for every entry in text.
    :return: a single string that can be used to create text.
    """
    if len(text) == 0:  # no text so no bullets
        return ''
    parts = []
    for line in text:  # for each line
        parts.extend(['\u2022', line, '\n'])  # prepend bullet and re append newline removed by split
    return ''.join(parts)


def cubic_bezier(c0: tuple, c1: tuple, c2: tuple, c3: tuple, steps: int) -> list:
    """
    Perform cubic bezier interpolation.
    :return: a list of point pairs defining segments to make up the designated curve.
    """
    segments = []

    def interp(t: float, dim: int) -> tuple:
        x = (1 - t) ** 3 * c0[dim] + 3 * (1 - t) ** 2 * t * c1[dim] + 3 * (1 - t) * t ** 2 * c2[dim] + t ** 3 * c3[dim]
        return x

    segments.append((c0[0], c0[1], interp(1 / steps, 0), interp(1 / steps, 1)))
    for i in range(1, steps):
        segments.append((
            interp((i - 1) / steps, 0),  # This helps smooth the curve
            interp((i - 1) / steps, 1),
            interp((i + 1) / steps, 0),
            interp((i + 1) / steps, 1)))

    return segments
