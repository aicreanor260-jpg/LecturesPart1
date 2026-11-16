# -*- coding: utf-8 -*-
"""Общие блоки титула и финала дек комплекта (шпаргалка, задачи, тренажёры, тест, итоги, финал)."""
from _sw_lib import slide, head, sc, grow, col, card, li, step, p, tags, tag


def cover(big, lead, tg, kicker="Лекция · Сетевые технологии"):
    slide("Титул", sc('<div class="cover"><div class="lead" style="font-weight:900;letter-spacing:.12em;text-transform:uppercase">%s</div><div class="big">%s</div><div class="lead">%s</div>%s'
                      '<div class="lead" style="font-size:clamp(12px,.95vw,17px)">← → шаги · ↑ ↓ слайды · Esc — содержание</div></div>'
                      % (kicker, big, lead, tags(*[tag(t, c) for t, c in tg]))), cover=True)


def qslide(title, sub, qs):
    slide(title, sc(head(title.replace("Тест", "<em>Тест</em>"), sub), grow("g2", col(*qs[:2]), col(*qs[2:])),
                    '<div class="foot" style="margin-top:8px"><i>✓</i><span>Результат по всем вопросам: '
                    '<span class="score">0 / 0</span></span></div>'))


def tslide(title, sub, items):
    slide(title, sc(head(title.replace("задачи", "<em>задачи</em>"), sub), grow("g2", col(*items[:2]), col(*items[2:]))))


def sslide(title, sub, box):
    slide(title, sc(head(title.replace("Тренажёр", "<em>Тренажёр</em>"), sub), grow("g", col(box))))


def remember(sub, left, right):
    slide("Что запомнить", sc(head("Что <em>запомнить</em>", sub), grow("g2",
        col(*[step(card(t, li(x), c)) for t, x, c in left]), col(*[step(card(t, li(x), c)) for t, x, c in right]))))


def final(sub, nxt):
    slide("Финал", sc(head("<em>Спасибо</em> за внимание", sub), grow("g2",
        col(step(card("Что дальше", li(nxt), "cy"))),
        col(step(card("Контакты", tags(tag("VKontakte", "v"), tag("Telegram")) + p("Вопросы по лекции и лабораторным — пишите."), "mg"))))))
