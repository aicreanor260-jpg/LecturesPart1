# -*- coding: utf-8 -*-
"""VLAN: передача кадра ПК1 -> ПК2 через access-порты SW1, таблица MAC — вёрстка на пиксельном фоне."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 98

CSS = """<style>
.vap{position:absolute;box-sizing:border-box}
.vap-pan{background:#fdf7e6;border:4px solid #3a1606;box-shadow:5px 5px 0 #000}
.vap-lil{background:#e9dcfb;border:4px solid #3a1606;box-shadow:4px 4px 0 #000;font:700 21px/1.15 "Golos Text",sans-serif;text-align:center;color:#1a1a3a}
.vap-bub{background:#fff;border:3px solid #3a1606;font:700 21px/40px "Golos Text",sans-serif;text-align:center;color:#1a1a2a;border-radius:10px}
.vap-big{font:700 32px/1 "Pixelify Sans",monospace;color:#1a3a8a;text-align:center}
.vap-t{font:600 22px/1.25 "Golos Text",sans-serif;color:#1a1a2a}
.vap-hd{background:#5a2e8a;color:#fff;font:700 32px/1 "Pixelify Sans",monospace;text-align:center}
.vap-tb{border-collapse:collapse;font:600 24px/1 "Golos Text",sans-serif;color:#1a1a2a;text-align:center}
.vap-tb td,.vap-tb th{border:2px solid #4a5a8a;height:68px}
.vap-tb th{background:#e3eefc;font-weight:700;height:54px}
.vap-tag{color:#fff;font:600 22px/1.15 "Golos Text",sans-serif;padding:8px 0 0 18px;clip-path:polygon(8% 0,100% 0,100% 100%,8% 100%,0 50%)}
.vap-n{font:900 28px/48px "Golos Text",sans-serif;color:#3a1606;text-align:center;background:#ffcc22;border:4px solid #3a1606;border-radius:50%}
.vap-row{background:#fff;border:3px solid #3a2a6a;border-radius:8px;font:600 22px/1.15 "Golos Text",sans-serif;color:#1a1a2a;padding:6px 18px}
.vap-row b{color:#1f7a5a}
.vap-foot{background:#3fae3a;border:5px solid #1d6e1a;box-shadow:5px 5px 0 #000;color:#fff;
  font:800 29px/34px "Golos Text",sans-serif;text-align:center;padding-top:8px;text-shadow:2px 2px 0 #1d4a1a}
.vap-mv{animation:vapm 3s linear infinite}
@keyframes vapm{0%{transform:translateX(-30px)}50%{transform:translateX(30px)}100%{transform:translateX(-30px)}}
</style>"""


def box(x, y, w, h, cls, inner="", st=""):
    return '<div class="vap %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s">%s</div>' % (cls, x, y, w, h, st, inner)


def env(x, y, w):
    return ('<svg class="vap" style="left:%dpx;top:%dpx" width="%d" height="%d" viewBox="0 0 70 49">'
            '<rect x="2" y="2" width="66" height="45" fill="#fff" stroke="#222" stroke-width="3"/>'
            '<path d="M2 2 L35 28 L68 2" fill="none" stroke="#222" stroke-width="3"/></svg>' % (x, y, w, int(w * .7)))


LINE = ('<svg class="vap" style="left:0;top:0;overflow:visible" width="1" height="1"><defs><marker id="vapa" viewBox="0 0 10 10" refX="5" refY="5" '
        'markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="#1a3ac8"/></marker></defs>'
        '<line x1="265" y1="266" x2="650" y2="266" stroke="#1a3ac8" stroke-width="5" marker-end="url(#vapa)"/>'
        '<line x1="1000" y1="266" x2="1410" y2="266" stroke="#1a3ac8" stroke-width="5" marker-end="url(#vapa)"/></svg>')

ROWS = '<tr><td>10</td><td>00:11:22:33:44:01</td><td>Gi0/1</td><td>Dynamic</td></tr>'
TABLE = ('<div class="step">' + box(25, 478, 888, 337, "vap-pan")
         + box(29, 482, 880, 82, "vap-hd", "Таблица MAC-адресов SW1<div style='font:600 21px \"Golos Text\",sans-serif;margin-top:10px'>ПК2 уже передавал кадры; его запись известна</div>", "padding-top:10px")
         + '<table class="vap vap-tb" style="left:42px;top:578px;width:686px"><tr><th style="width:98px">VID</th><th style="width:258px">MAC-address</th><th style="width:162px">Interface</th><th>Type</th></tr>'
         + ROWS.replace("<tr>", '<tr style="background:#dff3c8">')
         + ROWS.replace("44:01", "44:02").replace("Gi0/1", "Gi0/2").replace("<tr>", '<tr style="background:#d6f0fa">') + '</table>'
         + box(728, 632, 174, 66, "vap-tag", "Изучение<br>источника", "background:#1d7a3a")
         + box(728, 708, 174, 66, "vap-tag", "Поиск<br>получателя", "background:#1aa0a6") + '</div>')


def row(y, n, html, h=46):
    return box(948, y - 2, 56, 56, "vap-n", str(n)) + box(1015, y, 622, h, "vap-row", html)


ORDER = ('<div class="step">' + box(930, 478, 720, 345, "vap-pan")
         + box(934, 482, 712, 42, "vap-hd", "Порядок передачи кадра", "line-height:42px")
         + row(536, 1, "<b>Вход Gi0/1:</b> принимается нетегированный кадр")
         + row(590, 2, "SW1 относит кадр к <b>VLAN 10</b> и изучает<br>MAC источника на Gi0/1", 62)
         + row(664, 3, "По паре <b>VID 10 + MAC ПК2</b> найден порт Gi0/2")
         + row(720, 4, "<b>Выход Gi0/2:</b> ПК2 получает кадр без тега")
         + box(950, 776, 690, 46, "vap-t", "<b style='color:#1f7a5a'>VID</b> — идентификатор VLAN<br><b style='color:#1f7a5a'>Dynamic</b> — запись изучена автоматически по MAC источника",
               "font-size:18px;line-height:1.2") + '</div>')

HTML = CSS + bg("bgk_ground") + LINE + "".join([
    box(553, 102, 565, 46, "vap-lil", "Передача кадра от ПК1 к ПК2", "line-height:38px;font-size:25px"),
    '<div class="step">' + img("v_access_pc_pc1.png", "left:113px;top:188px;width:164px")
    + box(50, 346, 304, 78, "vap-pan", "<div class='vap-big'>ПК1</div><div class='vap-t' style='text-align:center;margin-top:6px'>MAC: 00:11:22:33:44:01</div>", "padding-top:8px")
    + img("v_access_pc_pc2.png", "left:1398px;top:188px;width:164px")
    + box(1320, 346, 304, 78, "vap-pan", "<div class='vap-big'>ПК2</div><div class='vap-t' style='text-align:center;margin-top:6px'>MAC: 00:11:22:33:44:02</div>", "padding-top:8px")
    + '</div>',
    '<div class="step">' + img("v_access_pc_sw.png", "left:666px;top:222px;width:336px")
    + box(755, 180, 162, 62, "vap", "SW1", "background:#2a8a4a;border:4px solid #0a3a1a;color:#fff;font:700 40px/54px 'Pixelify Sans',monospace;text-align:center;box-shadow:4px 4px 0 #000")
    + box(496, 290, 180, 62, "vap-lil", "Gi0/1<br><span style='font-size:19px'>access VLAN 10</span>", "padding-top:4px")
    + box(996, 290, 180, 62, "vap-lil", "Gi0/2<br><span style='font-size:19px'>access VLAN 10</span>", "padding-top:4px")
    + box(690, 318, 292, 66, "vap-pan", "Принадлежность кадра:<br><span style='font:700 28px \"Pixelify Sans\"'>VLAN 10</span>",
          "background:#fff3b0;font:700 20px/1.25 'Golos Text',sans-serif;text-align:center;padding-top:2px")
    + box(622, 388, 428, 74, "vap-pan", "<b style='color:#1a5a8a'>Источник:</b>&nbsp;&nbsp; 00:11:22:33:44:01<br><b style='color:#1a5a8a'>Назначение:</b> 00:11:22:33:44:02",
          "background:#e6f4ff;font:600 22px/1.35 'Golos Text',sans-serif;text-align:center;padding-top:4px") + '</div>',
    '<div class="step">' + box(414, 192, 198, 40, "vap-bub", "Кадр без тега") + box(1060, 192, 198, 40, "vap-bub", "Кадр без тега")
    + '<div class="vap-mv" style="position:absolute;left:0;top:0">' + env(372, 236, 74) + env(1225, 236, 74) + '</div></div>',
    TABLE, ORDER,
    '<div class="step">' + box(300, 845, 1080, 82, "vap-foot", "На обоих кабелях кадр нетегированный;<br>внутри SW1 учитывается VLAN 10") + '</div>',
])
