# -*- coding: utf-8 -*-
"""MPLS 2.9 v2 — титул и финал. Содержание финала (шпаргалка, задачи, тренажёры, живой тренажёр LSP, тест, итоги)
берётся из _mp_final; слайды получают фон комплекта и рамку v2."""
import _sw_lib as L
import _mp_final as FIN
from _mp2_kit import slide, step, _bg_used

# фон для слайдов финала по порядку (циклом)
FIN_BG = ["bgk_29", "bgk_25", "bgk_26", "bgk_28", "bgk_06", "bgk_24", "bgk_27", "bgk_20", "bgk_21", "bgk_22", "bgk_10"]


def head():
    slide("Титул", "bgk_11", "", "".join([
        '<div class="m2cover">',
        '<div class="m2cv-big">MPLS</div>',
        '<div class="m2cv-lead">Технологии внутри оператора связи</div>',
        step('<div class="m2cv-tags"><span class="m2pill bl">2.9</span><span class="m2pill or">метки · LSP</span>'
             '<span class="m2pill gr">LDP · RSVP-TE</span><span class="m2pill bl">LSP Ping · BFD</span>'
             '<span class="m2pill or">MPLS TE · защита</span><span class="m2pill gr">Segment Routing</span></div>'),
        '<div class="m2cv-hint">← → шаги · ↑ ↓ слайды · Esc — содержание · в сценах кнопки «Назад / Вперёд»</div>',
        '</div>']))
    L.SL[-1] = L.SL[-1].replace('class="slide m2 ', 'class="slide m2 cover-slide ', 1)


def tail():
    n0 = len(L.SL)
    FIN.tail()
    for i in range(n0, len(L.SL)):
        bg = FIN_BG[(i - n0) % len(FIN_BG)]
        _bg_used.add(bg)
        L.SL[i] = L.SL[i].replace('<section class="slide', '<section class="slide mpold %s' % bg, 1)


def build():
    pass


CSS = FIN.CSS + r"""
.slide.mpold{background-color:#4aa8f0}
.slide.mpold .head h1.t{font-size:clamp(26px,2.9vw,56px)}
.slide.mpold .c ul.li li,.slide.mpold .c p{font-size:clamp(15px,1.3vw,26px)!important;line-height:1.38}
.slide.mpold .ch h3{font-size:clamp(16px,1.45vw,28px)!important}
.slide.mpold[data-label="Шпаргалка"] .c ul.li li{font-size:clamp(13px,1.08vw,21px)!important}
.slide.mpold .q .qt{font-size:clamp(14px,1.15vw,22px)}
.slide.mpold .opts button{font-size:clamp(13px,1.02vw,20px)}
.m2cover{margin:auto auto auto 3vw;max-width:860px;background:rgba(253,248,234,.94);border:3px solid #1f63c6;border-radius:26px;
 padding:clamp(20px,2.4vw,44px) clamp(24px,3vw,56px);box-shadow:0 8px 0 rgba(21,80,168,.3),0 16px 40px rgba(10,40,90,.3)}
.m2cv-big{font:900 clamp(80px,10vw,190px)/.95 "Rubik",sans-serif;color:#1f63c6;letter-spacing:-.02em}
.m2cv-lead{font:800 clamp(22px,2.3vw,44px)/1.2 "Rubik",sans-serif;color:#e8742c;margin:.2em 0 .6em}
.m2cv-tags{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}
.m2cv-hint{font:600 clamp(12px,.95vw,17px)/1.3 "Golos Text",sans-serif;color:#3e5175}
.slide.m2.cover-slide>.m2in{justify-content:center}
.slide.m2.cover-slide h1.m2t{display:none}
"""
JS = FIN.JS
