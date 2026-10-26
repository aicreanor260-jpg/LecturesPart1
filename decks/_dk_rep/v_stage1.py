# -*- coding: utf-8 -*-
"""VLAN: этап 1 — приём кадра на красный порт (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 160

CSS = """<style>
.vs1-b{position:absolute;box-sizing:border-box;border:4px solid #3a1606;box-shadow:5px 5px 0 #000;background:#fff8ea}
.vs1-sub{font:800 40px/66px "Golos Text",sans-serif;color:#1a0a04;text-align:center}
.vs1-sub b{color:#e8141e}
.vs1-t{position:absolute;font:700 23px/1.25 "Golos Text",sans-serif;color:#1a0a04}
.vs1-t b{color:#e8141e}
.vs1-ff{color:#e8141e;font:800 25px/1 "Golos Text",monospace;letter-spacing:.03em}
.vs1-n{position:absolute;width:62px;height:62px;border:4px solid #1a0a04;border-radius:50%;box-sizing:border-box;
  font:800 36px/54px "Golos Text",sans-serif;text-align:center;color:#fff}
.vs1-pl{position:absolute;box-sizing:border-box;border:4px solid #1a0a04;box-shadow:4px 4px 0 #000;color:#fff;
  font:700 24px/38px "Pixelify Sans",sans-serif;text-align:center}
.vs1-h{position:absolute;font:800 28px/1 "Golos Text",sans-serif;color:#1a0a04}
.vs1-li{position:absolute;font:500 23px/1.3 "Golos Text",sans-serif;color:#1a2a5a}
.vs1-grn{background:#3fae3a;border-color:#1c4a14;color:#fff;font:800 30px/58px "Golos Text",sans-serif;text-align:center}
.vs1-arr{position:absolute;left:230px;top:428px;width:350px;height:100px}
.vs1-env{animation:vs1e 2.6s ease-in-out infinite}
@keyframes vs1e{0%{transform:translateX(-110px);opacity:0}20%{opacity:1}75%{transform:translateX(0);opacity:1}100%{transform:translateX(0);opacity:1}}
.vs1-port{animation:vs1p 1.3s steps(2) infinite}
@keyframes vs1p{50%{box-shadow:0 0 0 4px #ff2020,0 0 22px 6px #ff4040}}
</style>"""

def b(x, y, w, h, cls="", inner="", st=""):
    return '<div class="vs1-b %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s">%s</div>' % (cls, x, y, w, h, st, inner)

def t(x, y, s, cls="vs1-t", st=""):
    return '<div class="%s" style="left:%dpx;top:%dpx;%s">%s</div>' % (cls, x, y, st, s)

def stepcard(y, n, col, txt, ico, ix, iy, iw, hh=126):
    return ('<div class="step">' + b(1190, y, 460, hh) + '<div class="vs1-n" style="left:1208px;top:%dpx;background:%s;%s">%d</div>'
            % (y + 30, col, "color:#1a0a04" if col == "#ffd21e" else "", n)
            + t(1292, y + 18, txt) + img(ico, "left:%dpx;top:%dpx;width:%dpx" % (ix, iy, iw)) + '</div>')

HTML = CSS + bg("bgk_hills") + "".join([
    '<div class="step">' + b(345, 172, 982, 72, "vs1-sub", "<b>Этап 1.</b> Приём кадра на красный порт") + '</div>',
    '<div class="step">' + b(25, 280, 1146, 356, "", "", "background:rgba(255,248,234,.96)")
    + img("v_stage1_pc.png", "left:42px;top:398px;width:200px")
    + b(64, 562, 144, 42, "", '<div class="vs1-h" style="position:static;text-align:center;font-size:24px;line-height:34px">ПК</div>', "background:#eee;box-shadow:none;border-width:3px")
    + '<svg class="vs1-arr" viewBox="0 0 350 100"><defs><linearGradient id="vs1g"><stop offset="0" stop-color="#ff6b6b" stop-opacity=".2"/><stop offset="1" stop-color="#e8141e"/></linearGradient></defs>'
      '<path d="M0 30h290V0l58 50-58 50V70H0z" fill="url(#vs1g)" stroke="#a00010" stroke-width="3"/></svg>'
    + b(222, 304, 364, 84, "", t(22, 14, "Широковещательный MAC:", "vs1-t", "position:absolute")
        + t(46, 44, "FF:FF:FF:FF:FF:FF", "vs1-ff", "position:absolute"), "box-shadow:none;border-radius:0")
    + '<svg style="position:absolute;left:392px;top:386px" width="30" height="34"><path d="M2 0l13 30L28 0" fill="#fff8ea" stroke="#3a1606" stroke-width="4"/></svg>'
    + '<div class="vs1-env" style="position:absolute;left:322px;top:436px">' + img("v_stage1_env.png", "position:static;width:116px") + '</div>'
    + b(272, 516, 224, 66, "", '<div class="vs1-t" style="position:static;text-align:center;padding-top:4px">Ethernet-кадр<br>без тега</div>', "box-shadow:none")
    + '</div>',
    '<div class="step">' + img("v_stage1_sw.png", "left:585px;top:338px;width:577px")
    + b(662, 356, 440, 70, "", '<div class="vs1-t" style="position:static;text-align:center;padding-top:4px">Определение VLAN<br>по PVID порта</div>',
        "background:#e9e9ef;border-color:#2a2a36;box-shadow:none;padding:0 50px")
    + '<div class="vs1-port" style="position:absolute;left:610px;top:458px;width:84px;height:84px"></div>'
    + '<div class="vs1-pl" style="left:630px;top:550px;width:218px;background:#e8141e">VLAN 10</div>'
    + '<div class="vs1-pl" style="left:902px;top:550px;width:218px;background:#1f5fe0">VLAN 20</div></div>',
    stepcard(266, 1, "#e8141e", "Устройство<br>отправляет<br>нетегированный кадр", "v_stage1_lap.png", 1553, 292, 74),
    stepcard(404, 2, "#ffd21e", "Коммутатор относит<br>кадр к <b>VLAN 10</b><br>по настройке<br>входного порта", "v_stage1_port.png", 1553, 462, 74, 148),
    stepcard(566, 3, "#1f5fe0", "Рассылка возможна<br>только внутри <b>VLAN 10</b>,<br>кроме входного порта", "v_stage1_mega.png", 1582, 607, 60),
    '<div class="step">' + b(230, 652, 496, 168, "", "", "background:#eef0ff;border-color:#2a2a5a")
    + t(290, 672, "На выходе trunk:", "vs1-h") + img("v_stage1_tag.png", "left:252px;top:703px;width:130px")
    + t(398, 712, "• добавляется тег 802.1Q<br>&nbsp;&nbsp;&nbsp;(4 байта)<br>• пересчитывается FCS", "vs1-li")
    + b(744, 652, 422, 168, "") + t(806, 672, "На выходе access:", "vs1-h") + img("v_stage1_env2.png", "left:793px;top:718px;width:99px")
    + t(924, 730, "• кадр передаётся<br>&nbsp;&nbsp;&nbsp;без тега", "vs1-li") + '</div>',
    '<div class="step">' + b(330, 838, 1014, 64, "vs1-grn", "Красные и синие порты принадлежат разным VLAN") + '</div>',
])
