import io
import math
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Literal

import manim
import numpy as np
from manim import Scene
from matplotlib import pyplot as plt

from config import (
    CACHING_SUBMOBJECT_LIMIT,
    CODE_BLOCK_RECTANGLE_CONFIG,
    CODE_BLOCKS_TOTAL_BUFF,
    CODE_FONT_SIZE,
    CODE_RECTANGLE_CONFIG,
    CORNER_RADIUS,
    INTRO_DURATION,
    NAME_FONT_SIZE,
    NAME_RECTANGLE_CONFIG,
    NAME_Y_SHIFT,
    NUMBER_FONT_SIZE,
    NUMBER_RECTANGLE_CONFIG,
    TITLE_FONT_SIZE,
    TRANSITION_TIME,
    WAIT_TIME,
)
from content import iter_content, read_code
from tex import get_tex_template, remove_vrules, to_tex

assert isinstance(sys.stdout, io.TextIOWrapper)
assert isinstance(sys.stderr, io.TextIOWrapper)
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

manim.Tex.set_default(tex_template=get_tex_template())


class HelloWorldScene(Scene):
    def __init__(self, *args, content: list[tuple[int, str, Path]] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.content = content or list(iter_content())

    def setup(self) -> None:
        self.title_obj = remove_vrules(construct_title(len(self.content)))
        self.number_rectangle = manim.RoundedRectangle(**NUMBER_RECTANGLE_CONFIG)
        self.name_rectangle = manim.RoundedRectangle(**NAME_RECTANGLE_CONFIG)
        self.code_rectangle = manim.VectorizedPoint()

        self.number_rectangle.set_z_index(-1)
        self.name_rectangle.set_z_index(-1)
        self.code_rectangle.set_z_index(-1)

        self.number_rectangle.to_corner(manim.UL, buff=0)
        self.name_rectangle.to_edge(manim.UP, buff=0)
        self.code_rectangle.shift(0.5 * self.name_rectangle.height * manim.DOWN)

        self.content_objects: list[tuple[manim.VMobject, manim.VMobject, manim.VMobject]] = []

        for entry in self.content:
            if manim.config.verbosity in {"DEBUG", "INFO", "WARNING"}:
                print("\t", *entry[:1], flush=True)
            self.content_objects.append(self.construct_entry(*entry))

    def construct(self) -> None:
        if len(self.content_objects) == 1:
            self.add(self.number_rectangle, self.name_rectangle, self.code_rectangle)
            self.add(*self.content_objects[0])
            return

        self.add(self.title_obj)
        self.wait(1 / manim.config.frame_rate)
        self.remove(self.title_obj)

        previous_entry = self.content_objects[0]
        self.play(
            manim.Succession(
                manim.Write(self.title_obj, run_time=INTRO_DURATION - TRANSITION_TIME - WAIT_TIME),
                manim.Wait(TRANSITION_TIME),
                manim.AnimationGroup(
                    manim.FadeIn(self.number_rectangle),
                    manim.FadeIn(self.name_rectangle),
                    manim.FadeIn(self.code_rectangle),
                    manim.FadeIn(previous_entry[0], scale=0),
                    manim.ReplacementTransform(self.title_obj, previous_entry[1]),
                    manim.FadeIn(previous_entry[2], scale=0),
                    run_time=WAIT_TIME,
                ),
            )
        )

        for info, entry in list(zip(self.content, self.content_objects))[1:]:
            if manim.config.verbosity in {"DEBUG", "INFO", "WARNING"}:
                print(
                    info[0],
                    info[1].ljust(20),
                    get_mobject_count(previous_entry[2]),
                    get_mobject_count(entry[2]),
                    flush=True,
                )
            temp_disable_caching = manim.config.disable_caching
            if (
                get_mobject_count(previous_entry[2]) + get_mobject_count(entry[2])
                > CACHING_SUBMOBJECT_LIMIT
            ):
                manim.config.disable_caching = True
            self.play(
                manim.Succession(
                    manim.Wait(WAIT_TIME),
                    manim.AnimationGroup(
                        manim.ReplacementTransform(previous_entry[0], entry[0]),
                        manim.ReplacementTransform(previous_entry[1], entry[1]),
                        manim.ReplacementTransform(
                            previous_entry[2], entry[2], rate_func=manim.linear
                        ),
                        run_time=TRANSITION_TIME,
                    ),
                ),
            )
            manim.config.disable_caching = temp_disable_caching
            previous_entry = entry

        self.wait()

    def construct_entry(
        self, index: int, name: str, code_file: Path
    ) -> tuple[manim.VMobject, manim.VMobject, manim.VMobject]:
        number_obj = construct_number(index)
        name_obj = construct_name(index, name)
        code_obj = construct_code(index, name, code_file)

        number_obj.move_to(self.number_rectangle).shift(0.05 * manim.DR)
        name_obj.move_to(self.name_rectangle).shift(NAME_Y_SHIFT * manim.DOWN)
        code_obj.move_to(self.code_rectangle)

        name_obj = remove_vrules(name_obj)
        code_obj = remove_vrules(code_obj)
        number_obj = remove_vrules(number_obj)

        return number_obj, name_obj, code_obj


def get_mobject_count(mobject: manim.Mobject) -> int:
    count = 1
    for child in mobject.submobjects:
        count += get_mobject_count(child)
    return count


def construct_title(count: int) -> manim.VMobject:
    tex = manim.Tex(
        to_tex(f"Hello World\nin {count}\nProgramming Languages", False),
        font_size=TITLE_FONT_SIZE,
    )
    return tex


def construct_number(index: int) -> manim.VMobject:
    tex = manim.Tex(to_tex(str(index + 1), False), font_size=NUMBER_FONT_SIZE)
    return tex


def construct_name(index: int, name: str) -> manim.VMobject:
    tex = manim.Tex(to_tex(name, False), font_size=NAME_FONT_SIZE)
    if tex.width >= NAME_RECTANGLE_CONFIG["width"] or tex.height >= NAME_RECTANGLE_CONFIG["height"]:
        print("Too large", "name", f"{tex.width:.2f}", f"{tex.height:.2f}", index, name)
    return tex


def construct_code(index: int, name: str, code_file: Path) -> manim.VMobject:
    blocks: list[manim.VMobject] = []
    match name:
        case (
            "Brainloller"  # 193
            | "MOONBlock"  # 611
            | "Piet"  # 703
        ):
            blocks = [construct_code_png(code_file)]
        case _:
            blocks = construct_code_text(index, name, code_file)

    code_obj = manim.VGroup(*blocks)

    width_scale = code_obj.width / CODE_RECTANGLE_CONFIG["width"]
    height_scale = code_obj.height / CODE_RECTANGLE_CONFIG["height"]
    if (width_scale > 2 or height_scale > 2) and (
        width_scale > height_scale * 2 or height_scale > width_scale * 2
    ):
        print("\t", "Too large", "code", f"{width_scale:.2f}", f"{height_scale:.2f}", index, name)
    code_obj.scale(min(1 / max(width_scale, height_scale), 1))

    return code_obj


def construct_code_text(index: int, name: str, code_file: Path) -> list[manim.VMobject]:
    code = read_code(name, code_file)
    disable_segmenting = False
    block_count = 1

    match name:
        case "420":  # 13
            disable_segmenting = True
        case "ドリトル":  # 30
            disable_segmenting = True
        case "ActionScript 3":  # 49
            disable_segmenting = True
            block_count = 2
        case "AnalF*ck":  # 73
            disable_segmenting = True
            block_count = 3
        case "ARTICLE":  # 93
            disable_segmenting = True
            block_count = 2
        case "Assembler 4004":  # 100
            disable_segmenting = True
            block_count = 2
        case "Assembler 6502":  # 101
            disable_segmenting = True
            block_count = 2
        case "Assembler 8048 videopac":  # 105
            disable_segmenting = True
            block_count = 3
        case "Assembler Atari 2600":  # 109
            disable_segmenting = True
            block_count = 6
        case "Assembler DCPU16":  # 111
            disable_segmenting = True
            block_count = 3
        case "Assembler HP85":  # 115
            disable_segmenting = True
        case "Assembler Intel":  # 117
            disable_segmenting = True
            block_count = 2
        case "Assembler m68000 amigaos":  # 119
            disable_segmenting = True
            block_count = 2
        case "Assembler MASM Win32":  # 121
            disable_segmenting = True
            block_count = 2
        case "Assembler MASM Win64":  # 122
            disable_segmenting = True
            block_count = 2
        case "Assembler NASM FreeBSD":  # 125
            disable_segmenting = True
            block_count = 2
        case "Assembler NASM Win64":  # 130
            disable_segmenting = True
            block_count = 4
        case "Assembler pdp11 palx":  # 132
            disable_segmenting = True
            block_count = 2
        case "Assembler tms9900 ti99 4a":  # 135
            disable_segmenting = True
            block_count = 2
        case "Assembler Z80 TI83calculator":  # 138
            disable_segmenting = True
            block_count = 2
        case "Assembler Z80 zxspectrum":  # 139
            disable_segmenting = True
            block_count = 2
        case "Beatnik":  # 167
            disable_segmenting = True
            block_count = 2
        case "BIT":  # 176
            disable_segmenting = True
            block_count = 2
        case "Boolfuck":  # 188
            disable_segmenting = True
        case "Brainfuck 2D":  # 191
            disable_segmenting = True
        case "Byter":  # 199
            disable_segmenting = True
        case "Catrobat":  # 216
            disable_segmenting = True
            block_count = 2
        case "Chef":  # 234
            disable_segmenting = True
            block_count = 2
        case "Chicken":  # 237
            disable_segmenting = True
        case "Cow":  # 266
            disable_segmenting = True
        case "DCPU":  # 291
            disable_segmenting = True
            block_count = 2
        case "DNA#":  # 303
            disable_segmenting = True
            block_count = 7
        case "DOGO":  # 307
            disable_segmenting = True
        case "Drive-In Window":  # 315
            disable_segmenting = True
            block_count = 2
        case "Evil":  # 353
            disable_segmenting = True
            block_count = 2
        case "GeoJSON":  # 402
            disable_segmenting = True
            block_count = 10
        case "groot":  # 428
            disable_segmenting = True
            block_count = 7
        case "ITAMFSARL":  # 487
            disable_segmenting = True
            block_count = 10
        case "Il":  # 473
            disable_segmenting = True
            block_count = 2
        case "JSFuck":  # 502
            disable_segmenting = True
        case "LBL":  # 535
            disable_segmenting = True
            block_count = 20
        case "LINE entry":  # 545
            disable_segmenting = True
            block_count = 3
        case "LNUSP":  # 554
            disable_segmenting = True
            block_count = 2
        case "Mmmm()":  # 601
            disable_segmenting = True
            block_count = 3
        case "Omgrofl":  # 660
            disable_segmenting = True
            block_count = 2
        case "Painter Programming":  # 675
            disable_segmenting = True
            block_count = 4
        case "Pebble":  # 690
            disable_segmenting = True
            block_count = 2
        case "Pit":  # 709
            disable_segmenting = True
            block_count = 14
        case "QuartzComposer":  # 760
            disable_segmenting = True
            block_count = 4
        case "React360":  # 773
            disable_segmenting = True
            block_count = 2
        case "Recurse":  # 780
            disable_segmenting = True
            block_count = 2
        case "Roco":  # 796
            disable_segmenting = True
            block_count = 1
        case "Scratch 2":  # 819
            disable_segmenting = True
            block_count = 2
        case "Scratch 3":  # 820
            disable_segmenting = True
            block_count = 3
        case "Shakespeare":  # 830
            disable_segmenting = True
            block_count = 2
        case "Snap!":  # 848
            disable_segmenting = True
        case "Velato":  # 930
            disable_segmenting = True
            block_count = 4
        case "VerboseFuck":  # 932
            block_count = 3
            disable_segmenting = True
        case "Vowels":  # 946
            disable_segmenting = True
        case "Whitespace":  # 955
            disable_segmenting = True
            block_count = 2
        case "Xlogo":  # 976
            disable_segmenting = True
            block_count = 4

    blocks = construct_code_text_blocks(code, block_count, disable_segmenting).submobjects
    if len(blocks) != block_count:
        print("\t", "More blocks", len(blocks), block_count, index, name)

    return blocks


def construct_code_block_rectangle(
    code_block: manim.VMobject,
    position: Literal["single", "start", "middle", "end"] = "single",
) -> manim.SurroundingRectangle:
    corner_radius: list[float]
    match position:
        case "single":
            corner_radius = [CORNER_RADIUS, CORNER_RADIUS, CORNER_RADIUS, CORNER_RADIUS]
        case "start":
            corner_radius = [CORNER_RADIUS, CORNER_RADIUS, 0, 0]
        case "middle":
            corner_radius = [0, 0, 0, 0]
        case "end":
            corner_radius = [0, 0, CORNER_RADIUS, CORNER_RADIUS]

    rectangle = manim.SurroundingRectangle(
        code_block,
        corner_radius=corner_radius,
        **CODE_BLOCK_RECTANGLE_CONFIG,
    )
    rectangle.add(code_block)
    return rectangle


def construct_code_text_blocks(code: str, count: int, disable_segmenting: bool) -> manim.VGroup:
    lines = code.split("\n")
    block_length = math.ceil(len(lines) / count)
    segments = ["\n".join(lines[x : x + block_length]) for x in range(0, len(lines), block_length)]
    tex = [
        manim.Tex(
            to_tex(segment, True),
            font_size=CODE_FONT_SIZE,
        )
        for segment in segments
    ]

    code_blocks = manim.VGroup(
        construct_code_block_rectangle(
            block,
            position="single"
            if len(segments) == 1
            else "start"
            if i == 0
            else "middle"
            if i < len(segments) - 1
            else "end",
        )
        for i, block in enumerate(tex)
    ).arrange(manim.RIGHT, buff=CODE_BLOCKS_TOTAL_BUFF / len(segments))

    too_high = code_blocks.height > CODE_RECTANGLE_CONFIG["height"]
    aspect_ratio = code_blocks.width / code_blocks.height
    target_aspect_ratio: float = CODE_RECTANGLE_CONFIG["width"] / CODE_RECTANGLE_CONFIG["height"]

    if not disable_segmenting and too_high and (aspect_ratio < target_aspect_ratio):
        wider_code_blocks = construct_code_text_blocks(code, count + 1, disable_segmenting)
        wider_aspect_ratio = wider_code_blocks.width / wider_code_blocks.height
        if wider_aspect_ratio < target_aspect_ratio:
            return wider_code_blocks

    return code_blocks


def construct_code_png(code_file: Path) -> manim.VMobject:
    img = (255 * plt.imread(code_file)).astype(np.uint8)
    height, width, _ = img.shape
    side_length = min(
        CODE_RECTANGLE_CONFIG["width"] / width, CODE_RECTANGLE_CONFIG["height"] / height
    )
    grid = manim.VGroup(
        manim.VGroup(
            manim.Square(color=img[y, x], fill_opacity=1, stroke_width=0, side_length=side_length)
            for x in range(width)
        ).arrange(manim.RIGHT, buff=0)
        for y in range(height)
    ).arrange(manim.DOWN, buff=0)

    return construct_code_block_rectangle(grid)


def render_single(entry: tuple[int, str, Path]) -> None:
    if manim.config.verbosity in {"DEBUG", "INFO"}:
        manim.config.verbosity = "WARNING"

    manim.config.media_dir = f"media/single/{entry[0]}"
    manim.config.output_file = str(entry[0])

    scene = HelloWorldScene(content=[entry])
    scene.render()

    previews_folder = Path("media", "previews")
    previews_folder.mkdir(parents=True, exist_ok=True)
    output_path = scene.renderer.file_writer.image_file_path.move_into(previews_folder)
    print("\t", output_path)


def main() -> None:
    if manim.config.verbosity in {"DEBUG", "INFO"}:
        manim.config.verbosity = "WARNING"

    with ProcessPoolExecutor(max_workers=1) as executor:
        futures = {executor.submit(render_single, entry): entry for entry in iter_content()}
        for future in as_completed(futures.keys()):
            try:
                future.result()
            except Exception:
                print("Error")
                raise


if __name__ == "__main__":
    main()
