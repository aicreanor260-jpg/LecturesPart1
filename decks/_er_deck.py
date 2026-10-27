# -*- coding: utf-8 -*-
"""Дека «Маршрутизаторы ESR» (2.3 доп.) — строго по порядку слайдов pptx «2_3».
Тексты и конфигурации — из pptx дословно (ошибки pptx перенесены как есть, вопросы — автору);
скриншоты консоли перерисованы терминалом, схемы — в стиле инфографик, инфографики автора — сразу за своим слайдом."""
import base64
import os
import re

from _sw_lib import card, p, li, slide, sc, head, grow, col, step, _esc
from _dk_kit import pslide, full, term, txt
import _er_fig as F
import _er_intro as I

HERE = os.path.dirname(os.path.abspath(__file__))
_PROMPT = re.compile(r"^(\S+?(?:\([^)]*\))?#)(.*)$")


def conf(lines, title="Конфигурация"):
    """Команды ESR: приглашение приглушено, команда выделена; прочие строки (вывод, синтаксис) — как есть."""
    out = []
    for ln in lines:
        m = _PROMPT.match(ln)
        if m and ("esr" in m.group(1) or m.group(1).startswith("R1")):
            out.append('<span class="p">%s</span><span class="k">%s</span>' % (_esc(m.group(1)), _esc(m.group(2))))
        else:
            out.append(_esc(ln))
    t = '<div class="clih">%s</div>' % _esc(title) if title else ""
    return '%s<pre class="cli">%s</pre>' % (t, "\n".join(out))


def syn(lines, title="Синтаксис"):
    return '<div class="clih">%s</div><pre class="cli syn">%s</pre>' % (title, "\n".join(_esc(l) for l in lines))


def pic(n):
    with open(os.path.join(HERE, "_er_assets", "p%02d.webp" % n), "rb") as fh:
        uri = "data:image/webp;base64," + base64.b64encode(fh.read()).decode()
    return '<div class="pic erpic"><img src="%s" alt="" loading="lazy"></div>' % uri


def info(n, title):
    """Инфографика автора к слайду pptx n — во весь слайд сразу за ним."""
    I.bleed(n, re.sub("<[^>]+>", "", title))


def build():
    # ---------------------------------------------------------------- pptx 2
    pslide("В этой главе", "В данной <em>главе</em>", [
        card("В данной главе будут рассмотрены:", li([
            "типы интерфейсов маршрутизатора ESR;", "способы проверки соединения;",
            "варианты аутентификации, поддерживающие маршрутизатор;", "базовая настройка маршрутизатора;",
            "процедура создания учетных записей пользователей с настройкой уровней привилегий."]), "cy")])
    # ---------------------------------------------------------------- pptx 3
    T3 = "Маршрутизатор <em>(Router)</em>"
    I.router_slide(T3)
    info(3, T3)
    # ---------------------------------------------------------------- pptx 4
    T4 = "Маршрутизатор <em>в сети Интернет</em>"
    I.internet_slide(T4)
    I.interfaces_slide(T4)
    I.home_slide(T4)
    info(4, T4)
    # ---------------------------------------------------------------- pptx 5
    T5 = "Основные функции <em>маршрутизаторов</em>"
    I.functions_slide(T5)
    info(5, T5)
    import _er_p1
    import _er_p2
    import _er_p3
    _er_p1.build()
    _er_p2.build()
    _er_p3.build()
