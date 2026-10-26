# -*- coding: utf-8 -*-
"""Схемы и сцены деки «Маршрутизаторы ESR» (2.3 доп.) — перерисовка рисунков pptx в стиле инфографик автора:
светлое лавандовое стекло, глянцевые синие маршрутизаторы, ПК и сервер — вырезки из инфографик.
Те же устройства, интерфейсы и адреса, что на рисунках pptx. Кабели — в свои порты."""
import base64
import os

from _sw_lib import scene, _esc

HERE = os.path.dirname(os.path.abspath(__file__))
INK, SOFT = "#141a5c", "#4a5290"
VI, BL, MG, CY, GR, RD, AM = "#6a4cff", "#2f6bff", "#c03ad6", "#18a8f0", "#18a75a", "#e23b5a", "#e89a10"
_cache = {}


def _uri(name):
    if name not in _cache:
        import io
        from PIL import Image
        buf = io.BytesIO()
        Image.open(os.path.join(HERE, "_er_assets", name + ".png")).save(buf, "WEBP", quality=86, method=5)
        _cache[name] = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    return _cache[name]


def defs():
    mk = "".join('<marker id="er%s" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">'
                 '<path d="M0 0L9 4.5L0 9z" fill="%s"/></marker>' % (k, c)
                 for k, c in (("a", VI), ("b", BL), ("m", MG), ("g", GR), ("r", RD), ("k", INK)))
    return ('<defs><linearGradient id="erRb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a62ff"/>'
            '<stop offset="1" stop-color="#1a2490"/></linearGradient>'
            '<radialGradient id="erRt" cx=".5" cy=".4" r=".7"><stop offset="0" stop-color="#8fb6ff"/>'
            '<stop offset="1" stop-color="#3f63f0"/></radialGradient>'
            '<linearGradient id="erSb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b4384"/>'
            '<stop offset="1" stop-color="#151a4c"/></linearGradient>'
            '<filter id="erGl" x="-40%%" y="-40%%" width="180%%" height="180%%"><feGaussianBlur stdDeviation="4" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            '<filter id="erSh" x="-20%%" y="-20%%" width="140%%" height="160%%"><feDropShadow dx="0" dy="6" stdDeviation="6" '
            'flood-color="#3a2a9a" flood-opacity=".28"/></filter>%s</defs>' % mk)


def fig(body, vb="0 0 1200 560"):
    return '<svg class="fig erfig" viewBox="%s">%s</svg>' % (vb, body)


def wrap(svg_html):
    return '<div class="figwrap erpanel">%s</div>' % svg_html


def ph(n, only=False):
    return ' data-ph="%d"%s' % (n, " data-ph-only" if only else "") if n is not None else ""


def t(x, y, s, size=16, col=INK, w=700, anchor="middle", mono=False, extra=""):
    fam = "font-family:JetBrains Mono,Consolas,monospace;" if mono else ""
    return ('<text x="%g" y="%g" text-anchor="%s" font-size="%g" font-weight="%d" style="fill:%s;%s"%s>%s</text>'
            % (x, y, anchor, size, w, col, fam, extra, s))


def pill(x, y, text, col=VI, size=15, fill="rgba(255,255,255,.92)", n=None, only=False, tc=None, mono=False):
    w = max(46, len(text) * size * (.6 if mono else .56) + 22)
    return ('<g%s><rect x="%g" y="%g" width="%g" height="%g" rx="%g" style="fill:%s;stroke:%s" stroke-width="2"/>%s</g>'
            % (ph(n, only), x - w / 2.0, y - size * .95, w, size * 1.9, size * .95, fill, col,
               t(x, y + size * .36, text, size, tc or INK, 800, mono=mono)))


def wire(x1, y1, x2, y2, col="#5b63b8", w=3.5, dash=False):
    d = ' stroke-dasharray="10 7"' if dash else ""
    return ('<path d="M%g %gL%g %g" style="stroke:%s" stroke-width="%g" stroke-linecap="round" fill="none"%s/>'
            % (x1, y1, x2, y2, col, w, d))


def dot(x, y, col=BL):
    return '<circle cx="%g" cy="%g" r="5.5" style="fill:#fff;stroke:%s" stroke-width="3"/>' % (x, y, col)


def router(x, y, name, r=56):
    """Глянцевый маршрутизатор-«шайба» как в инфографиках. (x, y) — центр."""
    h, ry = 34, r * .36
    o = ['<g filter="url(#erSh)">',
         '<path d="M%g %g v%g a%g %g 0 0 0 %g 0 v-%g z" fill="url(#erRb)"/>' % (x - r, y - h / 2, h, r, ry, 2 * r, h),
         '<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="url(#erRt)" style="stroke:#c9d8ff" stroke-width="2"/>' % (x, y - h / 2, r, ry)]
    for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        x1, y1 = x + dx * r * .14, y - h / 2 + dy * ry * .16
        x2, y2 = x + dx * r * .5, y - h / 2 + dy * ry * .62
        o.append('<path d="M%g %gL%g %g" style="stroke:#fff" stroke-width="3.4" stroke-linecap="round"/>' % (x1, y1, x2, y2))
    o.append('</g>')
    o.append(t(x, y + h / 2 + 2, name, 19, "#fff", 900))
    return "".join(o)


def switch(x, y, name, n=4, w=170, h=44):
    """Коммутатор: (x, y) — центр. Возвращает (svg, [координаты портов слева направо])."""
    o = ['<g filter="url(#erSh)"><rect x="%g" y="%g" width="%g" height="%g" rx="9" fill="url(#erSb)" style="stroke:#9fb0ff" stroke-width="2"/>'
         % (x - w / 2, y - h / 2, w, h)]
    pts = []
    pw, gap = 16, (w - 30 - n * 16) / float(max(1, n - 1))
    for i in range(n):
        px = x - w / 2 + 15 + i * (pw + gap)
        o.append('<rect x="%g" y="%g" width="%g" height="11" rx="2" style="fill:#7fd0ff;stroke:#cfe9ff" stroke-width="1"/>'
                 % (px, y + 4, pw))
        pts.append((px + pw / 2, y + h / 2))
    o.append('</g>')
    o.append(t(x, y - 4, name, 16, "#fff", 900))
    return "".join(o), pts


def pc(x, y, name, ip="", w=104, col=VI):
    """ПК из инфографики автора; (x, y) — верх монитора. Порт — (x, y + 6)."""
    hh = w * 112 / 168.0
    o = ['<image href="%s" x="%g" y="%g" width="%g" height="%g"/>' % (_uri("dev_pc"), x - w / 2, y, w, hh)]
    o.append(pill(x, y + hh + 16, name, col, 15))
    if ip:
        o.append(t(x, y + hh + 46, ip, 14, INK, 700, mono=True))
    return "".join(o)


def phone(x, y, name, w=70, col=VI):
    """IP-телефон: корпус с трубкой и клавиатурой, в цветах устройств инфографик."""
    o = ['<g filter="url(#erSh)"><path d="M%g %g l%g 0 l10 %g l-%g 0 z" fill="url(#erSb)" style="stroke:#9fb0ff" stroke-width="2"/>'
         % (x - w / 2, y + 22, w, w * .62, w + 20),
         '<rect x="%g" y="%g" width="%g" height="16" rx="8" style="fill:#3a62ff;stroke:#c9d8ff" stroke-width="2"/>' % (x - w / 2 - 4, y + 6, w + 8)]
    for i in range(3):
        for j in range(3):
            o.append('<rect x="%g" y="%g" width="9" height="6" rx="1.5" style="fill:#7fd0ff"/>' % (x - 14 + i * 13, y + 34 + j * 10))
    o.append('</g>')
    o.append(pill(x, y + w * .62 + 46, name, col, 15))
    return "".join(o)


def server(x, y, name, w=96, col=VI, lines=()):
    hh = w * 317 / 354.0
    o = ['<image href="%s" x="%g" y="%g" width="%g" height="%g"/>' % (_uri("dev_srv"), x - w / 2, y, w, hh)]
    o.append(pill(x, y + hh + 16, name, col, 15))
    for i, l in enumerate(lines):
        o.append(t(x, y + hh + 46 + i * 19, l, 14, INK, 700, mono=True))
    return "".join(o)


def cloud(x, y, w, h, label="", col="#9aa6ff", fill="rgba(235,238,255,.85)", size=20):
    rx, ry = w / 2.0, h / 2.0
    d = ("M{a} {b} C{a} {c} {d} {c} {e} {f} C{g} {h} {i} {h} {j} {f} C{k} {f} {k} {l} {j} {l} "
         "C{j} {m} {n} {m} {o} {l} C{p} {m} {a} {q} {a} {b}z").format(
        a=x - rx, b=y + ry * .3, c=y - ry * .2, d=x - rx * .6, e=x - rx * .45, f=y - ry * .55,
        g=x - rx * .3, h=y - ry * 1.05, i=x + rx * .35, j=x + rx * .5, k=x + rx, l=y + ry * .25,
        m=y + ry, n=x + rx * .1, o=x - rx * .1, p=x - rx * .6, q=y + ry * .9)
    o = '<path d="%s" style="fill:%s;stroke:%s" stroke-width="2.5"/>' % (d, fill, col)
    return o + (t(x, y + size * .4, label, size, INK, 800) if label else "")


def env(x0, y0, x1, y1, n, col=VI, only=True):
    """Летящий конверт-пакет (класс mv движка)."""
    s = "--x0:0px;--y0:0px;--x1:%gpx;--y1:%gpx" % (x1 - x0, y1 - y0)
    return ('<g class="mv"%s style="%s"><rect x="%g" y="%g" width="44" height="30" rx="5" style="fill:#fff;stroke:%s" stroke-width="3" filter="url(#erGl)"/>'
            '<path d="M%g %gL%g %gL%g %g" style="stroke:%s" stroke-width="2.6" fill="none"/></g>'
            % (ph(n, only), s, x0 - 22, y0 - 15, col, x0 - 19, y0 - 11, x0, y0 + 3, x0 + 19, y0 - 11, col))


def arr(x1, y1, x2, y2, col=BL, mk="b", w=3.4, n=None, only=False, flow=False):
    cls = ' class="flow"' if flow else ""
    return ('<path d="M%g %gL%g %g" style="stroke:%s" stroke-width="%g" fill="none" marker-end="url(#er%s)"%s%s/>'
            % (x1, y1, x2, y2, col, w, mk, cls, ph(n, only)))


def note(x, y, w, lines, col=VI, n=None, only=False, size=15):
    h = 18 + len(lines) * (size + 6)
    o = ['<g%s><rect x="%g" y="%g" width="%g" height="%g" rx="12" style="fill:rgba(255,255,255,.95);stroke:%s" stroke-width="2.4" filter="url(#erSh)"/>'
         % (ph(n, only), x, y, w, h, col)]
    for i, l in enumerate(lines):
        o.append(t(x + 14, y + 26 + i * (size + 6), l, size, INK, 700 if i else 800, "start"))
    o.append('</g>')
    return "".join(o)


def htable(cols, rows, cls=""):
    th = "".join("<th>%s</th>" % c for c in cols)
    tr = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return '<div class="tw ertw %s"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (cls, th, tr)


# ====================================================================== pptx 6: две LAN через WAN
def wan():
    o = []
    s1, p1 = switch(300, 190, "SW1", 5)
    s2, p2 = switch(900, 190, "SW2", 5)
    # кабели — за устройствами
    o += [wire(p1[0][0], p1[0][1], 110, 300), wire(p1[1][0], p1[1][1], 200, 320), wire(p1[2][0], p1[2][1], 300, 330),
          wire(p1[3][0], p1[3][1], 395, 330), wire(p1[4][0], p1[4][1], 480, 380)]
    o += [wire(p2[0][0], p2[0][1], 720, 380), wire(p2[1][0], p2[1][1], 805, 330), wire(p2[2][0], p2[2][1], 900, 330),
          wire(p2[3][0], p2[3][1], 1000, 320), wire(p2[4][0], p2[4][1], 1090, 300)]
    o += [wire(480, 380, 520, 420), wire(720, 380, 680, 420, "#e89a10", 4)]
    o.append(wire(560, 428, 640, 428, "#e89a10", 4.5))
    o += [s1, s2]
    o += [pc(110, 300, "ПК", w=88), pc(200, 320, "ПК", w=88), server(300, 330, "Сервер", 70), phone(395, 330, "Телефон")]
    o += [pc(805, 330, "ПК", w=88), server(900, 330, "Сервер", 70), pc(1000, 320, "ПК", w=88), phone(1090, 300, "Телефон")]
    o += [router(520, 440, "R1", 50), router(680, 440, "R2", 50)]
    o += [t(300, 120, "LAN 192.168.1.0/24", 18, INK, 800), t(900, 120, "LAN 192.168.2.0/24", 18, INK, 800),
          t(600, 400, "WAN 192.168.3.0/30", 17, "#b06a00", 800), t(560, 500, "3.1", 15, INK, 800),
          t(640, 500, "3.2 · G1", 15, INK, 800), t(760, 440, "G2", 15, INK, 800)]
    o.append(note(820, 455, 360, ["R2# show ip route", "C 192.168.3.0/30 G1", "C 192.168.2.0/24 G2",
                                  "S 192.168.1.0/24 via 192.168.3.1"], BL, size=14))
    return wrap(fig("".join(o), "0 0 1200 570"))


# ====================================================================== pptx 18: домашняя сеть
def home():
    s, pt = switch(780, 400, "", 4, 170)
    o = [wire(560, 160, 330, 380), wire(640, 160, pt[0][0], pt[0][1] - 44), wire(pt[3][0], pt[3][1] - 44, 980, 250)]
    o += [cloud(300, 420, 260, 140, "Internet", size=26), s, router(600, 130, "R1", 70), pc(990, 170, "ПК", w=130)]
    o += [pill(400, 230, "gi1/0/1", BL, 17, mono=True), pill(800, 230, "gi1/0/2", BL, 17, mono=True),
          dot(560, 160), dot(640, 160), t(300, 520, "динамический адрес (провайдер)", 15, SOFT, 700),
          t(780, 470, "статический адрес · локальная сеть", 15, SOFT, 700)]
    return wrap(fig("".join(o), "0 0 1200 540"))


def ipv4_window():
    def row(lbl):
        return '<div class="erw-row"><span>%s</span><i>.&nbsp;&nbsp;&nbsp;.&nbsp;&nbsp;&nbsp;.</i></div>' % lbl
    return ('<div class="erwin"><div class="erw-t">Свойства: IP версии 4 (TCP/IPv4)<b>✕</b></div><div class="erw-b">'
            '<div class="erw-tab">Общие</div>'
            '<p>Параметры IP можно назначать автоматически, если сеть поддерживает эту возможность. В противном случае узнайте '
            'параметры IP у сетевого администратора.</p>'
            '<div class="erw-r"><i class="o"></i>Получить IP-адрес автоматически</div>'
            '<div class="erw-r"><i class="o on"></i>Использовать следующий IP-адрес:</div>'
            '<div class="erw-g">%s%s%s</div>'
            '<div class="erw-r dis"><i class="o"></i>Получить адрес DNS-сервера автоматически</div>'
            '<div class="erw-r"><i class="o on"></i>Использовать следующие адреса DNS-серверов:</div>'
            '<div class="erw-g">%s%s</div>'
            '<div class="erw-f"><span><i class="x"></i>Подтвердить параметры при выходе</span><u>Дополнительно...</u></div>'
            '<div class="erw-f r"><u>OK</u><u>Отмена</u></div></div></div>'
            % (row("IP-адрес:"), row("Маска подсети:"), row("Основной шлюз:"),
               row("Предпочитаемый DNS-сервер:"), row("Альтернативный DNS-сервер:")))


# ====================================================================== pptx 20: сцена PC1 → PC3
def gw_scene():
    s1, a = switch(300, 300, "SW1", 3, 150)
    s2, b = switch(900, 300, "SW2", 3, 150)
    o = [wire(555, 120, a[2][0], a[2][1] - 44), wire(645, 120, b[0][0], b[0][1] - 44),
         wire(a[0][0], a[0][1], 190, 400), wire(a[1][0], a[1][1], 410, 400),
         wire(b[1][0], b[1][1], 790, 400), wire(b[2][0], b[2][1], 1010, 400)]
    o += [s1, s2, router(600, 95, "R1", 64)]
    o += [pc(190, 400, "PC1", ".10"), pc(410, 400, "PC2", ".11"), pc(790, 400, "PC3", ".10"), pc(1010, 400, "PC4", ".11")]
    o += [dot(555, 120), dot(645, 120), pill(430, 70, "gi 1/0/1 · .1", BL, 16), pill(770, 70, "gi 1/0/2 · .1", BL, 16),
          t(150, 300, "192.168.10.0/24", 18, INK, 800), t(1060, 300, "192.168.11.0/24", 18, INK, 800)]
    o += [env(190, 395, a[0][0], a[0][1] + 6, 1), env(a[2][0], a[2][1] - 50, 555, 125, 2),
          env(645, 125, b[0][0], b[0][1] - 50, 3), env(b[1][0], b[1][1] + 6, 790, 395, 4)]
    o += [note(30, 30, 330, ["Пакет PC1 → PC3", "Источник: IP PC1", "Назначение: IP PC3"], VI, 1),
          note(840, 140, 340, ["R1 проверяет таблицу", "маршрутизации → gi1/0/2"], BL, 3, True)]
    return scene(fig("".join(o), "0 0 1200 560"), [
        "Схема: R1 — шлюз по умолчанию в каждой из двух подсетей.",
        "PC3 в другой сети: PC1 отправляет пакет на свой шлюз — gi 1/0/1 R1.",
        "R1 принимает пакет и проверяет таблицу маршрутизации.",
        "Пакет уходит через интерфейс gi1/0/2 в подсеть PC3.",
        "PC3 получает пакет."], "er_gw")


# ====================================================================== pptx 22: PuTTY
def putty():
    cats = ["▼ Session", "&nbsp;&nbsp;&nbsp;Logging", "▼ Terminal", "&nbsp;&nbsp;&nbsp;Keyboard", "&nbsp;&nbsp;&nbsp;Bell",
            "&nbsp;&nbsp;&nbsp;Features", "▼ Window", "&nbsp;&nbsp;&nbsp;Appearance", "&nbsp;&nbsp;&nbsp;Behaviour",
            "&nbsp;&nbsp;&nbsp;Translation", "&nbsp;&nbsp;&nbsp;▸ Selection", "&nbsp;&nbsp;&nbsp;Colours",
            "&nbsp;&nbsp;&nbsp;Fonts", "▼ Connection", "&nbsp;&nbsp;&nbsp;Data", "&nbsp;&nbsp;&nbsp;Proxy",
            "&nbsp;&nbsp;&nbsp;▸ SSH", "&nbsp;&nbsp;&nbsp;Serial", "&nbsp;&nbsp;&nbsp;Telnet"]
    return ('<div class="erwin putty"><div class="erw-t">PuTTY Configuration<b>✕</b></div><div class="erw-b pt">'
            '<div class="pt-l"><div class="pt-h">Category:</div>%s</div>'
            '<div class="pt-r"><div class="pt-h c">Basic options for your PuTTY session</div>'
            '<fieldset><legend>Specify the destination you want to connect to</legend>'
            '<div class="pt-2"><label>Host Name (or IP address)<i class="in"></i></label><label class="sm">Port<i class="in">22</i></label></div>'
            '<div>Connection type:</div><div class="pt-rad"><span><i class="o on"></i>SSH</span><span><i class="o"></i>Serial</span>'
            '<span><i class="o"></i>Other:</span><i class="in sel">Telnet ▾</i></div></fieldset>'
            '<fieldset><legend>Load, save or delete a stored session</legend><div>Saved Sessions</div><i class="in"></i>'
            '<div class="pt-2"><div class="pt-list">Default Settings</div><div class="pt-bt"><u>Load</u><u>Save</u><u>Delete</u></div></div></fieldset>'
            '<fieldset><legend>Close window on exit:</legend><div class="pt-rad"><span><i class="o on"></i>Always</span>'
            '<span><i class="o"></i>Never</span><span><i class="o"></i>Only on clean exit</span></div></fieldset></div>'
            '<div class="pt-f"><u>About</u><span><u>Open</u><u>Cancel</u></span></div></div></div>'
            % "".join('<div class="pt-c%s">%s</div>' % (" on" if i == 0 else "", c) for i, c in enumerate(cats)))


# ====================================================================== pptx 29: формат ICMP
def icmp_format():
    return ('<div class="ericmp"><div class="ei-row"><span>Заголовок Ethernet</span><span>IP-заголовок</span>'
            '<span class="hl">Сообщение ICMP</span><span>Концевик Ethernet</span></div>'
            '<div class="ei-msg"><div class="ei-row"><span class="hl">Тип</span><span class="hl">Код</span><span class="w">Контрольная сумма</span></div>'
            '<div class="ei-row"><span class="w2">Содержание сообщения ICMP</span></div></div></div>')


def icmp_codes():
    return htable(["Тип", "Код", "Описание"], [["0", "0", "Эхо-ответ"], ["3", "0", "Сеть недоступна"],
                  ["3", "1", "Хост недоступен"], ["3", "2", "Протокол недоступен"], ["3", "3", "Порт недоступен"],
                  ["5", "0", "Переадресация"], ["8", "0", "Эхо-запрос"]], "ctr")


# ====================================================================== pptx 30: ping
def _two_lans(w2="192.168.30.0"):
    s1, a = switch(330, 270, "SW1", 3, 150)
    s2, b = switch(870, 270, "SW2", 3, 150)
    o = [wire(450, 110, 750, 110), wire(390, 140, a[2][0], a[2][1] - 44), wire(810, 140, b[0][0], b[0][1] - 44),
         wire(a[0][0], a[0][1], 110, 350), wire(a[1][0], a[1][1], 330, 380),
         wire(b[1][0], b[1][1], 870, 380), wire(b[2][0], b[2][1], 1090, 350)]
    o += [s1, s2, router(390, 110, "R1", 58), router(810, 110, "R2", 58)]
    o += [pc(110, 350, "ПК1", ".2", 96), pc(330, 380, "ПК2", ".3", 96), pc(870, 380, "ПК3", ".2", 96), pc(1090, 350, "ПК4", ".3", 96)]
    o += [pill(250, 150, ".1", BL, 15), pill(950, 150, ".1", BL, 15),
          t(180, 270, "192.168.10.0", 18, INK, 800), t(1030, 270, w2, 18, INK, 800)]
    return o, a, b


def ping_scene():
    o, a, b = _two_lans()
    o += [pill(110, 60, "ping 192.168.30.2", VI, 17, mono=True)]
    o += [env(110, 345, a[0][0], a[0][1] + 6, 1), env(a[2][0], a[2][1] - 50, 400, 140, 2), env(450, 110, 750, 110, 3), env(800, 140, b[0][0], b[0][1] - 50, 4),
          env(b[1][0], b[1][1] + 6, 870, 375, 5)]
    o += [env(870, 375, b[1][0], b[1][1] + 6, 6, GR), env(b[0][0], b[0][1] - 50, 800, 140, 7, GR),
          env(750, 110, 450, 110, 8, GR), env(400, 140, a[2][0], a[2][1] - 50, 9, GR), env(a[0][0], a[0][1] + 6, 110, 345, 10, GR)]
    o += [note(450, 470, 300, ["Отправка ICMP", "эхо-запроса"], VI, 1), pill(1010, 470, "ПК 3 - доступен", GR, 18, n=10)]
    o.append(note(450, 470, 300, ["Отправка ICMP", "эхо-ответа"], GR, 6))
    return scene(fig("".join(o), "0 0 1200 560"), [
        "Сеть: ПК1 (192.168.10.2) проверяет связь с ПК3 (192.168.30.2).",
        "ПК1: ping 192.168.30.2 — отправка ICMP эхо-запроса на SW1.",
        "SW1 → шлюз R1 (.1).", "R1 → R2.", "R2 → SW2.", "SW2 → ПК3: эхо-запрос доставлен.",
        "ПК3 отправляет ICMP эхо-ответ.", "SW2 → R2.", "R2 → R1.", "R1 → SW1.", "SW1 → ПК1: ПК 3 - доступен."], "er_ping")


# ====================================================================== pptx 31: Redirect
def redirect_scene():
    o = [wire(150, 90, 520, 90, "#5b63b8", 3), wire(330, 90, 330, 150), wire(330, 190, 330, 320),
          wire(150, 320, 1050, 320, "#5b63b8", 3), wire(870, 190, 870, 320), wire(870, 150, 870, 110), wire(600, 320, 600, 380)]
    o += [server(330, -6, "Сервер A", 66), router(330, 175, "R", 48), router(870, 175, "R", 48),
          cloud(870, 70, 200, 90, "Интернет", size=20), pc(600, 380, "Хост A", w=110)]
    o += [t(400, 82, "20.0.0.1/24", 15, INK, 700, "start"), t(395, 140, "20.0.0.2/24", 15, INK, 700, "start"),
          t(140, 175, "Маршрутизатор A", 17, INK, 800, "start"), t(940, 175, "Маршрутизатор B", 17, INK, 800, "start"),
          t(170, 305, "10.0.0.200/24", 15, INK, 700, "start"), t(890, 305, "10.0.0.100/24", 15, INK, 700, "start"),
          t(680, 420, "IP-адрес: 10.0.0.1/24", 16, INK, 700, "start"), t(680, 444, "Шлюз по умолчанию: 10.0.0.100", 16, INK, 700, "start")]
    o += [arr(640, 380, 850, 220, BL, "b", 4, 1, flow=True), pill(760, 280, "1", BL, 16, n=1),
          arr(850, 225, 640, 395, MG, "m", 4, 2, flow=True), note(900, 360, 280, ["Сообщение", "перенаправления ICMP"], MG, 2),
          pill(720, 350, "2", MG, 16, n=2),
          arr(560, 380, 350, 220, GR, "g", 4, 3, flow=True), pill(450, 280, "3", GR, 16, n=3)]
    return scene(fig("".join(o), "0 -20 1200 600"), [
        "Хост A, его шлюз по умолчанию — маршрутизатор B (10.0.0.100).",
        "1. Пакет к серверу A уходит на маршрутизатор B — маршрут неоптимален.",
        "2. Маршрутизатор B отправляет хосту сообщение перенаправления ICMP.",
        "3. Хост меняет маршрут: пакеты к серверу A идут через маршрутизатор A."], "er_redir")


# ====================================================================== pptx 37: traceroute
def trace_scene():
    o = [cloud(650, 230, 620, 330, "", fill="rgba(255,226,196,.55)", col="#f0b070")]
    R = {"R1": (230, 110), "R2": (520, 110), "R3": (440, 300), "R4": (650, 300), "R5": (760, 110), "R6": (880, 300)}
    s1, a = switch(260, 290, "SW1", 3, 140)
    s2, b = switch(1030, 160, "SW2", 3, 140)
    o += [wire(*R["R1"] + R["R2"]), wire(*R["R2"] + R["R3"]), wire(*R["R3"] + R["R4"]), wire(*R["R4"] + R["R5"]),
          wire(*R["R5"] + R["R6"]), wire(880, 300, b[0][0], b[0][1]), wire(230, 135, a[2][0], a[2][1] - 44),
          wire(a[0][0], a[0][1], 90, 360), wire(a[1][0], a[1][1], 200, 400), wire(b[2][0], b[2][1], 1120, 300),
          wire(b[1][0], b[1][1], 1000, 330)]
    o += [s1, s2] + [router(x, y, k, 50) for k, (x, y) in R.items()]
    o += [pc(90, 360, "ПК1", ".2", 92), pc(200, 400, "ПК2", ".3", 92), server(1120, 300, "eltex-co.ru", 70),
          server(1000, 330, "Сервер", 60)]
    o += [pill(140, 180, ".1", BL, 15), t(310, 380, "192.168.10.0", 16, INK, 800), pill(130, 40, "traceroute eltex-co.ru", VI, 16, mono=True)]
    path = [(90, 355), a[0], (a[2][0], a[2][1] - 50), R["R1"], R["R2"], R["R3"], R["R4"], R["R5"], R["R6"], b[0], (1120, 300)]
    for i in range(len(path) - 1):
        o.append(env(path[i][0], path[i][1], path[i + 1][0], path[i + 1][1], i + 1, AM))
    return scene(fig("".join(o), "0 0 1200 520"), [
        "Маршрут от ПК1 до сервера eltex-co.ru через сеть Интернет."] + [
        "Пакет: шаг %d." % i for i in range(1, 11)], "er_trace")


# ====================================================================== pptx 38: этапы AAA
def aaa_steps():
    st = [("Шаг 1", "Определение пользователя", "Определение пользователей по такой информации, как учетная запись и пароль."),
          ("Шаг 2", "Аутентификация", "Определение и аутентификация пользователей, которые пытаются получить доступ к ресурсам."),
          ("Шаг 3", "Авторизация", "Определяется, разрешён ли доступ авторизацией."),
          ("Шаг 4", "Учет", "Проверяется и записывается информация о доступе.")]
    return '<div class="ersteps">%s</div>' % "".join(
        '<div class="step"><div class="es"><u>%s</u><b>%s</b><p>%s</p></div></div>' % s for s in st)


# ====================================================================== pptx 39–45: архитектура AAA
def _users(o, x=120, tablet3=True):
    for i, (y, nm) in enumerate(((60, "Пользователь 1@Домен 1"), (200, "Пользователь 2@Домен 2"), (340, "Пользователь 3@Домен 3"))):
        o.append(pc(x, y, nm, w=88, col=BL))


def aaa_arch(mode=None):
    """mode: None — общая архитектура; 'auth' | 'authz' | 'acct' — с таблицей и стрелками (pptx 40/44/45)."""
    o = []
    o += [wire(165, 90, 420, 230), wire(165, 230, 420, 250), wire(165, 370, 420, 270), wire(560, 260, 640, 260),
          wire(640, 260, 760, 260), wire(880, 260, 1020, 260), wire(700, 110, 700, 220)]
    o += [cloud(480, 260, 300, 180, "IP-сеть", size=22), cloud(900, 250, 280, 170, "IP-сеть", size=22),
          cloud(700, 80, 170, 70, "Internet", col="#2f6bff", fill="rgba(70,110,255,.9)", size=19)]
    o.append('<g filter="url(#erSh)"><rect x="672" y="228" width="58" height="58" rx="10" fill="url(#erRb)" style="stroke:#c9d8ff" stroke-width="2"/></g>'
             + t(701, 266, "R", 28, "#fff", 900) + t(701, 316, "NAS", 18, INK, 800))
    o.append(server(1050, 200, "AAA Сервер", 74))
    _users(o)
    if mode == "auth":
        o += [arr(230, 200, 380, 215, INK, "k", 2.4), t(200, 185, "Имя пользователя и пароль", 14, INK, 700, "start"),
              arr(230, 380, 400, 300, INK, "k", 2.4), t(240, 405, "Имя пользователя и пароль", 14, INK, 700, "start"),
              arr(760, 238, 1010, 238, INK, "k", 2.4), t(770, 228, "Имя пользователя и пароль пользователя 3", 13, INK, 700, "start"),
              arr(1010, 285, 760, 285, INK, "k", 2.4), t(775, 306, "Возврат результата аутентификации", 13, INK, 700, "start")]
    if mode == "authz":
        o += [arr(1010, 270, 760, 270, INK, "k", 2.4), t(885, 300, "Разрешение пользователю 2", 13, INK, 700),
              t(885, 318, "после успешной аутентификации", 13, INK, 700)]
    if mode == "acct":
        o += [arr(760, 240, 1010, 240, INK, "k", 2.4), t(885, 230, "Запрос Accounting-Start", 13, INK, 700),
              arr(1010, 280, 760, 280, INK, "k", 2.4), t(885, 300, "Ответ Accounting-Start", 13, INK, 700)]
    if mode is None:
        o.append(t(900, 470, "Общая архитектура AAA", 20, INK, 800))
    return wrap(fig("".join(o), "0 0 1200 500"))


AUTH_T = (["Пользователь", "Домен", "Режим аутентификации"],
          [["Пользователь 1@Домен 1", "Домен 1", "Без аутентификации"], ["Пользователь 2@Домен 2", "Домен 2", "Локальная аутентификация"],
           ["Пользователь 3@Домен 3", "Домен 3", "Удаленная аутентификация"]])
AUTHZ_T = (["Пользователь", "Домен", "Режим авторизации", "Содержание авторизации"],
           [["Пользователь 1@Домен 1", "Домен 1", "Без авторизации", "—"],
            ["Пользователь 2@Домен 2", "Домен 2", "Локальная авторизация", "Доступ в Интернет разрешен."],
            ["Пользователь 3@Домен 3", "Домен 3", "Удаленная авторизация", "Авторизация предоставляется удаленным сервером."]])
ACCT_T = (["Пользователь", "Домен", "Режим учета"],
          [["Пользователь 1@Домен 1", "Домен 1", "Без учета"], ["Пользователь 2@Домен 2", "Домен 2", "Без учета"],
           ["Пользователь 3@Домен 3", "Домен 3", "Удаленный учет"]])


# ====================================================================== pptx 41/42: локальная и серверная
def local_auth():
    o = [wire(260, 200, 700, 200, INK, 3), arr(260, 175, 680, 175, RD, "r", 3.4, flow=True), arr(700, 225, 280, 225, RD, "r", 3.4, flow=True),
         pc(170, 120, "Пользователь", w=160), router(800, 200, "R1", 80)]
    return wrap(fig("".join(o), "0 60 1100 300"))


def radius_auth():
    o = [wire(250, 200, 1000, 200, INK, 3), arr(250, 175, 520, 175, RD, "r", 3.4, flow=True), arr(520, 225, 270, 225, RD, "r", 3.4, flow=True),
         arr(680, 215, 960, 215, RD, "r", 3.4, flow=True), arr(960, 215, 690, 215, RD, "r", 3.4),
         pc(160, 120, "Пользователь", w=150), router(600, 200, "R1", 76), server(1050, 120, "Radius сервер", 110),
         t(600, 290, "Маршрутизатор", 17, INK, 800), t(600, 312, "AAA", 17, INK, 800)]
    return wrap(fig("".join(o), "0 60 1200 340"))


# ====================================================================== pptx 43: обмен RADIUS
def radius_seq():
    X = (150, 600, 1050)
    rows = [(1, 0, "Пользователь вводит имя пользователя и пароль.", BL), (1, 2, "Access-Request", BL),
            (2, 1, "Прием или отклонение аутентификации, доставка соответствующего пакета.", BL),
            (1, 0, "Уведомление пользователя о результате аутентификации.", BL),
            (1, 2, "Запрос Accounting-Start", BL), (2, 1, "Ответ Accounting-Start", BL),
            (0, 2, "Пользователь инициирует доступ к сетевым ресурсам.", VI),
            (0, 1, "Пользователь запрашивает переход в офлайн.", BL), (1, 2, "Запрос Accounting-Stop", BL),
            (2, 1, "Ответ Accounting-Stop", BL), (1, 0, "Уведомление пользователя о завершении доступа.", BL)]
    o = [wire(x, 100, x, 640, INK, 2, True) for x in X]
    o += [t(150, 60, "Пользователь", 19, INK, 800), t(600, 60, "NAS", 19, INK, 800), t(1050, 60, "Сервер RADIUS", 19, INK, 800)]
    for i, (a, b, lab, c) in enumerate(rows):
        y = 125 + i * 48
        if (a, b) == (1, 0) and i == 0:
            a, b = 0, 1
        x1, x2 = X[a], X[b]
        if a == 0 and b == 2:
            o.append('<g%s>%s%s</g>' % (ph(i + 1), arr(x1 + 8, y, x2 - 8, y, c, "a", 4), arr(x2 - 8, y, x1 + 8, y, c, "a", 4))
                     + t(600, y - 10, lab, 17, INK, 800, extra=ph(i + 1)))
            continue
        sgn = 1 if x2 > x1 else -1
        o.append(arr(x1 + 8 * sgn, y, x2 - 8 * sgn, y, c, "b", 3.2, i + 1))
        o.append(t((x1 + x2) / 2.0, y - 10, lab, 14.5, INK, 700, extra=ph(i + 1)))
    caps = ["Участники обмена: пользователь, NAS (клиент RADIUS), сервер RADIUS."] + [
        "Шаг %d." % (i + 1) for i in range(len(rows))]
    return scene(fig("".join(o), "0 20 1200 640"), caps, "er_rad")


# ====================================================================== pptx 3: ESR-200 (перерисовка фото)
def esr200():
    o = ['<g filter="url(#erSh)"><path d="M120 120 L1080 120 L1120 200 L80 200 Z" style="fill:#e7e9f6;stroke:#b8bde0" stroke-width="2"/>',
         '<rect x="80" y="200" width="1040" height="190" rx="8" style="fill:#f3f4fb;stroke:#b8bde0" stroke-width="2"/></g>']
    for i in range(14):
        for j in range(4):
            o.append('<circle cx="%g" cy="%g" r="6" style="fill:#c9cce6"/>' % (110 + i * 16 + (j % 2) * 8, 225 + j * 14))
            o.append('<circle cx="%g" cy="%g" r="6" style="fill:#c9cce6"/>' % (780 + i * 16 + (j % 2) * 8, 225 + j * 14))
    o += [t(110, 300, "ELTEX", 20, INK, 900, "start"), t(200, 300, "ESR-200", 18, INK, 700, "start"),
          '<rect x="105" y="350" width="80" height="10" rx="3" style="fill:#2a2f55"/>']
    o += ['<rect x="210" y="320" width="22" height="40" rx="3" style="fill:#fff;stroke:#555"/>', t(221, 315, "USB1", 12, INK, 700),
          '<rect x="250" y="320" width="22" height="40" rx="3" style="fill:#2f6bff;stroke:#555"/>', t(261, 315, "USB2", 12, INK, 700)]

    def rj(x, y, n, top):
        return ('<rect x="%g" y="%g" width="40" height="34" rx="3" style="fill:#2a2f55;stroke:#9aa0c8" stroke-width="2"/>'
                '<rect x="%g" y="%g" width="24" height="10" style="fill:#c9a24a"/>' % (x, y, x + 8, y + (4 if top else 20))
                + t(x + 20, y - 6 if top else y + 52, str(n), 13, INK, 700))
    for k, (x, n1, n2) in enumerate(((300, 1, 5), (346, 2, 6), (410, 3, 7), (456, 4, 8))):
        o.append(rj(x, 250, n1, True) + rj(x, 290, n2, False))
    for x, n1, n2 in ((520, 3, 7), (575, 4, 8)):
        o.append('<rect x="%g" y="250" width="44" height="34" rx="2" style="fill:#d9dcee;stroke:#777"/>'
                 '<rect x="%g" y="290" width="44" height="34" rx="2" style="fill:#d9dcee;stroke:#777"/>' % (x, x)
                 + t(x + 22, 244, str(n1), 13, INK, 700) + t(x + 22, 342, str(n2), 13, INK, 700))
    o.append('<path d="M405 240 L625 240" style="stroke:#555" stroke-width="1.5"/>' + t(515, 233, "Combo ports", 13, INK, 700))
    for i, lb in enumerate(("Power", "Status", "Alarm", "Fan")):
        o.append('<circle cx="650" cy="%g" r="5" style="fill:#5b5f7a"/>' % (262 + i * 18) + t(662, 267 + i * 18, lb, 13, INK, 700, "start"))
    o += ['<rect x="760" y="300" width="56" height="44" rx="3" style="fill:#2a2f55;stroke:#9aa0c8" stroke-width="2"/>',
          t(788, 292, "Console", 13, INK, 700),
          '<rect x="960" y="230" width="120" height="110" rx="10" style="fill:#1b1d2e"/>',
          '<rect x="990" y="260" width="60" height="40" rx="4" style="fill:#000"/>', t(1095, 270, "110-250 VAC", 11, INK, 700, "start")]
    return wrap(fig("".join(o), "60 100 1080 310"))
