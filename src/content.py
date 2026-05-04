import json
import tarfile
from collections.abc import Generator
from pathlib import Path
from zipfile import ZipFile

from utils import get_project_folder, strip_lines, wrap_long_lines


def get_content_folder() -> Path:
    return get_project_folder() / "content"


def iter_content() -> Generator[tuple[int, str, Path]]:
    index = 0
    while True:
        try:
            code = get_specific(index)
            yield code
            index += 1
        except ValueError:
            break


def get_specific(index: int) -> tuple[int, str, Path]:
    name_file = Path(get_content_folder(), f"{index}.name")
    code_file = Path(get_content_folder(), f"{index}.code")
    if name_file.exists() and code_file.exists():
        return index, name_file.read_text(encoding="utf-8"), code_file

    raise ValueError(index)


def read_code(name: str, code_file: Path) -> str:
    def read_zip(file_ending: str) -> tuple[str, str]:
        with ZipFile(code_file) as zip_file:
            nested_name = next(file for file in zip_file.namelist() if file.endswith(file_ending))
            return nested_name, zip_file.read(nested_name).decode("utf-8")

    def read_tar(file_ending: str) -> tuple[str, str]:
        with tarfile.open(code_file) as tar_file:
            nested_name = next(file for file in tar_file.getnames() if file.endswith(file_ending))
            member = tar_file.getmember(nested_name)
            member_file = tar_file.extractfile(member)
            assert member_file
            with member_file as file:
                return nested_name, file.read().decode("utf-8")

    match name:
        case "App Inventor":  # 84
            code = read_zip(".scm")[1]
        case "Brainloller":  # 193
            code = ""  # png
        case "Catrobat":  # 216
            code = read_zip("code.xml")[1]
        case "Executable":  # 354
            code = f"{len(code_file.read_bytes())} Binary Data"
        case "LINE entry":  # 545
            code = read_tar("project.json")[1]
            code = json.dumps(json.loads(code), indent=4, ensure_ascii=False)
        case "Mind":  # 594
            code = code_file.read_text(encoding="euc-jp")
        case "MOONBlock":  # 611
            code = ""  # png
        case "Piet":  # 703
            code = ""  # png
        case "Pxem":  # 740
            code = read_zip(".pxe")[0]
        case "Scratch 1":  # 818
            code = f"{len(code_file.read_bytes())} Binary Data"
        case "Scratch 2":  # 819
            code = read_zip("project.json")[1]
        case "Scratch 3":  # 820
            code = read_zip("project.json")[1]
            code = json.dumps(json.loads(code), indent=4, ensure_ascii=False)
        case "Swift Playgrounds":  # 872
            code = read_zip("main.swift.delta")[1]
        case "ThotPatrol":  # 888
            code = code_file.read_text(encoding=" UTF-16LE")
        case _:
            code = code_file.read_text(encoding="utf-8")
    code = strip_code(name, code)
    code = wrap_code(name, code)
    return code


def strip_code(name: str, code: str) -> str:
    match name:
        case "App Inventor":  # 84
            lines = code.split("\n")
            lines[2] = json.dumps(json.loads(lines[2]), indent=4, ensure_ascii=False)
            code = "\n".join(lines)
        case "Assembler 6809vectrex":  # 104:
            code = strip_lines(code, lambda line: line.startswith(";"))
        case "Assembler 8048 videopac":  # 105
            code = strip_lines(code, lambda line: line.startswith(";"))
        case "Assembler Atari 2600":  # 109
            code = strip_lines(code, lambda line: line.startswith(";"))
        case "Assembler MASM Win32":  # 121
            code = strip_lines(code, lambda line: line.startswith(";"))
        case "Assembler MASM Win64":  # 122
            code = strip_lines(code, lambda line: line.startswith(";"))
        case "Assembler tms9900 ti99 4a":  # 135
            code = strip_lines(code, lambda line: line.startswith("*"))
        case "Awful":  # 147
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "AWK":  # 148
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Bash":  # 155
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Battlestar":  # 160
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Beta":  # 170
            code = strip_lines(code, lambda line: not line.startswith("(#"))
        case "Blitz3D":  # 182
            code = strip_lines(code, lambda line: line.startswith(";"))
        case "Bolgefuck":  # 185
            code = code[: code.index("//")]
        case "Brainfuck 2D":  # 191
            code = code[: code.index("/*")]
        case "C Shell":  # 200
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Centura":  # 220
            code = strip_lines(code, lambda line: line.startswith("!"))
        case "Cil":  # 239
            code = strip_lines(code, lambda line: line.startswith("//"))
        case "Curry":  # 275
            code = strip_lines(code, lambda line: line.startswith("--"))
        case "Delphi":  # 294
            code = strip_lines(code, lambda line: line.startswith("//"))
        case "DTrace":  # 316
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "EBuild":  # 323
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Eiffel":  # 329
            code = strip_lines(code, lambda line: line.startswith("indexing"))
        case "Elixir":  # 332
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Elvish":  # 334
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Erlang EScript":  # 348
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Falcon":  # 360
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Fantom":  # 363
            code = strip_lines(code, lambda line: line.startswith("//"))
        case "Fish":  # 370
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "GeoJSON":  # 402
            code = json.dumps(json.loads(code), indent=4, ensure_ascii=False)
        case "J":  # 489
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "KSH":  # 525
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Like, Python":  # 542
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Lisaac":  # 547
            code = strip_lines(code, lambda line: line.startswith("//"))
        case "LNUSP":  # 554
            code = strip_lines(code, lambda line: line.startswith("---"))
        case "MaxScript":  # 586
            code = strip_lines(code, lambda line: line.startswith("--"))
        case "NewLISP":  # 631
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Node.js":  # 640
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "NWScript":  # 645
            code = strip_lines(code, lambda line: line.startswith("//"))
        case "Objective C":  # 652
            code = code[code.index("*/") + 2 :]
        case "Orc":  # 668
            code = code[code.index("-}") + 2 :]
        case "Parenthetic":  # 680
            code = strip_lines(code, lambda line: not (line.startswith(("(", ")"))))
        case "PB":  # 687
            code = strip_lines(code, lambda line: line.startswith(";"))
        case "Perl":  # 694, 695
            code = strip_lines(code, lambda line: line.strip().startswith("#"))
        case "Perl6":  # 696
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Python 2":  # 748
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Python 3":  # 749
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Qore":  # 756
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Racket":  # 765
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Ruby":  # 803
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Sed":  # 823
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Shell":  # 831
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Simpl+":  # 835
            code = strip_lines(code, lambda line: line.startswith("//"))
        case "Tao Presentations":  # 878
            code = strip_lines(code, lambda line: line.startswith("//"))
            code = (
                code[: code.index("milkyway R ->")].strip("\n")
                + "\n\n\n"
                + code[code.index("hello_world R ->") :].strip("\n")
            )
        case "TCSH":  # 881
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "THP":  # 889
            code = strip_lines(code, lambda line: line.startswith(";"))
        case "VerboseFuck":  # 932
            code = "\n".join(
                line
                for line in code.split("\n")
                if not (line.strip().startswith("~!comment!~") and line.endswith("~!uncomment!~"))
            )
        case "Vi":  # 936
            code = strip_lines(code, lambda line: not line.startswith("\t"))
            code = "\n".join(line.strip() for line in code.split("\n"))
        case "VRML":  # 947
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "X10":
            code = code[code.index("*/") + 2 :]
        case "XL":  # 974
            code = strip_lines(code, lambda line: line.startswith("//"))
        case "Yorick":  # 991
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Z Shell":  # 993
            code = strip_lines(code, lambda line: line.startswith("#"))
        case "Zinc":  # 1001
            code = strip_lines(code, lambda line: line.startswith("//"))
        case "zx":  # 1008
            code = strip_lines(code, lambda line: line.startswith("#"))

    return code.strip("\n").replace("\t", " " * 4)


def wrap_code(name: str, code: str) -> str:
    optimal_line_width = 70
    match name:
        case "2B":  # 11
            code = wrap_long_lines(code, optimal_line_width)
        case "420":  # 12
            code = wrap_long_lines(code, 188)
        case "@text":  # 19
            code = wrap_long_lines(code, optimal_line_width)
        case "タイルズ":  # 29
            code = wrap_long_lines(code, 131)
        case "ActionScript 3":  # 49
            code = wrap_long_lines(code, 52)
        case "Ante":  # 79
            code = wrap_long_lines(code, 48)
        case "ARTICLE":
            code = wrap_long_lines(code, 60)
        case "Assembler 8048 videopac":  # 105
            code = wrap_long_lines(code, 28)
        case "Assembler IBM360":  # 116
            code = wrap_long_lines(code, optimal_line_width)
        case "Brainfuck":  # 192
            code = wrap_long_lines(code, optimal_line_width)
        case "C+":  # 201
            code = wrap_long_lines(code, optimal_line_width)
        case "Catrobat":  # 216
            code = wrap_long_lines(code, 93)
        case "Chicken":  # 237
            code = wrap_long_lines(code, 167)
        case "Emmental":  # 337
            code = wrap_long_lines(code, optimal_line_width)
        case "Freebrain":  # 390
            code = wrap_long_lines(code, 128)
        case "GeoJSON":  # 402
            code = json.dumps(json.loads(code), indent=1, ensure_ascii=False)
        case "Goldfish":  # 413
            code = wrap_long_lines(code, optimal_line_width)
        case "Homespring":  # 450
            pass  # Empty on purpose
        case "HTML":  # 457
            code = wrap_long_lines(code, 38)
        case "Il":  # 473
            code = wrap_long_lines(code, 55)
        case "JSFuck":  # 502
            code = wrap_long_lines(code, 377)
        case "LINE entry":  # 545
            code = wrap_long_lines(code, 90)
        case "LLVM":  # 553
            code = wrap_long_lines(code, optimal_line_width)
        case "Logicode":  # 556
            code = wrap_long_lines(code, optimal_line_width)
        case "Mathematica Online":  # 581
            code = wrap_long_lines(code, 53)
        case "Meq":  # 589
            code = wrap_long_lines(code, optimal_line_width)
        case "Mostawesomeprograminglanguage":  # 615
            code = wrap_long_lines(code, 167)
        case "Panther":  # 678
            code = wrap_long_lines(code, 43)
        case "Polynomial":  # 716
            code = wrap_long_lines(code, 177)
        case "QuartzComposer":  # 760
            code = wrap_long_lines(code, 64)
        case "Qugord":  # 761
            code = wrap_long_lines(code, optimal_line_width)
        case "Sacred":  # 808
            code = wrap_long_lines(code, optimal_line_width)
        case "Scratch 3":  # 820
            code = wrap_long_lines(code, 69)
        case "Seed":  # 824
            code = wrap_long_lines(code, 157)
        case "Snap!":  # 848
            code = wrap_long_lines(code, 236)
        case "Spoon":  # 855
            code = wrap_long_lines(code, optimal_line_width)
        case "Sus":  # 869
            code = wrap_long_lines(code, optimal_line_width)
        case "TrollScript":  # 902
            code = wrap_long_lines(code, optimal_line_width)
        case "VerboseFuck":  # 932
            code = wrap_long_lines(code, 86)
        case "Whitespace":  # 955
            code = code.replace(" ", "\u2423").replace("\t", "\\t")
        case "wowLang":  # 960
            code = wrap_long_lines(code, optimal_line_width)
        case "YoLang":  # 989
            code = wrap_long_lines(code, optimal_line_width)

    return code
