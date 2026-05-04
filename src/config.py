import manim

INTRO_DURATION = 2
ENTRY_DURATION = 0.5
TRANSITION_TIME = ENTRY_DURATION * (1 / 5)
WAIT_TIME = ENTRY_DURATION * (4 / 5)

CORNER_RADIUS = 0.3
RECTANGLE_BASE_CONFIG = {
    "fill_color": manim.ManimColor("#222"),
    "stroke_color": manim.GRAY,
    "stroke_width": 1,
    "fill_opacity": 1,
}

TITLE_FONT_SIZE = 128

NUMBER_FONT_SIZE = 48
NUMBER_RECTANGLE_CONFIG = {
    **RECTANGLE_BASE_CONFIG,
    "width": 1,
    "height": 1,
    "corner_radius": [0, 0, CORNER_RADIUS, 0],
}
NAME_FONT_SIZE = 72
NAME_RECTANGLE_CONFIG = {
    **RECTANGLE_BASE_CONFIG,
    "width": 11.75,
    "height": 1,
    "corner_radius": [0, CORNER_RADIUS, CORNER_RADIUS, 0],
}
NAME_Y_SHIFT = 0.07
CODE_FONT_SIZE = 36
CODE_RECTANGLE_CONFIG = {
    **RECTANGLE_BASE_CONFIG,
    "width": manim.config.frame_width - 2 * manim.DEFAULT_MOBJECT_TO_EDGE_BUFFER,
    "height": (
        manim.config.frame_height
        - 2 * manim.DEFAULT_MOBJECT_TO_EDGE_BUFFER
        - NAME_RECTANGLE_CONFIG["height"]
    ),
    "corner_radius": CORNER_RADIUS / 2,
    "stroke_opacity": 0,
    "fill_color": manim.ManimColor("#222").darker(0.75),
}
CODE_BLOCK_RECTANGLE_CONFIG = {
    **RECTANGLE_BASE_CONFIG,
    "buff": 0.3,
}
CODE_BLOCKS_TOTAL_BUFF = 2

CACHING_SUBMOBJECT_LIMIT = 3000
