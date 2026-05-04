CHARACTERS: dict[str | None, str] = {
    "english": "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~¨©«°»½íöĆř̳̹̊̿͗ΔΘΚέαδεηκλμρςσωόавгдиклмносхчыяṭẇ“”•…\u202b⁏⁰⁾\ufeff",
    "chinese": "うんちく「」って書。なでしこと表示ひまわり、タイルズドリトラベ！（）作るプロデ出力す文言吾有一曰之易语调试输火星姠屛募潑鎹牸苻賗：【沵恏，迣鎅】蔠圵姟珵垿秀丸マク🆒あろよいアーッのさぁｱｰｯ来ファ？♦♥♣♠←畀我睇下点样先收工ポケコシン背景寫を唠♭➡カ歩ブウスォチ答え品メは\u3000改行系统打印╯□︵┻━に世界␣",
    "japanese": "",
    "korean": "밤밣따빠밟뿌맣파빨받뚜뭏돋밬탕붏두붇볻뫃박발뚷투붖도희멓붘봌토범더벌뽑뽀벓뻐뚠덩벐덕벅",
    "hebrew": "בקרהתעד",
    "bengali": "দেখাও",
    "arabic": "قلبومرحايعکھ",
    "javanese": "ꦥꦿꦶꦤ꧀",
    "emoji": "💬🔤👋🗺️🏁🍇😀❗🍉🔡🌚🌝😭😲⏪⏬⏩🌍📡🕵🍑📧🇺🇸",
    "runic": "ᚱᚢᚾᛅᛦᛋᚭᛁᚹᛧ",
    "symbols": "◄❨❩",
    "math": "⎕⌡",
    None: "\n\t ",
}


def get_character_language(character: str) -> str | None:
    return next(
        (
            language
            for language, language_characters in CHARACTERS.items()
            if character in language_characters
        ),
        None,
    )
