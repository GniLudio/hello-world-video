import io
import sys

import manim
from manim import Scene

from characters import CHARACTERS
from fonts import FONTS
from tex import get_tex_template, to_tex

for std in [sys.stdout, sys.stderr]:
    assert isinstance(std, io.TextIOWrapper)
    std.reconfigure(encoding="utf-8")


manim.config.pixel_width = 4096
manim.config.pixel_height = 4096


class FontTestScene(Scene):
    def construct(self) -> None:
        self.add(
            manim
            .VGroup(
                *[
                    tex.add(
                        manim.SurroundingRectangle(
                            tex,
                            color=manim.WHITE,
                            stroke_width=1,
                            buff=0.1,
                            stroke_opacity=0.5,
                        )
                    )
                    for language in FONTS
                    for is_verbatim in [False, True]
                    if language
                    and (
                        tex := manim.Tex(
                            to_tex(CHARACTERS[language], is_verbatim),
                            tex_environment="{minipage}{100em}",
                            tex_template=get_tex_template(),
                        )
                    )
                ],
            )
            .arrange(manim.DOWN)
            .scale_to_fit_width(manim.config.frame_width - manim.DEFAULT_MOBJECT_TO_EDGE_BUFFER),
        )
