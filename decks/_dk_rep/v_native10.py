# -*- coding: utf-8 -*-
"""VLAN: Native VLAN 10 на обоих концах trunk — путь кадра без тега, формат, таблицы MAC — вёрстка на пиксельном фоне."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 130

CSS = """<style>
.vn10{position:absolute;box-sizing:border-box}
.vn10-pan{background:#fdf7e6;border:4px solid #1a2a5a;box-shadow:4px 4px 0 #000;border-radius:12px}
.vn10-lb{background:#e6f2ff;border:2px solid #4a6a9a;border-radius:6px;font:600 20px/1.25 "Golos Text",sans-serif;text-align:center;padding-top:4px;color:#111}
.vn10-sw{background:#d9c6fb;border:3px solid #7a3fc8;border-radius:6px;font:700 26px/40px "Pixelify Sans",monospace;text-align:center;color:#1a1a3a}
.vn10-nt{background:#fff;border:2px solid #1a2a5a;border-radius:6px;font:600 18px/28px "Golos Text",sans-serif;text-align:center}
.vn10-pt{font:600 19px/1.1 "Golos Text",sans-serif;text-align:center;color:#111}
.vn10-n{width:62px;height:62px;border-radius:50%;border:4px solid #1a2a5a;color:#fff;font:900 34px/54px "Golos Text",sans-serif;text-align:center}
.vn10-h{font:700 22px/44px "Golos Text",sans-serif;text-align:center;border-radius:6px}
.vn10-t{font:600 20px/1.3 "Golos Text",sans-serif;color:#111}
.vn10-f{display:flex;position:absolute}
.vn10-f div{border:2px solid #2a3a6a;font:500 20px/1.1 "Golos Text",sans-serif;text-align:center;display:flex;align-items:center;justify-content:center;height:64px}
.vn10-tb{position:absolute;border-collapse:collapse;font:500 18px/28px "Golos Text",sans-serif;text-align:center;color:#111;border:2px solid #4a3a8a}
.vn10-tb th{font-weight:600;background:#d6ecfb}
.vn10-tb td,.vn10-tb th{border-bottom:1px solid #aab}
.vn10-tb caption{background:#d9c6fb;font:700 20px/32px "Golos Text",sans-serif;border:2px solid #4a3a8a;border-bottom:none}
.vn10-foot{background:#1d7a2a;border:4px solid #0d4a1a;box-shadow:4px 4px 0 #000;color:#fff;border-radius:8px;
  font:700 26px/60px "Golos Text",sans-serif;padding-left:80px}
.vn10-go{animation:vn10g 3s ease-in-out infinite}
@keyframes vn10g{50%{transform:translateX(16px)}}
</style>"""


def box(x, y, w, h, cls, inner="", st=""):
    return '<div class="vn10 %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s">%s</div>' % (cls, x, y, w, h, st, inner)


def env(x, y, w):
    return ('<svg class="vn10" style="left:%dpx;top:%dpx" width="%d" height="%d" viewBox="0 0 70 49">'
            '<rect x="2" y="2" width="66" height="45" fill="#fff" stroke="#222" stroke-width="3"/>'
            '<path d="M2 2 L35 28 L68 2" fill="none" stroke="#222" stroke-width="3"/></svg>' % (x, y, w, int(w * .7)))


WIRE = ('<svg class="vn10" style="left:0;top:0" width="1672" height="941"><g stroke-width="5">'
        '<line x1="240" y1="315" x2="500" y2="315" stroke="#2a9a3a"/><line x1="680" y1="315" x2="990" y2="315" stroke="#f0b020"/>'
        '<line x1="1172" y1="315" x2="1440" y2="315" stroke="#2a9a3a"/></g></svg>')


def stage(x, w, n, col, bandc, head, text):
    return ('<div class="step">' + box(x, 418, w, 136, "vn10-pan")
            + box(x + 60, 428, w - 80, 44, "vn10-h", head, "background:%s" % bandc)
            + box(x + 14, 422, 62, 62, "vn10-n", str(n), "background:%s" % col)
            + box(x + 80, 484, w - 90, 64, "vn10-t", text) + '</div>')


ROW = '<tr><td>10</td><td>00:11:22:33:44:0%s</td><td>%s</td><td>Dynamic</td></tr>'


def table(x, name, p1, p2):
    return ('<table class="vn10-tb" style="left:%dpx;top:706px;width:%dpx;background:#fff"><caption>Таблица MAC-адресов %s</caption>'
            '<tr><th style="width:84px">VID</th><th style="width:200px">MAC-address</th><th style="width:140px">Interface</th><th>Type</th></tr>'
            % (x, 615 if x < 500 else 560, name) + ROW % ("1", p1) + ROW % ("2", p2) + '</table>')


HTML = CSS + bg("bgk_sky") + "".join([
    box(264, 134, 1144, 48, "vn10-pan", "Native VLAN 10 на обоих концах trunk. Тегирование native VLAN отключено.",
        "background:#fbefc6;font:700 24px/40px 'Golos Text',sans-serif;text-align:center;color:#1a3a8a"),
    box(55, 185, 1570, 226, "vn10-pan"),
    '<div class="step">' + WIRE
    + box(94, 194, 268, 62, "vn10-lb", "ПК1 — VLAN 10<br>MAC: 00:11:22:33:44:01") + img("v_native10_pc1.png", "left:148px;top:266px;width:106px")
    + box(1366, 194, 244, 62, "vn10-lb", "ПК2 — VLAN 10<br>MAC: 00:11:22:33:44:02") + img("v_native10_pc2.png", "left:1428px;top:266px;width:106px")
    + '</div>',
    '<div class="step">' + box(518, 216, 136, 42, "vn10-sw", "SW1") + box(1023, 216, 136, 42, "vn10-sw", "SW2")
    + img("v_native10_sw1.png", "left:493px;top:273px;width:194px") + img("v_native10_sw2.png", "left:983px;top:273px;width:197px")
    + box(410, 342, 162, 46, "vn10-pt", "Gi0/1<br>access VLAN 10") + box(620, 342, 150, 66, "vn10-pt", "Gi0/24<br>trunk<br>native VLAN 10")
    + box(900, 342, 150, 66, "vn10-pt", "Gi0/24<br>trunk<br>native VLAN 10") + box(1100, 342, 152, 46, "vn10-pt", "Gi0/2<br>access VLAN 10") + '</div>',
    '<div class="step">' + box(340, 260, 114, 30, "vn10-nt", "Без тега") + box(775, 259, 116, 30, "vn10-nt", "Без тега")
    + box(1220, 260, 110, 30, "vn10-nt", "Без тега")
    + '<div class="vn10-go" style="position:absolute;left:0;top:0">' + env(362, 296, 56) + env(805, 296, 56) + env(1250, 296, 56) + '</div></div>',
    stage(58, 395, 1, "#1aa6a6", "#3ac6c6;color:#fff", "Вход access SW1", "Кадр относится к VLAN 10<br>по настройке Gi0/1."),
    stage(460, 375, 2, "#8a4ad8", "#a878e8;color:#fff", "Выход trunk SW1", "VLAN 10 является native —<br>тег не добавляется."),
    stage(843, 390, 3, "#d8a010", "#ffd23a", "Вход trunk SW2", "Кадр без тега относится<br>к native VLAN 10."),
    stage(1240, 380, 4, "#1aa6a6", "#3ac6c6;color:#fff", "Выход access SW2", "Кадр передаётся через<br>Gi0/2 без тега."),
    '<div class="step">' + box(78, 566, 1515, 92, "vn10-pan")
    + box(95, 575, 238, 74, "vn10", "Формат кадра<br>на всех кабелях:", "background:#132a5a;color:#fff;border-radius:8px;font:700 22px/1.2 'Golos Text',sans-serif;text-align:center;padding-top:10px")
    + '<div class="vn10-f" style="left:363px;top:578px">'
    + "".join('<div style="width:%dpx;background:%s">%s</div>' % w for w in [
        (184, "#cfe6fb", "MAC ПК2<br>(назначение)"), (174, "#8adcd2", "MAC ПК1<br>(источник)"), (146, "#d9c6fb", "EtherType"),
        (218, "#ffd23a", "Данные"), (138, "#cfe6fb", "FCS")]) + '</div>'
    + '<div class="vn10" style="left:1254px;top:585px;width:3px;height:52px;background:#2a3a6a"></div>'
    + box(1280, 586, 300, 56, "vn10-t", "MAC-адреса источника<br>и назначения сохраняются.", "font-size:20px") + '</div>',
    '<div class="step">' + box(112, 670, 1462, 175, "vn10-pan")
    + box(145, 675, 700, 28, "vn10-t", "После обмена в обе стороны: MAC ПК2 уже известен", "font-size:20px;font-weight:700")
    + table(138, "SW1", "Gi0/1", "Gi0/24") + table(772, "SW2", "Gi0/24", "Gi0/2")
    + box(1342, 706, 218, 120, "vn10", "<b style='display:inline-block;width:36px;height:36px;border-radius:50%;background:#e8a010;color:#fff;text-align:center;line-height:36px;float:left;margin:4px 8px 30px 0'>i</b>MAC источника изучается на входящем порту.",
          "background:#fbefc6;border:3px solid #e8b020;border-radius:12px;font:700 16px/1.35 'Golos Text',sans-serif;padding:10px 8px 0 12px")
    + '</div>',
    '<div class="step">' + box(202, 855, 905, 64, "vn10-foot", "★&nbsp; В этом примере тег 802.1Q не появляется ни на одном кабеле.".replace("★&nbsp; ", ""))
    + '<div class="vn10" style="left:218px;top:860px;color:#ffd23a;font:900 46px/56px sans-serif">★</div>'
    + box(1117, 855, 420, 64, "vn10", "На том же trunk разрешённая VLAN 20<br>передавалась бы с тегом VID 20.",
          "background:#e6f2ff;border:3px solid #1a2a5a;border-radius:10px;font:600 16px/1.3 'Golos Text',sans-serif;padding:8px 0 0 72px;white-space:nowrap")
    + img("v_native10_mush.png", "left:1133px;top:860px;width:54px") + '</div>',
])
