# -*- coding: utf-8 -*-
"""Сборка деки MPLS 2.9 в подаче v2 (фон слайда = фон комплекта, логические блоки, живые схемы).
    python _mp2_build.py   → mpls.html (или MP2_OUT)"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _sw_lib as L  # noqa: E402

OUT = os.environ.get("MP2_OUT") or os.path.join(HERE, "mpls.html")
ALL = ["_mp2_s%d" % i for i in range(1, 10)]
MODULES = [m for m in os.environ.get("MP2_MODULES", ",".join(ALL)).split(",") if m]
FULL = "MP2_MODULES" not in os.environ


def main():
    from _sw_style import CSS
    from _sw_engine import JS
    import _sw_build
    import _mp_theme as T
    import _mp2_kit as K
    import _mp_lib

    import _mp2_fin as FN
    del L.SL[:]
    if FULL:
        FN.head()
    for m in MODULES:
        __import__(m).build()
    if FULL:
        FN.tail()
    labs = [x.split('data-label="', 1)[1].split('"', 1)[0] for x in L.SL]
    dup = sorted({x for x in labs if labs.count(x) > 1})
    if dup:
        raise SystemExit("дубли data-label: %s" % dup)
    slides = list(L.SL)
    extra = "".join(getattr(sys.modules[m], "CSS", "") for m in MODULES) + (FN.CSS if FULL else "")
    css = CSS + T.css(_mp_lib.b64("bg_main"), _mp_lib.b64("bg_cover")) + K.CSS + extra + K.bg_css()
    html = ('<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            "<title>MPLS — лекция</title>\n%s\n<style>%s</style>\n</head>\n<body class=\"th-mpls\">\n"
            '<div id="bgimg"></div><div id="bgfx"></div>\n<div id="stage">\n%s\n</div>\n%s\n'
            "<script>%s</script>\n</body>\n</html>\n" % (T.FONTS, css, "\n".join(slides), _sw_build.HUD, JS + (FN.JS if FULL else "")))
    with io.open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("готово: %s — %d слайдов, %.2f МБ" % (OUT, len(slides), os.path.getsize(OUT) / 1048576.0))


if __name__ == "__main__":
    main()
