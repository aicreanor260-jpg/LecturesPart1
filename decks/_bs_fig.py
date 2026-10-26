# -*- coding: utf-8 -*-
"""Рисунки pptx «2.2 Базовые настройки» в стиле деки: схемы подключения, окна Tera Term и Web-интерфейса."""
import os

import _sw_svg as S
import _dk_replib


def T(x, y, s, size=14, col="#fff", w=700, anchor="middle", mono=False):
    """Текст SVG: цвет через style, иначе общий CSS svg.fig text перекрашивает всё в белый."""
    return S.txt(x, y, s, size, col, w, anchor, mono, ' style="fill:%s"' % col)
from _sw_lib import _esc

CR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_dk_rep", "crops")
PINK, CYAN, INK = "#ff2e93", "#3fe6ff", "#2a0a2a"


def im(name, x, y, w, h):
    return ('<image href="%s" x="%g" y="%g" width="%g" height="%g" preserveAspectRatio="xMidYMid meet"/>'
            % (_dk_replib._webp(os.path.join(CR, name + ".png")), x, y, w, h))


def img(name, style=""):
    return '<img class="bsimg" src="%s" style="%s" alt="">' % (_dk_replib._webp(os.path.join(CR, name + ".png")), style)


def lap(cx, top, label, w=150):
    return im("dev_base_pc", cx - w / 2, top, w, w * 153 / 150.0) + T(cx, top + w + 22, label, 15, "#fff", 800)


def swi(cx, cy, w=330):
    h = w * 162 / 1068.0
    return im("dev_base_sw", cx - w / 2, cy - h / 2, w, h)


def wire(x1, y1, x2, y2, col=CYAN, w=5):
    return '<path class="lnk" d="M%g %gL%g %g" stroke="%s" stroke-width="%g" stroke-linecap="round"/>' % (x1, y1, x2, y2, col, w)


def tagbox(x, y, lines, col=PINK, anchor="start"):
    w = max(len(l) for l in lines) * 9.2 + 24
    x0 = x if anchor == "start" else x - w
    o = ['<g><rect x="%g" y="%g" width="%g" height="%g" rx="5" fill="#fff" stroke="%s" stroke-width="3"/>'
         % (x0, y, w, 12 + len(lines) * 22, INK)]
    for i, l in enumerate(lines):
        o.append(T(x0 + 12, y + 27 + i * 22, l, 15, col if i == 0 else INK, 800, "start"))
    o.append("</g>")
    return "".join(o)


def dot(x, y, col="#ff2e93"):
    return '<circle cx="%g" cy="%g" r="10" fill="%s" stroke="#fff" stroke-width="3"/>' % (x, y, col)


# ------------------------------------------------ подключение по SSH (рисунок 2.6.1.2.1)
def ssh_topo():
    o = [wire(190, 210, 330, 330), wire(470, 330, 610, 330), wire(700, 330, 880, 330, "#ff7a3d", 9),
         '<path d="M200 250 L350 360 Q 520 450 700 390 L 880 360" stroke="%s" stroke-width="5" fill="none" '
         'stroke-dasharray="14 9" marker-end="url(#ah)" class="flow"/>' % CYAN]
    o.append(lap(150, 60, "Admin", 130))
    o.append('<ellipse cx="400" cy="330" rx="80" ry="46" fill="#fff" stroke="%s" stroke-width="3"/>' % INK)
    o.append(T(400, 336, "Internet", 17, INK, 800))
    o.append('<circle cx="660" cy="330" r="44" fill="#2f6fe0" stroke="#fff" stroke-width="4"/>')
    o.append(T(660, 337, "R1", 20, "#fff", 900))
    o.append(swi(990, 330, 280))
    o.append(T(990, 400, "SW-1", 18, "#fff", 900))
    o.append(dot(880, 330))
    o.append(dot(704, 330))
    o.append(wire(990, 290, 990, 175, PINK, 4))
    o.append(dot(990, 175))
    o.append(tagbox(700, 360, ["Gi1/0/1.20", "IP add: 10.10.1.1"]))
    o.append(tagbox(830, 230, ["Gi1/0/24"], CYAN))
    o.append(tagbox(1190, 120, ["VLAN20", "IP add: 10.10.1.28 /24", "DefGW: 10.10.1.1"], PINK, "end"))
    return S.fig("".join(o), "0 0 1200 520")


# ------------------------------------------------ первое подключение к Web (рисунок 2.6.1.3.1)
def web_first():
    o = [wire(260, 300, 860, 300)]
    o.append(lap(170, 150, "Admin", 170))
    o.append(tagbox(250, 360, ["IP add: 192.168.1.2/24"], INK))
    o.append(dot(860, 300))
    o.append(tagbox(700, 230, ["Gi1/0/1"], CYAN))
    o.append(swi(1000, 300, 300))
    o.append(T(1000, 372, "SW-1", 18, "#fff", 900))
    o.append(wire(1000, 260, 1000, 160, PINK, 4))
    o.append(dot(1000, 160))
    o.append(tagbox(1190, 80, ["VLAN 1", "IP add: 192.169.1.239 /24"], PINK, "end"))
    return S.fig("".join(o), "0 0 1200 460")


# ------------------------------------------------ Web в функционирующей сети (рисунок 2.6.1.3.4)
def web_work():
    o = [wire(260, 300, 860, 300)]
    o.append(lap(170, 150, "Admin", 170))
    o.append(tagbox(250, 360, ["IP add: 10.10.1.121/24"], INK))
    o.append(dot(860, 300))
    o.append(tagbox(720, 230, ["Gi1/0/2"], CYAN))
    o.append(swi(1000, 300, 300))
    o.append(T(1000, 372, "SW-1", 18, "#fff", 900))
    o.append(wire(1000, 260, 1000, 160, PINK, 4))
    o.append(dot(1000, 160))
    o.append(tagbox(1190, 60, ["VLAN20", "IP add: 10.10.1.28 /24", "DefGW: 10.10.1.1"], PINK, "end"))
    return S.fig("".join(o), "0 0 1200 460")


# ------------------------------------------------ окна
def form_teraterm(d):
    rows = "".join('<div class="fm-r"><span>%s</span><b>%s</b></div>' % (_esc(a), _esc(b)) for a, b in d["fields"])
    btn = "".join('<button>%s</button>' % _esc(b) for b in d["buttons"])
    info = "".join("<div>%s</div>" % _esc(i) for i in d.get("info", []))
    return ('<div class="win"><div class="win-t">%s</div><div class="win-b"><div class="fm">%s</div>'
            '<div class="fm-btn">%s</div></div><div class="win-i">%s</div></div>' % (_esc(d["title"]), rows, btn, info))


def form_auth(d):
    rows = "".join('<label>%s<input value="%s" readonly></label>' % (_esc(a), _esc(b)) for a, b in d["fields"])
    return ('<div class="win auth"><div class="auth-l">ELTEX</div><div class="auth-r"><div class="win-t">%s</div>%s'
            '<div class="fm-btn"><button class="pri">%s</button></div></div></div>' % (_esc(d["title"]), rows, _esc(d["buttons"][0])))


def web_ui(d):
    h = d["header"]
    tree = "".join('<div class="wt l%d%s">%s %s</div>' % (lv, " sel" if t == d["selected"] else "", _esc(sg), _esc(t))
                   for sg, t, lv in d["tree"])
    fields = "".join('<div class="fm-r"><span>%s</span><b>%s</b></div>' % (_esc(a), _esc(b) or "&nbsp;") for a, b in d["fields"])
    return ('<div class="win webui"><div class="wu-h"><b>%s</b><div><div class="wu-ti">%s</div><div>%s</div></div>'
            '<span class="wu-r">%s</span></div><div class="wu-b"><div class="wu-tree"><div class="win-t">%s</div>%s</div>'
            '<div class="wu-p"><div class="win-t">%s</div><div class="fm">%s</div><div class="fm-btn"><button>%s</button></div>'
            '</div></div></div>' % (_esc(h["logo"]), _esc(h["title"]), _esc(h["subtitle"]),
                                     _esc(h["right"]).replace("Save", '<em class="save">Save</em>'),
                                     _esc(d["tree_title"]), tree, _esc(d["panel_title"]), fields, _esc(d["buttons"][0])))


CSS = r"""
.bsimg{display:block;max-width:100%;max-height:30vh;margin:0 auto;border:3px solid #2a0a2a;border-radius:6px;box-shadow:6px 6px 0 #ff2e93}
.bsrow{display:flex;gap:14px;align-items:center;justify-content:center;flex-wrap:wrap}
.bsrow .bsimg{max-height:22vh;max-width:46%}
.win{background:#fff;color:#2a0a2a;border:3px solid #2a0a2a;border-radius:6px;box-shadow:7px 7px 0 #ff2e93;overflow:hidden;
 font:600 clamp(11px,.8vw,15px)/1.35 var(--f)}
.win-t{background:#ff2e93;color:#fff;font:800 clamp(12px,.86vw,16px)/1.2 var(--f);padding:7px 12px}
.win-b{padding:10px 14px;display:flex;gap:16px}
.fm{flex:1;display:flex;flex-direction:column;gap:5px;padding:4px 0}
.fm-r{display:flex;gap:10px;border-bottom:1px dashed #e7b5cf;padding:3px 0}
.fm-r span{flex:0 0 46%;color:#7a4a66}.fm-r b{font-family:var(--m)}
.fm-btn{display:flex;flex-direction:column;gap:6px;justify-content:flex-start}
.fm-btn button{font:700 12px/1 var(--f);padding:7px 12px;border:2px solid #2a0a2a;background:#ffe3f1;border-radius:4px}
.fm-btn button.pri{background:#ff2e93;color:#fff}
.win-i{padding:8px 14px;background:#fff2f8;font:500 clamp(10px,.7vw,13px)/1.35 var(--m);color:#5a2a46}
.auth{display:flex;max-width:520px;margin:0 auto}
.auth-l{flex:0 0 120px;background:#2a2a36;color:#7fd8ff;font:900 18px/1 var(--f);display:grid;place-items:center;letter-spacing:.1em}
.auth-r{flex:1;display:flex;flex-direction:column;gap:6px;padding-bottom:10px}
.auth-r label{display:flex;flex-direction:column;padding:0 14px;color:#7a4a66}
.auth-r input{font:600 14px/1 var(--m);padding:6px 8px;border:2px solid #2a0a2a;border-radius:3px;color:#2a0a2a}
.auth-r .fm-btn{padding:0 14px;align-items:flex-end}
.webui .wu-h{display:flex;align-items:center;gap:16px;padding:8px 12px;background:#2a0a2a;color:#fff}
.webui .wu-h>b{font:900 20px/1 var(--f);color:#7fd8ff}
.wu-ti{font:800 15px/1.2 var(--f)}.wu-r{margin-left:auto;font-size:12px}
.wu-r .save{font-style:normal;background:#ff2e93;padding:3px 8px;border-radius:3px;animation:pls 1.4s ease-in-out infinite}
.wu-b{display:flex}.wu-tree{flex:0 0 34%;border-right:2px solid #2a0a2a;padding-bottom:8px}
.wt{padding:2px 10px;font-size:12.5px}.wt.l1{padding-left:26px}.wt.l2{padding-left:44px}
.wt.sel{background:#ffe3f1;color:#ff2e93;font-weight:800}
.wu-p{flex:1;padding-bottom:8px}.wu-p .fm{padding:6px 12px}.wu-p .fm-btn{padding:0 12px;align-items:flex-end}
"""
