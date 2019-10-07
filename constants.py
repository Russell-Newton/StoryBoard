# Screen constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# PlotPoints constants
PLOT_LINES = 5  # Should be equal to or less than len(COLORS_LIST)
PLOT_POINT_WIDTH = 300  # Default PlotPoint width
PLOT_POINT_HEIGHT = 200  # Default PlotPoint height
PLOT_POINT_STROKE = 10  # Stroke width for PlotPoints
ARROW_POINT_ANGLE = 20  # Degrees       # The angle to fan the arrow point out to
ARROW_POINT_LENGTH = 30  # Length of the slanted sides of the point
ARROW_POINT_TYPE = "triangle"  # "triangle", "arrow", or "none". Defaults to "none"
ARROW_STROKE = 5  # Stroke width for arrows
ARROW_STEPS = 25000  # Interpolation steps for arrows

# Settings for the PlotPoint text
FONT_FAMILY = "Comic Sans MS"
FONT_SIZE = 13  # Content font size
LABEL_SIZE = 18  # Point_type font size
LABEL_WEIGHT = "bold"
LABEL_UNDERLINE = 1  # 1 for True, 0 for False

# Colors
COLORS_LIST = [
    (255, 0, 0),  # Red
    (255, 0, 255),  # Magenta
    (0, 0, 255),  # Blue
    (0, 255, 0),  # Green
    (255, 127, 0),  # Orange
    (255, 255, 0)]  # Yellow

# Miscellaneous
SAVE_IMAGE = True
