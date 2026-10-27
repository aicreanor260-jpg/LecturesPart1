# -*- coding: utf-8 -*-
"""Сборка decks/mpls.html — лекция «2.9. MPLS» строго по pptx, на движке деки «Коммутация 2.2».

    python _mp_build.py

Слайды: _mp_s1…_mp_s3 (pptx 1–71 по порядку) + титул и финал из _mp_final.
Стиль — инфографики и фоны комплекта «2.9. MPLS» (небо Гибли): _mp_assets, тема _mp_theme.
Общие модули (_sw_*, _dk_*) не меняются.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _sw_lib as L  # noqa: E402

OUT = os.environ.get("MP_OUT") or os.path.join(HERE, "mpls.html")


def main():
    from _sw_style import CSS
    from _sw_engine import JS
    import _sw_build
    import _dk_kit
    import _mp_theme as T
    import _mp_final as FIN
    import _mp_lib
    import _mp_replib

    del L.SL[:]
    FIN.head()
    for m in ("_mp_s1", "_mp_s2", "_mp_s3"):
        __import__(m).build()
    FIN.tail()
    slides = list(L.SL)
    labs = [s.split('data-label="', 1)[1].split('"', 1)[0] for s in slides]
    dup = sorted({x for x in labs if labs.count(x) > 1})
    if dup:
        raise SystemExit("дубли data-label: %s" % dup)

    css = CSS + _dk_kit.CSS + T.css(_mp_lib.b64("bg_main"), _mp_lib.b64("bg_cover")) + FIN.CSS + _mp_replib.CSS
    js = JS + _dk_kit.JS + FIN.JS + _mp_replib.JS
    html = (
        '<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        "<title>MPLS — лекция</title>\n%s\n<style>%s</style>\n</head>\n<body class=\"th-mpls\">\n"
        '<div id="bgimg"></div><div id="bgfx"></div>\n<div id="stage">\n%s\n</div>\n%s\n'
        "<script>%s</script>\n</body>\n</html>\n"
        % (T.FONTS, css, "\n".join(slides), _sw_build.HUD, js))
    with io.open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("готово: %s — %d слайдов, %.2f МБ" % (OUT, len(slides), os.path.getsize(OUT) / 1048576.0))


if __name__ == "__main__":
    # дека переделана в подаче v2: собирается _mp2_build.py (этот сборщик — прежняя подача, оставлен как библиотека сцен)
    import runpy
    runpy.run_path(os.path.join(HERE, "_mp2_build.py"), run_name="__main__")
