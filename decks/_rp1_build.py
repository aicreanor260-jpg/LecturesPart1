# -*- coding: utf-8 -*-
"""Сборка decks/rip-251.html — «Протокол RIP» (2.5.1) строго по pptx, на движке дек 2.2.
Стиль — мятно-ботанические инфографики автора (комплект «RIP 2.5»): светлые панели, бирюзовые маршрутизаторы."""
import base64
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _sw_lib as L  # noqa: E402

ADIR = os.path.join(HERE, "_rp1_assets")
OUT = os.environ.get("RP1_OUT") or os.path.join(HERE, "rip-251.html")
_cache = {}


def b64(name):
    if name not in _cache:
        with open(os.path.join(ADIR, name + ".webp"), "rb") as fh:
            _cache[name] = "data:image/webp;base64," + base64.b64encode(fh.read()).decode()
    return _cache[name]


def pic(name):
    return '<div class="pic rppic"><img src="%s" alt="" loading="lazy"></div>' % b64(name)


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@600;800;900&'
         'family=Golos+Text:wght@400;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap">')


SECTION_START = {"Принцип работы": "general2", "Сетевое обнаружение": "split",
                 "Обеспечение сходимости": "split", "Беллман–Форд: проходы": "bf", "Выход из строя канала": "loops",
                 "Формат сообщения RIPv2": "general2", "Создание процесса RIP": "setup", "Таймеры": "loops",
                 "Проверка конфигурации": "setup", "Шпаргалка команд": "general1"}


def assign_bg(slides):
    """Обычные слайды получают фон-подложку своего раздела (у каждого раздела — своя инфографика)."""
    import re
    cur, out = "general1", []
    for s in slides:
        lab = re.search(r'data-label="([^"]*)"', s).group(1)
        cur = SECTION_START.get(lab, cur)
        m = re.search(r'data-plate="([^"]+)"', s)
        if m:
            cur = m.group(1)
        else:
            s = s.replace('<section class="slide', '<section class="slide bgp-%s' % cur, 1)
        out.append(s)
    return out


def main():
    from _sw_style import CSS
    from _sw_engine import JS
    import _sw_build
    import _dk_kit
    import _dk_cli
    import _rp1_style
    import _rp1_deck
    import _rp1_final

    del L.SL[:]
    _rp1_final.head_slides()
    _rp1_deck.build()
    _rp1_final.tail_slides()
    slides = assign_bg(list(L.SL))
    cli_js = io.open(os.path.join(HERE, "_rp1_cli.js"), encoding="utf-8").read()
    import _rp1_canvas
    import _rp1_cv
    css = CSS + _dk_kit.CSS + _dk_cli.CSS + _rp1_style.css(b64("bg_main"), b64("bg_cover")) + _rp1_canvas.CSS + _rp1_cv.CSS + _rp1_canvas.section_bg_css()
    html = ('<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            "<title>Протокол RIP — лекция 2.5.1</title>\n%s\n<style>%s</style>\n</head>\n<body class=\"th-rp1\">\n"
            '<div id="bgimg"></div><div id="bgfx"></div>\n<div id="stage">\n%s\n</div>\n%s\n'
            "<script>%s</script>\n<script>%s</script>\n</body>\n</html>\n"
            % (FONTS, css, "\n".join(slides), _sw_build.HUD, JS + _dk_kit.JS + _rp1_canvas.JS, cli_js))
    with io.open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("готово: %s — %d слайдов, %.2f МБ" % (OUT, len(slides), os.path.getsize(OUT) / 1048576.0))


if __name__ == "__main__":
    main()
