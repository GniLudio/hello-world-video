import re
import shutil

import requests

from content import get_content_folder


def main() -> None:
    url = "https://raw.githubusercontent.com/leachim6/hello-world/refs/heads/main/readme.md"
    response = requests.get(url, timeout=None)
    response.raise_for_status()

    content = response.text.split("<!--Languages start-->")[1]
    content = content.split("<!--Languages end-->")[0]
    content = content.strip()

    lines = content.split("\n")
    assert lines.pop(0).startswith("## Languages")
    assert lines.pop(0) == ""

    code_folder = get_content_folder()
    if code_folder.exists():
        shutil.rmtree(code_folder)
    code_folder.mkdir(parents=True, exist_ok=True)

    for i, line in enumerate(lines):
        match = re.fullmatch(r"\* \[(.*)\]\((.*)\)", line)
        assert match
        name, sub_url = match.groups()

        code_url = (
            f"https://raw.githubusercontent.com/leachim6/hello-world/refs/heads/main/{sub_url}"
        )

        code_response = requests.get(code_url, timeout=None)
        code_response.raise_for_status()

        (code_folder / f"{i}.name").write_text(name, encoding="utf-8")
        (code_folder / f"{i}.code").write_bytes(code_response.content)


if __name__ == "__main__":
    main()
