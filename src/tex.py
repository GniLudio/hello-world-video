import manim

from characters import get_character_language
from fonts import FONT_ARGS, FONTS

TEX_ESCAPE_CHARACTERS_NORMAL: dict[str, str] = {
    "#": "\\#",
    "$": "\\$",
    "%": "\\%",
    "_": "\\_",
    "&": "\\&",
    "{": "\\{",
    "}": "\\}",
    "\\": "\\textbackslash{}",
    "~": "\\~{}",
    "^": "\\^{}",
    "\n": "\\\\",
    "\r": "",
    "\v": "",
    "\f": "",
    "\t": "\\qquad{}",
}
TEX_ESCAPE_CHARACTERS_VERBATIM: dict[str, str] = {
    "\r": "",
    "\v": "",
    "\f": "",
    "{": "\\{",
    "}": "\\}",
    "\\": "\\symbol{92}",
    "\t": "\\qquad{}",
}


def get_tex_template() -> manim.TexTemplate:
    preamble = """
\\usepackage{fontspec,fancyvrb}
\\newcommand\\strutvrule[0]{\\strut{}{\\vrule width 1sp}}
\\defaultfontfeatures{Scale=MatchLowercase}
"""

    for language, (serif_font, mono_font) in FONTS.items():
        preamble += f"\\newfontfamily\\{language}font{{{serif_font}}}[{FONT_ARGS[language][0]}]\n"
        preamble += f"\\newfontfamily\\{language}fonttt{{{mono_font}}}[{FONT_ARGS[language][1]}]\n"
    return manim.TexTemplate(tex_compiler="xelatex", output_format=".xdv", preamble=preamble)


def to_tex(text: str, is_verbatim: bool) -> str:
    text = __insert_tex_languages(text, is_verbatim)
    text = __make_lines_full_height(text)
    if is_verbatim:
        text = (
            "\n"
            r"\begin{Verbatim}[commandchars={\\\{\}}]"
            "\n" + text + "\n"
            r"\end{Verbatim}"
            "\n"
        )
        num_lefts = text.count("{") - text.count("\\{") + text.count("\\\\{")
        num_rights = text.count("}") - text.count("\\}") + text.count("\\\\}")
        text += "%" + ("}" * (num_lefts - num_rights)) + ("{" * (num_rights - num_lefts)) + "\n"
    return text


def remove_vrules[T: manim.VMobject](obj: T) -> T:
    for child in obj.submobjects:
        if child.width < 0.01:
            obj.remove(child)
        else:
            remove_vrules(child)
    return obj


def __escape_tex(text: str, is_verbatim: bool) -> str:
    escape_map = TEX_ESCAPE_CHARACTERS_NORMAL if not is_verbatim else TEX_ESCAPE_CHARACTERS_VERBATIM
    return "".join(escape_map.get(char, char) for char in text)


def __insert_tex_languages(text: str, is_verbatim: bool) -> str:
    font_suffix = "" if not is_verbatim else "tt"

    new_text: str = ""

    for line in text.split("\n"):
        current_language = get_character_language(line[:1])
        if current_language is not None:
            new_text += "\\" + current_language + "font" + font_suffix + "{}"
        new_text += __escape_tex(line[:1], is_verbatim)
        for char in line[1:]:
            char_language = get_character_language(char)
            if current_language != char_language and char_language is not None:
                new_text += "\\" + char_language + "font" + font_suffix + "{}"
                current_language = char_language
            new_text += __escape_tex(char, is_verbatim)
        new_text += __escape_tex("\n", is_verbatim)
    new_text = new_text.removesuffix(__escape_tex("\n", is_verbatim))

    return new_text


def __make_lines_full_height(text: str) -> str:
    return "\n".join(r"\strutvrule{}" + line + r"\strutvrule{}" for line in text.split("\n"))
