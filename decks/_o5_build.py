# -*- coding: utf-8 -*-
"""Дека «Протокол OSPF» строго по pptx «OSPF 2 5» на движке дек 2.2:

    python -X utf8 _o5_build.py   → ospf-2-5.html

Слайды — _o5_deck (порядок pptx), финал — _o5_final, тренажёр CLI маршрутизатора ESR — _o5_cli.js,
инфографики — вёрстка _o5_rep/ поверх чистых фонов, схемы pptx — SVG (_o5_figA/_o5_figB), скриншоты — _o5_tx.
Существующая ospf.html не меняется."""
import base64
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _sw_lib as L  # noqa: E402


def _b64(path):
    with open(path, "rb") as fh:
        return "data:image/webp;base64," + base64.b64encode(fh.read()).decode()


def label(s):
    return re.search(r'data-label="([^"]*)"', s).group(1)


def check(slides):
    labs = [label(s) for s in slides]
    dup = sorted({x for x in labs if labs.count(x) > 1})
    if dup:
        raise SystemExit("дубли data-label: %s" % dup)


def build():
    import _o5_theme as T
    import _o5_deck
    import _o5_final
    import _o5_cli
    import _dk_kit
    import _sw_fig
    import _sw_build
    from _sw_style import CSS
    from _sw_engine import JS

    del L.SL[:]
    _o5_deck.build()
    _o5_final.build()
    slides = list(L.SL)
    check(slides)
    bgdir = os.path.join(HERE, "_ospf_assets", "bg")
    css = (CSS + _sw_fig.CSS + _dk_kit.CSS + _o5_cli.CSS
           + T.css(_b64(os.path.join(bgdir, "bg5.webp")), _b64(os.path.join(bgdir, "bg2.webp"))) + _o5_deck.CSS)
    js = JS + _sw_fig.JS + _dk_kit.JS + _o5_cli.JS
    html = (
        '<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        "<title>Протокол OSPF — лекция</title>\n%s\n<style>%s</style>\n</head>\n<body class=\"th-o5\">\n"
        '<div id="bgimg"></div><div id="bgfx"></div>\n<div id="stage">\n%s\n</div>\n%s\n'
        "<script>%s</script>\n</body>\n</html>\n"
        % (T.FONTS, css, "\n".join(slides), _sw_build.HUD, js))
    out = os.environ.get("DK_OUT") or os.path.join(HERE, "ospf-2-5.html")
    with io.open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("готово: %s — %d слайдов, %.2f МБ" % (out, len(slides), os.path.getsize(out) / 1048576.0))


if __name__ == "__main__":
    build()
