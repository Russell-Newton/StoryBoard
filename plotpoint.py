import tkinter as tk
from tkinter import font

from constants import *
from utils import *


class PlotPoint(object):
    """
    A PlotPoint object represents a StoryBoard element you want to display on the screen.
    """

    def __init__(self, percent_time: float = 0, vertical: float = 0, plot_line: float = 0, point_type: str = None,
                 content: tuple = (), connects_to: tuple = (), override_width: float = None, override_height: float =
                 None, override_color: tuple = None):
        """
        :param percent_time: a proportion that corresponds to horizontal position.
        :param vertical: a proportion that corresponds to vertical position.
        :param plot_line: corresponds to color. Starts at 0.
        :param point_type: type of plot point (Pinch Point 1, Plot Point 2, etc.).
        :param content: a tuple of bullet points attributed to this PlotPoint.
        :param connects_to: a tuple of PlotPointConnections this PlotPoint points to.
        :param override_width: overrides the default width.
        :param override_height: override the default height.
        :param override_color: override the default color.
        """
        self.percent_time = percent_time
        self.vertical = vertical
        self.plot_line = plot_line
        self.point_type = point_type
        self.content = content
        self.connects_to = connects_to
        self.override_width = override_width
        self.override_height = override_height
        self.override_color = override_color
        self.shape = self.get_shape()
        self.arrows = self.get_arrows()

    def get_shape(self) -> dict:
        """
        :return: the parameters defining the PlotPoint's shape on the screen.
        """
        plot_start = int(math.floor(self.plot_line))
        plot_end = int(math.ceil(self.plot_line))

        if self.override_color is not None:
            color = self.override_color
        else:  # Interpolate between the defined plot colors
            color = interpolate_color(COLORS_LIST[plot_start], COLORS_LIST[plot_end], self.plot_line - plot_start)

        if self.override_width is None:
            width = PLOT_POINT_WIDTH
        else:
            width = self.override_width

        if self.override_height is None:
            height = PLOT_POINT_HEIGHT
        else:
            height = self.override_height

        x = SCREEN_WIDTH * self.percent_time
        y = SCREEN_HEIGHT * self.vertical

        return {'x': x,
                'y': y,
                'color': color,
                'points': {'x1': x,
                           'y1': y,
                           'x2': x + width,
                           'y2': y + height},
                }

    def get_arrows(self) -> list:
        """
        :return: the parameters defining the arrows coming from this PlotPoint.
        """
        x1, y1, x2, y2 = self.shape['points'].values()
        middle_points = (  # Bisecting points on each side
            ((x1 + x2) / 2, y1),
            (x2, (y2 + y1) / 2),
            ((x1 + x2) / 2, y2),
            (x1, (y2 + y1) / 2)
        )

        arrows = []

        for connection in self.connects_to:
            arrows.append(connection.get_arrows(self, middle_points))

        return arrows

    def render(self, canvas: tk.Canvas) -> tuple:
        """
        Render the PlotPoint onto a tk.Canvas.
        :param canvas: the canvas to render this PlotPoint onto.
        :return: the rendered objects.
        """
        x1, y1, x2, y2 = self.shape['points'].values()
        rectangle = canvas.create_rectangle(x1, y1, x2, y2, outline=from_rgb(self.shape['color']),
                                            width=PLOT_POINT_STROKE)

        # Place the label at the top of the rectangle
        label = canvas.create_text(((x1 + x2) / 2), y1 + PLOT_POINT_STROKE + LABEL_SIZE / 2, text=self.point_type,
                                   font=font.Font(family=FONT_FAMILY, size=LABEL_SIZE, underline=LABEL_UNDERLINE,
                                                  weight=LABEL_WEIGHT))

        # Center the text inside the rectangle
        text = canvas.create_text(((x1 + x2) / 2, (y1 + y2) / 2), text=add_bullets(
            self.content), width=PLOT_POINT_WIDTH - 2 * PLOT_POINT_STROKE, font=font.Font(family=FONT_FAMILY,
                                                                                          size=FONT_SIZE))

        # Render the arrows belonging to this PlotPoint
        arrows = []
        for arrow in self.arrows:
            c0, c1, c2, c3 = arrow['control_points']
            color_start, color_end = arrow['colors']

            # Generate arrow segments
            segments = cubic_bezier(c0, c1, c2, c3, ARROW_STEPS)
            # Interpolate colors to determine segment colors
            colors = [interpolate_color(color_start, color_end, n / ARROW_STEPS) for n in range(0, ARROW_STEPS)]
            for segment, i in zip(segments, range(0, len(segments))):
                x1, y1, x2, y2 = segment
                arrows.append(canvas.create_line(x1, y1, x2, y2, fill=from_rgb(colors[i]), width=ARROW_STROKE))

            # Set up arrow point
            point_left, point_right = arrow['point_angles']
            point_left_prime = offset_on_angle(c3, point_left, ARROW_POINT_LENGTH)
            point_right_prime = offset_on_angle(c3, point_right, ARROW_POINT_LENGTH)
            if ARROW_POINT_TYPE is "arrow":  # Generates an arrow like ->
                arrows.append(
                    canvas.create_line(c3[0], c3[1], point_left_prime[0], point_left_prime[1], fill=from_rgb(color_end),
                                       width=ARROW_STROKE))
                arrows.append(
                    canvas.create_line(c3[0], c3[1], point_right_prime[0], point_right_prime[1],
                                       fill=from_rgb(color_end), width=ARROW_STROKE))
            elif ARROW_POINT_TYPE is "triangle":  # Generates an arrow with a solid triangle point
                arrows.append(canvas.create_polygon((c3[0], c3[1], point_left_prime[0], point_left_prime[1],
                                                     point_right_prime[0], point_right_prime[1]),
                                                    fill=from_rgb(color_end)))
            else:  # No point
                continue

        canvas.pack()
        return rectangle, label, text, arrows


class PlotPointConnection(object):
    """
    A PlotPointConnection defines parameters for an arrow between two PlotPoints.
    """

    def __init__(self, plot_point: PlotPoint, override_i: int = None, override_j: int = None,
                 override_point_angle: float = None, rotate_point: float = 0):
        """
        :param plot_point: the PlotPoint the arrow point to.
        :param override_i: override for the arrow's start position. 0 is top, 1 is right, 2 is bottom, 3 is left.
        :param override_j: override for the arrow's end position. 0 is top, 1 is right, 2 is bottom, 3 is left.
        :param override_point_angle: override the arrow's point's open angle (in degrees).
        :param rotate_point: rotate the arrow's point (in degrees).
        """
        self.plot_point = plot_point
        self.override_i = override_i
        self.override_j = override_j
        self.override_point_angle = override_point_angle
        self.rotate_point = rotate_point

    def get_arrows(self, master: PlotPoint, middle_points: tuple) -> dict:
        """
        Determine the parameters for the arrow between master and self.plot_point.
        :param master: the PlotPoint to start the arrow at.
        :param middle_points: the locations of possible starting positions. This enhances efficiency.
        :return: a dict with the arrow parameters.
        """
        x1_prime, y1_prime, x2_prime, y2_prime = self.plot_point.shape['points'].values()
        middle_points_prime = (
            ((x2_prime + x1_prime) / 2, y1_prime),
            (x2_prime, (y2_prime + y1_prime) / 2),
            ((x2_prime + x1_prime) / 2, y2_prime),
            (x1_prime, (y2_prime + y1_prime) / 2)
        )

        # Optimize the start and end points for the smallest distance. Override as necessary.
        start, end, i, j = closest_two_points(middle_points, middle_points_prime)
        if self.override_i is not None:
            start = middle_points[self.override_i]
            i = self.override_i
        if self.override_j is not None:
            end = middle_points_prime[self.override_j]
            j = self.override_j

        # Prepare point triangle
        if self.override_point_angle is not None:
            angle = self.override_point_angle
        else:
            angle = ARROW_POINT_ANGLE
        point_left, point_right = math.radians(angle + self.rotate_point), -math.radians(angle - self.rotate_point)

        dx = middle_points_prime[j][0] - middle_points[i][0]
        dy = middle_points_prime[j][1] - middle_points[i][1]

        # Find c1
        if i == 0:
            control_point_start = offset(middle_points[i], (0, -abs(dy)))
        elif i == 1:
            control_point_start = offset(middle_points[i], (abs(dx), 0))
        elif i == 2:
            control_point_start = offset(middle_points[i], (0, abs(dy)))
        else:
            control_point_start = offset(middle_points[i], (-abs(dx), 0))

        # Find c2
        if j == 0:
            control_point_end = offset(middle_points_prime[j], (0, -abs(dy)))
            point_left -= math.pi / 2
            point_right -= math.pi / 2
        elif j == 1:
            control_point_end = offset(middle_points_prime[j], (abs(dx), 0))
        elif j == 2:
            control_point_end = offset(middle_points_prime[j], (0, abs(dy)))
            point_left += math.pi / 2
            point_right += math.pi / 2
        else:
            control_point_end = offset(middle_points_prime[j], (-abs(dx), 0))
            point_left += math.pi
            point_right += math.pi

        # Start and end colors
        colors = master.shape['color'], self.plot_point.shape['color']

        return {'control_points': (start, control_point_start, control_point_end, end), 'colors': colors,
                'point_angles': (point_left, point_right)}


def get_plot_points() -> tuple:
    """
    Populate this with your PlotPoints to add to the screen.
    :return: the PlotPoints you generate.
    """
    yikes = PlotPoint(.6, .5, 0, "Climax", ("Oop", "That's a climax"), (), override_color=(0, 0, 0))
    a = PlotPoint(.4, .02, 1, "Pinch Point 1", ("Yeeteeeeeetttt", "Skeet"),
                  (PlotPointConnection(yikes, override_j=3, rotate_point=40),), override_color=(255, 127, 0))
    b = PlotPoint(.25, .33, 2, "Plot Point 1", ("Oh ho!", "Nerd.", "Oof", "Oh", "Hello"),
                  (PlotPointConnection(a), PlotPointConnection(yikes)),
                  override_height=300)
    c = PlotPoint(.1, .75, 3, "Something", (), (PlotPointConnection(a, 1, 2), PlotPointConnection(b, 1, 2)))
    return yikes, a, b, c
