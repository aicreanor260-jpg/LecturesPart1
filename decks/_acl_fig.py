# -*- coding: utf-8 -*-
"""Схемы деки «Списки контроля доступа (ACL)» в стиле ретро-окон инфографик автора.
Всё — по рисункам pptx: те же адреса, порты, правила и подписи."""
from _sw_lib import _esc

INK = "#1d1d1b"
PAPER = "#faf3e0"
TEAL = "#1f4a44"
BLUE = "#2a4f6d"
RED = "#a8473b"
GREEN = "#2f7a3a"
GOLD = "#b8933a"
YEL = "#fff1a8"


def t(x, y, s, size=18, col=INK, w=700, anchor="middle", mono=False, extra=""):
    fam = "JetBrains Mono,monospace" if mono else "Golos Text,sans-serif"
    return ('<text x="%g" y="%g" text-anchor="%s" style="fill:%s;font:%d %dpx %s"%s>%s</text>'
            % (x, y, anchor, col, w, size, fam, extra, _esc(s)))


def lines(x, y, rows, size=17, col=INK, w=700, lh=None, mono=False):
    lh = lh or size * 1.22
    y0 = y - (len(rows) - 1) * lh / 2.0 + size * .35
    return "".join(t(x, y0 + i * lh, r, size, col, w, mono=mono) for i, r in enumerate(rows))


def fig(body, vb, cls="fig aclfig"):
    defs = ('<defs><marker id="aa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            '<path d="M0 0L10 5L0 10z" style="fill:%s"/></marker>'
            '<marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            '<path d="M0 0L10 5L0 10z" style="fill:%s"/></marker>'
            '<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            '<path d="M0 0L10 5L0 10z" style="fill:%s"/></marker></defs>' % (INK, GREEN, RED))
    return '<svg class="%s" viewBox="%s" preserveAspectRatio="xMidYMid meet">%s%s</svg>' % (cls, vb, defs, body)


def panel(html):
    return '<div class="figwrap aclpanel">%s</div>' % html


def path(d, col=INK, w=3, mk="aa", extra="", dash=False):
    da = ' stroke-dasharray="10 7"' if dash else ""
    m = ' marker-end="url(#%s)"' % mk if mk else ""
    return '<path d="%s" style="fill:none;stroke:%s;stroke-width:%g"%s%s%s/>' % (d, col, w, da, m, extra)


def rect(x, y, w, h, fill=PAPER, stroke=INK, sw=3, extra=""):
    return ('<rect x="%g" y="%g" width="%g" height="%g" style="fill:%s;stroke:%s;stroke-width:%g"%s/>'
            % (x, y, w, h, fill, stroke, sw, extra))


# ---------------------------------------------------------------- иконки (как в инфографиках)
def router(x, y, label="", r=34, col=BLUE):
    g = ['<g>', '<ellipse cx="%g" cy="%g" rx="%g" ry="%g" style="fill:%s;stroke:%s;stroke-width:3"/>' % (x, y + 10, r, r * .42, "#1c3a52", INK),
         '<rect x="%g" y="%g" width="%g" height="12" style="fill:%s;stroke:none"/>' % (x - r, y - 2, 2 * r, col),
         '<ellipse cx="%g" cy="%g" rx="%g" ry="%g" style="fill:%s;stroke:%s;stroke-width:3"/>' % (x, y - 2, r, r * .42, "#4f86b8", INK)]
    for dx, dy in ((-1, -1), (1, 1), (1, -1), (-1, 1)):
        g.append('<path d="M%g %g L%g %g" style="stroke:#fff;stroke-width:3.4;stroke-linecap:round"/>'
                 % (x + dx * 6, y - 2 + dy * 3, x + dx * 18, y - 2 + dy * 8))
    g.append('</g>')
    if label:
        g.append(t(x, y + r * .42 + 34, label, 18, INK, 800))
    return "".join(g)


def pc(x, y):
    return ('<g><rect x="%g" y="%g" width="46" height="34" style="fill:#cfe3f3;stroke:%s;stroke-width:3"/>'
            '<rect x="%g" y="%g" width="34" height="22" style="fill:#5b9bd0;stroke:none"/>'
            '<path d="M%g %g h18 M%g %g v8" style="stroke:%s;stroke-width:3"/></g>'
            % (x - 23, y - 22, INK, x - 17, y - 16, x - 9, y + 20, x, y + 12, INK))


def server(x, y):
    g = ['<g><rect x="%g" y="%g" width="40" height="60" style="fill:#2f5a86;stroke:%s;stroke-width:3"/>' % (x - 20, y - 30, INK)]
    for k in range(3):
        g.append('<rect x="%g" y="%g" width="28" height="9" style="fill:#cfe3f3;stroke:none"/>' % (x - 14, y - 22 + k * 16))
    g.append('</g>')
    return "".join(g)


def switch(x, y):
    return ('<g><rect x="%g" y="%g" width="62" height="26" style="fill:#2f5a86;stroke:%s;stroke-width:3"/>'
            '<path d="M%g %g h40" style="stroke:#cfe3f3;stroke-width:4;stroke-dasharray:4 3"/></g>'
            % (x - 31, y - 13, INK, x - 20, y))


def cloud(x, y, w, h, label=""):
    rx, ry = w / 2.0, h / 2.0
    d = ("M%g %g c%g %g %g %g %g %g c%g %g %g %g %g %g c%g %g %g %g %g %g c%g %g %g %g %g %g z"
         % (x - rx * .7, y + ry * .55,
            -rx * .5, 0, -rx * .45, -ry * .9, 0, -ry * .9,
            0, -ry * .8, rx * .9, -ry * 1.0, rx * .95, -ry * .35,
            rx * .5, -ry * .55, rx * 1.05, ry * .1, rx * .7, ry * .75,
            rx * .1, ry * .35, -rx * .6, ry * .45, -rx * 1.65, ry * .45))
    g = '<path d="%s" style="fill:#e3edf6;stroke:%s;stroke-width:2.5"/>' % (d, "#7a95ad")
    return g + (t(x, y + 6, label, 17, INK, 800) if label else "")


# ================================================================ pptx 3: схема задачи
def topo_task():
    b = []
    b.append(cloud(170, 120, 230, 120))
    b.append(t(150, 80, "VLAN 10", 17, INK, 800))
    b.append(pc(130, 128) + switch(225, 120))
    b.append(lines(170, 220, ["Отдел исследований и", "разработок — 192.168.2.0/24"], 16, INK, 700))
    b.append(cloud(170, 360, 230, 120))
    b.append(t(150, 320, "VLAN 20", 17, INK, 800))
    b.append(pc(130, 368) + switch(225, 360))
    b.append(lines(170, 462, ["Офис руководителя —", "192.168.3.0/24"], 16, INK, 700))
    # каналы к маршрутизатору
    b.append(path("M256 120 L470 255", INK, 3, None))
    b.append(path("M256 360 L470 265", INK, 3, None))
    b.append(router(500, 258, "R"))
    b.append(server(520, 80))
    b.append(lines(690, 80, ["Сервер финансового", "отдела —", "192.168.4.4/24"], 16, INK, 700))
    b.append(path("M500 228 L515 115", INK, 3, None))
    b.append(router(840, 258, "Интернет"))
    b.append(path("M535 258 L805 258", INK, 3, None))
    # запрещённый и разрешённый трафик
    b.append(path("M300 150 C380 160 450 140 488 118", "#3a9ad9", 3.5, None, dash=False))
    b.append(t(395, 158, "✕", 30, "#d23a2c", 900))
    b.append(path("M300 335 C380 300 460 210 505 128", "#3a9ad9", 3, "aa", extra="", dash=True))
    b.append(path("M800 236 L560 236", "#3a9ad9", 3, None))
    b.append(t(680, 228, "✕", 30, "#d23a2c", 900))
    b.append(rect(830, 40, 320, 90, "#fff2c2", INK, 3))
    b.append(lines(990, 85, ["Есть инструмент для", "фильтрации IP-трафика?"], 19, INK, 800))
    # легенда
    b.append(path("M650 380 L740 380", "#3a9ad9", 3.5, None) + t(695, 388, "✕", 22, "#d23a2c", 900))
    b.append(t(760, 387, "Запрещенный трафик", 17, INK, 700, "start"))
    b.append(path("M650 420 L740 420", "#3a9ad9", 3.5, None, dash=True))
    b.append(t(760, 427, "Разрешенный трафик", 17, INK, 700, "start"))
    return fig("".join(b), "0 0 1180 500")


# ================================================================ pptx 5: поля заголовков
def header_bar(hl=()):
    """Заголовок L2 | 802.1q | L3 | L4 — цветные поля как на рисунке pptx (порядок и подписи те же)."""
    groups = [("Заголовок L2", "#cfe6c8", [("Destination MAC", 3), ("Source MAC", 3)]),
              ("802.1q", "#cfe6c8", [("CoS", 1), ("VLAN ID", 1.6)]),
              ("Заголовок L3", "#f7d9b0", [("DSCP", 1.1), ("Prot", 1.1), ("Source IP", 2.3), ("Destination IP", 2.3)]),
              ("Заголовок L4", "#ddd0ec", [("Source Port", 1.5), ("Dest Port", 1.5)])]
    out = []
    for name, col, cells in groups:
        tds = "".join('<div class="hb-f%s" style="flex:%g;background:%s">%s</div>'
                      % (" hl" if c in hl else "", w, col, c) for c, w in cells)
        tot = sum(w for _, w in cells)
        out.append('<div class="hb-g" style="flex:%g"><div class="hb-h">%s</div><div class="hb-r">%s</div></div>' % (tot, name, tds))
    return '<div class="hbar">%s</div>' % "".join(out)


# ================================================================ pptx 8: пакет на интерфейсе R1
def packet_r1(src="10.10.1.130", dst="10.10.10.248", hl_dst=True):
    b = [rect(40, 60, 230, 70, "#f9dfbd", "#d9a35e", 2.5), lines(155, 95, ["Source IP", src], 21, INK, 700),
         rect(270, 60, 230, 70, "#f9dfbd", RED if hl_dst else "#d9a35e", 5 if hl_dst else 2.5),
         lines(385, 95, ["Destination IP", dst], 21, INK, 700),
         path("M10 95 L40 95", INK, 2.5, None), path("M500 95 L560 95", INK, 2.5, None),
         '<circle cx="566" cy="95" r="12" style="fill:#2f9a3a;stroke:%s;stroke-width:2"/>' % INK,
         router(650, 95, "R1", 52), t(600, 40, "Gi1/0/1", 20, INK, 800)]
    return fig("".join(b), "0 0 760 200")


# ================================================================ блок-схемы ACL со сценой
def _dia(cx, cy, hw, hh, fill, stroke, sw=3, extra=""):
    return ('<path d="M%g %g L%g %g L%g %g L%g %g Z" style="fill:%s;stroke:%s;stroke-width:%g"%s/>'
            % (cx, cy - hh, cx + hw, cy, cx, cy + hh, cx - hw, cy, fill, stroke, sw, extra))


def acl_flow(rules, packet, steps, sid, hw=165, hh=118, gap=55, fsize=24, **_):
    """Сцена «пакет проходит ACL» по рисунку pptx — блок-схема слева направо (экран 16:9).
    rules  — [{'rows': ['Rule 10', 'Действие Permit', 'IP = 10.10.3.1'], 'act': 'permit'|'deny'}, ...]
    packet — [(поле, значение), ...] — полоса полей пакета сверху (как на рисунках pptx)
    steps  — [(подпись, {'rule': i, 'match': bool, 'fields': [индексы полей]} | {'end': 'permit'|'deny'} | {})]
    «Нет» — вправо к следующему правилу; «Да» у Deny — вверх на шину «отбросить», у Permit — вниз на шину «разрешить».
    """
    n = len(rules)
    fw, fh2 = 190, 72
    ptop = 96 if packet else 0
    ytop = ptop + 120                          # шина «отбросить»
    yc = ytop + 70 + hh                        # ось правил
    ybot = yc + hh + 70                        # шина «разрешить»
    yend = ybot + 128
    xs = [40 + hw + i * (2 * hw + gap) for i in range(n)]
    xd = xs[-1] + hw + gap + 110               # колонка итоговых блоков
    W = max(xd + 160, 40 + len(packet) * (fw + 8) + 150 if packet else 0)
    H = yend + 60
    b = []
    # начало — над первым правилом
    sy = ytop - 25
    b.append('<ellipse cx="%g" cy="%g" rx="105" ry="46" style="fill:%s;stroke:%s;stroke-width:3"/>' % (xs[0], sy, PAPER, INK))
    b.append(lines(xs[0], sy, ["Начало", "работы ACL"], 21, INK, 700))
    b.append(path("M%g %g L%g %g" % (xs[0], sy + 46, xs[0], yc - hh), INK, 3))
    for i, r in enumerate(rules):
        x = xs[i]
        b.append(_dia(x, yc, hw, hh, PAPER, INK))
        b.append(lines(x, yc, r["rows"], fsize, INK, 700))
        nx = xs[i + 1] - hw if i + 1 < n else xd - 110
        b.append(path("M%g %g L%g %g" % (x + hw, yc, nx, yc), INK, 3))
        b.append(t(x + hw + 8, yc - 12, "Нет", 21, INK, 700, "start"))
        if r["act"] == "deny":
            b.append(path("M%g %g L%g %g" % (x, yc - hh, x, ytop), INK, 3, None))
            b.append(t(x + 12, yc - hh - 16, "Да", 21, INK, 700, "start"))
        else:
            b.append(path("M%g %g L%g %g" % (x, yc + hh, x, ybot), INK, 3, None))
            b.append(t(x + 12, yc + hh + 30, "Да", 21, INK, 700, "start"))
    dx = [xs[i] for i, r in enumerate(rules) if r["act"] == "deny"]
    px_ = [xs[i] for i, r in enumerate(rules) if r["act"] == "permit"]
    if dx:
        b.append(path("M%g %g L%g %g L%g %g" % (min(dx), ytop, xd, ytop, xd, yc - 50), INK, 3))
    if px_:
        b.append(path("M%g %g L%g %g" % (min(px_), ybot, xd - 110, ybot), INK, 3))
    b.append(rect(xd - 110, yc - 50, 220, 100, PAPER, INK, 3))
    b.append(lines(xd, yc, ["Пакет", "отбрасывается"], 23, INK, 700))
    b.append(rect(xd - 110, ybot - 50, 220, 100, PAPER, INK, 3))
    b.append(lines(xd, ybot, ["Пакет", "разрешается"], 23, INK, 700))
    b.append(path("M%g %g L%g %g" % (xd, ybot + 50, xd, yend - 44), INK, 3))
    b.append(path("M%g %g L%g %g L%g %g L%g %g" % (xd + 110, yc, xd + 140, yc, xd + 140, yend, xd + 108, yend), INK, 3))
    b.append('<ellipse cx="%g" cy="%g" rx="105" ry="44" style="fill:%s;stroke:%s;stroke-width:3"/>' % (xd, yend, PAPER, INK))
    b.append(lines(xd, yend, ["Конец", "работы ACL"], 21, INK, 700))

    # полоса полей пакета
    fy = []
    if packet:
        b.append(rect(14, 10, len(packet) * (fw + 8) + 132, fh2 + 16, "#fff", INK, 3))
        b.append(t(70, 10 + (fh2 + 16) / 2.0 + 8, "ПАКЕТ", 22, TEAL, 800))
        for k, (nm, v) in enumerate(packet):
            cx_ = 128 + k * (fw + 8)
            fy.append(cx_)
            colr = "#cfe6c8" if "MAC" in nm else ("#ddd0ec" if "Port" in nm else "#f9dfbd")
            b.append(rect(cx_, 18, fw, fh2, colr, "#8a7a5a", 2))
            b.append(lines(cx_ + fw / 2.0, 18 + fh2 / 2.0, [nm, v], 19, INK, 700))

    caps = []
    for k, (cap, s_) in enumerate(steps):
        caps.append(cap)
        if "rule" in s_:
            i = s_["rule"]; x = xs[i]
            ok = s_.get("match")
            colr = (GREEN if rules[i]["act"] == "permit" else RED) if ok else GOLD
            fill = ("#cfe8c4" if rules[i]["act"] == "permit" else "#f3c9c0") if ok else YEL
            b.append('<g data-ph="%d" data-ph-only="%d">%s%s</g>' % (k, k, _dia(x, yc, hw, hh, fill, colr, 6),
                                                                     lines(x, yc, rules[i]["rows"], fsize, INK, 800)))
            b.append('<g data-ph="%d" data-ph-only="%d" class="pop">%s</g>' % (k, k, t(x - hw + 16, yc - hh + 30, "✉", 54, TEAL, 900)))
            for f in s_.get("fields", []):
                b.append('<g data-ph="%d" data-ph-only="%d">%s</g>' % (k, k, rect(fy[f] - 3, 15, fw + 6, fh2 + 6, "none", "#e0261c", 6)))
            if not ok:
                nx = xs[i + 1] - hw if i + 1 < n else xd - 110
                b.append('<g data-ph="%d" data-ph-only="%d">%s</g>' % (k, k, path("M%g %g L%g %g" % (x + hw, yc, nx, yc), GREEN, 6, "ag")))
            elif rules[i]["act"] == "deny":
                b.append('<g data-ph="%d">%s</g>' % (k, path("M%g %g L%g %g L%g %g L%g %g" % (x, yc - hh, x, ytop, xd, ytop, xd, yc - 50), GREEN, 6, "ag")))
            else:
                b.append('<g data-ph="%d">%s</g>' % (k, path("M%g %g L%g %g L%g %g" % (x, yc + hh, x, ybot, xd - 110, ybot), GREEN, 6, "ag")))
        if "end" in s_:
            ey = ybot if s_["end"] == "permit" else yc
            fill = "#bfe3b2" if s_["end"] == "permit" else "#f0b9ae"
            b.append('<g data-ph="%d" class="pop">%s%s</g>' % (k, rect(xd - 110, ey - 50, 220, 100, fill, GREEN, 6),
                     lines(xd, ey, ["Пакет", "разрешается" if s_["end"] == "permit" else "отбрасывается"], 23, INK, 800)))
    from _sw_lib import scene
    return scene(fig("".join(b), "0 0 %d %d" % (W, H), "fig aclfig flowfig"), caps, sid)


# ================================================================ рисунок 7.x: карточка пакета (расширенный ACL)
EXT_PACKET = [("Destination MAC", "E4:5A:D4:11:22:01"), ("Source MAC", "AA:BB:CC:33:22:11"), ("DSCP", "0"),
              ("Prot", "TCP"), ("Source IP", "10.10.1.25"), ("Destination IP", "62.109.1.166"),
              ("Source Port", "56785"), ("Dest Port", "443")]


def ext_packet_card():
    """Поля пакета из примера расширенного ACL — как на рисунке pptx."""
    cells = []
    for n, v in EXT_PACKET:
        col = "#cfe6c8" if "MAC" in n else ("#ddd0ec" if "Port" in n else "#f9dfbd")
        cells.append('<div class="pk-f" style="background:%s"><small>%s</small><b>%s</b></div>' % (col, n, v))
    return '<div class="pkcard">%s</div>' % "".join(cells)


CSS = r"""
.aclpanel{background:#faf3e0;border:3px solid #1d1d1b;box-shadow:6px 6px 0 rgba(0,0,0,.45);padding:10px}
svg.aclfig text{font-family:"Golos Text",sans-serif}
.col>.col{flex:1 1 auto;min-height:0}
.col>.scene,.scene{flex:1 1 auto;min-height:0}
.scene .figwrap{flex:1 1 auto;min-height:0;display:flex;align-items:center;justify-content:center}
svg.flowfig{flex:1 1 auto;width:100%;height:100%;min-height:0;max-height:none}
.hbar{display:flex;gap:0;border:3px solid #1d1d1b;box-shadow:5px 5px 0 rgba(0,0,0,.4);background:#fff}
.hb-g{display:flex;flex-direction:column;border-right:3px solid #1d1d1b;min-width:0}
.hb-g:last-child{border-right:0}
.hb-h{font:800 clamp(12px,1vw,19px)/1.2 "Golos Text",sans-serif;text-align:center;padding:5px 4px;border-bottom:2px solid #1d1d1b;background:#fff}
.hb-r{display:flex}
.hb-f{padding:10px 4px;text-align:center;font:700 clamp(11px,.95vw,18px)/1.2 "Golos Text",sans-serif;border-right:2px solid #8a7a5a;min-width:0;overflow-wrap:anywhere}
.hb-r>div{padding:10px 4px;text-align:center;font:700 clamp(11px,.95vw,18px)/1.2 "Golos Text",sans-serif;border-right:2px solid #8a7a5a;min-width:0;overflow-wrap:anywhere}
.hb-r>div:last-child{border-right:0}
.hb-r>div.hl{outline:4px solid #e0261c;outline-offset:-4px}
.pkcard{display:grid;grid-template-columns:1fr 1fr;gap:6px;border:3px solid #1d1d1b;background:#fff;padding:8px;box-shadow:5px 5px 0 rgba(0,0,0,.4)}
.pk-f{border:2px solid #8a7a5a;padding:6px 10px;text-align:center}
.pk-f small{display:block;font:700 clamp(11px,.85vw,16px)/1.2 "Golos Text",sans-serif;color:#4a4636}
.pk-f b{font:800 clamp(14px,1.2vw,23px)/1.25 "JetBrains Mono",monospace;color:#1d1d1b}
"""
