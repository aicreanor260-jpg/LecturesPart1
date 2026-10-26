# -*- coding: utf-8 -*-
"""VLAN: типы VLAN — три признака классификации (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 118

CSS = """<style>
.vty-b{position:absolute;box-sizing:border-box;border:5px solid #2a1a0a;box-shadow:5px 5px 0 #000;background:#fff8ea}
.vty-sub{background:#fff1dc;font:800 28px/52px "Golos Text",sans-serif;color:#1a0a04;text-align:center;border-color:#5a2a0a}
.vty-hd{position:absolute;box-sizing:border-box;color:#fff;font:800 29px/1.0 "Golos Text",sans-serif;text-align:center;padding-top:14px;
  text-shadow:2px 2px 0 #1a0a04}
.vty-it{position:absolute;box-sizing:border-box;border:2px solid #e0d6c0;border-radius:8px}
.vty-n{position:absolute;font:800 26px/1 "Golos Text",sans-serif;color:#13245a}
.vty-d{position:absolute;white-space:nowrap;font:500 17px/1.25 "Golos Text",sans-serif;color:#1a1a2a}
.vty-grn{background:#3fae3a;border-color:#1c4a14;color:#fff;font:800 28px/50px "Golos Text",sans-serif;text-align:center}
.vty-note{font:500 19px/50px "Golos Text",sans-serif;color:#1a0a04;padding-left:120px}
.vty-coin{position:absolute;width:30px;height:30px;border-radius:50%;background:#ffb81c;border:3px solid #8a4a00;box-sizing:border-box;
  animation:vtyc 1.6s ease-in-out infinite}
@keyframes vtyc{50%{transform:translateY(-6px)}}
</style>"""


def b(x, y, w, h, cls="", inner="", st=""):
    return '<div class="vty-b %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s">%s</div>' % (cls, x, y, w, h, st, inner)


def item(x, y, w, h, bgc, icon, iw, name, desc):
    return ('<div class="vty-it" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s"></div>' % (x, y, w, h, bgc)
            + img(icon, "left:%dpx;top:%dpx;width:%dpx" % (x + 4, y + 2, iw))
            + '<div class="vty-n" style="left:%dpx;top:%dpx">%s</div>' % (x + 140 if iw > 115 else x + 124, y + 18, name)
            + '<div class="vty-d" style="left:%dpx;top:%dpx;width:%dpx">%s</div>' % (x + 142 if iw > 115 else x + 126, y + 52, w - 145, desc))


def column(x, w, col, title, items):
    return ('<div class="step">' + b(x, 210, w, 576, "", "", "border-color:%s" % col)
            + '<div class="vty-hd" style="left:%dpx;top:210px;width:%dpx;height:90px;background:%s">%s</div>' % (x, w, col, title)
            + "".join(item(*it) for it in items) + '</div>')


COL1 = [(234, 314, 386, 120, "#eef7e4", "v_types_st.png", 124, "Статические", "Создаются<br>администратором вручную"),
        (234, 454, 386, 136, "#eef7e4", "v_types_dy.png", 124, "Динамические", "Регистрация и<br>распространение VLAN<br>протоколами GVRP/MVRP, VTP"),
        (234, 614, 386, 146, "#eef7e4", "v_types_df.png", 124, "По умолчанию", "Обычно VLAN 1; исходная<br>принадлежность портов<br>зависит от устройства")]
COL2 = [(664, 314, 352, 102, "#f4ecff", "v_types_port.png", 111, "Port-based", "По настройке входного<br>порта, например PVID 15"),
        (664, 430, 352, 94, "#f4ecff", "v_types_mac.png", 111, "MAC-based", "По MAC-адресу источника"),
        (664, 540, 352, 100, "#f4ecff", "v_types_proto.png", 111, "Protocol-based", "По протоколу кадра,<br>например IPv4 или IPv6"),
        (664, 656, 352, 118, "#f4ecff", "v_types_pol.png", 111, "Policy-based", "По условиям политики<br>или результатам<br>аутентификации")]
COL3 = [(1060, 312, 386, 104, "#e4f8f4", "v_types_data.png", 127, "Data VLAN", "Пользовательские данные:<br>файлы, приложения"),
        (1060, 430, 386, 104, "#e4f8f4", "v_types_voice.png", 127, "Voice VLAN", "Голос; приоритет задаётся<br>настройками QoS"),
        (1060, 546, 386, 104, "#e4f8f4", "v_types_tv.png", 127, "Multicast VLAN", "Многоадресные сервисы,<br>например IPTV"),
        (1060, 662, 386, 112, "#e4f8f4", "v_types_mgmt.png", 127, "VLAN управления", "SSH, мониторинг<br>и администрирование<br>устройств")]

HTML = CSS + bg("bgk_ground") + "".join([
    '<div class="step">' + b(576, 126, 520, 56, "vty-sub", "Три признака классификации")
    + '<svg style="position:absolute;left:0;top:0;width:1672px;height:941px"><path d="M576 160H420v40" fill="none" stroke="#3fae3a" stroke-width="6"/>'
      '<path d="M836 182v18" stroke="#8a3ad8" stroke-width="6"/><path d="M1096 160h156v40" fill="none" stroke="#1ab0a8" stroke-width="6"/></svg>'
    + '<div class="vty-coin" style="left:405px;top:192px"></div><div class="vty-coin" style="left:821px;top:192px"></div>'
      '<div class="vty-coin" style="left:1237px;top:192px"></div></div>',
    column(214, 424, "#3a9a2a", "По созданию<br>и исходной настройке", COL1),
    column(646, 384, "#7a3ad0", "По назначению<br>трафика в VLAN", COL2),
    column(1040, 422, "#139a90", "По назначению<br>трафика", COL3),
    '<div class="step">' + b(186, 804, 1304, 52, "vty-grn", "Одна VLAN может одновременно относиться к нескольким категориям")
    + img("v_types_star.png", "left:258px;top:808px;width:47px") + img("v_types_star.png", "left:1368px;top:808px;width:47px") + '</div>',
    '<div class="step">' + b(204, 858, 1266, 56, "vty-note",
                             "Нетегированный трафик относится к VLAN по PVID; VLAN управления обычно выделяют отдельно от VLAN 1.", "padding-left:120px")
    + img("v_types_warn.png", "left:253px;top:860px;width:54px") + '</div>',
])
