# -*- coding: utf-8 -*-
"""VLAN: структура метки IEEE 802.1Q (TPID, TCI = PCP/DEI/VLAN ID) — вёрстка на чистом фоне."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg

W, H, TOP = 1672, 941, 170

CSS = """<style>
.vts-b{position:absolute;border:4px solid #14324e;box-shadow:5px 5px 0 #000;box-sizing:border-box}
.vts-note{left:242px;top:182px;width:1186px;height:56px;background:#fdf6e3;font:500 27px/48px "Golos Text",sans-serif;text-align:center;color:#14324e}
.vts-note b{font-weight:800}
.vts-row{position:absolute;left:140px;top:258px;width:1392px;height:107px;display:flex;border:4px solid #14324e;box-shadow:5px 5px 0 #000;box-sizing:border-box}
.vts-row div{border-right:3px solid #14324e;font:800 27px/1.1 "Golos Text",sans-serif;color:#14324e;text-align:center;display:flex;flex-direction:column;justify-content:center}
.vts-row div:last-child{border-right:0}
.vts-row small{font:500 21px/1.2 "Golos Text",sans-serif;margin-top:8px}
.vts-row .tg{background:#ffc83a;outline:5px solid #14324e;position:relative;z-index:1}
.vts-z{position:absolute;left:248px;top:405px;width:1107px;height:237px;background:#fff6c8;border:4px dashed #e0a800;border-radius:12px}
.vts-c{position:absolute;top:420px;height:212px;background:#fdf3e0;border:3px solid #c89a50;border-radius:8px;overflow:hidden}
.vts-c h4{margin:0;height:50px;background:#fbe0a8;font:800 29px/50px "Golos Text",sans-serif;text-align:center;color:#14324e}
.vts-hex{position:absolute;left:38px;top:108px;width:388px;height:54px;background:#f8e4cc;border-radius:8px;font:800 42px/54px "Golos Text",sans-serif;text-align:center;color:#111}
.vts-bits{position:absolute;left:0;top:168px;width:100%;font:500 25px/1 "Golos Text",sans-serif;text-align:center;color:#14324e;word-spacing:10px}
.vts-f{position:absolute;top:513px;height:106px;border:3px solid #14324e;font:800 28px/1.15 "Golos Text",sans-serif;text-align:center;color:#14324e;padding-top:22px;box-sizing:border-box}
.vts-f small{display:block;font:600 23px/1.2 "Golos Text",sans-serif}
.vts-d{position:absolute;top:662px;height:123px;border:3px solid;border-radius:6px;box-shadow:4px 4px 0 #000;padding:12px 26px;box-sizing:border-box;
  font:500 21px/1.4 "Golos Text",sans-serif;color:#14324e}
.vts-d b{font-weight:800;font-size:25px}
.vts-d ul{margin:2px 0 0;padding-left:26px}.vts-d li{line-height:1.3}
.vts-fcs{position:absolute;left:1388px;top:410px;width:262px;height:98px;background:#d8f8f0;border:3px solid #14324e;border-radius:8px;font:700 21px/1.2 "Golos Text",sans-serif;text-align:center;color:#14324e;padding-top:10px;box-sizing:border-box}
.vts-foot{position:absolute;left:228px;top:805px;width:1214px;height:95px;background:#a8e880;border:4px solid #14324e;box-shadow:5px 5px 0 #000;text-align:center;color:#14324e}
.vts-svg{position:absolute;left:0;top:0;width:1672px;height:941px}
.vts-up{animation:vtsu 1s ease-in-out infinite}
@keyframes vtsu{50%{transform:translateY(-8px)}}
.vts-tgp{animation:vtsp 1.4s steps(2) infinite}
@keyframes vtsp{50%{filter:brightness(1.12)}}
</style>"""

L = "#dcd8f8"
CELLS = [(242, L, "Destination<br>MAC<small>6 байт</small>", ""), (222, L, "Source<br>MAC<small>6 байт</small>", ""),
         (234, "#ffc83a", "Тег 802.1Q<small>4 байта</small>", "tg vts-tgp"), (230, L, "EtherType<small>2 байта</small>", ""),
         (277, "#f8c8d8", "Данные<small>46–1500 байт</small>", ""), (187, "#a8f0e0", "FCS<small>4 байта</small>", "")]

HTML = CSS + bg("bgk_ground") + "".join([
    '<div class="step"><div class="vts-b vts-note"><b>Тег 802.1Q — 32 бита (4 байта)</b>, добавляемые между Source MAC и EtherType.</div></div>',
    '<div class="step"><div class="vts-row">'
    + "".join('<div class="%s" style="width:%dpx;background:%s">%s</div>' % (k, w, c, t) for w, c, t, k in CELLS) + '</div></div>',
    '<div class="step"><svg class="vts-svg" viewBox="0 0 1672 941"><path d="M604 372 L252 408 M838 372 L1352 408 M721 372 L721 420" '
    'stroke="#3a1606" stroke-width="3" stroke-dasharray="6 5" fill="none"/>'
    '</svg>'
    '<div class="vts-z"></div>'
    '<div class="vts-c" style="left:260px;width:460px"><h4>TPID — 16 бит</h4>'
    '<div style="position:absolute;left:0;top:54px;width:100%;font:500 22px/1.1 Golos Text,sans-serif;text-align:center;color:#14324e">Идентификатор протокола<br>тегирования</div>'
    '<div class="vts-hex">0x8100</div><div class="vts-bits">1000 0001 0000 0000</div></div>'
    '<div class="vts-c" style="left:735px;width:610px"><h4>TCI — 16 бит</h4></div>'
    '<svg class="vts-svg" viewBox="0 0 1672 941"><path d="M780 505 L780 490 Q780 480 790 480 L1030 480 Q1040 480 1040 470 Q1040 480 1050 480 L1290 480 Q1300 480 1300 490 L1300 505" stroke="#14324e" stroke-width="4" fill="none"/></svg>'
    '<div class="vts-f" style="left:750px;width:205px;background:#d8c8f8;border-radius:8px 0 0 8px">PCP (PRI)<small>— 3 бита</small></div>'
    '<div class="vts-f" style="left:952px;width:172px;background:#f8a8a8">DEI<small>— 1 бит</small></div>'
    '<div class="vts-f" style="left:1121px;width:207px;background:#98f0e0;border-radius:0 8px 8px 0">VLAN ID<small>— 12 бит</small></div></div>',
    '<div class="step"><div class="vts-up"><svg class="vts-svg" viewBox="0 0 1672 941"><path d="M1457 408 L1457 372" stroke="#14324e" stroke-width="5"/>'
    '<path d="M1445 378 L1457 360 L1469 378z" fill="#14324e"/></svg></div>'
    '<div class="vts-fcs">После добавления<br>тега FCS<br>пересчитывается.</div></div>',
    '<div class="step"><div class="vts-d" style="left:198px;width:410px;background:#ead8fb;border-color:#7a4ae0"><b>PCP:</b> <b style="font-weight:700">приоритет трафика</b><br>0–7,<br>Class of Service (802.1p).</div></div>',
    '<div class="step"><div class="vts-d" style="left:625px;width:423px;background:#fbe0dc;border-color:#d83030"><b>DEI:</b> <span style="font-weight:700;font-size:23px">признак допустимости отбрасывания при перегрузке.</span><br><span style="font-size:19px">Историческое название поля — <b style="font-size:21px">CFI</b>.</span></div></div>',
    '<div class="step"><div class="vts-d" style="left:1065px;width:413px;background:#d8f8f0;border-color:#1aa890;padding-top:8px;font-size:19px">'
    '<b style="font-size:23px">VLAN ID:</b> <span style="font-weight:700;font-size:22px">идентификатор VLAN.</span>'
    '<ul><li>Рабочие значения <b style="font-size:19px">1–4094</b>.</li><li><b style="font-size:19px">0</b> — без указания VLAN;</li>'
    '<li><b style="font-size:19px">4095</b> — зарезервировано.</li></ul></div></div>',
    '<div class="step"><div class="vts-foot"><div style="font:800 31px/1 Golos Text,sans-serif;margin-top:16px;white-space:nowrap">'
    '<span style="font-size:37px">VLAN</span> — логически выделенный широковещательный домен уровня L2.</div>'
    '<div style="font:600 24px/1 Golos Text,sans-serif;margin-top:12px">Тег 802.1Q обозначает VLAN при передаче кадров с меткой.</div></div></div>',
])
