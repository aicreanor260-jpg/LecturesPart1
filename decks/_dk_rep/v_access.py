# -*- coding: utf-8 -*-
"""VLAN: порты доступа — вход/выход кадра и 4 шага обработки, вёрстка на пиксельном фоне."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 128

CSS = """<style>
.vac{position:absolute;box-sizing:border-box}
.vac-pan{background:#fdf7e6;border:4px solid #fff;outline:3px solid #3a1606;box-shadow:5px 5px 0 #000}
.vac-rib{color:#fff;font:700 31px/50px "Pixelify Sans",monospace;padding-left:30px;white-space:nowrap;text-shadow:2px 2px 0 rgba(0,0,0,.35)}
.vac-t{font:600 23px/1.25 "Golos Text",sans-serif;color:#1a1a2a}
.vac-c{font:700 20px/1.1 "Golos Text",sans-serif;color:#1a1a2a;text-align:center}
.vac-red{background:#e8303a;color:#fff;border:3px solid #8a0a10;font:800 19px/1.15 "Golos Text",sans-serif;text-align:center;padding-top:3px}
.vac-zone{border:3px dashed #7a8fa8;background:rgba(190,215,240,.45)}
.vac-gray{background:#7f93a8;color:#fff;font:600 20px/34px "Golos Text",sans-serif;text-align:center;border-radius:6px}
.vac-note{background:#e6dcf3;font:600 21px/36px "Golos Text",sans-serif;text-align:center;color:#1a1a2a}
.vac-num{color:#fff;font:900 54px/76px "Golos Text",sans-serif;text-align:center;border:3px solid #000;border-radius:6px}
.vac-h{font:700 33px/1 "Pixelify Sans",monospace;color:#111}
.vac-foot{background:#3fae3a;border:5px solid #1d6e1a;box-shadow:5px 5px 0 #000;color:#fff;
  font:800 27px/50px "Golos Text",sans-serif;text-align:center;text-shadow:2px 2px 0 #1d4a1a}
.vac-mv{animation:vacm 2.6s ease-in-out infinite}
@keyframes vacm{50%{transform:translateX(12px)}}
</style>"""


def box(x, y, w, h, cls, inner="", st=""):
    return '<div class="vac %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s">%s</div>' % (cls, x, y, w, h, st, inner)


def env(x, y, w, fill="#fff"):
    return ('<svg class="vac" style="left:%dpx;top:%dpx" width="%d" height="%d" viewBox="0 0 70 49">'
            '<rect x="2" y="2" width="66" height="45" fill="%s" stroke="#222" stroke-width="3"/>'
            '<path d="M2 2 L35 28 L68 2" fill="none" stroke="#222" stroke-width="3"/></svg>' % (x, y, w, int(w * .7), fill))


def arr(x1, y, x2, col="#1e9a3e", dash=False):
    return ('<svg class="vac" style="left:0;top:0;overflow:visible" width="1" height="1"><defs><marker id="vaca%s" viewBox="0 0 10 10" refX="5" refY="5" '
            'markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="%s"/></marker></defs>'
            '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="5" %s marker-end="url(#vaca%s)"/></svg>'
            % (col[1:], col, x1, y, x2, y, col, 'stroke-dasharray="8 6"' if dash else "", col[1:]))


def step(y, n, col, ico, title, text):
    return ('<div class="step">' + box(1095, y, 545, 140, "vac-pan")
            + box(1110, y + 22, 72, 80, "vac-num", str(n), "background:%s" % col)
            + ico + box(1316, y + 28, 320, 34, "vac-h", title)
            + box(1318, y + 68, 320, 70, "vac-t", text) + '</div>')


IN = ('<div class="step">' + box(50, 290, 1020, 230, "vac-pan")
      + box(58, 296, 368, 50, "vac-rib", "Вход в коммутатор", "background:#1aa6a6;clip-path:polygon(0 0,96% 0,100% 100%,0 100%)")
      + img("v_access_pc1.png", "left:123px;top:348px;width:104px") + box(130, 428, 90, 26, "vac-c", "ПК")
      + arr(236, 386, 320) + '<div class="vac-mv" style="position:absolute;left:0;top:0">' + env(333, 360, 80) + '</div>'
      + box(310, 422, 120, 26, "vac-c", "Без тега", "font-weight:600")
      + arr(424, 386, 510) + img("v_access_port.png", "left:514px;top:344px;width:94px")
      + box(476, 415, 175, 54, "vac-red", "Access VLAN 10<br>PVID 10")
      + arr(613, 386, 735)
      + box(660, 322, 330, 142, "vac-zone") + box(752, 304, 158, 34, "vac-gray", "Коммутатор")
      + env(804, 354, 80) + box(743, 398, 200, 58, "vac-red", "Принадлежность:<br>VLAN 10")
      + box(60, 476, 1000, 38, "vac-note", "VLAN назначается по настройке входного порта.") + '</div>')

OUT = ('<div class="step">' + box(50, 528, 1020, 290, "vac-pan")
       + box(58, 534, 370, 50, "vac-rib", "Выход к устройству", "background:#e8434a;clip-path:polygon(0 0,96% 0,100% 100%,0 100%)")
       + box(198, 588, 475, 178, "vac-zone") + box(488, 557, 154, 34, "vac-gray", "Коммутатор")
       + env(270, 604, 82, "#f7b6b8") + box(258, 646, 108, 28, "vac-red", "VLAN 10", "background:#d8202c;padding-top:1px")
       + arr(360, 638, 510) + img("v_access_port.png", "left:516px;top:606px;width:94px")
       + env(272, 690, 80, "#7fc0f0") + box(258, 730, 108, 28, "vac-red", "VLAN 20", "background:#1a3a6a;border-color:#0a1a3a;padding-top:1px")
       + arr(358, 716, 418, "#5a6f88", True) + img("v_access_x.png", "left:423px;top:688px;width:64px")
       + box(495, 692, 170, 54, "vac-t", "Другая VLAN —<br>передачи нет.", "font-size:21px")
       + arr(613, 638, 712) + env(722, 610, 76) + box(705, 668, 115, 26, "vac-c", "Без тега", "font-weight:600")
       + arr(806, 638, 880) + img("v_access_pc2.png", "left:886px;top:596px;width:108px")
       + box(890, 680, 90, 26, "vac-c", "ПК")
       + box(60, 774, 1000, 38, "vac-note", "На линию к ПК кадр передаётся без метки 802.1Q.") + '</div>')

HTML = CSS + bg("bgk_ground") + "".join([
    box(385, 132, 902, 50, "vac-pan", "Access-порт: подключение конечного устройства&nbsp; к одной VLAN.",
        "outline:none;border:4px solid #3a1606;font:800 24px/42px 'Golos Text',sans-serif;text-align:center"),
    '<div class="step">' + box(128, 194, 918, 82, "vac-pan")
    + img("v_access_pc0.png", "left:158px;top:203px;width:94px")
    + box(282, 206, 700, 64, "vac-t", "Обычный ПК обменивается с access-портом<br>нетегированными Ethernet-кадрами.") + '</div>',
    IN, OUT,
    step(205, 1, "#2a9a32", env(1210, 240, 76), "Приём:", "обычно нетегированные<br>кадры."),
    step(355, 2, "#1f86e0", img("v_access_gear.png", "left:1203px;top:383px;width:89px"), "Классификация:", "VLAN определяется<br>по PVID порта."),
    step(510, 3, "#8a4ad8", img("v_access_fun.png", "left:1203px;top:538px;width:89px"), "Фильтрация:", "выход разрешён только<br>для VLAN порта."),
    step(665, 4, "#e8434a", img("v_access_doc.png", "left:1210px;top:688px;width:77px"), "Передача:",
         "кадр выходит без тега;<br>при изменении кадра<br>FCS пересчитывается.").replace("height:140px", "height:155px", 1),
    '<div class="step">' + box(218, 834, 1232, 58, "vac-foot", "★ &nbsp;Для ПК — обычный Ethernet.&nbsp; Для коммутатора — трафик назначенной VLAN. &nbsp;★")
    + box(255, 896, 1162, 42, "vac-t", "ⓘ&nbsp; Обработка входящих tagged-кадров зависит от модели и настроек; возможны исключения, например Voice VLAN.",
          "background:#e6f2ff;font-size:18px;line-height:42px;text-align:center") + '</div>',
])
