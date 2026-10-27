# -*- coding: utf-8 -*-
"""pptx: Операции над стеком меток Push/Swap/Pop — вёрстка поверх bgk_08."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg

W, H, TOP = 1672, 941, 168

CSS = """<style>
.i17-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i17-h{position:absolute;font:900 33px/50px "Rubik",sans-serif;color:#13306e;text-align:center;background:#ccefea;border-radius:25px}
.i17-pl{position:absolute;font:600 20px/32px "Golos Text",sans-serif;color:#13306e;text-align:center;background:#d6ebfb;border-radius:16px;width:110px}
.i17-st{position:absolute;width:108px}
.i17-st div{height:42px;margin-top:2px;border:3px solid #1d3f8a;border-radius:6px;font:700 24px/36px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i17-sh{position:absolute;height:14px;border-radius:50%;background:rgba(29,63,138,.15)}
.i17-ar{position:absolute;font:900 44px/1 "Golos Text",sans-serif;color:#1d3f8a}
.i17-t{position:absolute;font:500 21px/1.42 "Golos Text",sans-serif;color:#1d2a44;text-align:center}
.i17-n{position:absolute;font:500 20px/44px "Golos Text",sans-serif;color:#1d2a44;text-align:center;background:#d9f0e4;border-radius:22px}
.i17-drop{animation:i17d 2.8s ease-in-out infinite}
@keyframes i17d{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
</style>"""

C = {"r": "#f2845f", "b": "#9ccaf2", "y": "#fbd56a", "w": "#fff"}


def st(x, y, cells, cls=""):
    return '<div class="i17-st %s" style="left:%dpx;top:%dpx">%s</div>' % (
        cls, x, y, "".join('<div style="background:%s">%s</div>' % (C[c], t) for t, c in cells)) + \
        '<div class="i17-sh" style="left:%dpx;top:%dpx;width:150px"></div>' % (x - 21, y + 44 * len(cells) + 6)


def card(x, title, before, after, ab, t1, t2, note, extra=""):
    return "".join([
    '<div class="step"><div style="position:absolute;left:112px;top:172px;width:1200px;text-align:left;font:800 44px/1.2 Rubik,sans-serif;color:#fffbe8;text-shadow:0 2px 0 #1550a8,0 3px 8px rgba(10,40,90,.5)">Операции над стеком меток: Push, Swap и Pop</div></div>',
        '<div class="step">',
        '<div class="i17-p" style="left:%dpx;top:318px;width:454px;height:446px"></div>' % x,
        '<div class="i17-h" style="left:%dpx;top:334px;width:418px">%s</div>' % (x + 18, title),
        '<div class="i17-pl" style="left:%dpx;top:398px">До</div>' % (x + 84),
        '<div class="i17-pl" style="left:%dpx;top:396px;width:122px">После</div>' % (x + 290),
        st(x + 86, 588 - 44 * len(before), before), '<div class="i17-ar" style="left:%dpx;top:514px">➜</div>' % (x + 224),
        st(x + 300, 600 - 44 * len(after), after, "i17-drop"), extra,
        '<div class="i17-t" style="left:%dpx;top:622px;width:454px">%s<br>%s</div>' % (x, t1, t2),
        '<div class="i17-n" style="left:%dpx;top:702px;width:438px">%s</div>' % (x + 22, note),
        '</div>'])


HTML = CSS + bg("bgk_08") + "".join([
    '<div class="step">',
    '<div class="i17-p" style="left:114px;top:240px;width:1176px;height:52px;border-radius:16px"></div>',
    '<div class="i17-t" style="left:142px;top:242px;width:1100px;text-align:left;font:800 25px/48px Golos Text,sans-serif;color:#13306e">'
    'Операция задаётся в поле действий таблицы продвижения.</div>',
    '</div>',
    card(116, "PUSH — ДОБАВИТЬ", [("50", "b"), ("IP", "w")], [("100", "r"), ("50", "b"), ("IP", "w")], 0,
         "Новая метка помещается на вершину.", "Прежние метки сдвигаются в глубь стека.",
         'Пустой стек: IP → [<span style="color:#e2332a">100</span> | IP]',
         '<div class="i17-ar" style="left:456px;top:432px;font-size:30px">↓</div>'),
    card(606, "SWAP — ЗАМЕНИТЬ", [("100", "r"), ("50", "b"), ("IP", "w")], [("200", "y"), ("50", "b"), ("IP", "w")], 0,
         "Верхняя метка заменяется новой.", "Остальная часть стека не изменяется.", "Глубина стека сохраняется."),
    card(1076, "POP — СНЯТЬ", [("200", "y"), ("50", "b"), ("IP", "w")], [("50", "b"), ("IP", "w")], 0,
         "Верхняя метка удаляется.", "Следующая метка становится вершиной.", "Если меток больше нет — открыт IP-пакет.",
         '<div class="i17-st i17-drop" style="left:1424px;top:438px;width:80px"><div style="background:#fbd56a">200</div></div>'
         '<svg style="position:absolute;left:1376px;top:420px" width="150" height="100"><path d="M8 92 Q8 60 36 48" '
         'style="fill:none;stroke:#13306e;stroke-width:4"/><path d="M44 42 L28 44 L36 58Z" style="fill:#13306e"/>'
         '<path d="M118 16 L122 4 M132 24 L144 16 M136 40 L148 40" style="stroke:#13306e;stroke-width:3"/></svg>'),
    '<div class="step">',
    '<div class="i17-p" style="left:236px;top:790px;width:1200px;height:100px"></div>',
    '<div class="i17-t" style="left:236px;top:804px;width:1200px;font:800 29px/40px Golos Text,sans-serif;color:#13306e">'
    'Push: +1 метка <span style="color:#f29a2e">&nbsp;•&nbsp;</span> Swap: замена верхней <span style="color:#f29a2e">&nbsp;•&nbsp;</span> Pop: −1 метка</div>',
    '<div class="i17-t" style="left:236px;top:848px;width:1200px;font-size:20px">Вершина стека — метка, обрабатываемая первой.</div>',
    '</div>',
])
