# -*- coding: utf-8 -*-
"""Сборка деки decks/eltex-devices.html.

Источники:
  sources/eltex-paras.json  — текст слайдов (по абзацам) из pptx «Сетевые устройства 2.1»
  sources/eltex-media.json  — какая картинка относится к какому слайду
  assets/eltex/*.jpg        — визуалы слайдов из pptx, пережатые, встраиваются в base64

Запуск:  python _eltex_build.py
"""
import base64
import io
import json
import os

from _eltex_lib import blocks, clean, mark, render
from _eltex_meta import DROP, TITLES

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets", "eltex")
OUT = os.path.join(ROOT, "decks", "eltex-devices.html")

FROST = """
<svg id="frost" viewBox="0 0 1600 900" preserveAspectRatio="none" aria-hidden="true">
 <defs>
  <linearGradient id="fg" x1="0" y1="1" x2="0" y2="0">
   <stop offset="0" stop-color="#b9d2ee" stop-opacity=".85"/>
   <stop offset="1" stop-color="#b9d2ee" stop-opacity="0"/>
  </linearGradient>
  <g id="leaf">
   <path d="M0 0 C -26 -34 -30 -78 0 -126 C 30 -78 26 -34 0 0 Z" fill="url(#fg)"/>
   <path d="M0 -4 L0 -118" stroke="#9bbde3" stroke-width=".8" fill="none" opacity=".7"/>
   <path d="M0 -30 L-14 -48 M0 -30 L14 -48 M0 -56 L-11 -72 M0 -56 L11 -72 M0 -82 L-7 -94 M0 -82 L7 -94"
         stroke="#9bbde3" stroke-width=".7" fill="none" opacity=".6"/>
  </g>
  <g id="flake" stroke="#a9c6e8" stroke-width="1" fill="none">
   <path d="M0 -22 L0 22 M-19 -11 L19 11 M-19 11 L19 -11"/>
   <path d="M0 -14 l-5 -5 M0 -14 l5 -5 M0 14 l-5 5 M0 14 l5 5"/>
   <path d="M-12 -7 l-7 0 M12 7 l7 0 M-12 7 l-7 0 M12 -7 l7 0"/>
  </g>
 </defs>
 <g opacity=".55">
  <use href="#leaf" x="42"  y="250" transform="rotate(-18 42 250)"/>
  <use href="#leaf" x="18"  y="430" transform="rotate(10 18 430)"/>
  <use href="#leaf" x="78"  y="560" transform="rotate(-32 78 560)"/>
  <use href="#leaf" x="30"  y="760" transform="rotate(22 30 760)"/>
  <use href="#leaf" x="112" y="900" transform="rotate(-8 112 900)"/>
  <use href="#leaf" x="1558" y="230" transform="rotate(16 1558 230)"/>
  <use href="#leaf" x="1582" y="420" transform="rotate(-12 1582 420)"/>
  <use href="#leaf" x="1520" y="570" transform="rotate(30 1520 570)"/>
  <use href="#leaf" x="1570" y="750" transform="rotate(-24 1570 750)"/>
  <use href="#leaf" x="1486" y="898" transform="rotate(8 1486 898)"/>
 </g>
 <g opacity=".5">
  <use href="#flake" x="196" y="160"/>
  <use href="#flake" x="1402" y="640" transform="scale(.8) translate(350 160)"/>
  <use href="#flake" x="1330" y="120" transform="scale(.6) translate(880 80)"/>
 </g>
 <g opacity=".55" fill="none" stroke="#a9c6e8" stroke-width=".9">
  <circle cx="1402" cy="150" r="104"/>
  <circle cx="1402" cy="150" r="74"/>
  <ellipse cx="1402" cy="150" rx="42" ry="104"/>
  <path d="M1298 150 h208 M1316 96 h172 M1316 204 h172"/>
 </g>
</svg>
"""


def img_tag(name, cls=""):
    path = os.path.join(ASSETS, os.path.splitext(name)[0] + ".jpg")
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode("ascii")
    return '<img class="%s" alt="" src="data:image/jpeg;base64,%s">' % (cls, b64)


def norm(s):
    return s.lower().strip(" .·—-«»").replace("ё", "е")


_seen = set()


def uniq_label(title, kicker, latin):
    """data-label должен быть уникальным — иначе содержание путает слайды."""
    label = title
    if label in _seen:
        label = "%s · %s" % (title, kicker or latin)
    while label in _seen:
        label += " ·"
    _seen.add(label)
    return label


def build_slide(n, paras, media):
    kicker, title, latin = TITLES[n]
    drop = {norm(title), norm(kicker or "")} | DROP
    body = []
    for raw in paras:
        t = clean(raw, n)
        if not t or norm(t) in drop:
            continue
        if len(t) <= 46 and norm(t).rstrip(":") in drop:
            continue
        body += blocks(t)

    head = []
    if kicker:
        head.append('<div class="kicker">%s</div>' % kicker)
    head.append("<h2>%s</h2>" % title)
    head.append('<div class="sub">%s</div>' % latin)

    shot = "".join(img_tag(m["f"]) for m in media)
    txt = "".join(render(b) for b in body)

    cls = "slide"
    if not shot:
        cls += " wide"
    elif not txt:
        cls += " hero"

    label = uniq_label(title, kicker, latin)
    parts = ['<section class="%s" data-label="%s">' % (cls, label.replace('"', "&quot;")),
             '<header class="shead">%s</header>' % "".join(head),
             '<div class="sbody">']
    if shot:
        parts.append('<figure class="shot ice">%s</figure>' % shot)
    if txt:
        parts.append('<div class="txt ice">%s</div>' % txt)
    parts.append("</div></section>")
    return "".join(parts)


TITLE_SLIDE = """
<section class="slide" data-label="Титул">
 <div class="title-wrap">
  <div class="kicker">Академия Eltex · лекция</div>
  <div class="sub">ROUTERS · SWITCHES · WIRELESS</div>
  {shot}
  <div class="authors">Общие сведения о сетевых устройствах</div>
 </div>
</section>
"""

LAB = """
<section class="slide" data-label="Тренажёр CLI">
 <header class="shead">
  <div class="kicker">Практика</div>
  <h2>Тренажёр командной строки</h2>
  <div class="sub">ESR CLI EMULATOR</div>
 </header>
 <div class="sbody" style="grid-template-columns:1.3fr 1fr">
  <div class="ice" style="display:flex;flex-direction:column;padding:12px;min-height:0">
   <div id="term"></div>
   <div id="termline" class="cli" style="margin:10px 0 0">
    <span id="prompt">esr&gt;</span>
    <input id="termin" autocomplete="off" spellcheck="false" aria-label="Команда">
   </div>
  </div>
  <div class="tasks ice">
   <div class="chead"><div class="cnum">01</div><div class="clab">TASK LIST</div></div>
   <ul>
    <li id="t_conf">Перейдите в режим глобального конфигурирования</li>
    <li id="t_user_f">Создайте пользователя (<code>username</code> + имя)</li>
    <li id="t_back">Вернитесь в привилегированный режим</li>
   </ul>
   <p class="hint">Проверка идёт по состоянию эмулятора, а не по тексту команды.
    История — стрелки вверх и вниз, автодополнение — Tab.
    Пока курсор в поле ввода, клавиши не листают слайды.</p>
   <button class="btn" id="termreset" type="button">Сбросить сессию</button>
  </div>
 </div>
</section>
"""

QUIZ_Q = [
    ("На каком уровне модели OSI работает коммутатор локальной сети?",
     [("Канальный, 2-й уровень", 1), ("Сетевой, 3-й уровень", 0), ("Физический, 1-й уровень", 0)]),
    ("Какой доступ к устройству называется внеполосным (out-of-band)?",
     [("Через консольный порт", 1), ("По протоколу Telnet", 0), ("По протоколу SSH", 0)]),
    ("Чем приглашение esr# отличается от esr&gt;?",
     [("Это привилегированный режим", 1), ("Это режим глобального конфигурирования", 0),
      ("Это режим настройки интерфейса", 0)]),
    ("Куда попадают введённые настройки до команды commit?",
     [("В candidate-config", 1), ("Сразу в running-config", 0), ("В factory-config", 0)]),
    ("Что произойдёт, если после commit не ввести confirm?",
     [("Через 600 с маршрутизатор вернётся к прежней конфигурации", 1),
      ("Настройки будут потеряны сразу", 0), ("Устройство перезагрузится", 0)]),
    ("Учётная запись по умолчанию на маршрутизаторах ESR —",
     [("admin / password", 1), ("admin / admin", 0), ("root / toor", 0)]),
    ("Сколько физических коммутаторов можно объединить в один стек?",
     [("До 8", 1), ("До 4", 0), ("До 16", 0)]),
    ("Что делает команда end?",
     [("Возвращает в привилегированный режим из любого", 1),
      ("Выходит на уровень назад", 0), ("Закрывает сеанс", 0)]),
]


def quiz_html():
    qs = []
    for i, (q, opts) in enumerate(QUIZ_Q, 1):
        bs = "".join('<button class="btn" type="button" data-a="%d">%s</button>' % (a, o)
                     for o, a in opts)
        qs.append('<div class="q"><p>%d. %s</p>%s</div>' % (i, q, bs))
    return """
<section class="slide wide" data-label="Проверь себя">
 <header class="shead">
  <div class="kicker">Контроль</div>
  <h2>Проверь себя</h2>
  <div class="sub">SELF CHECK</div>
 </header>
 <div class="sbody"><div class="quiz ice">%s</div></div>
</section>""" % "".join(qs)


def main():
    paras = json.load(io.open(os.path.join(ROOT, "sources", "eltex-paras.json"), encoding="utf8"))
    media = json.load(io.open(os.path.join(ROOT, "sources", "eltex-media.json"), encoding="utf8"))
    css = io.open(os.path.join(ROOT, "_eltex_style.css"), encoding="utf8").read()
    js = io.open(os.path.join(ROOT, "_eltex_engine.js"), encoding="utf8").read()

    body = [TITLE_SLIDE.format(shot=img_tag(media["1"][0]["f"] if media.get("1") else "image1.png",
                                            "title-shot") or
                               img_tag("image1.png", "title-shot"))]
    for n in range(2, 85):
        body.append(build_slide(n, paras[str(n)], media.get(str(n), [])))
    body.append(LAB)
    body.append(quiz_html())

    html = """<!doctype html>
<html lang="ru"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Сетевые устройства Eltex</title>
<style>%s</style>
</head><body>
%s
<div id="deck">%s</div>
<div id="prog"></div>
<div id="bar">
 <b id="count"></b><span id="sname"></span><span class="grow"></span>
 <button class="btn" id="bprev" type="button">Назад</button>
 <button class="btn" id="bnext" type="button">Вперёд</button>
 <button class="btn" id="bspeed" type="button">1×</button>
 <button class="btn" id="btoc" type="button">Содержание</button>
</div>
<div id="toc"><h3>Содержание</h3><div id="tocg"></div></div>
<script>%s</script>
</body></html>""" % (css, FROST, "".join(body), js)

    with io.open(OUT, "w", encoding="utf8") as fh:
        fh.write(html)
    print("decks/eltex-devices.html  %.1f МБ" % (os.path.getsize(OUT) / 1048576))


if __name__ == "__main__":
    main()
