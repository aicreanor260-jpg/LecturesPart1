# -*- coding: utf-8 -*-
"""pptx: Продвижение MPLS-кадра — два домена, LSP1/LSP2 — вёрстка поверх bgk_20."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 108

CSS = """<style>
.i20-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i20-t{position:absolute;font:500 21px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i20-cl{position:absolute;border-radius:70px}
.i20-dm{position:absolute;font:800 26px/42px "Golos Text",sans-serif;color:#13306e;text-align:center;border-radius:21px}
.i20-n{position:absolute;font:800 20px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:140px}
.i20-op{position:absolute;font:700 19px/34px "Golos Text",sans-serif;color:#13306e;text-align:center;width:134px;white-space:nowrap;font-size:17.5px;border-radius:8px;
 background:rgba(255,255,255,.55);border:2px solid rgba(29,63,138,.25)}
.i20-lb{position:absolute;font:700 21px/34px "Golos Text",sans-serif;color:#1d1d1d;text-align:center;width:54px;background:#f2694a;border:2px solid #1d3f8a;border-radius:3px}
.i20-ar{position:absolute;height:3px;background:#1d3f8a}
.i20-ar::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:12px solid #1d3f8a;border-right:0}
.i20-al{position:absolute;height:3px;background:#1d3f8a}
.i20-al::after{content:"";position:absolute;left:-2px;top:-7px;border:8px solid transparent;border-right:12px solid #1d3f8a;border-left:0}
.i20-ic{position:absolute;width:92px;height:92px;border-radius:50%;background:#ccefea}
.i20-hh{display:block;font:900 22px/1.4 "Rubik",sans-serif;color:#13306e}
.i20-fly{animation:i20f 2.6s ease-in-out infinite}
@keyframes i20f{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
</style>"""


def node(x, y, name, op_, top_name=True, grey=False):
    ny = y - 26 if top_name else y + 72
    s = img("i20a_rg.png" if grey else "i20a_rt.png", "left:%dpx;top:%dpx;width:96px" % (x, y)) + \
        '<div class="i20-n" style="left:%dpx;top:%dpx">%s</div>' % (x - 22, ny, name)
    if op_:
        s += '<div class="i20-op" style="left:%dpx;top:%dpx">%s</div>' % (x - 17, y + 64, op_)
    return s


def lb(x, y, t):
    return '<div class="i20-fly" style="position:absolute;left:%dpx;top:%dpx"><div class="i20-lb" style="left:0;top:0">%s</div></div>' % (x, y, t)


def ar(x, y, w, left=False):
    return '<div class="%s" style="left:%dpx;top:%dpx;width:%dpx"></div>' % ("i20-al" if left else "i20-ar", x, y, w)


TOP_ROW = [(270, "LER1", "Push 256"), (506, "LSR1", "Swap 272"), (730, "LSR2", "Swap 132"), (962, "LSR3", "Pop"),
           (1178, "LER2", "IP-пересылка")]
BOT_ROW = [(272, "LER4", "IP-пересылка"), (500, "LSR6", "Pop"), (730, "LSR5", "Swap 101"), (956, "LSR4", "Swap 112"),
           (1178, "LER3", "Push 188")]

HTML = CSS + bg("bgk_20") + "".join([
    '<div class="step">',
    '<div class="i20-p" style="left:118px;top:114px;width:920px;height:50px;border-radius:12px"></div>',
    '<div class="i20-t" style="left:140px;top:120px;width:900px;font-size:26px;line-height:38px;font-weight:600;color:#13306e">Решение о продвижении прини!мается по верхней метке стека.</div>',
    '<div class="i20-t" style="left:1058px;top:116px;width:546px;height:48px;background:#bfe9e4;border:2px solid #fdf8ea;border-radius:12px;'
    'font-size:16px;line-height:44px;text-align:center"><b style="color:#13306e">Одноуровневый LSP:</b> одна MPLS-метка, без вложенных путей.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i20-p" style="left:52px;top:180px;width:1568px;height:452px;border-radius:22px"></div>',
    '<div class="i20-cl" style="left:212px;top:224px;width:1100px;height:176px;background:#cfe7fb"></div>',
    '<div class="i20-dm" style="left:640px;top:194px;width:336px;background:#cfe7fb">MPLS-домен 1 • LSP1</div>',
    '<div class="i20-t" style="left:80px;top:284px;width:120px;text-align:center;font-weight:600;color:#13306e">IP-пакет<br>(вход)</div>',
    '<div class="i20-ar" style="left:188px;top:315px;width:68px;background:#2b6f80"></div>',
    "".join(node(x, 282, n, o) for x, n, o in TOP_ROW),
    ar(368, 312, 132), lb(406, 293, 256), ar(598, 312, 126), lb(638, 293, 272), ar(828, 312, 126), lb(866, 293, 132),
    ar(1054, 312, 118), '<div class="i20-n" style="left:1060px;top:290px;width:110px">IP</div>',
    '</div>',
    '<div class="step">',
    '<div class="i20-cl" style="left:1306px;top:210px;width:300px;height:372px;background:#e3e3e3"></div>',
    '<div class="i20-n" style="left:1360px;top:246px;width:220px;font-size:23px;color:#555">MPLS-домен 3</div>',
    node(1426, 310, "LER5", "", grey=True), node(1426, 444, "LER6", "", top_name=False, grey=True),
    '<div style="position:absolute;left:1472px;top:376px;width:3px;height:70px;background:#666"></div>',
    '<svg style="position:absolute;left:1264px;top:316px" width="170" height="226"><path d="M0 4 L160 34 M0 220 L160 168" style="stroke:#666;stroke-width:3"/></svg>',
    '<div style="position:absolute;left:1220px;top:372px;width:4px;height:56px;background:#1d3f8a"></div>',
    '<div style="position:absolute;left:1210px;top:424px;border:12px solid transparent;border-top:16px solid #1d3f8a"></div>',
    '<div class="i20-n" style="left:1236px;top:378px;width:80px;text-align:left;line-height:1.1">IP без<br>метки</div>',
    '</div>',
    '<div class="step">',
    '<div class="i20-cl" style="left:228px;top:450px;width:1090px;height:168px;background:#cdeee4"></div>',
    '<div class="i20-dm" style="left:640px;top:426px;width:336px;background:#cdeee4">MPLS-домен 2 • LSP2</div>',
    '<div class="i20-t" style="left:72px;top:508px;width:120px;text-align:center;font-weight:600;color:#13306e">IP-пакет<br>(выход)</div>',
    ar(190, 534, 76, left=True),
    "".join(node(x, 504, n, o) for x, n, o in BOT_ROW),
    ar(368, 534, 130, left=True), lb(412, 515, "IP"), ar(598, 534, 128, left=True), lb(636, 515, 101),
    ar(828, 534, 124, left=True), lb(864, 515, 112), ar(1054, 534, 120, left=True), lb(1092, 515, 188),
    '</div>',
    '<div class="step">',
    '<div class="i20-p" style="left:344px;top:650px;width:916px;height:118px"></div>',
    '<div class="i20-ic" style="left:364px;top:662px"></div>', img("i20a_tag.png", "left:364px;top:660px;width:94px"),
    '<div class="i20-t" style="left:474px;top:664px;width:780px;font-size:19.5px"><span class="i20-hh">СНЯТИЕ МЕТКИ НА ПРЕДПОСЛЕДНЕМ УЗЛЕ</span>'
    'LSR3 и LSR6 выполняют Pop. LER2 и LER4 получают IP-пакет без метки.<br>На границе доменов LER3 добавляет новую метку 188 для LSP2.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i20-p" style="left:432px;top:782px;width:788px;height:142px"></div>',
    '<div class="i20-ic" style="left:458px;top:798px"></div>', img("i20a_ch.png", "left:452px;top:790px;width:104px"),
    '<div class="i20-t" style="left:578px;top:790px;width:640px;font-size:19.5px;line-height:1.22"><span class="i20-hh">МЕЖДУ ДОМЕНАМИ: СШИВАНИЕ LSP</span>'
    'LSP1 и LSP2 можно связать в единый одноуровневый путь.<br>Недостаток: требуется согласование между доменами,<br>'
    'что ограничивает независимость разных операторов.<br><span style="font-size:15px;color:#1f63c6">На схеме выше показаны отдельные LSP с '
    'IP-пересылкой между ними.</span></div>',
    '</div>',
])
