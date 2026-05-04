# Hello World Video

A video of the `Hello World` program in countless different programming languages.

[![Watch the video](https://img.youtube.com/vi/ujyR_8zTYoE/maxresdefault.jpg)](https://youtu.be/ujyR_8zTYoE)

## Rendering from Source

The following fonts must be installed beforehand: [fonts.google.com/share?...](https://fonts.google.com/share?selection.family=Noto+Emoji|Noto+Naskh+Arabic|Noto+Sans+Arabic|Noto+Sans+Bengali|Noto+Sans+Hebrew|Noto+Sans+JP|Noto+Sans+Javanese|Noto+Sans+KR|Noto+Sans+Math|Noto+Sans+Mono|Noto+Sans+Runic|Noto+Sans+SC|Noto+Sans+Symbols+2|Noto+Serif+Bengali|Noto+Serif+Hebrew|Noto+Serif+JP|Noto+Serif+KR|Noto+Serif+SC|Noto+Serif)

To install the required python packages:
```console
uv sync
```

To render the video:
```console
uv run manim src/main.py
```

To render a preview image for every programming languages:
```console
uv run python src/main.py
```

## Credits
The list of programming languages and the corresponding programs were obtained from [leachim6/hello-world](https://github.com/leachim6/hello-world).
