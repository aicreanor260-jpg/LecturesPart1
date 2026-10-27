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


EYEBROW = [("Общие сведения", "Общие сведения"), ("Версии", "Общие сведения"), ("Обновления", "Общие сведения"),
           ("Возможности", "Общие сведения"), ("Принцип работы", "Принцип работы"), ("Запуск", "Принцип работы"),
           ("Сетевое обнаружение", "Сходимость"), ("Первый обмен", "Сходимость"), ("Обмен данными", "Сходимость"),
           ("Метод разделения", "Сходимость"), ("Обеспечение сходимости", "Сходимость"), ("Беллман", "Беллман–Форд"),
           ("Алгоритм Беллмана", "Беллман–Форд"), ("Шаг ", "Беллман–Форд"), ("Итоговая таблица", "Беллман–Форд"),
           ("Выход из строя", "Изменения топологии"), ("Время распространения", "Изменения топологии"),
           ("Формат", "Формат сообщения"), ("Поля RIPv2", "Формат сообщения"), ("Настройка", "Настройка на ESR"),
           ("Создание", "Настройка на ESR"), ("Аутентификация", "Настройка на ESR"), ("Другие команды", "Настройка на ESR"),
           ("Сосед", "Настройка на ESR"), ("Объявление", "Настройка на ESR"), ("Redistribute", "Настройка на ESR"),
           ("Пассивный", "Настройка на ESR"), ("Механизмы", "Защита от петель"), ("Таймеры", "Таймеры"),
           ("Проверка", "Проверка конфигурации"), ("Пример", "Пример настройки"), ("Шпаргалка", "Повторение"),
           ("Итоговые задачи", "Практика"), ("Тренажёр", "Тренажёры"), ("Тест", "Проверь себя"), ("Что запомнить", "Итоги")]


def assign_bg(slides):
    """Надзаголовок раздела над заголовком каждого обычного слайда (как в главах 1–9)."""
    import re
    out = []
    for s in slides:
        lab = re.search(r'data-label="([^"]*)"', s).group(1)
        eb = next((v for k, v in EYEBROW if lab.startswith(k)), "")
        if eb:
            s = s.replace('<div class="head">', '<div class="head"><div class="eb">%s</div>' % eb, 1)
        s = re.sub(r'<pre class="(cli|term)([^"]*)">(.*?)</pre>', _fit_pre, s, flags=re.S)
        out.append(s)
    return out


def _fit_pre(m):
    """Длинный вывод CLI (дословно из pptx) уменьшается так, чтобы весь помещался по высоте экрана."""
    n = m.group(3).count("\n") + 1
    if n <= 20:
        return m.group(0)
    return ('<pre class="%s%s" style="font-size:min(.92vw,calc((100vh - 230px) / %.1f))!important">%s</pre>'
            % (m.group(1), m.group(2), n * 1.47, m.group(3)))


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
    css = CSS + _dk_kit.CSS + _dk_cli.CSS + _rp1_style.css() + _rp1_style.SPLIT + _rp1_canvas.CSS + _rp1_cv.CSS + _rp1_canvas.section_bg_css()
    html = ('<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            "<title>Протокол RIP — лекция 2.5.1</title>\n%s\n<style>%s</style>\n</head>\n<body class=\"th-rp1\">\n"
            '%s\n<div id="stage">\n%s\n</div>\n%s\n'
            "<script>%s</script>\n<script>%s</script>\n</body>\n</html>\n"
            % (FONTS, css, _rp1_style.BG, "\n".join(slides), _sw_build.HUD, JS + _dk_kit.JS + _rp1_canvas.JS, cli_js))
    with io.open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("готово: %s — %d слайдов, %.2f МБ" % (OUT, len(slides), os.path.getsize(OUT) / 1048576.0))


if __name__ == "__main__":
    main()
