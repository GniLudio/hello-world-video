import subprocess

from fontTools.ttLib import TTFont
from matplotlib import font_manager

from content import iter_content, read_code
from fonts import FONTS
from utils import get_project_folder


def main() -> None:
    font_cmaps = {
        language: (
            TTFont(font_manager.findfont(serif_font, fallback_to_default=False)).getBestCmap()
            or {},
            TTFont(font_manager.findfont(mono_font, fallback_to_default=False)).getBestCmap() or {},
        )
        for language, (serif_font, mono_font) in FONTS.items()
    }

    character_map: dict[str | None, str] = {language: "" for language in FONTS}
    character_map[None] = ""

    def add_char(char: str) -> None:
        value = ord(char)
        language: str | None = None
        language = next(
            (
                font_language
                for font_language, (serif_font, mono_font) in font_cmaps.items()
                if value in serif_font and value in mono_font
            ),
            None,
        )
        if char not in character_map[language]:
            character_map[language] += char

    for i, name, code_file in iter_content():
        print(i, name)
        code = read_code(name, code_file)
        for char in name + code:
            add_char(char)
    add_char("\u2423")

    character_map["english"] = "".join(sorted(character_map["english"]))
    character_map["english"] = character_map["english"].replace(" ", "")
    character_map[None] += " "

    text = "CHARACTERS: dict[str | None, str] = " + repr(character_map)

    output_file = get_project_folder() / "src" / "characters.py"
    output_file.write_text(text, encoding="utf-8")
    subprocess.run(["ruff", "format", str(output_file)], check=True)


if __name__ == "__main__":
    main()
