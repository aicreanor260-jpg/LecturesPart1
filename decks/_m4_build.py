# -*- coding: utf-8 -*-
"""Сборка decks/marshrutizaciya-2-4.html — лекция 2.4 «Маршрутизация и типы маршрутизации».

    python _m4_build.py

Слайды строго по порядку pptx «2_4»: _m4_d1 (pptx 1–30), _m4_d2 (31–61), _m4_d3 (62–75), _m4_d4 (76–94);
финал (шпаргалка → задачи → тренажёры → CLI ESR → тест → итоги → финал) — _m4_final.
Движок слайдов — общий с 2.2 (_sw_*), стиль — _m4_theme, схемы — _m4_svg, инфографики — _m4_rep.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _sw_lib as L  # noqa: E402

OUT = os.environ.get("M4_OUT") or os.path.join(HERE, "marshrutizaciya-2-4.html")
MODULES = ["_m4_d1", "_m4_d2", "_m4_d3", "_m4_d4", "_m4_final"]


def dedupe(slides):
    seen, out = {}, []
    for s in slides:
        lab = re.search(r'data-label="([^"]*)"', s).group(1)
        if lab in seen:
            seen[lab] += 1
            s = s.replace('data-label="%s"' % lab, 'data-label="%s (%d)"' % (lab, seen[lab]), 1)
        else:
            seen[lab] = 1
        out.append(s)
    return out


def main():
    from _sw_style import CSS
    from _sw_engine import JS
    import _sw_fig
    import _sw_build
    import _dk_kit
    import _dk_cli
    import _m4_theme as T
    import _m4_kit as K
    from _dk_build import recolor, hue_map

    del L.SL[:]
    for m in MODULES:
        __import__(m).build()
    slides = dedupe(list(L.SL))
    fn = hue_map(T.HUES)
    import _m4_cli
    css = (recolor(CSS + _sw_fig.CSS, fn) + _dk_kit.CSS + _dk_cli.CSS + _m4_cli.CSS
           + T.css(K.b64("bg_main"), K.b64("bg_cover")) + T.EXTRA + __import__("_m4_final").CSS)
    js = recolor(JS + _sw_fig.JS + _dk_kit.JS, fn) + _m4_cli.JS + __import__("_m4_final").JS
    html = ('<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>Маршрутизация и типы маршрутизации — лекция 2.4</title>\n%s\n<style>%s</style>\n</head>\n<body class="th-m4">\n'
            '<div id="bgimg"></div><div id="bgfx"></div>\n<div id="stage">\n%s\n</div>\n%s\n<script>%s</script>\n</body>\n</html>\n'
            % (T.FONTS, css, "\n".join(slides), _sw_build.HUD, js))
    with io.open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("готово: %s — %d слайдов, %.2f МБ" % (OUT, len(slides), os.path.getsize(OUT) / 1048576.0))


if __name__ == "__main__":
    main()
