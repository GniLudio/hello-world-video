from collections.abc import Callable
from pathlib import Path


def get_project_folder() -> Path:
    return Path(__file__).resolve().parent.parent


def strip_lines(text: str, should_strip: Callable[[str], bool]) -> str:
    lines = text.split("\n")
    while len(lines) > 0 and (should_strip(lines[0]) or lines[0] == ""):
        lines.pop(0)
    while len(lines) > 0 and (should_strip(lines[-1]) or lines[-1] == ""):
        lines.pop(-1)

    return "\n".join(lines)


def wrap_long_lines(
    text: str,
    line_length: int,
    new_line: str = "\n",
    indent: str = "\t",
    indent_width: int = 4,
) -> str:
    lines: list[str] = []
    step = max(1, line_length - indent_width)
    for line in text.splitlines():
        if not line:
            lines.append("")
            continue
        lines.append(line[:line_length])
        for x in range(line_length, len(line), step):
            lines.append(f"{indent}{line[x : x + step]}")

    return new_line.join(lines)
