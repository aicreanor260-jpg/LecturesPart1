# -*- coding: utf-8 -*-
import math, json, pathlib, base64, io, glob
from PIL import Image as _Im0
def _jpg(path, w=2400, q=92):
    im = _Im0.open(path).convert("RGB")
    if im.width > w: im = im.resize((w, round(im.height*w/im.width)), _Im0.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True, progressive=True, subsampling=0)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
def _dl(pref): return glob.glob(r"C:/Users/anank/Downloads/" + pref + "*.jpg")[0]

OUT = pathlib.Path(r"D:/Преза лекций/decks/glava8-transport.html")

# ---------------------------------------------------------------- SVG helpers
def arrow(x1, y1, x2, y2, col, step, label="", w=1000, half=False, k=None, lcls=""):
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    if half:
        x2, y2 = x1 + dx * .5, y1 + dy * .5
    ex, ey = (x2 - ux * 12, y2 - uy * 12) if not half else (x2, y2)
    nx, ny = -uy, ux
    bx, by = x2 - ux * 22, y2 - uy * 22
    head = "" if half else (f'<polygon class="head" points="{x2:.1f},{y2:.1f} {bx+nx*9:.1f},{by+ny*9:.1f} {bx-nx*9:.1f},{by-ny*9:.1f}"/>')
    kat = f' data-k="{k}"' if k else ""
    lab = ""
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ox, oy = (nx, ny) if ny < 0 else (-nx, -ny)
        ang = math.degrees(math.atan2(dy, dx))
        if dx < 0: ang += 180
        lx, ly = mx + ox * 16, my + oy * 16
        lab = f'<text class="lbl {lcls}" x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" transform="rotate({ang:.1f} {lx:.1f} {ly:.1f})">{label}</text>'
    return (f'<g class="arr {col}" data-s="{step}" data-w="{w}"{kat}>'
            f'<path class="draw" pathLength="1" d="M{x1} {y1}L{ex:.1f} {ey:.1f}"/>{head}{lab}</g>')

XA, XB = 150, 610

def lifelines(a, b, H, fade=None, kd=0):
    kat = f' data-k="{fade}" style="--kd:{kd}ms"' if fade else ""
    s = f'<g class="life"{kat}>'
    for x, t in ((XA, a), (XB, b)):
        s += (f'<line class="ll" x1="{x}" y1="74" x2="{x}" y2="{H-14}"/>'
              f'<rect class="node" x="{x-95}" y="16" width="190" height="58" rx="14"/>'
              f'<text class="nodet" x="{x}" y="53" text-anchor="middle">{t}</text>')
    return s + "</g>"

def seqsvg(H, a, b, body, fade=None, kd=0):
    return (f'<svg class="dg" viewBox="0 0 760 {H}" role="img">'
            + lifelines(a, b, H, fade, kd) + body + "</svg>")

def A2B(y1, y2, col, step, label, **kw): return arrow(XA, y1, XB, y2, col, step, label, **kw)
def B2A(y1, y2, col, step, label, **kw): return arrow(XB, y1, XA, y2, col, step, label, **kw)

def plate(cx, y, text, step, cls="plate", w=380, extra=""):
    return (f'<g data-s="{step}" {extra}><rect class="{cls}" x="{cx-w/2}" y="{y}" width="{w}" height="54" rx="14"/>'
            f'<text class="{cls}t" x="{cx}" y="{y+35}" text-anchor="middle">{text}</text></g>')

# ---------------------------------------------------------------- diagrams
HAND = seqsvg(500, "Узел А", "Узел Б",
    A2B(110, 180, "c-ind", 1, '<tspan class="b">SYN</tspan>')
  + B2A(210, 280, "c-blue", 2, '<tspan class="b">SYN + ACK</tspan>')
  + A2B(310, 380, "c-ind", 3, '<tspan class="b">ACK</tspan>')
  + plate(380, 420, "TCP-соединение установлено", 4, "okp", 420, 'data-w="900"'))

HANDSEQ = seqsvg(500, "ПК1", "ПК2",
    A2B(110, 180, "c-ind", 1, '<tspan class="b">SYN</tspan>   Seq = a   Ack = 0', lcls="mono")
  + B2A(210, 280, "c-blue", 2, '<tspan class="b">SYN, ACK</tspan>   Seq = b   Ack = a+1', lcls="mono")
  + A2B(310, 380, "c-ind", 3, '<tspan class="b">ACK</tspan>   Seq = a+1   Ack = b+1', lcls="mono")
  + plate(380, 420, "TCP-соединение установлено", 4, "okp", 420, 'data-w="900"'))

FIN = seqsvg(540, "Узел А", "Узел Б",
    A2B(110, 170, "c-vio", 1, '<tspan class="b">FIN</tspan>')
  + B2A(200, 260, "c-blue", 2, '<tspan class="b">ACK</tspan>')
  + B2A(290, 350, "c-vio", 3, '<tspan class="b">FIN</tspan>')
  + A2B(380, 440, "c-ind", 4, '<tspan class="b">ACK</tspan>', w=1900),
  fade=4, kd=900)

WIN = seqsvg(600, "Узел А", "Узел Б",
    '<g data-s="1" data-w="700"><path class="brk" d="M112 100 H100 V236 H112"/>'
    '<text class="brkt" x="84" y="168" text-anchor="middle" transform="rotate(-90 84 168)">окно 3000 байт</text></g>'
  + A2B(100, 160, "c-ind", 2, "1500 байт", lcls="mono")
  + A2B(176, 236, "c-ind", 3, "1500 байт", lcls="mono")
  + '<g data-s="4" data-w="1100"><line class="waitl" x1="150" y1="236" x2="150" y2="330"/>'
    '<text class="waitt" x="170" y="292">ожидание подтверждения</text></g>'
  + B2A(262, 330, "c-blue", 5, '<tspan class="b">ACK</tspan>   3001', lcls="mono")
  + A2B(380, 440, "c-ind", 6, "1500 байт", lcls="mono")
  + A2B(456, 516, "c-ind", 6, "1500 байт", lcls="mono"))

LOSS = seqsvg(600, "Отправитель", "Получатель",
    A2B(100, 160, "c-ind", 1, "1–3000", lcls="mono")
  + A2B(180, 240, "c-ind", 2, "3001–6000", half=True, k=4, lcls="mono")
  + A2B(260, 320, "c-ind", 3, "6001–9000", lcls="mono")
  + '<g data-s="4" data-w="900"><path class="xmark" d="M366 196 l28 28 M394 196 l-28 28"/>'
    '<text class="lostt" x="420" y="218">потерян</text></g>'
  + B2A(350, 410, "c-blue", 5, '<tspan class="b">ACK</tspan> = 3001', lcls="mono")
  + A2B(440, 500, "c-ind", 6, "повтор 3001–6000", lcls="mono"))

def roll():
    t = "".join(f'<text x="0" y="{i*34}" text-anchor="middle">a+{i+1}</text>' for i in range(12))
    return t

SEQN = (f'<svg class="dg" viewBox="0 0 760 520" role="img">' + lifelines("ПК1", "ПК2", 520)
  + '<defs><clipPath id="rc"><rect x="-64" y="-26" width="128" height="36"/></clipPath></defs>'
  + '<g data-s="1" data-w="700"><g class="mv lin" data-m="2" data-w="1700" style="--dx:460px;--md:1400ms">'
    '<g transform="translate(150 150)"><rect class="segb" x="-78" y="-62" width="156" height="92" rx="12"/>'
    '<rect class="segh" x="-78" y="-62" width="156" height="26" rx="12"/><rect class="segh" x="-78" y="-46" width="156" height="10"/>'
    '<text class="segl" x="0" y="-43" text-anchor="middle">байт</text>'
    '<g clip-path="url(#rc)"><g class="roll" data-m="2">' + roll() + '</g></g></g></g></g>'
  + B2A(250, 320, "c-blue", 3, '<tspan class="b">ACK</tspan>   Ack = a+1+12', lcls="mono")
  + '<g data-s="4"><g transform="translate(150 400)"><rect class="segb" x="-110" y="-34" width="220" height="68" rx="12"/>'
    '<text class="mono segn" x="0" y="8" text-anchor="middle">Seq = a+1+12</text></g></g>'
  + "</svg>")

def segblk(i):
    x = 40 + i * 82
    dx = 500 + i * 36
    return (f'<g data-s="2"><g class="mv" data-m="3" style="--dx:{dx}px;--dl:{i*80}ms;--md:800ms">'
            f'<rect class="segb" x="{x}" y="100" width="74" height="120" rx="10"/>'
            f'<rect class="segh" x="{x}" y="100" width="74" height="28" rx="10"/><rect class="segh" x="{x}" y="116" width="74" height="12"/>'
            f'<text class="segl" x="{x+37}" y="120" text-anchor="middle">заг.</text>'
            f'<text class="mono segn" x="{x+37}" y="170" text-anchor="middle">1460</text>'
            f'<text class="segs" x="{x+37}" y="196" text-anchor="middle">байт</text></g></g>')

SEGM = ('<svg class="dg" viewBox="0 0 1000 320" role="img">'
  '<g class="fd" data-s="1" data-k="2" data-w="700"><rect class="file" x="30" y="90" width="330" height="140" rx="14"/>'
  '<text class="filet" x="195" y="150" text-anchor="middle">Файл</text>'
  '<text class="mono filen" x="195" y="192" text-anchor="middle">300 КБ</text></g>'
  + "".join(segblk(i) for i in range(4))
  + '<text class="dgc" data-s="3" x="740" y="70" text-anchor="middle" style="--dl:500ms">сегменты по 1460 байт</text>'
  + '<text class="mono dgbig" data-s="4" x="500" y="296" text-anchor="middle">300 КБ   =   206 фрагментов</text>'
  + '</svg>')

def muxribbon():
    cols = ["c-ind", "c-blue", "c-vio"]
    s = '<g data-s="5" data-w="1500">'
    for i in range(9):
        dx = 120 + i * 44
        s += (f'<g class="mv {cols[i%3]}" data-m="5" style="--dx:{dx}px;--dl:{(8-i)*110}ms;--md:900ms">'
              f'<rect class="rseg" x="490" y="180" width="38" height="40" rx="6"/></g>')
    return s + '</g>'

MUX = ('<svg class="dg" viewBox="0 0 1000 400" role="img">'
  + "".join(
      f'<g data-s="{i+1}"><rect class="src {c}" x="20" y="{y}" width="180" height="60" rx="12"/>'
      f'<text class="srct" x="110" y="{y+38}" text-anchor="middle">Приложение {i+1}</text></g>'
      f'<g class="arr {c}" data-s="{i+1}" data-w="800"><path class="draw" pathLength="1" d="{d}"/></g>'
      for i, (y, c, d) in enumerate([
          (40, "c-ind", "M200 70 C330 70 360 180 470 185"),
          (170, "c-blue", "M200 200 C330 200 360 200 470 200"),
          (300, "c-vio", "M200 330 C330 330 360 220 470 215")]))
  + '<g data-s="5" style="--dl:200ms"><line class="track" x1="580" y1="236" x2="990" y2="236"/>'
    '<text class="dgc" x="785" y="280" text-anchor="middle">один канал передачи</text></g>'
  + muxribbon()
  + '<g data-s="4"><rect class="muxb" x="470" y="140" width="110" height="120" rx="14"/>'
    '<text class="muxt" x="525" y="208" text-anchor="middle">MUX</text></g>'
  + '</svg>')

SOCK = ('<svg class="dg" viewBox="0 0 760 300" role="img">'
  '<g data-s="1"><rect class="addr" x="10" y="120" width="260" height="92" rx="14"/>'
  '<text class="addrk" x="140" y="154" text-anchor="middle">источник</text>'
  '<text class="mono addrv" x="140" y="190" text-anchor="middle">IP-адрес:54824</text></g>'
  '<g data-s="2"><rect class="addr" x="490" y="120" width="260" height="92" rx="14"/>'
  '<text class="addrk" x="620" y="154" text-anchor="middle">назначение</text>'
  '<text class="mono addrv" x="620" y="190" text-anchor="middle">IP-адрес:443</text></g>'
  + arrow(270, 166, 490, 166, "c-ind", 3, "", w=900)
  + '<g data-s="4"><rect class="pairb" x="300" y="60" width="160" height="46" rx="12"/>'
    '<text class="pairt" x="380" y="90" text-anchor="middle">сокет-пара</text></g>'
  + '</svg>')

def reseg(n, slot, target, step=1):
    x = 90 + slot * 210
    dx = (target - slot) * 210
    return (f'<g data-s="{step}" style="--dl:{(n-1)*120}ms"><g class="mv" data-m="4" data-w="1200" style="--dx:{dx}px;--md:900ms">'
            f'<rect class="segb" x="{x}" y="140" width="160" height="96" rx="12"/>'
            f'<text class="srct" x="{x+80}" y="178" text-anchor="middle">сегмент {n}</text>'
            f'<text class="mono segn" x="{x+80}" y="214" text-anchor="middle">№ {n}</text></g></g>')

REORD = ('<svg class="dg" viewBox="0 0 760 330" role="img">'
  '<rect class="frame" x="40" y="70" width="680" height="220" rx="14"/>'
  '<text class="framet" x="60" y="104">узел назначения</text>'
  + reseg(2, 0, 1) + reseg(3, 1, 2) + reseg(1, 2, 0)
  + '<g data-s="2"><rect class="pairb" x="540" y="18" width="180" height="42" rx="12"/>'
    '<text class="pairt mono" x="630" y="46" text-anchor="middle">ISN</text></g>'
  + '</svg>')

def dgram(i):
    x = 180 + i * 64
    k = ' data-k="3"' if i == 2 else ""
    return (f'<g class="mv" data-m="2" data-w="1300" style="--dx:360px;--dl:{(4-i)*90}ms;--md:1000ms">'
            f'<g class="dgm"{k}><rect class="rseg" x="{x}" y="96" width="52" height="46" rx="8"/></g></g>')

UDPS = ('<svg class="dg c-ind" viewBox="0 0 1000 230" role="img">'
  '<rect class="node" x="10" y="90" width="150" height="58" rx="14"/><text class="nodet" x="85" y="127" text-anchor="middle">Узел А</text>'
  '<rect class="node" x="840" y="90" width="150" height="58" rx="14"/><text class="nodet" x="915" y="127" text-anchor="middle">Узел Б</text>'
  '<line class="track" x1="160" y1="170" x2="840" y2="170"/>'
  '<g data-s="1">' + "".join(dgram(i) for i in range(5)) + '</g>'
  '<text class="lostt" data-s="3" x="500" y="214" text-anchor="middle">потерянная датаграмма повторно не отправляется</text>'
  '</svg>')

# ------------------------------------------------- большие схемы «как на фото»
def harr(x1, x2, y, col, step, w=900):
    d = 1 if x2 > x1 else -1
    ex = x2 - d * 14
    head = f'<polygon class="head" points="{x2},{y} {x2-d*22},{y-9} {x2-d*22},{y+9}"/>'
    return (f'<g class="arr {col}" data-s="{step}" data-w="{w}">'
            f'<path class="draw" pathLength="1" d="M{x1} {y}L{ex} {y}"/>{head}</g>')

def ftxt(parts, y, step, dl=0):
    s = f'<g data-s="{step}" style="--dl:{dl}ms">'
    for x, t, c in parts:
        s += f'<text class="{c}" x="{x}" y="{y}">{t}</text>'
    return s + "</g>"

def bdg(cx, cy, n, step=None, r=20, col="bdgc", fs=20):
    a = f' data-s="{step}"' if step else ""
    return (f'<g{a}><circle class="{col}" cx="{cx}" cy="{cy}" r="{r}"/>'
            f'<text class="bdgt" x="{cx}" y="{cy+fs*0.35:.0f}" text-anchor="middle" style="font-size:{fs}px">{n}</text></g>')

def monitor(cx, y):
    return (f'<g><rect class="mon" x="{cx-54}" y="{y}" width="108" height="72" rx="9"/>'
            f'<rect class="monsc" x="{cx-44}" y="{y+10}" width="88" height="46" rx="5"/>'
            f'<rect class="mon" x="{cx-17}" y="{y+72}" width="34" height="13"/>'
            f'<rect class="mon" x="{cx-36}" y="{y+85}" width="72" height="10" rx="5"/></g>')

# ---- Слайд «Установление TCP-соединения и передача данных» (схема из ЛК)
STAGES = [(["ТРЁХСТОРОННЕЕ", "КВИТИРОВАНИЕ"], ["Установка", "соединения"]),
          (["ПЕРЕДАЧА", "ДАННЫХ"], ["Отправка сегментов", "с данными"]),
          (["ДАННЫЕ", "ПОЛУЧЕНЫ"], ["Сегменты приняты", "и помещены в буфер"]),
          (["ПОДТВЕРЖДЕНИЕ", "ПОЛУЧЕНИЯ"], ["Отправка ACK", "(подтверждения)"]),
          (["ПРОДОЛЖЕНИЕ", "ПЕРЕДАЧИ"], ["Дальнейшая передача", "данных"])]

def stage_g(i, step):
    y = 232 + i * 128
    t, s = STAGES[i]
    g = f'<g data-s="{step}"><rect class="stagec" x="272" y="{y}" width="230" height="115" rx="14"/>'
    g += f'<text class="stagt" x="292" y="{y+32}">{t[0]}</text><text class="stagt" x="292" y="{y+54}">{t[1]}</text>'
    g += f'<text class="stags" x="292" y="{y+80}">{s[0]}</text><text class="stags" x="292" y="{y+100}">{s[1]}</text></g>'
    g += bdg(252, y + 26, i + 1, step, 19, "bdgc", 19)
    return g

def bcells(y, filled, step, dl=0):
    g = f'<g data-s="{step}" style="--dl:{dl}ms">'
    for i in range(3):
        cls = "cellf" if i < filled else "celle"
        g += f'<rect class="{cls}" x="{1320+i*90}" y="{y}" width="74" height="54" rx="8"/>'
    return g + "</g>"

def bracket(y1, y2, step):
    return f'<g data-s="{step}"><path class="brc" d="M548 {y1} H528 V{y2} H548"/></g>'

XP1, XP2 = 580, 1180
TCPFLOW = ('<svg class="dg" viewBox="0 0 1660 900" role="img" aria-label="Установление TCP-соединения и передача данных">'
  '<g data-s="1">'
  f'<text class="nname" x="{XP1}" y="46" text-anchor="middle">ПК1</text>'
  f'<text class="nsub" x="{XP1}" y="74" text-anchor="middle">(отправитель)</text>' + monitor(XP1, 92) +
  f'<text class="nname" x="{XP2}" y="46" text-anchor="middle">ПК2</text>'
  f'<text class="nsub" x="{XP2}" y="74" text-anchor="middle">(получатель)</text>' + monitor(XP2, 92) +
  f'<line class="ll" x1="{XP1}" y1="200" x2="{XP1}" y2="872"/><line class="ll" x1="{XP2}" y1="200" x2="{XP2}" y2="872"/>'
  '<line class="spine" x1="252" y1="232" x2="252" y2="859"/>'
  '<rect class="qcard" x="20" y="232" width="200" height="380" rx="16"/>'
  '<text class="stagt" x="120" y="282" text-anchor="middle">ДАННЫЕ ДЛЯ</text>'
  '<text class="stagt" x="120" y="306" text-anchor="middle">ОТПРАВКИ</text>'
  + "".join(f'<rect class="sheet" x="{46+i*12}" y="{348+i*14}" width="104" height="132" rx="8"/>' for i in range(4))
  + '<rect class="qcard" x="1300" y="220" width="320" height="150" rx="16"/>'
    '<text class="stagt" x="1460" y="266" text-anchor="middle">БУФЕР ПОЛУЧАТЕЛЯ</text>'
  + "".join(f'<rect class="celle" x="{1320+i*90}" y="290" width="74" height="54" rx="8"/>' for i in range(3))
  + '</g>'
  + stage_g(0, 2) + bracket(250, 446, 2)
  + harr(595, 1165, 268, "c-ind", 3) + ftxt([(620, "seq=100", "fl"), (780, "win=3", "fv"), (910, "flags=SYN", "fl")], 252, 3)
  + harr(1165, 595, 348, "c-blue", 4) + ftxt([(595, "seq=200", "fl"), (745, "Ack=101", "fa"), (895, "win=3", "fv"), (995, "flags=SYN, ACK", "fl")], 332, 4)
  + harr(595, 1165, 428, "c-ind", 5) + ftxt([(620, "seq=101", "fl"), (770, "Ack=201", "fa"), (920, "win=3", "fv"), (1020, "flags=ACK", "fl")], 412, 5)
  + stage_g(1, 6) + bracket(500, 676, 6)
  + harr(595, 1165, 520, "c-ind", 7) + ftxt([(620, "seq=101", "fl"), (780, "win=3", "fv")], 504, 7) + bcells(430, 1, 7, 500)
  + harr(595, 1165, 588, "c-ind", 8) + ftxt([(620, "seq=102", "fl"), (780, "win=3", "fv")], 572, 8) + bcells(498, 2, 8, 500)
  + harr(595, 1165, 656, "c-ind", 9) + ftxt([(620, "seq=103", "fl"), (780, "win=3", "fv")], 640, 9) + bcells(566, 3, 9, 500)
  + stage_g(2, 9) + bdg(1600, 498, 3, 9, 22, "bdgb", 22)
  + stage_g(3, 10) + bracket(720, 838, 10)
  + harr(1165, 595, 740, "c-blue", 10) + ftxt([(810, "Ack=104", "fa"), (950, "win=1", "fv"), (1050, "ctl=ACK", "fl")], 724, 10)
  + '<g data-s="10" style="--dl:500ms"><rect class="celle" x="1320" y="650" width="74" height="54" rx="8"/>'
    '<rect class="cellf" x="1410" y="650" width="74" height="54" rx="8"/>'
    '<rect class="celle" x="1500" y="650" width="74" height="54" rx="8"/></g>'
  + bdg(1600, 677, 4, 10, 22, "bdgb", 22)
  + stage_g(4, 11)
  + harr(595, 1165, 818, "c-ind", 11) + ftxt([(620, "seq=104", "fl"), (780, "win=3", "fv")], 802, 11)
  + '<g data-s="12"><rect class="qcard" x="1300" y="720" width="320" height="160" rx="16"/>'
  + bdg(1336, 758, "?", None, 20, "bdgc", 22)
  + '<text class="stagt" x="1368" y="766">ВОПРОС</text>'
  + '<text class="qline" x="1318" y="802">Почему значение поля</text>'
    '<text class="qline" x="1318" y="824">подтверждения (Ack) в сегменте,</text>'
    '<text class="qline" x="1318" y="846">отправленном узлом А,</text>'
    '<text class="qline" x="1318" y="868">не увеличивается?</text></g>'
  + '</svg>')

TCPFLOW_LEG = ('<div class="dleg">'
  '<span><b class="mono">seq</b> — порядковый номер <i>(sequence number)</i></span>'
  '<span><b class="mono fa2">Ack</b> — номер подтверждения <i>(acknowledgment number)</i></span>'
  '<span><b class="mono fv2">win</b> — размер окна <i>(window size)</i></span>'
  '<span><b class="mono">flags</b> — управляющие флаги</span>'
  '<span><b class="mono">ctl</b> — управляющее поле</span></div>')

# ---- Слайд «Выключение TCP — четырёхстороннее квитирование» (схема из ЛК)
def dashline(x1, x2, y, step):
    d = 1 if x2 > x1 else -1
    return (f'<g data-s="{step}" style="--dl:200ms"><path class="dash" d="M{x1+d*16} {y}H{x2-d*16}"/>'
            f'<polygon class="dhead" points="{x1},{y} {x1+d*16},{y-8} {x1+d*16},{y+8}"/>'
            f'<polygon class="dhead" points="{x2},{y} {x2-d*16},{y-8} {x2-d*16},{y+8}"/></g>')

def fnode(x, name, ip):
    cx = x + 125
    return (f'<g data-s="1"><rect class="qcard" x="{x}" y="30" width="250" height="290" rx="16"/>'
            f'<rect class="chipr" x="{cx-85}" y="50" width="170" height="46" rx="12"/>'
            f'<text class="chipt" x="{cx}" y="81" text-anchor="middle">{name}</text>'
            + monitor(cx, 120) +
            f'<rect class="ipb" x="{cx-100}" y="252" width="200" height="46" rx="11"/>'
            f'<text class="ipt" x="{cx}" y="282" text-anchor="middle">{ip}</text></g>')

FINROWS = [
    (1, "c-ind", 1, "Seq = 101   Ack = 301", "(флаг: FIN)",
     ["Узел А отправляет", "запрос на выключение", "соединения (FIN)."],
     ["Узел В получает", "запрос и отвечает", "подтверждением (ACK)."]),
    (2, "c-cr", -1, "Seq = 301   Ack = 102", "(флаг: ACK)",
     ["Узел А получает", "подтверждение (ACK)", "от узла В."],
     ["Узел В отправляет", "подтверждение (ACK)", "для узла А."]),
    (3, "c-cr", -1, "Seq = 302   Ack = 102", "(флаг: FIN)",
     ["Узел А получает", "запрос на выключение", "соединения (FIN)."],
     ["Узел В отправляет", "запрос на выключение", "соединения (FIN)."]),
    (4, "c-ind", 1, "Seq = 102   Ack = 303", "(флаг: ACK)",
     ["Узел А отправляет", "подтверждение (ACK)", "для узла В."],
     ["Узел В получает ACK.", "TCP-соединение", "выключено."]),
]

def finrow(i, step):
    n, col, dr, hdr, flg, lt, rt = FINROWS[i]
    yc = 380 + i * 120
    top = yc - 50
    g = f'<g data-s="{step}"><rect class="hplate {col}" x="560" y="{top}" width="340" height="100" rx="12"/>'
    g += f'<path class="hbar {col}" d="M572 {top} H888 a12 12 0 0 1 12 12 V{top+28} H560 V{top+12} a12 12 0 0 1 12 -12 z"/>'
    g += f'<text class="hbart" x="730" y="{top+20}" text-anchor="middle">TCP-заголовок</text>'
    g += f'<text class="hseq" x="730" y="{top+62}" text-anchor="middle">{hdr}</text>'
    g += f'<text class="hflg" x="730" y="{top+88}" text-anchor="middle">{flg}</text></g>'
    if dr > 0:
        g += harr(330, 545, yc, col, step) + harr(915, 1060, yc, col, step)
    else:
        g += harr(545, 330, yc, col, step) + harr(1060, 915, yc, col, step)
    bc = "bdgc" if col == "c-ind" else "bdgr"
    g += bdg(40, yc - 34, n, step, 18, bc, 18)
    g += f'<g data-s="{step}">' + "".join(
        f'<text class="rowt" x="74" y="{yc-28+k*23}">{t}</text>' for k, t in enumerate(lt)) + '</g>'
    g += bdg(1090, yc - 34, n, step + 1, 18, bc, 18)
    g += f'<g data-s="{step+1}">' + "".join(
        f'<text class="rowt" x="1124" y="{yc-28+k*23}">{t}</text>' for k, t in enumerate(rt)) + '</g>'
    return g

FINFLOW = ('<svg class="dg" viewBox="0 0 1660 880" role="img" aria-label="Выключение TCP: четырёхстороннее квитирование">'
  + fnode(30, "УЗЕЛ А", "IP: 1.1.1.1:1024") + fnode(1090, "УЗЕЛ В", "IP: 2.2.2.2:23")
  + '<g data-s="2"><rect class="statb" x="430" y="50" width="520" height="72" rx="14"/>'
  + bdg(478, 86, 1, None, 18, "bdgc", 18)
  + '<text class="statt" x="512" y="94">Установлено TCP-соединение</text></g>'
  + dashline(290, 420, 86, 2) + dashline(1080, 960, 86, 2)
  + '<g data-s="3"><rect class="statb" x="430" y="142" width="520" height="72" rx="14"/>'
  + bdg(478, 178, 2, None, 18, "bdgc", 18)
  + '<text class="statt" x="512" y="186">Обмен сегментами TCP</text></g>'
  + dashline(290, 420, 178, 3) + dashline(1080, 960, 178, 3)
  + "".join(finrow(i, 4 + i * 2) for i in range(4))
  + '<g data-s="1"><rect class="qcard" x="1370" y="120" width="260" height="420" rx="16"/>'
    '<text class="stagt" x="1500" y="168" text-anchor="middle">Обозначения</text>'
  + harr(1395, 1455, 215, "c-ind", 1, 400)
  + '<text class="legt" x="1470" y="222">Отправка от узла А</text>'
  + harr(1395, 1455, 275, "c-cr", 1, 400)
  + '<text class="legt" x="1470" y="282">Отправка от узла В</text>'
  + '<text class="legk fa2" x="1395" y="355">FIN</text>'
    '<text class="legt" x="1395" y="382">– запрос на выключение</text>'
    '<text class="legt" x="1395" y="404">соединения</text>'
    '<text class="legk fc2" x="1395" y="455">ACK</text>'
    '<text class="legt" x="1395" y="482">– подтверждение</text>'
    '<text class="legt" x="1395" y="504">получения</text></g>'
  + '<g data-s="12"><rect class="banner" x="30" y="790" width="1310" height="70" rx="14"/>'
  + bdg(84, 825, "!", None, 24, "bdgc", 26)
  + '<text class="bannert" x="132" y="835">TCP-соединение выключено после шага 4.</text></g>'
  + '</svg>')

def finchips():
    s = '<div class="hchips">'
    for i, (n, col, dr, hdr, flg, lt, rt) in enumerate(FINROWS):
        s += (f'<div class="hchip {col}" data-s="{5+i}"><span class="hct">TCP-заголовок</span>'
              f'<b class="mono">{hdr}</b><span class="hcf">{flg}</span>'
              f'<span class="hcd mono">{"А → В" if dr > 0 else "В → А"}</span></div>')
    return s + "</div>"

def stagecards():
    s = '<div class="stgs">'
    for i, (t, sub) in enumerate(STAGES):
        s += (f'<div class="stg" data-s="{6+i}"><span class="badge">{i+1}</span>'
              f'<div><b>{" ".join(t)}</b><span>{" ".join(sub)}</span></div></div>')
    return s + "</div>"

# ---- UDP: пример движения датаграмм (в стиле слайда про Seq/Ack)
UDPSEQ = seqsvg(520, "Узел А", "Узел Б",
    A2B(110, 165, "c-vio", 4, '<tspan class="b">датаграмма 1</tspan>   заголовок 8 байт', lcls="mono")
  + A2B(195, 250, "c-vio", 5, '<tspan class="b">датаграмма 2</tspan>', lcls="mono")
  + A2B(280, 335, "c-vio", 6, '<tspan class="b">датаграмма 3</tspan>', half=True, k=7, lcls="mono")
  + '<g data-s="7" data-w="900"><path class="xmark" d="M366 294 l28 28 M394 294 l-28 28"/>'
    '<text class="lostt" x="420" y="316">потеряна</text></g>'
  + A2B(365, 420, "c-vio", 8, '<tspan class="b">датаграмма 4</tspan>', lcls="mono")
  + plate(380, 440, "ACK не отправляется, повтора нет", 9, "okp", 470, 'data-w="900"'))

# ---------------------------------------------------------------- data
PORTS = [("HTTP", 80), ("SSH", 22), ("DNS", 53), ("POP3", 110), ("IMAP", 143), ("FTP (команды)", 21),
         ("FTP (передача)", 20), ("TFTP", 69), ("Telnet", 23), ("HTTPS", 443), ("NTP", 123),
         ("DHCP (клиент)", 67), ("DHCP (сервер)", 68), ("SMTP", 25)]

def ports_table(rows, step):
    tr = "".join(f'<tr><th>{s}</th><td class="mono">{p}</td></tr>' for s, p in rows)
    return f'<div class="tw card" data-s="{step}"><table class="tbl"><thead><tr><th>Сервис</th><th>Порт</th></tr></thead><tbody>{tr}</tbody></table></div>'

HDR = [  # (label, bits, span, tip)
    [("Порт источника", "16 бит", 16, "Порт источника и порт назначения (по 16 бит) определяют порты отправителя и получателя."),
     ("Порт назначения", "16 бит", 16, "Порт источника и порт назначения (по 16 бит) определяют порты отправителя и получателя.")],
    [("Порядковый номер", "32 бита", 32, "Порядковый номер (32 бита) в сегменте используется для контроля порядка сегментов.")],
    [("Номер подтверждения", "32 бита", 32, "Номер подтверждения (32 бита) необходим для подтверждения успешного получения узлом определенного сегмента.")],
    [("Длина заг.", "4 бита", 4, "Длина заголовка (смещение данных) (4 бита) – длина заголовка сегмента TCP в «словах», то есть в группах по 4 байта (32 бита)."),
     ("Резерв", "6 бит", 6, "Зарезервировано (6 бит) – это биты, которые могут быть использованы в будущем."),
     ("Флаги", "6 бит", 6, "Управляющие биты (6 бит) содержат флаги, определяющие назначение и функции сегмента TCP."),
     ("Размер окна", "16 бит", 16, "Размер окна (16 бит) указывает количество байт данных, которые получатель может принять в данный момент.")],
    [("Контрольная сумма", "16 бит", 16, "Контрольная сумма (16 бит) используется для проверки наличия ошибок в сегменте."),
     ("Срочность", "16 бит", 16, "Срочность (16 бит) определяет данные, которые должны быть переданы сразу.")],
]

def hdr_grid():
    s = '<div class="hdr">'
    for r, row in enumerate(HDR):
        s += f'<div class="hrow" data-s="{r+1}">'
        for lab, bits, span, tip in row:
            s += (f'<div class="fld" tabindex="0" style="grid-column:span {span}"><b>{lab}</b>'
                  f'<span class="mono">{bits}</span><span class="tip">{tip}</span></div>')
        s += '</div>'
    return s + '</div>'

FLAGS = [("SYN", "c-ind", "флаг синхронизации порядковых номеров. Когда флаг SYN установлен, в поле «порядковый номер» передается изначальный номер последовательности (Initial Sequence Number, ISN). Первый байт данных будет передан в следующем пакете с номером последовательности, равным ISN+1."),
         ("ACK", "c-blue", "флаг подтверждения. Данный флаг указывает на то, что в поле «номер подтверждения» указан следующий порядковый номер сегмента, который ожидается для получения на приемной стороне. Также, данный флаг подтверждает приём предыдущих сегментов."),
         ("FIN", "c-vio", "флаг завершения сеанса связи. Если такой флаг установлен, это означает, что отправитель сигнализирует о завершении передачи данных и не планирует отправлять какие-либо дополнительные данные в рамках текущего соединения."),
         ("RST", "c-cr", "флаг сброса соединения. Установка этого флага означает немедленный разрыв соединения и игнорирование всех последующих входящих данных из этого соединения."),
         ("PSH", "c-navy", "флаг функции push. Когда такой флаг установлен, это означает, что необходимо передать все данные из буфера памяти в обработку, даже если он не был заполнен. Протокол TCP использует буферизированную передачу данных как на отправке, так и на приеме. То есть, данные перед отправкой поступают в буфер, и при его заполнении отправляются по адресу. Такой метод позволяет снизить количество служебного трафика (заголовков) в сети."),
         ("URG", "c-dim", "флаг указателя важности. Установка данного флага означает, что данные в пакете необходимо обработать в приоритетном порядке.")]

def flag_slide(part):
    strip = '<div class="fstrip">' + "".join(
        f'<span class="fplate {c}" data-p="{(i-part*3)+1 if part*3<=i<part*3+3 else 0}">{n}</span>'
        for i, (n, c, _) in enumerate(FLAGS)) + '</div>'
    cards = '<div class="g3">' + "".join(
        f'<article class="card fcard {c}" data-s="{j+1}" data-w="900"><div class="ftag">{n}</div><p>{n} – {t}</p></article>'
        for j, (n, c, t) in enumerate(FLAGS[part*3:part*3+3])) + '</div>'
    return strip + cards

def steps(items, start=1, cls=""):
    return f'<ol class="steps {cls}">' + "".join(
        f'<li data-s="{start+i}"><span class="badge">{i+1}</span><div>{t}</div></li>' for i, t in enumerate(items)) + '</ol>'

def bullets(items, start=1):
    return '<ul class="bul">' + "".join(f'<li data-s="{start+i}">{t}</li>' for i, t in enumerate(items)) + '</ul>'

WS = [
    ("Первый этап", "SYN", "c-ind", [("Порт источника", "54824"), ("Порт назначения", "443"), ("Sequence Number", "0"),
      ("Sequence Number (raw)", "3638817700"), ("Next Sequence Number", "1"), ("Acknowledgment number", "0"), ("Флаги", "SYN"), ("Window", "64240")],
     "Клиент отправляет запрос на сервер, используя в качестве порта источника частный порт 54824, а в роли порта назначения – общеизвестный порт 443 (HTTPS). Ноль в Sequence Number обозначает порядковый номер относительно начала сессии; raw – настоящий, «сырой» номер."),
    ("Второй этап", "SYN, ACK", "c-blue", [("Порт источника", "443"), ("Порт назначения", "54824"), ("Sequence Number", "0"),
      ("Sequence Number (raw)", "1565342372"), ("Next Sequence Number", "1"), ("Acknowledgment number", "1"), ("Acknowledgment (raw)", "3638817701"), ("Window", "65160")],
     "В ответе роли портов меняются местами. Ack указан 1 и 3638817701, потому что +1 к начальному номеру последовательности. Размер окна изменился – механизм «скользящего окна»."),
    ("Третий этап", "ACK", "c-ind", [("Порт источника", "54824"), ("Порт назначения", "443"), ("Sequence Number", "1"),
      ("Sequence Number (raw)", "3638817701"), ("Acknowledgment number", "1"), ("Acknowledgment (raw)", "1565342373"), ("Флаги", "ACK"), ("Window", "502")],
     "Вновь порты поменялись местами, потому что это данные от клиента для сервера. Последовательность сменилась на единицу. Размер окна будет изменяться в зависимости от параметров сторон и загруженности сети."),
]

def ws_cards():
    s = '<div class="g3">'
    for i, (t, fl, c, rows, note) in enumerate(WS):
        kv = "".join(f'<div class="kv"><span>{k}</span><b class="mono">{v}</b></div>' for k, v in rows)
        s += (f'<article class="card wcard {c}" data-s="{i+1}" data-w="900"><div class="whead"><span class="badge">{i+1}</span>'
              f'<b>{t}</b><span class="ftag sm">{fl}</span></div>{kv}<p class="note">{note}</p></article>')
    return s + '</div>'

CMP = [("Гарантия доставки", "Является надежным протоколом транспортного уровня, гарантирует доставку сообщения до узла назначения", "Не обеспечивает надежную доставку сообщений"),
       ("Упорядоченная доставка", "Есть. Для того чтобы воссоздать исходный порядок сегментов, протокол TCP использует порядковые номера в заголовках каждого сегмента", "Нет. Протокол UDP не использует порядковые номера датаграмм, поэтому не восстанавливает их исходный порядок, а просто пересылает приложению"),
       ("Установка соединения", "Устанавливает соединение перед отправкой данных", "Не устанавливает соединение"),
       ("Повторная передача данных", "Повторная передача сегментов в случае потери", "Нет повторной передачи"),
       ("Скорость передачи", "Из-за дополнительных функций гарантии доставки имеет увеличенное время передачи данных", "Имеет высокую скорость передачи данных"),
       ("Сферы применения", "Передача сообщений электронной почты, HTML-страниц, FTP, SMTP, DNS", "TFTP, DHCP, VoIP, DNS")]

def cmp_table():
    rows = "".join(f'<tr data-s="{i+1}"><th>{a}</th><td>{b}</td><td>{c}</td></tr>' for i, (a, b, c) in enumerate(CMP))
    return f'<div class="tw card"><table class="tbl cmp"><thead><tr><th>Параметры</th><th>TCP</th><th>UDP</th></tr></thead><tbody>{rows}</tbody></table></div>'

QUIZ = [
    {"q": "В каком диапазоне лежат значения портов?", "o": ["0 – 1023", "0 – 65535", "1024 – 49151", "0 – 1460"], "a": 1,
     "e": "Порты представляют собой значения в диапазоне от 0 до 65535 и состоят из 16-битных чисел. 0 – 1023 – только известные порты."},
    {"q": "На сколько фрагментов будет разделён файл размером 300 килобайт?", "o": ["300", "1460", "206", "4"], "a": 2,
     "e": "Данные разбиваются на сегменты размером не более 1460 байт, поэтому файл 300 КБ делится на 206 фрагментов."},
    {"q": "Какой флаг установлен в первом сегменте трёхэтапного рукопожатия?", "o": ["ACK", "FIN", "SYN", "PSH"], "a": 2,
     "e": "Узел А, инициализирующий сессию, отправляет на узел Б запрос SYN. ACK появляется во втором и третьем сегментах."},
    {"q": "ПК1 отправил SYN с порядковым номером a. Чему равен номер подтверждения в ответе ПК2?", "o": ["0", "a", "a+1", "b+1"], "a": 2,
     "e": "Поскольку сегмент является ответом для ПК1, номер подтверждения равен a+1. b+1 – это номер подтверждения в третьем сегменте."},
    {"q": "Получены сегменты с номерами от 1 до 3000 и от 6001 до 9000. Каким будет номер ACK?", "o": ["9001", "3001", "6001", "3000"], "a": 1,
     "e": "Подтверждаются только данные, поступившие в непрерывной последовательности байт. Байты 3001–6000 не пришли, поэтому ACK = 3001."},
    {"q": "Сколько байт занимает заголовок UDP-датаграммы?", "o": ["8 байт", "20 байт", "16 байт", "32 байта"], "a": 0,
     "e": "Заголовок датаграммы состоит из 8 байт: порт источника, порт назначения, длина и контрольная сумма – по 16 бит."},
    {"q": "К какой группе относятся порты 49152 – 65535?", "o": ["Известные", "Зарегистрированные", "Динамические/частные", "Зарезервированные"], "a": 2,
     "e": "Динамические/частные порты присваиваются, когда пользователь производит инициализацию сеанса связи при подключении к определенному сервису."},
    {"q": "Какой флаг означает немедленный разрыв соединения?", "o": ["FIN", "RST", "URG", "SYN"], "a": 1,
     "e": "RST – флаг сброса соединения. FIN тоже завершает сеанс, но штатно: отправитель сообщает, что больше не будет передавать данные."},
]

# ---------------------------------------------------------------- slides
S = []
def slide(label, kick, title, body, cls=""):
    S.append((label, kick, title, body, cls))

slide("Титул", "", "", """
<div class="title">
  <div class="kick big">Глава 8</div>
  <h1>Транспортный уровень</h1>
  <p class="lead">Протоколы TCP и UDP: порты, сокеты, установка сеанса, надёжная и ускоренная передача данных</p>
  <div class="tchips"><span class="chip mono">TCP</span><span class="chip mono">UDP</span><span class="chip mono">0 – 65535</span></div>
  <p class="authors">Ананко Софья Михайловна<br>Качур Анна Юрьевна</p>
</div>""", "tslide")

slide("Цели главы", "Введение", "Цели данной главы", steps([
    "Протоколы, используемые на транспортном уровне;",
    "Функции и задачи данных протоколов;",
    "Установление сеанса и надежная передача данных с использованием протокола TCP;",
    "Ускоренная передача данных через протокол UDP."], cls="big"))

slide("Протоколы", "Введение", "Протоколы транспортного уровня", """
<div class="two">
  <p class="p lg">Основными протоколами транспортного уровня являются <b>TCP</b> и <b>UDP</b>. Они предназначены для передачи данных по сети, разделяя их на сегменты установленного размера. Более подробная информация о каждом протоколе будет представлена в рамках последующих тематических блоков.</p>
  <div class="pgrid">
    <div class="card proto c-ind" data-s="1"><span class="mono pn">TCP</span><span>надёжная доставка, установление сеанса</span></div>
    <div class="card proto c-vio" data-s="2"><span class="mono pn">UDP</span><span>ускоренная передача без подтверждений</span></div>
  </div>
</div>""")

OSI = ["Прикладной", "Представления", "Сеансовый", "Транспортный", "Сетевой", "Канальный", "Физический"]
slide("Функции уровня", "Введение", "Значение и функции транспортного уровня", """
<div class="two">
  <div>
    <p class="p" data-s="2">Транспортный уровень, являющийся <b>четвертым</b> уровнем в модели OSI, осуществляет передачу сегментов и выполняет роль посредника между уровнем приложений и нижними уровнями, которые используются сетевыми устройствами для передачи данных.</p>
    <p class="p" data-s="3">Транспортный уровень может поддерживать несколько одновременных сеансов связи, сформированных несколькими приложениями, при этом отслеживая каждый процесс отдельно.</p>
  </div>
  <div class="osi">""" + "".join(
    f'<div class="layer{" hl c-ind" if i==3 else ""}" data-s="1" style="--dl:{i*70}ms"{" data-p=\"2\"" if i==3 else ""}><span class="mono">{7-i}</span>{n}</div>'
    for i, n in enumerate(OSI)) + """</div>
</div>""")

slide("Сегментация", "Сегменты и потоки", "Сегментация TCP/UDP", """
<div class="two">
  <div>
    <p class="p">С целью передачи больших объемов данных существует <b>сегментация</b>. Суть сегментации состоит в разделении большого объема данных на меньшие фрагменты, которые затем снабжаются заголовками и передаются по сети. В большинстве случаев данные разбиваются на сегменты размером не превышающим <b class="mono">1460</b> байт. Например, при передаче файла размером <b class="mono">300</b> килобайт он будет разделен на <b class="mono">206</b> фрагментов, которые затем передадутся по сети.</p>
    <p class="p" data-s="5">Использование сегментации позволяет передавать большие объемы данных в средах передачи данных с ограниченной пропускной способностью. Кроме того, сегментация позволяет мультиплексировать данные из различных приложений через один канал передачи.</p>
  </div>
  <div class="card dgcard">""" + SEGM + """</div>
</div>""")

slide("Мультиплексирование", "Сегменты и потоки", "Мультиплексирование", """
<p class="p wide">Чтобы предотвратить заполнение всей полосы пропускания одним типом данных, что может привести к блокированию передачи другой информации, используется сегментация. С помощью <b>мультиплексирования</b> (чередования) сегментов существует возможность передачи большого количества различных данных в одной и той же сети.</p>
<div class="card dgcard wide2">""" + MUX + "</div>")

slide("Адресация", "Порты и сокеты", "Адресация транспортного уровня", """
<div class="two">
  <div>
    <p class="p">Идентификация приложений на транспортном уровне осуществляется с использованием портов.</p>
    <p class="p" data-s="1"><b>Порт</b> – это идентификатор приложения (протокола), которое обрабатывает текущий сегмент на устройстве отправителя и на устройстве получателя.</p>
    <p class="p" data-s="2">Порты являются дополнительным компонентом IP-адреса и представляют собой значения в диапазоне от <b class="mono">0</b> до <b class="mono">65535</b>. Они указываются в заголовке TCP/UDP и состоят из 16-битных чисел, отвечающих за порт источника и порт назначения соответственно.</p>
  </div>
  <div class="vstack">
    <p class="p" data-s="3">Номер порта представлен вместе с IP-адресом в следующем формате:</p>
    <div class="addrbig card" data-s="3"><span class="mono ip">192.168.1.19</span><span class="mono colon">:</span><span class="mono port">80</span></div>
    <div class="addrcap" data-s="4"><span class="c-ind">IP-адрес узла</span><span class="c-vio">порт приложения</span></div>
  </div>
</div>""")

slide("Известные порты", "Порты и сокеты", "Наиболее известные порты", '<div class="g2 ports">' + ports_table(PORTS[:7], 1) + ports_table(PORTS[7:], 2) + '</div>')

slide("Сокеты", "Порты и сокеты", "Сокеты и принцип адресации", """
<div class="two">
  <p class="p lg"><b>Сокет</b> – это сочетания IP-адреса источника с номером порта источника и IP-адреса назначения с номером порта назначения. Такая связка «IP-адрес:Порт» позволяет однозначно определить конечную точку доставки сообщения, потому что оно будет адресовано не просто какому-то устройству, а конкретному приложению на данном устройстве.</p>
  <div class="card dgcard">""" + SOCK + """</div>
</div>""")

slide("Группы портов", "Порты и сокеты", "Группы номеров портов", """
<p class="p wide">Всего существует три группы портов: общеизвестные, зарегистрированные и динамические/частные.</p>
<div class="g3">
  <article class="card pg c-ind" data-s="1"><div class="mono rng">0 – 1023</div><h3>Известные порты</h3><p>Общеизвестные порты зарезервированы для определенных служб и приложений. Они используется, например, веб-службами (HTTP - порт <b class="mono">80</b>) / почтовыми клиентами (POP3 - порт <b class="mono">110</b>).</p></article>
  <article class="card pg c-blue" data-s="2"><div class="mono rng">1024 – 49151</div><h3>Зарегистрированные порты</h3><p>Зарегистрированные порты регистрируется организацией IANA для каких-либо нестандартных служб, в основном, это службы, которыми пользуются не все пользователи, к примеру, RADIUS-сервер использует порт <b class="mono">1812</b> для аутентификации пользователей.</p></article>
  <article class="card pg c-vio" data-s="3"><div class="mono rng">49152 – 65535</div><h3>Динамические/частные порты</h3><p>Динамические/частные порты присваиваются, когда пользователь производит инициализацию сеанса связи при подключении к определенному сервису.</p></article>
</div>
<p class="src mono" data-s="4">iana.org/assignments/service-names-port-numbers</p>""")

slide("Протокол TCP", "Протокол TCP", "Протокол TCP", """
<p class="p wide">TCP - один из протоколов транспортного уровня. Его главное отличие - обеспечение <b>надежности</b> доставки данных.</p>
<div class="g2">
  <article class="card lst"><h3>Для осуществления гарантированной доставки протокол использует следующие функции:</h3>""" + steps([
    "Отслеживание количества сегментов, отправленных на определенный узел;",
    "Подтверждение получения данных;",
    "Если получение данных не подтвердилось, инициирование повторной передачи сегментов."]) + """</article>
  <article class="card lst"><h3>Основные задачи протокола TCP:</h3>""" + steps([
    "Доставка сегментов в одинаковом порядке;", "Установление сеанса связи;", "Регулирование потока передачи данных."], start=4) + """</article>
</div>""")

slide("Заголовок TCP", "Протокол TCP", "Заголовок TCP-сегмента", """
<p class="p wide">Поля заголовка по порядку, ширина строки – 32 бита. Наведите курсор на поле, чтобы увидеть его назначение.</p>
<div class="card hdrcard"><div class="ruler mono"><span>0</span><span>8</span><span>16</span><span>24</span><span>31</span></div>""" + hdr_grid() + """
<div class="hdata" data-s="5" style="--dl:250ms">Данные</div></div>""")

slide("Флаги 1", "Протокол TCP", "Флаги TCP: SYN, ACK, FIN", """
<p class="p wide">Для управления сеансом связи в заголовке протокола TCP используется поле длиной <b class="mono">6</b> бит. Данные биты называются флагами.</p>""" + flag_slide(0))
slide("Флаги 2", "Протокол TCP", "Флаги TCP: RST, PSH, URG", flag_slide(1))

slide("Рукопожатие", "Установка соединения", "Установка TCP-соединения", """
<div class="two">""" + steps([
    "Узел А, инициализирующий сессию для обмена данными «клиент-сервер», отправляет на узел Б запрос <b>SYN</b>;",
    "Узел Б подтверждает запрос на инициализацию сессии для обмена данными «клиент-сервер», отправляет узлу А ответ <b>ACK</b> и запрос <b>SYN</b> «сервер-клиент»;",
    "В конце узел А подтверждает запрос SYN «сервер-клиент» и отправляет <b>ACK</b> узлу Б."]) + """
  <div class="card dgcard">""" + HAND + """</div>
</div>""")

slide("Рукопожатие: номера", "Установка соединения", "Установка TCP-соединения: Seq и Ack", """
<div class="two">""" + steps([
    "Инициатор TCP-соединения (ПК1) отправляет первый TCP-сегмент с установленным флагом SYN. Начальный порядковый номер (<b class='mono'>a</b>) является случайно сгенерированным числом. Номер подтверждения равен <b class='mono'>0</b>, потому что ранее от ПК 2 не поступали сегменты.",
    "После получения корректного TCP-сегмента с флагом SYN получатель (ПК2) отвечает TCP-сегментом с установленными флагами SYN и ACK. Начальный порядковый номер (<b class='mono'>b</b>) является случайно сгенерированным числом. Поскольку сегмент является ответом для ПК1, номер подтверждения равен <b class='mono'>a+1</b>.",
    "После получения сегмента с флагами SYN и ACK ПК1 отвечает сегментом с флагом ACK, порядковый номер равен <b class='mono'>a+1</b>, а номер подтверждения – <b class='mono'>b+1</b>. После того, как ПК2 получает сегмент, устанавливается TCP-соединение."], cls="sm") + """
  <div class="card dgcard">""" + HANDSEQ + """</div>
</div>""")


slide("Wireshark", "Установка соединения", "Установка TCP-соединения в Wireshark", ws_cards())

HANDNUM = seqsvg(540, "ПК1", "ПК2",
    A2B(110, 175, "c-ind", 1, '<tspan class="b">SYN</tspan>   Seq = 5000', lcls="mono")
  + B2A(215, 280, "c-blue", 2, '<tspan class="b">SYN, ACK</tspan>   Seq = 9000   Ack = 5001', lcls="mono")
  + A2B(320, 385, "c-ind", 3, '<tspan class="b">ACK</tspan>   Seq = 5001   Ack = 9001', lcls="mono")
  + plate(380, 420, "Соединение установлено", 4, "okp", 400, 'data-w="900"')
  + '<g data-s="5"><text class="mono dgc" x="380" y="505" text-anchor="middle">'
    'первый байт данных ПК1 — 5001,   ПК2 — 9001</text></g>')

SEQDATA = seqsvg(620, "ПК1", "ПК2",
    A2B(110, 170, "c-ind", 1, 'Seq = a+1   Ack = b+1   12 байт', lcls="mono")
  + B2A(210, 270, "c-blue", 2, '<tspan class="b">ACK</tspan>   Seq = b+1   Ack = a+13   0 байт', lcls="mono")
  + A2B(310, 370, "c-ind", 3, 'Seq = a+13   Ack = b+1   66 байт', lcls="mono")
  + B2A(410, 470, "c-blue", 4, '<tspan class="b">ACK</tspan>   Seq = b+1   Ack = a+79   0 байт', lcls="mono")
  + '<g data-s="5"><text class="mono dgc" x="380" y="540" text-anchor="middle">'
    'сегмент 1: байты a+1 … a+12   →   следующий a+13</text>'
    '<text class="mono dgc" x="380" y="574" text-anchor="middle">'
    'сегмент 2: байты a+13 … a+78   →   следующий a+79</text></g>')

NUMEX = seqsvg(560, "ПК1", "ПК2",
    A2B(105, 160, "c-ind", 1, 'Seq = 1001   20 байт   →   1001 … 1020', lcls="mono")
  + B2A(200, 255, "c-blue", 2, '<tspan class="b">ACK</tspan>   Seq = 5001   Ack = 1021', lcls="mono")
  + A2B(295, 350, "c-ind", 3, 'Seq = 1021   50 байт   →   1021 … 1070', lcls="mono")
  + B2A(390, 445, "c-blue", 4, '<tspan class="b">ACK</tspan>   Seq = 5001   Ack = 1071', lcls="mono")
  + '<g data-s="5"><text class="mono dgc" x="380" y="512" text-anchor="middle">'
    'нумерация ПК1 → ПК2 и ПК2 → ПК1 ведётся независимо</text></g>')

def minitbl(step, head, rows, cls=""):
    th = "".join(f"<th>{h}</th>" for h in head)
    tb = "".join("<tr>" + "".join(f'<td class="mono">{c}</td>' for c in r) + "</tr>" for r in rows)
    return (f'<div class="tw card {cls}" data-s="{step}"><table class="tbl num">'
            f'<thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>')

slide("Рукопожатие: числа", "Установка соединения", "Трёхстороннее рукопожатие: как считаются Seq и Ack", """
<div class="two">
  <div>
    <p class="p sm">Перед передачей данных ПК1 и ПК2 устанавливают TCP-соединение. Процесс состоит из трёх сообщений: <b class="mono">SYN → SYN/ACK → ACK</b>.</p>
    <ol class="steps sm">
      <li data-s="1"><span class="badge">1</span><div><b>ПК1 отправляет SYN.</b> Источник <b class="mono">1.1.1.1:1024</b>, назначение <b class="mono">2.2.2.2:23</b>, <b class="mono">SYN = 1</b>, <b class="mono">Seq = a</b>, поле Ack пока не используется. Число <b class="mono">a</b> — начальный порядковый номер, выбранный ПК1.
        <span class="say">«Я хочу установить соединение. Мой начальный порядковый номер — a».</span></div></li>
      <li data-s="2"><span class="badge">2</span><div><b>ПК2 отвечает SYN/ACK.</b> <b class="mono">SYN = 1</b>, <b class="mono">ACK = 1</b>, <b class="mono">Seq = b</b>, <b class="mono">Ack = a + 1</b>. Число <b class="mono">b</b> — собственный начальный номер ПК2, а <b class="mono">Ack = a + 1</b> подтверждает получение SYN от ПК1.
        <span class="say">«Запрос получил. Ожидаю от тебя номер a + 1. Мой начальный номер — b».</span></div></li>
      <li data-s="3"><span class="badge">3</span><div><b>ПК1 отправляет ACK.</b> <b class="mono">ACK = 1</b>, <b class="mono">Seq = a + 1</b>, <b class="mono">Ack = b + 1</b>. После этого TCP-соединение установлено и стороны могут передавать данные.
        <span class="say">«Твой SYN получил. Ожидаю от тебя номер b + 1».</span></div></li>
    </ol>
    <p class="p sm callout" data-s="4"><b>Важно:</b> хотя SYN обычно не содержит пользовательских данных, он занимает один порядковый номер — поэтому подтверждается значением <b class="mono">a + 1</b>.</p>
  </div>
  <div class="vstack gap">
    <div class="card dgcard">""" + HANDNUM + """</div>
    <p class="p sm dimh" data-s="5">Числовой пример: ПК1 выбрал <b class="mono">Seq = 5000</b>, ПК2 — <b class="mono">Seq = 9000</b>.</p>""" +
    minitbl(5, ["Шаг", "Направление", "Флаги", "Seq", "Ack"],
            [["1", "ПК1 → ПК2", "SYN", "5000", "—"],
             ["2", "ПК2 → ПК1", "SYN, ACK", "9000", "5001"],
             ["3", "ПК1 → ПК2", "ACK", "5001", "9001"]]) + """
    <p class="p sm callout" data-s="6">Если ПК1 отправит <b class="mono">100</b> байт с <b class="mono">Seq = 5001</b>, они получат номера <b class="mono">5001 … 5100</b>. ПК2 подтвердит их так: <b class="mono">Ack = 5001 + 100 = 5101</b>.</p>
  </div>
</div>""")

slide("Передача: Seq и Ack", "Установка соединения", "Передача данных по TCP после установления соединения", """
<div class="two">
  <div>
    <p class="p sm">TCP обеспечивает надёжную и упорядоченную передачу благодаря двум полям: <b class="mono">Seq</b> — номер первого байта данных в сегменте, <b class="mono">Ack</b> — номер следующего байта, который получатель ожидает получить. Каждое направление соединения имеет собственную, независимую нумерацию.</p>
    <ol class="steps sm">
      <li data-s="1"><span class="badge">1</span><div><b>ПК1 отправляет первый сегмент:</b> <b class="mono">Seq = a + 1</b>, <b class="mono">Ack = b + 1</b>, полезная нагрузка — <b class="mono">12</b> байт. Байты получают номера <b class="mono">a+1, a+2, …, a+12</b>, поэтому следующий сегмент начнётся с <b class="mono">a + 1 + 12 = a + 13</b>.</div></li>
      <li data-s="2"><span class="badge">2</span><div><b>ПК2 подтверждает получение:</b> <b class="mono">Seq = b + 1</b>, <b class="mono">Ack = a + 13</b>, полезная нагрузка — <b class="mono">0</b> байт.
        <span class="say">«Байты до a + 12 включительно получены. Теперь ожидаю байт a + 13».</span></div></li>
      <li data-s="3"><span class="badge">3</span><div><b>ПК1 отправляет следующий сегмент:</b> <b class="mono">Seq = a + 13</b>, <b class="mono">Ack = b + 1</b>, полезная нагрузка — <b class="mono">66</b> байт. Сегмент содержит байты <b class="mono">a+13, a+14, …, a+78</b>, следующий ожидаемый байт — <b class="mono">a + 13 + 66 = a + 79</b>.</div></li>
      <li data-s="4"><span class="badge">4</span><div><b>ПК2 подтверждает второй сегмент:</b> <b class="mono">Seq = b + 1</b>, <b class="mono">Ack = a + 79</b>, полезная нагрузка — <b class="mono">0</b> байт.</div></li>
    </ol>
  </div>
  <div class="vstack gap">
    <div class="card dgcard">""" + SEQDATA + """</div>
    <p class="p sm callout warn" data-s="5"><b>Осторожно с исходной схемой:</b> значение <b class="mono">Ack = a + 12 + 66</b> ошибочно. Правильно <b class="mono">Ack = a + 13 + 66 = a + 79</b>. Это накопительное подтверждение: ПК2 получил все байты до <b class="mono">a + 78</b> включительно и теперь ожидает <b class="mono">a + 79</b>.</p>
    <div class="card qbox" data-s="6"><h3>Почему Seq у ПК2 не увеличивается?</h3>
      <p class="p sm">ПК2 отправляет только подтверждения без данных: и первое, и второе с <b class="mono">Seq = b + 1</b>. Пустой ACK не занимает место в пространстве порядковых номеров. Seq растёт на количество переданных <b>байт данных</b>; дополнительно по одному номеру расходуют только управляющие флаги <b class="mono">SYN</b> и <b class="mono">FIN</b>.</p></div>
  </div>
</div>""")

slide("Передача: числовой пример", "Установка соединения", "Передача данных: числовой пример", """
<div class="two">
  <div>
    <p class="p sm">Пусть после установления соединения следующий номер ПК1 — <b class="mono">Seq = 1001</b>, а следующий номер ПК2 — <b class="mono">Seq = 5001</b>.</p>
    <h3 data-s="1">Первый сегмент — ПК1 отправляет 20 байт</h3>""" +
    minitbl(1, ["Направление", "Seq", "Ack", "Данные"],
            [["ПК1 → ПК2", "1001", "5001", "20 байт"]]) + """
    <p class="p sm" data-s="2">Переданы байты <b class="mono">1001 … 1020</b>, поэтому ПК2 отвечает:</p>""" +
    minitbl(2, ["Направление", "Seq", "Ack", "Данные"],
            [["ПК2 → ПК1", "5001", "1021", "0 байт"]]) + """
    <p class="p sm dimh" data-s="2"><b class="mono">Ack = 1021</b> означает: «Получено всё до байта 1020, ожидаю байт 1021».</p>
    <h3 data-s="3">Второй сегмент — ПК1 отправляет ещё 50 байт</h3>""" +
    minitbl(3, ["Направление", "Seq", "Ack", "Данные"],
            [["ПК1 → ПК2", "1021", "5001", "50 байт"]]) + """
    <p class="p sm" data-s="4">Переданы байты <b class="mono">1021 … 1070</b>, ПК2 подтверждает:</p>""" +
    minitbl(4, ["Направление", "Seq", "Ack", "Данные"],
            [["ПК2 → ПК1", "5001", "1071", "0 байт"]]) + """
  </div>
  <div class="vstack gap">
    <div class="card dgcard">""" + NUMEX + """</div>
    <div class="formula card" data-s="5"><span class="mono">Ack = Seq + количество байт данных</span></div>
    <p class="p sm callout" data-s="6"><b>Главная идея:</b> <b class="mono">Seq</b> показывает номер первого передаваемого байта, а <b class="mono">Ack</b> — номер <b>следующего ожидаемого</b> байта, а не номер последнего полученного.</p>
  </div>
</div>""")

slide("Окно: принцип", "Надёжность TCP", "Подтверждение и размер окна", """<div class="two">""" + steps([
    "При трехстороннем квитировании в TCP-соединении обе стороны уведомляют друг друга о максимальном количестве байтов (размере буфера), которые могут быть получены локальной стороной с помощью поля <b>Окно</b>.",
    "После установления TCP-соединения отправитель отправляет данные указанного количества байтов на основе размера окна, заявленного получателем.",
    "После получения данных получатель хранит данные в буфере и ожидает получения буферизированных данных приложением верхнего уровня. После получения данных приложением верхнего уровня освобождается соответствующее пространство в буфере.",
    "Получатель сообщает текущий приемлемый размер данных (окна) в соответствии с его размером буфера.",
    "Отправитель отправляет определенный объем данных в зависимости от текущего размера окна получателя."], cls="sm") + """
  <div><p class="p sm dimh" data-s="6">Этапы, которые мы разберём на следующем слайде:</p>""" + stagecards() + """</div>
</div>""")

slide("Окно: пример", "Надёжность TCP", "Размер окна: пример передачи", """
<div class="two">
  <p class="p lg">Пример передачи данных при TCP-соединении с размером окна, равным <b class="mono">3000</b> байт, который был согласован в процессе установления TCP-соединения. После передачи получателю <b class="mono">3000</b> байт, последний уведомляет отправителя об успешном приеме сообщением с флагом <b>ACK</b>, и отправитель начинает передавать следующий блок данных.</p>
  <div class="card dgcard">""" + WIN + """</div>
</div>""")

slide("Потеря данных", "Надёжность TCP", "Потеря данных и повторная передача", """
<div class="two">
  <div>
    <p class="p">В любой, даже хорошо организованной сети, обычно возникают потери данных. Чтобы справиться с этой проблемой, протокол TCP имеет механизм <b>повторной передачи</b> сегментов.</p>
    <p class="p">При получении сегментов целевым узлом подтверждаются только те данные, которые поступили в непрерывной последовательности байт. Если после истечения таймаута узел-отправитель не получил подтверждение о доставке, он повторно отправляет сегменты, начиная с последнего полученного подтверждения (ACK).</p>
    <p class="p callout" data-s="5">К примеру, были получены сегменты с порядковыми номерами от <b class="mono">1</b> до <b class="mono">3000</b> и от <b class="mono">6001</b> до <b class="mono">9000</b>, то номер ACK будет равен <b class="mono">3001</b>.</p>
  </div>
  <div class="card dgcard">""" + LOSS + """</div>
</div>""")

slide("Завершение сеанса", "Надёжность TCP", "Завершение TCP-сеанса", """
<div class="two">""" + steps([
    "После завершения отправки данных, узел А отправляет сегмент с установленным в заголовке флагом <b>FIN</b> для прекращения сессии «клиент-сервер»;",
    "Узел Б принимает запрос на завершение соединения и отправляет подтверждение <b>ACK</b> узлу А;",
    "Узел Б отправляет сегмент с установленным в заголовке флагом <b>FIN</b> для прекращения сессии «сервер-клиент»;",
    "Узел А, в свою очередь, отправляет ответ <b>ACK</b> для подтверждения получения FIN от узла Б."]) + """
  <div class="card dgcard">""" + FIN + """</div>
</div>""")

slide("Завершение: детали", "Надёжность TCP", "Завершение TCP-сеанса: ПК1 и ПК2", """<div class="two">""" + steps([
    "ПК1 отправляет TCP-сегмент с установленным флагом <b>FIN</b>. Сегмент не содержит данных.",
    "После получения ПК1 сегмента TCP ПК2 отвечает сегментом TCP с установленным флагом <b>ACK</b>.",
    "ПК2 проверяет необходимость отправки данных. Если необходимо, ПК2 отправляет данные, а затем TCP-сегмент с флагом <b>FIN</b> для закрытия соединения. Если нет, ПК2 напрямую отправляет TCP-сегмент с установленным флагом FIN.",
    "После получения TCP-сегмента с установленным флагом FIN ПК1 отвечает сегментом с флагом <b>ACK</b>. Затем TCP-соединение разрывается в обоих направлениях."], cls="sm") + """
  <div><p class="p sm dimh" data-s="5">Seq и Ack на каждом шаге — подробнее на следующем слайде:</p>""" + finchips() + """</div>
</div>""")

slide("Управление потоком", "Надёжность TCP", "Установление TCP-соединения и управление потоком", """
<div class="two">
  <div>
    <p class="p sm" data-s="1">Данные при передаче по протоколу TCP делятся на сегменты, которые при выборе различных путей маршрутизации могут быть доставлены на узел назначения в измененном порядке. Для того чтобы воссоздать исходный порядок сегментов, протокол TCP использует порядковые номера в заголовках каждого сегмента.</p>
    <p class="p sm" data-s="2">При установлении сеанса связи задается начальный порядковый номер сеанса (<b>ISN</b>), представляющий собой случайное начальное значения счетчика байт, которые были переданы целевому узлу. При дальнейшей передаче сегментов указанное число увеличивается на определенное число байт, что позволяет контролировать передачу данных.</p>
    <p class="p sm" data-s="3">Стоит обратить внимание, что ISN не является строго определенным числом, а задается случайно. Таким образом, можно предотвратить осуществление вредоносных атак.</p>
    <p class="p sm" data-s="4">На узле назначения все полученные сегменты распределяются в правильном порядке и только после этого передаются на уровень приложений.</p>
  </div>
  <div class="card dgcard">""" + REORD + """</div>
</div>""")

slide("UDP: функции", "Протокол UDP", "Функции протокола UDP", """
<p class="p wide">Протокол UDP так же, как и TCP, использует сегментацию данных, при этом не задействует процессы, отвечающие за уведомление об успешном получении сегмента, что позволяет значительно быстрее передавать данные. Пользуясь преимуществом в скорости и отсутствием подтверждения полученной информации, протокол UDP используется при передаче данных которые могут перенести кратковременные потери во время передачи, например, потоковой видео и звуковой информации, где потеря одной или нескольких датаграмм, т.е. с незначительными перебоями, может не повлиять на общую ситуацию в целом во время передачи.</p>
<div class="two">
  <div class="card dgcard wide2">""" + UDPS + """</div>
  <div class="card dgcard">""" + UDPSEQ + """</div>
</div>""")

slide("UDP: датаграммы", "Протокол UDP", "Основные характеристики протокола UDP", """
<div class="two">
  <div>
    <p class="p">Основными характеристиками протокола UDP являются:</p>""" + bullets([
    "Отсутствие установления сеанса связи;", "Отсутствие повторной отправки потерянных сегментов;", "Наличие высокоскоростного потока."]) + """
    <p class="p" data-s="4"><b>Датаграмма</b> – блок информации, передающийся с помощью протокола UDP, без гарантированной доставки на узел назначения.</p>
  </div>
  <div class="vstack">
    <p class="p" data-s="5">Части сообщения в UDP, передающиеся без предварительного установления канала и последующей гарантии передачи, называются датаграммами. У датаграммы есть заголовок, состоящий из <b class="mono">8</b> байт:</p>
    <div class="card udph">
      <div class="uf" data-s="6"><b>Порт источника</b><span class="mono">16 бит</span></div>
      <div class="uf" data-s="6" style="--dl:100ms"><b>Порт назначения</b><span class="mono">16 бит</span></div>
      <div class="uf" data-s="7"><b>Длина</b><span class="mono">16 бит</span></div>
      <div class="uf" data-s="7" style="--dl:100ms"><b>Контрольная сумма</b><span class="mono">16 бит</span></div>
      <div class="uf ud" data-s="8">Данные</div>
    </div>
  </div>
</div>""")

slide("TCP и UDP", "Протокол UDP", "Сравнение функций протоколов TCP и UDP", cmp_table())

slide("Приложения UDP", "Протокол UDP", "Основные типы приложений, которые используют UDP", """
<div class="g3">
  <article class="card app" data-s="1"><div class="mono appn">TFTP</div><p>Приложения, которые могут самостоятельно гарантировать полную передачу данных. В таком случае, контроль правильности передачи данных осуществляется приложением 7-го уровня модели OSI, а не самим протоколом;</p></article>
  <article class="card app" data-s="2"><div class="mono appn">DHCP</div><p>Приложения, осуществляющие только отправку запросов и получение ответов;</p></article>
  <article class="card app" data-s="3"><div class="mono appn">VoIP</div><p>Приложения для передачи мультимедийного контента в режиме реального времени.</p></article>
</div>""")

slide("Тренажёр: порты", "Тренажёры", "Тренажёр: номера портов", """
<div class="two">
  <div class="card trn" id="tp">
    <div class="tq">Какой порт использует сервис <b class="mono" id="tp-s">HTTP</b>?</div>
    <div class="trow"><input id="tp-in" class="mono" inputmode="numeric" autocomplete="off" aria-label="Номер порта"><button class="btn pri" id="tp-ok">Проверить</button><button class="btn" id="tp-nx">Другой сервис</button></div>
    <div class="tres" id="tp-r" aria-live="polite"></div>
    <div class="tscore mono" id="tp-sc">0 / 0</div>
  </div>
  <div class="card trn">
    <div class="tq">К какой группе относится порт <b class="mono" id="tg-p">443</b>?</div>
    <div class="opts" id="tg-o"></div>
    <div class="tres" id="tg-r" aria-live="polite"></div>
    <button class="btn" id="tg-nx">Другой порт</button>
  </div>
</div>""")

slide("Тренажёр: Seq/Ack", "Тренажёры", "Тренажёр: порядковые номера", """
<div class="two">
  <div class="card trn">
    <div class="tq" id="ts-q"></div>
    <div class="trow"><input id="ts-in" class="mono" inputmode="numeric" autocomplete="off" aria-label="Ответ"><button class="btn pri" id="ts-ok">Проверить</button><button class="btn" id="ts-nx">Новая задача</button></div>
    <div class="tres" id="ts-r" aria-live="polite"></div>
    <div class="tscore mono" id="ts-sc">0 / 0</div>
  </div>
  <div class="card lst">
    <h3>Правило из лекции</h3>
    <p class="p sm">Порядковый номер + длина полезной нагрузки = порядковый номер первого байта следующего сегмента.</p>
    <p class="p sm">В рукопожатии: ответ на SYN с номером <b class="mono">a</b> содержит номер подтверждения <b class="mono">a+1</b>; третий сегмент – порядковый номер <b class="mono">a+1</b> и номер подтверждения <b class="mono">b+1</b>.</p>
    <p class="p sm">Подтверждаются только данные, поступившие в непрерывной последовательности байт.</p>
  </div>
</div>""")

slide("Проверь себя", "Итог", "Проверь себя", """
<div class="card quiz" id="quiz">
  <div class="qtop"><span class="mono" id="qz-n">1 / 8</span><span class="mono" id="qz-sc">верно: 0</span></div>
  <div class="tq" id="qz-q"></div>
  <div class="opts col" id="qz-o"></div>
  <div class="tres" id="qz-e" aria-live="polite"></div>
  <div class="trow"><button class="btn" id="qz-pv">Предыдущий</button><button class="btn pri" id="qz-nx">Следующий вопрос</button></div>
</div>""")

# ---------------------------------------------------------------- CSS / JS
CSS = r"""
:root{
  --paper:#f4f5fb;--card:#ffffff;--line:#dfe2f2;--tint:#eceefb;
  --navy:#111a52;--indigo:#2a2fd0;--blue:#1f56ff;--violet:#6b3ff0;--crimson:#d81b60;
  --ink:#1b2150;--dim:#5a6288;--ok:#1d8a5b;
  --f:"Golos Text","Inter","Manrope","Segoe UI",system-ui,sans-serif;
  --mono:"JetBrains Mono","Cascadia Mono","Consolas","Roboto Mono",ui-monospace,monospace;
  --r:14px;--sh:0 1px 2px rgba(17,26,82,.05),0 8px 24px rgba(17,26,82,.07);
  --ez:cubic-bezier(.22,.7,.3,1);--sp:1;
  color-scheme:light;
}
*{box-sizing:border-box;margin:0;padding:0}
html{font-size:clamp(14px,min(1.02vw,1.86vh),28px)}
html,body{height:100%;overflow:hidden;background:var(--paper);color:var(--ink);font-family:var(--f)}
body::before,body::after{content:"";position:fixed;z-index:0;width:clamp(56px,8vw,190px);aspect-ratio:1;pointer-events:none;
  background:repeating-linear-gradient(135deg,rgba(255,255,255,.16) 0 2px,transparent 2px 13px),var(--navy)}
body::before{left:0;top:0;clip-path:polygon(0 0,100% 0,0 100%)}
body::after{right:0;bottom:0;clip-path:polygon(100% 0,100% 100%,0 100%)}
.mono{font-family:var(--mono);font-variant-numeric:tabular-nums;letter-spacing:-.01em}
b{font-weight:700}
#prog{position:fixed;left:0;top:0;height:4px;width:100%;z-index:30;background:var(--line)}
#prog i{display:block;height:100%;width:0;background:var(--indigo);transition:width .3s var(--ez)}
.slide{position:fixed;inset:0;z-index:1;display:none}
.slide.on{display:block}
.sc{height:100%;overflow-y:auto;overflow-x:hidden;display:flex;flex-direction:column;
  padding:clamp(18px,5.4vh,70px) clamp(16px,6vw,130px) calc(5.4rem + 12px);scrollbar-width:thin}
.wrap{margin:auto;width:100%;max-width:96rem}
.sh{margin-bottom:1.6rem}
.kick{font-size:.8rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--indigo);margin-bottom:.4rem}
h2{font-size:2.5rem;line-height:1.08;font-weight:800;color:var(--navy);text-transform:uppercase;letter-spacing:-.01em;max-width:40ch}
h3{font-size:1.1rem;color:var(--navy);font-weight:700;margin-bottom:.7rem;line-height:1.3}
.p{font-size:1.2rem;line-height:1.5;margin-bottom:1rem;max-width:62ch}
.p.lg{font-size:1.4rem}.p.sm{font-size:1.05rem;margin-bottom:.7rem}
.p.wide{max-width:none;margin-bottom:1.3rem}
.two{display:grid;grid-template-columns:minmax(0,1fr);gap:1.6rem 3rem;align-items:center}
.g2{display:grid;grid-template-columns:minmax(0,1fr);gap:1.4rem}
.g3{display:grid;grid-template-columns:minmax(0,1fr);gap:1.2rem}
.vstack{display:flex;flex-direction:column;gap:.4rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh)}
.dgcard{padding:1rem 1.2rem}
.dg{display:block;width:100%;height:auto;max-height:66vh;overflow:visible}
.wide2 .dg{max-height:46vh}
.bigdg .dg{max-height:68vh}
.bigdg{padding:.7rem .9rem}
/* steps & badges */
.steps{list-style:none;display:flex;flex-direction:column;gap:1rem}
.steps li{display:flex;gap:1rem;align-items:flex-start;font-size:1.2rem;line-height:1.45}
.steps.sm li{font-size:1.02rem;gap:.8rem}
.steps.big li{font-size:1.65rem;align-items:center}
.steps.cols{display:grid;grid-template-columns:minmax(0,1fr);gap:1rem 3rem}
.badge{flex:none;display:grid;place-items:center;width:2.1em;height:2.1em;border-radius:6px;color:#fff;font-weight:700;font-family:var(--mono);font-size:.9em;
  background:linear-gradient(135deg,var(--indigo),var(--violet))}
.steps.big .badge{font-size:.75em}
.bul{list-style:none;display:flex;flex-direction:column;gap:.6rem;margin-bottom:1rem}
.bul li{font-size:1.25rem;padding-left:1.4rem;position:relative}
.bul li::before{content:"";position:absolute;left:0;top:.5em;width:.55rem;height:.55rem;border-radius:2px;background:var(--indigo)}
.lst{padding:1.3rem 1.5rem}
.lst .steps li{font-size:1.1rem}
.callout{background:var(--tint);border-radius:var(--r);padding:.9rem 1.1rem}
.note2{color:var(--dim);margin-top:1rem}
.src{font-size:.85rem;color:var(--dim);margin-top:1rem}
/* colors */
.c-ind{--c:var(--indigo)}.c-blue{--c:var(--blue)}.c-vio{--c:var(--violet)}.c-cr{--c:var(--crimson)}.c-navy{--c:var(--navy)}.c-dim{--c:var(--dim)}
/* reveal engine */
[data-s]{opacity:0;transform:translateY(8px);
  transition:opacity calc(220ms / var(--sp)) var(--ez) calc(var(--dl,0ms) / var(--sp)),transform calc(220ms / var(--sp)) var(--ez) calc(var(--dl,0ms) / var(--sp))}
[data-s].in{opacity:1;transform:none}
tr[data-s]{transform:none}
.arr[data-s]{opacity:1;transform:none}
.arr .draw{fill:none;stroke:var(--c);stroke-width:3.2;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1;
  transition:stroke-dashoffset calc(600ms / var(--sp)) linear}
.arr.in .draw{stroke-dashoffset:0}
.arr .head{fill:var(--c);opacity:0;transition:opacity calc(90ms / var(--sp)) linear calc(560ms / var(--sp))}
.arr.in .head{opacity:1}
.arr .lbl{opacity:0;fill:var(--c);font-size:21px;transition:opacity calc(220ms / var(--sp)) var(--ez) calc(750ms / var(--sp))}
.arr.in .lbl{opacity:1}
.arr .lbl .b{font-weight:800;font-family:var(--f)}
.arr.kl .draw{stroke:var(--crimson);stroke-dasharray:.035 .03;opacity:.55;transition:opacity calc(300ms / var(--sp))}
.arr.kl .lbl{fill:var(--crimson)}
.mv{transition:transform calc(var(--md,900ms) / var(--sp)) var(--ez) calc(var(--dl,0ms) / var(--sp))}
.mv.lin{transition-timing-function:linear}
.mv.go{transform:translate(var(--dx,0px),var(--dy,0px))}
.roll{transition:transform calc(1400ms / var(--sp)) steps(11,end)}
.roll.go{transform:translateY(-374px)}
.fd{transition:opacity calc(260ms / var(--sp)) var(--ez)}
.fd.kl{opacity:0!important}
.life{transition:opacity calc(700ms / var(--sp)) ease calc(var(--kd,0ms) / var(--sp))}
.life.kl{opacity:.28}
.dgm rect{transition:fill .3s,stroke .3s,opacity .3s}
.dgm.kl rect{fill:none;stroke:var(--crimson);stroke-dasharray:6 5;opacity:.7}
.ni,.ni *{transition:none!important}
.pulse{animation:pls calc(400ms / var(--sp)) var(--ez) 1}
@keyframes pls{0%,100%{background:var(--card);color:var(--navy)}25%,75%{background:var(--c);color:#fff}}
/* svg primitives */
.dg text{font-family:var(--f);font-size:22px;fill:var(--ink)}
.dg .mono{font-family:var(--mono)}
.ll{stroke:var(--dim);stroke-width:2;stroke-dasharray:6 7;opacity:.55}
.node{fill:var(--navy)}.dg .nodet{fill:#fff;font-weight:700;font-size:23px}
.okp{fill:var(--tint);stroke:var(--indigo);stroke-width:2}.dg .okpt{fill:var(--navy);font-weight:700}
.segb{fill:#fff;stroke:var(--indigo);stroke-width:2.4}.segh{fill:var(--indigo)}
.dg .segl{fill:#fff;font-size:15px;font-weight:600}.dg .segn{font-size:21px;font-weight:700;fill:var(--navy)}.dg .segs{font-size:15px;fill:var(--dim)}
.roll text{font-family:var(--mono);font-size:26px;font-weight:700;fill:var(--indigo)}
.file{fill:var(--tint);stroke:var(--indigo);stroke-width:2.4}.dg .filet{font-size:26px;font-weight:700;fill:var(--navy)}.dg .filen{font-size:32px;font-weight:700;fill:var(--indigo)}
.dg .dgc{fill:var(--dim);font-size:22px}.dg .dgbig{font-size:28px;font-weight:700;fill:var(--navy)}
.src.c-ind,.src.c-blue,.src.c-vio{}
rect.src{fill:#fff;stroke:var(--c);stroke-width:2.4}.dg .srct{font-size:21px;font-weight:600;fill:var(--navy)}
.muxb{fill:var(--navy)}.dg .muxt{fill:#fff;font-weight:800;font-size:26px}
.rseg{fill:var(--c);stroke:#fff;stroke-width:1.5}
.track{stroke:var(--line);stroke-width:4;stroke-linecap:round}
.addr{fill:#fff;stroke:var(--line);stroke-width:2}.dg .addrk{fill:var(--dim);font-size:18px}.dg .addrv{font-size:24px;font-weight:700;fill:var(--navy)}
.pairb{fill:var(--navy)}.dg .pairt{fill:#fff;font-weight:700;font-size:20px}
.brk{fill:none;stroke:var(--indigo);stroke-width:2.4}.dg .brkt{fill:var(--indigo);font-size:18px;font-weight:600}
.waitl{stroke:var(--crimson);stroke-width:5;stroke-dasharray:8 7}.dg .waitt{fill:var(--crimson);font-size:19px;font-weight:600}
.xmark{stroke:var(--crimson);stroke-width:5;stroke-linecap:round;fill:none}.dg .lostt{fill:var(--crimson);font-size:20px;font-weight:700}
.frame{fill:var(--tint);stroke:var(--line);stroke-width:2}.dg .framet{fill:var(--dim);font-size:19px}
/* --- крупные схемы «как на фото» --- */
.dg .nname{font-size:30px;font-weight:800;fill:var(--navy)}
.dg .nsub{font-size:19px;fill:var(--dim)}
.mon{fill:var(--navy)}.monsc{fill:var(--indigo)}
.spine{stroke:var(--line);stroke-width:3}
.qcard{fill:var(--card);stroke:var(--line);stroke-width:2}
.stagec{fill:var(--card);stroke:var(--line);stroke-width:2}
.dg .stagt{font-size:19px;font-weight:800;fill:var(--navy);letter-spacing:.01em}
.dg .stags{font-size:15px;fill:var(--dim)}
.sheet{fill:var(--tint);stroke:var(--indigo);stroke-width:2}
.bdgc{fill:var(--indigo)}.bdgb{fill:var(--blue)}.bdgr{fill:var(--crimson)}
.dg .bdgt{fill:#fff;font-weight:800}
.celle{fill:var(--card);stroke:var(--line);stroke-width:2.4}
.cellf{fill:var(--blue)}
.brc{fill:none;stroke:var(--line);stroke-width:2.4}
.dg .fl{font-size:21px;fill:var(--ink);font-family:var(--mono)}
.dg .fv{font-size:21px;fill:var(--violet);font-weight:700;font-family:var(--mono)}
.dg .fa{font-size:21px;fill:var(--blue);font-weight:700;font-family:var(--mono)}
.dg .qline{font-size:15px;fill:var(--dim)}
.chipr{fill:var(--indigo)}.dg .chipt{fill:#fff;font-weight:800;font-size:21px}
.ipb{fill:var(--tint);stroke:var(--line);stroke-width:2}
.dg .ipt{font-family:var(--mono);font-size:19px;fill:var(--navy);font-weight:700}
.statb{fill:var(--card);stroke:var(--line);stroke-width:2}
.dg .statt{font-size:21px;font-weight:600;fill:var(--navy)}
.dash{fill:none;stroke:var(--indigo);stroke-width:2.6;stroke-dasharray:11 9;opacity:.75}
.dhead{fill:var(--indigo);opacity:.75}
.hplate{fill:var(--card);stroke:var(--c);stroke-width:2.4}
.hbar{fill:var(--c)}
.dg .hbart{fill:#fff;font-size:17px;font-weight:700}
.dg .hseq{font-family:var(--mono);font-size:22px;font-weight:700;fill:var(--navy)}
.dg .hflg{font-size:18px;fill:var(--dim)}
.dg .rowt{font-size:18px;fill:var(--ink)}
.dg .legt{font-size:16px;fill:var(--ink)}
.dg .legk{font-size:20px;font-weight:800}
.dg .fa2{fill:var(--indigo)}.dg .fc2{fill:var(--crimson)}
.banner{fill:var(--tint);stroke:var(--line);stroke-width:2}
.dg .bannert{font-size:24px;font-weight:700;fill:var(--navy)}
.dleg{display:flex;flex-wrap:wrap;gap:.5rem 1.8rem;margin-top:.9rem;font-size:.92rem;color:var(--dim);justify-content:center}
.dleg i{font-style:normal;opacity:.75}
.dleg b.fa2{color:var(--blue)}.dleg b.fv2{color:var(--violet)}
.stgs{display:flex;flex-direction:column;gap:.7rem}
.stg{display:flex;gap:.9rem;align-items:flex-start;background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:.7rem .9rem;box-shadow:var(--sh)}
.stg b{display:block;font-size:.98rem;color:var(--navy);text-transform:uppercase;letter-spacing:.01em}
.stg span:last-child{display:block;font-size:.88rem;color:var(--dim);margin-top:.15rem}
.hchips{display:flex;flex-direction:column;gap:.7rem}
.hchip{border:2px solid var(--c);border-radius:var(--r);padding:.55rem .9rem;background:var(--card);display:grid;grid-template-columns:auto 1fr auto;gap:.2rem .8rem;align-items:center;box-shadow:var(--sh)}
.hchip .hct{grid-column:1/-1;font-size:.72rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--c)}
.hchip b{font-size:1.1rem;color:var(--navy)}
.hchip .hcf{font-size:.9rem;color:var(--dim)}
.hchip .hcd{font-size:.95rem;font-weight:700;color:var(--c);justify-self:end;grid-row:2}
.dimh{color:var(--dim);font-weight:600}
.say{display:block;margin-top:.35rem;padding-left:.7rem;border-left:3px solid var(--indigo);color:var(--dim);font-style:italic}
.vstack.gap{gap:.8rem}
.vstack.gap .dg{max-height:32vh}
.vstack.gap .qbox .p,.vstack.gap .callout{font-size:.95rem;line-height:1.4}
.vstack.gap .qbox h3{font-size:1rem}
.vstack.gap .dgcard{padding:.6rem .8rem}
.vstack.gap .callout,.vstack.gap .qbox{padding:.6rem .85rem}
.vstack.gap .p{margin-bottom:0}
.callout.warn{background:#fdeaf1;border-left:4px solid var(--crimson)}
.qbox{padding:.9rem 1.1rem}
.qbox h3{margin-bottom:.4rem}
.qbox .p{margin-bottom:0}
.formula{padding:.9rem 1.1rem;text-align:center;font-size:1.25rem;font-weight:700;color:var(--navy);background:var(--tint)}
.tbl.num td{font-size:1rem;white-space:nowrap}
.tbl.num th{font-size:.9rem}
/* title */
.tslide .sc{padding-left:clamp(16px,10vw,220px)}
.title h1{font-size:clamp(2.4rem,6.5vw,5.6rem);line-height:1;font-weight:800;color:var(--navy);text-transform:uppercase;letter-spacing:-.02em;max-width:14ch;margin:.3rem 0 1.4rem}
.kick.big{font-size:1rem}
.lead{font-size:1.45rem;line-height:1.45;color:var(--dim);max-width:44ch;margin-bottom:2rem}
.tchips{display:flex;flex-wrap:wrap;gap:.7rem;margin-bottom:3rem}
.chip{border:1px solid var(--line);background:#fff;border-radius:var(--r);padding:.5rem .95rem;font-weight:700;color:var(--indigo);font-size:1.1rem}
.authors{font-size:1.05rem;line-height:1.6;color:var(--ink)}
/* specific */
.pgrid{display:grid;gap:1rem}
.proto{padding:1.4rem 1.6rem;display:flex;align-items:center;gap:1.4rem;font-size:1.2rem}
.proto .pn{font-size:2.6rem;font-weight:800;color:var(--c)}
.osi{display:flex;flex-direction:column;gap:.45rem}
.layer{display:flex;gap:1rem;align-items:center;padding:.6rem 1rem;border:1px solid var(--line);border-radius:var(--r);background:#fff;font-size:1.15rem;color:var(--navy)}
.layer .mono{color:var(--dim);width:1.4rem}
.layer.hl{border-color:var(--indigo);font-weight:700;box-shadow:inset 0 0 0 1px var(--indigo)}
.addrbig{display:flex;align-items:baseline;justify-content:center;padding:1.2rem;font-size:clamp(1.6rem,3.2vw,3.2rem);font-weight:700}
.addrbig .ip{color:var(--indigo)}.addrbig .port{color:var(--violet)}.addrbig .colon{color:var(--dim)}
.addrcap{display:flex;justify-content:space-around;font-weight:600;color:var(--c);margin-bottom:1rem}
.addrcap span{color:var(--c)}
.tw{overflow-x:auto}
.tbl{width:100%;border-collapse:collapse;font-size:1.1rem}
.tbl th,.tbl td{text-align:left;padding:.5rem 1rem;border-bottom:1px solid var(--line);vertical-align:top}
.tbl thead th{background:var(--navy);color:#fff;font-weight:700}
.tbl tbody th{font-weight:600;color:var(--navy)}
.ports .tbl td{font-weight:700;color:var(--indigo);text-align:right}
.ports .tbl thead th:last-child{text-align:right}
.cmp{font-size:1rem;min-width:44rem}.cmp th:first-child{width:18%}
.pg{padding:1.3rem 1.4rem}.pg .rng{font-size:1.7rem;font-weight:800;color:var(--c);margin-bottom:.5rem}.pg p{font-size:1.05rem;line-height:1.5}
.hdrcard{padding:1.2rem 1.4rem}
.ruler{display:flex;justify-content:space-between;color:var(--dim);font-size:.8rem;margin-bottom:.3rem}
.hdr{display:flex;flex-direction:column;gap:.4rem}
.hrow{display:grid;grid-template-columns:repeat(32,minmax(0,1fr));gap:.4rem}
.fld{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:.15rem;
  min-height:3.6rem;padding:.4rem;border:1.5px solid var(--line);border-radius:var(--r);background:var(--tint);cursor:help;outline:none;
  transition:background .15s,border-color .15s}
.fld b{font-size:1.02rem;color:var(--navy);line-height:1.15}.fld .mono{font-size:.8rem;color:var(--dim)}
.fld:hover,.fld:focus-visible{background:#fff;border-color:var(--indigo);z-index:5}
.tip{position:absolute;left:50%;bottom:calc(100% + 10px);transform:translate(-50%,4px);width:min(24rem,80vw);background:var(--navy);color:#fff;
  font-size:.95rem;line-height:1.4;text-align:left;padding:.7rem .9rem;border-radius:var(--r);opacity:0;pointer-events:none;transition:opacity .15s,transform .15s}
.fld:hover .tip,.fld:focus-visible .tip{opacity:1;transform:translate(-50%,0)}
.hrow:first-child .tip{bottom:auto;top:calc(100% + 10px)}
.hdata{margin-top:.4rem;padding:.8rem;text-align:center;border:1.5px dashed var(--line);border-radius:var(--r);color:var(--dim)}
.fstrip{display:flex;flex-wrap:wrap;gap:.6rem;margin-bottom:1.3rem}
.fplate{font-family:var(--mono);font-weight:800;font-size:1.2rem;padding:.45rem 1rem;border-radius:var(--r);border:1.5px solid var(--c);color:var(--navy);background:var(--card)}
.fcard{padding:1.3rem 1.4rem}.fcard p{font-size:1.02rem;line-height:1.5}
.ftag{display:inline-block;font-family:var(--mono);font-weight:800;font-size:1.5rem;color:var(--c);margin-bottom:.5rem}
.ftag.sm{font-size:.95rem;margin:0 0 0 auto}
.wcard{padding:1.1rem 1.2rem}
.whead{display:flex;align-items:center;gap:.7rem;margin-bottom:.7rem;font-size:1.1rem;color:var(--navy)}
.kv{display:flex;justify-content:space-between;gap:.8rem;font-size:.92rem;padding:.28rem 0;border-bottom:1px solid var(--line)}
.kv span{color:var(--dim)}.kv b{color:var(--navy)}
.note{font-size:.9rem;line-height:1.45;margin-top:.7rem;color:var(--ink)}
.udph{display:grid;grid-template-columns:1fr 1fr;gap:.45rem;padding:1rem}
.uf{display:flex;flex-direction:column;align-items:center;padding:.8rem;border-radius:var(--r);background:var(--tint);border:1.5px solid var(--line)}
.uf b{color:var(--navy)}.uf .mono{color:var(--dim);font-size:.85rem}
.ud{grid-column:span 2;background:#fff;border-style:dashed;color:var(--dim)}
.app{padding:1.4rem}.appn{font-size:2rem;font-weight:800;color:var(--violet);margin-bottom:.6rem}.app p{font-size:1.1rem;line-height:1.5}
/* trainers */
.trn,.quiz{padding:1.5rem 1.6rem}
.quiz{max-width:60rem}
.tq{font-size:1.35rem;line-height:1.4;color:var(--navy);margin-bottom:1rem}
.trow{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;margin-bottom:.8rem}
.trow input{font-size:1.3rem;width:8em;padding:.5rem .7rem;border:1.5px solid var(--line);border-radius:var(--r);color:var(--navy);background:#fff}
.trow input:focus-visible{outline:3px solid var(--indigo);outline-offset:1px}
.btn{font:inherit;font-size:.95rem;font-weight:600;padding:.55rem .95rem;border-radius:var(--r);border:1.5px solid var(--line);background:#fff;color:var(--navy);cursor:pointer;transition:background .15s,border-color .15s}
.btn:hover{border-color:var(--indigo)}
.btn:active{background:var(--tint)}
.btn.pri{background:var(--indigo);border-color:var(--indigo);color:#fff}
.btn.pri:hover{background:var(--navy)}
.btn:focus-visible,.opt:focus-visible,#nav button:focus-visible,.ovi:focus-visible{outline:3px solid var(--violet);outline-offset:2px}
.tres{min-height:2.6rem;font-size:1.1rem;line-height:1.45;margin-bottom:.6rem}
.tres.ok{color:var(--ok)}.tres.no{color:var(--crimson)}
.tscore{color:var(--dim)}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:.6rem;margin-bottom:1rem}
.opts.col{grid-template-columns:1fr 1fr}
.opt{font:inherit;text-align:left;font-size:1.1rem;padding:.75rem 1rem;border-radius:var(--r);border:1.5px solid var(--line);background:#fff;color:var(--ink);cursor:pointer}
.opt:hover{border-color:var(--indigo)}
.opt.ok{border-color:var(--ok);background:#e8f6ef}.opt.no{border-color:var(--crimson);background:#fdecf2}
.qtop{display:flex;justify-content:space-between;color:var(--dim);margin-bottom:.6rem}
/* nav */
#nav{position:fixed;z-index:40;left:50%;bottom:12px;transform:translateX(-50%);display:flex;align-items:center;gap:.35rem;flex-wrap:wrap;justify-content:center;
  background:rgba(255,255,255,.94);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh);padding:.35rem .5rem;font-size:14px;max-width:calc(100vw - 24px)}
#nav button{font:inherit;font-size:13px;font-weight:600;border:1px solid transparent;background:transparent;color:var(--navy);border-radius:10px;padding:.42rem .65rem;cursor:pointer;display:inline-flex;align-items:center;gap:.3rem}
#nav button:hover{background:var(--tint)}
#nav button[aria-pressed="true"]{background:var(--navy);color:#fff}
#nav svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}
.nsep{width:1px;height:22px;background:var(--line);margin:0 .2rem}
#ind{font-family:var(--mono);font-size:13px;color:var(--ink);padding:0 .4rem;white-space:nowrap}
#ind .st{color:var(--dim);margin-left:.8rem}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:10px;padding:2px}
#ov{position:fixed;inset:0;z-index:60;background:rgba(244,245,251,.97);overflow:auto;padding:clamp(16px,5vh,60px) clamp(16px,6vw,120px)}
#ov h2{margin-bottom:1.2rem;font-size:1.8rem}
.ovg{display:grid;grid-template-columns:repeat(auto-fill,minmax(14rem,1fr));gap:.7rem}
.ovi{font:inherit;text-align:left;display:flex;gap:.8rem;align-items:center;padding:.8rem 1rem;background:#fff;border:1px solid var(--line);border-radius:var(--r);cursor:pointer;color:var(--navy);font-size:1rem}
.ovi:hover{border-color:var(--indigo)}.ovi.cur{border-color:var(--indigo);box-shadow:inset 0 0 0 1px var(--indigo)}
.ovi .mono{color:var(--indigo);font-weight:700;width:2rem}
@media (min-width:768px){.g2{grid-template-columns:repeat(2,minmax(0,1fr))}.g3{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (min-width:768px) and (max-width:1279px){.g3{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:1280px){
  .two{grid-template-columns:repeat(2,minmax(0,1fr))}
  .steps.cols{grid-template-columns:repeat(2,minmax(0,1fr))}
  .pgrid{grid-template-columns:1fr}
}
@media (max-width:767px){
  html{font-size:15px}
  h2{font-size:min(1.9rem,30px)}
  .sc{padding-bottom:9rem}
  .steps.big li{font-size:1.3rem}
  .hrow{gap:.25rem}.fld b{font-size:.75rem}.fld .mono{font-size:.65rem}.fld{min-height:3rem;padding:.25rem}
  .opts,.opts.col{grid-template-columns:1fr}
  .dg{max-height:none}
  #nav{bottom:6px;font-size:12px}
  #nav .lbl2{display:none}
}
.figs .wrap{max-width:none;width:100%}.figs .sh{margin-bottom:.4rem}.figs .sh h2{font-size:1.5rem}.figx{margin:0;display:flex;justify-content:center}.figx img{width:auto;max-width:100%;max-height:80vh;image-rendering:auto;height:auto;border-radius:14px;box-shadow:0 10px 40px rgba(20,24,80,.18);background:#fff}
.figcap{text-align:center;margin-top:1rem}.wsx{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:2rem;align-items:start}.wsx .figx img{max-height:76vh}.wsh{margin:0 0 1rem;font-size:1.3rem}
@media (max-width:900px){.wsx{grid-template-columns:1fr}}
.ovg{grid-template-columns:repeat(auto-fill,minmax(17rem,1fr));gap:1rem}
.ovi{flex-direction:column;align-items:stretch;gap:.45rem;padding:.5rem}
.ovt{position:relative;width:100%;aspect-ratio:16/9;overflow:hidden;border-radius:8px;background:var(--paper);border:1px solid var(--line);pointer-events:none}
.ovt>.slide{position:absolute!important;inset:auto!important;left:0;top:0;display:block!important;transform-origin:0 0}
.ovt [data-s]{opacity:1!important;transform:none!important}.ovt .arr .draw{stroke-dashoffset:0!important}.ovt .arr .head,.ovt .arr .lbl{opacity:1!important}
.ovi .ovn{display:flex;gap:.6rem;align-items:baseline;font-size:.95rem}
.wsk{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:0 10px 30px rgba(20,24,80,.1);font-size:.78rem}
.wst{width:100%;border-collapse:collapse;font-family:var(--fm,ui-monospace,Consolas,monospace)}
.wst th{background:#eef0f7;text-align:left;font-family:var(--f);font-weight:600;padding:.45em .6em;border-bottom:1px solid var(--line);color:#556}
.wst td{padding:.45em .6em;border-bottom:1px solid #eef0f7;white-space:nowrap}.wst td:last-child{white-space:normal}
.wst tr.sel td{background:#2d5bff;color:#fff;font-weight:600}
.wsd{padding:.8em 1em;font-family:var(--fm,ui-monospace,Consolas,monospace);line-height:1.75;background:#fafbfe}
.wl{white-space:nowrap}.wl.i1{padding-left:1.4em}.wl.i3{padding-left:2.8em;color:#445}.wl.dim{color:#8a8fa8}
.whl{background:#fff1a8;border-radius:5px;padding:.1em .35em}
.wn{display:inline-grid;place-items:center;width:1.45em;height:1.45em;border-radius:50%;background:#e5383b;color:#fff;font:700 .8em/1 var(--f);margin-right:.45em;vertical-align:.1em}
.wst tr.sel .wn{background:#fff;color:#2d5bff}
.wbad{background:#e5383b!important;color:#fff!important}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{transition:none!important;animation:none!important}
}
@media print{.slide{display:block;position:relative;height:auto;page-break-after:always}[data-s]{opacity:1;transform:none}.arr .draw{stroke-dashoffset:0}.arr .head,.arr .lbl{opacity:1}#nav,#prog{display:none}html,body{overflow:visible;height:auto}}
"""

JS = r"""
(function(){
'use strict';
var $=function(s,r){return (r||document).querySelector(s)}, $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
var slides=$$('.slide'), N=slides.length, cur=0, step=0, mode='all', speed=1, timer=null, playing=false, paused=false;
var RM=window.matchMedia('(prefers-reduced-motion: reduce)');
var root=document.documentElement;
slides.forEach(function(s){
  var els=$$('[data-s],[data-m],[data-k],[data-p]',s), mx=0;
  els.forEach(function(e){['s','m','k','p'].forEach(function(a){var v=+e.dataset[a]||0; if(v>mx)mx=v;});});
  s._els=els; s._max=mx;
});
function waitFor(sl,k){
  var w=0;
  sl._els.forEach(function(e){ if(+e.dataset.s===k||+e.dataset.m===k||+e.dataset.k===k){ w=Math.max(w,+e.dataset.w||650); } });
  return w||650;
}
function setStep(k,instant){
  var sl=slides[cur]; step=Math.max(0,Math.min(sl._max,k));
  if(instant) sl.classList.add('ni');
  sl._els.forEach(function(e){
    var d=e.dataset;
    if(d.s) e.classList.toggle('in',+d.s<=step);
    if(d.m) e.classList.toggle('go',+d.m<=step);
    if(d.k) e.classList.toggle('kl',+d.k<=step);
    if(d.p!==undefined && !instant){ e.classList.remove('pulse'); if(+d.p===step && step>0){ void e.getBoundingClientRect(); e.classList.add('pulse'); } }
  });
  if(instant){ void sl.offsetWidth; sl.classList.remove('ni'); }
  ui();
}
function stopPlay(){ clearTimeout(timer); timer=null; playing=false; paused=false; ui(); }
function schedule(ms){ clearTimeout(timer); timer=setTimeout(tick, ms/speed); }
function tick(){
  var sl=slides[cur];
  if(step>=sl._max){ playing=false; paused=false; ui();
    if(sl.dataset.anim==='loop'&&!RM.matches){ var me=cur; timer=setTimeout(function(){ if(cur===me&&ov.hidden){ play(); } },2600); }
    return; }
  setStep(step+1,false);
  schedule(waitFor(sl,step));
}
function play(){
  stopPlay();
  if(RM.matches){ setStep(slides[cur]._max,true); return; }
  if(!slides[cur]._max) return;
  setStep(0,true); playing=true; ui(); schedule(350);
}
function togglePause(){
  if(!playing) return false;
  if(paused){ paused=false; schedule(250); } else { paused=true; clearTimeout(timer); }
  ui(); return true;
}
function go(i,atEnd){
  i=Math.max(0,Math.min(N-1,i));
  stopPlay();
  slides.forEach(function(s){s.classList.remove('on')}); cur=i; slides[cur].classList.add('on');
  var sc=$('.sc',slides[cur]); if(sc) sc.scrollTop=0;
  var an=slides[cur].dataset.anim;
  setStep((RM.matches||!an)?slides[cur]._max:0,true);
  try{ history.replaceState(null,'','#'+(cur+1)); }catch(e){}
  if(an && !RM.matches) play();
}
function next(){
  if(cur<N-1) go(cur+1);
}
function prev(){
  if(cur>0) go(cur-1);
}
function setMode(m){ mode=m; stopPlay(); ui(); if(mode==='all') play(); }
function setSpeed(v){ speed=v; root.style.setProperty('--sp',v); ui(); }
/* ---- UI ---- */
var ind=$('#ind'), bPlay=$('#b-play');
function ui(){
  var mx=slides[cur]._max;
  ind.innerHTML='слайд '+(cur+1)+' / '+N;
  $('#prog i').style.width=((cur+1)/N*100)+'%';
  $$('[data-speed]').forEach(function(b){ b.setAttribute('aria-pressed', +b.dataset.speed===speed); });
  bPlay.style.display=slides[cur].dataset.anim?'':'none';
  bPlay.querySelector('.lbl2').textContent = playing&&!paused ? 'Пауза' : 'Повторить';
}
$('#b-prev').onclick=prev; $('#b-next').onclick=next;
bPlay.onclick=function(){ if(!togglePause()) play(); };
$$('[data-speed]').forEach(function(b){ b.onclick=function(){ setSpeed(+b.dataset.speed); }; });
/* overview */
var ov=$('#ov'), ovg=$('.ovg',ov);
slides.forEach(function(s,k){
  var b=document.createElement('button'); b.className='ovi'; b.type='button';
  b.innerHTML='<span class="ovt"></span><span class="ovn"><span class="mono">'+(k+1)+'</span><span></span></span>'; b.querySelector('.ovn').lastChild.textContent=s.dataset.label;
  b.onclick=function(){ closeOv(); go(k); }; ovg.appendChild(b);
});
var ovBuilt=false;
function buildThumbs(){
  var W=innerWidth, H=innerHeight;
  $$('.ovi',ov).forEach(function(b,k){
    var box=$('.ovt',b); box.innerHTML='';
    var c=slides[k].cloneNode(true); c.classList.add('on'); c.removeAttribute('id');
    $$('[id]',c).forEach(function(e){e.removeAttribute('id')});
    $$('input,button,select,textarea',c).forEach(function(e){e.tabIndex=-1});
    c.setAttribute('aria-hidden','true'); c.style.width=W+'px'; c.style.height=H+'px';
    box.appendChild(c);
    var sc=box.clientWidth/W; c.style.transform='scale('+sc+')';
  });
  ovBuilt=true;
}
addEventListener('resize',function(){ ovBuilt=false; if(!ov.hidden) buildThumbs(); });
function openOv(){ stopPlay(); ov.hidden=false; if(!ovBuilt) buildThumbs(); $$('.ovi',ov).forEach(function(b,k){b.classList.toggle('cur',k===cur)}); var c=$('.ovi.cur',ov); if(c)c.focus(); }
function closeOv(){ ov.hidden=true; }
$('#b-ov').onclick=openOv;
/* keys */
var dbuf='', dtm=null;
document.addEventListener('keydown',function(e){
  var t=e.target, tag=t.tagName;
  if(e.ctrlKey||e.metaKey||e.altKey) return;
  if(tag==='INPUT'||tag==='TEXTAREA'){ if(e.key==='Escape') t.blur(); return; }
  if(e.key==='Escape'){ e.preventDefault(); ov.hidden?openOv():closeOv(); return; }
  if(!ov.hidden) return;
  var isBtn=tag==='BUTTON';
  switch(e.key){
    case 'ArrowRight': case 'PageDown': e.preventDefault(); next(); return;
    case 'ArrowLeft': case 'PageUp': e.preventDefault(); prev(); return;
    case ' ': if(isBtn) return; e.preventDefault();
      next(); return;
    case 'Home': e.preventDefault(); go(0); return;
    case 'End': e.preventDefault(); go(N-1); return;
  }
  var k=e.key.toLowerCase();
  if(k==='r'||k==='к'){ play(); return; }
  if(/^[0-9]$/.test(e.key)){
    dbuf+=e.key; clearTimeout(dtm);
    dtm=setTimeout(function(){ var n=parseInt(dbuf,10); dbuf=''; if(n>=1&&n<=N) go(n-1); },550);
  }
});
/* wheel */
var lastWheel=0;
window.addEventListener('wheel',function(e){
  if(!ov.hidden) return;
  var sc=$('.sc',slides[cur]); if(!sc) return;
  var dy=e.deltaY; if(Math.abs(dy)<4) return;
  if(dy>0 && sc.scrollTop+sc.clientHeight<sc.scrollHeight-2) return;
  if(dy<0 && sc.scrollTop>0) return;
  var now=Date.now(); if(now-lastWheel<420){ lastWheel=now; return; } lastWheel=now;
  if(dy>0){ if(cur<N-1) go(cur+1); } else { if(cur>0) go(cur-1,true); }
},{passive:true});
/* swipe */
var tx=0, ty=0, tt=0;
window.addEventListener('touchstart',function(e){ var p=e.changedTouches[0]; tx=p.clientX; ty=p.clientY; tt=Date.now(); },{passive:true});
window.addEventListener('touchend',function(e){
  var p=e.changedTouches[0], dx=p.clientX-tx, dy=p.clientY-ty;
  if(Date.now()-tt>700||Math.abs(dx)<60||Math.abs(dx)<Math.abs(dy)*1.4) return;
  if(e.target.closest&&e.target.closest('input,.tw')) return;
  dx<0?next():prev();
},{passive:true});

/* ---- trainers ---- */
var PORTS=__PORTS__;
function rnd(n){ return Math.floor(Math.random()*n); }
(function(){
  var cur=null, tot=0, ok=0, answered=false, inp=$('#tp-in'), res=$('#tp-r');
  function nx(){ var p; do{ p=PORTS[rnd(PORTS.length)]; }while(cur&&p[0]===cur[0]); cur=p; answered=false; $('#tp-s').textContent=p[0]; inp.value=''; res.textContent=''; res.className='tres'; }
  function chk(){
    var v=inp.value.trim(); if(!/^\d{1,5}$/.test(v)){ res.textContent='Введите номер порта числом.'; res.className='tres no'; return; }
    if(!answered){ tot++; if(+v===cur[1]) ok++; answered=true; }
    if(+v===cur[1]){ res.textContent='Верно: '+cur[0]+' использует порт '+cur[1]+'.'; res.className='tres ok'; }
    else { res.textContent='Неверно. '+cur[0]+' использует порт '+cur[1]+'.'; res.className='tres no'; }
    $('#tp-sc').textContent=ok+' / '+tot;
  }
  $('#tp-ok').onclick=chk; $('#tp-nx').onclick=nx;
  inp.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); answered?nx():chk(); } });
  nx();
})();
(function(){
  var G=[['Известные',0,1023],['Зарегистрированные',1024,49151],['Динамические/частные',49152,65535]];
  var pool=[80,443,22,53,110,25,1812,3389,8080,5060,49152,54824,60000,65535,1023,1024,49151];
  var p=0;
  function nx(){ var q; do{ q=pool[rnd(pool.length)]; }while(q===p); p=q; $('#tg-p').textContent=p; $('#tg-r').textContent=''; $('#tg-r').className='tres'; render(); }
  function render(){
    var o=$('#tg-o'); o.innerHTML='';
    G.forEach(function(g){
      var b=document.createElement('button'); b.type='button'; b.className='opt'; b.textContent=g[0]+' ('+g[1]+' – '+g[2]+')';
      b.onclick=function(){
        var right=G.filter(function(x){return p>=x[1]&&p<=x[2]})[0];
        $$('.opt',o).forEach(function(x,i){ if(G[i]===right) x.classList.add('ok'); });
        if(g!==right){ b.classList.add('no'); $('#tg-r').textContent='Неверно. Порт '+p+' лежит в диапазоне '+right[1]+' – '+right[2]+'.'; $('#tg-r').className='tres no'; }
        else { $('#tg-r').textContent='Верно.'; $('#tg-r').className='tres ok'; }
      };
      o.appendChild(b);
    });
  }
  $('#tg-nx').onclick=nx; nx();
})();
(function(){
  var ans=0, expl='', tot=0, ok=0, answered=false, inp=$('#ts-in'), res=$('#ts-r');
  function nx(){
    var t=rnd(3), s=1000+rnd(9000), L=[12,100,500,1460][rnd(4)], b=1000+rnd(9000);
    if(t===0){ $('#ts-q').innerHTML='Сегмент имеет порядковый номер <b class="mono">'+s+'</b> и полезную нагрузку <b class="mono">'+L+'</b> байт. Какой номер подтверждения пришлёт получатель?'; ans=s+L; expl=s+' + '+L+' = '+ans; }
    else if(t===1){ $('#ts-q').innerHTML='ПК1 отправил SYN с порядковым номером <b class="mono">'+s+'</b>. Какой номер подтверждения будет в ответе SYN, ACK от ПК2?'; ans=s+1; expl='номер подтверждения равен a+1 = '+ans; }
    else { $('#ts-q').innerHTML='ПК1 отправил SYN с номером <b class="mono">'+s+'</b>, ПК2 ответил SYN, ACK с номером <b class="mono">'+b+'</b>. Какой номер подтверждения будет в третьем сегменте ACK?'; ans=b+1; expl='номер подтверждения равен b+1 = '+ans; }
    inp.value=''; res.textContent=''; res.className='tres'; answered=false;
  }
  function chk(){
    var v=inp.value.trim(); if(!/^\d+$/.test(v)){ res.textContent='Введите ответ числом.'; res.className='tres no'; return; }
    if(!answered){ tot++; if(+v===ans) ok++; answered=true; }
    res.textContent=(+v===ans?'Верно: ':'Неверно: ')+expl+'.'; res.className='tres '+(+v===ans?'ok':'no');
    $('#ts-sc').textContent=ok+' / '+tot;
  }
  $('#ts-ok').onclick=chk; $('#ts-nx').onclick=nx;
  inp.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); answered?nx():chk(); } });
  nx();
})();
(function(){
  var Q=__QUIZ__, i=0, got=Q.map(function(){return -1});
  function render(){
    var q=Q[i]; $('#qz-n').textContent=(i+1)+' / '+Q.length; $('#qz-q').textContent=q.q;
    var o=$('#qz-o'); o.innerHTML=''; var e=$('#qz-e'); e.textContent=''; e.className='tres';
    q.o.forEach(function(t,k){
      var b=document.createElement('button'); b.type='button'; b.className='opt'; b.textContent=t;
      b.onclick=function(){ if(got[i]<0) got[i]=k; show(); };
      o.appendChild(b);
    });
    if(got[i]>=0) show();
    $('#qz-sc').textContent='верно: '+got.filter(function(g,k){return g===Q[k].a}).length;
    $('#qz-pv').disabled=i===0; $('#qz-nx').textContent=i===Q.length-1?'Начать заново':'Следующий вопрос';
  }
  function show(){
    var q=Q[i], bs=$$('.opt',$('#qz-o'));
    bs[q.a].classList.add('ok'); if(got[i]!==q.a) bs[got[i]].classList.add('no');
    var e=$('#qz-e'); e.textContent=(got[i]===q.a?'Верно. ':'Неверно. ')+q.e; e.className='tres '+(got[i]===q.a?'ok':'no');
    $('#qz-sc').textContent='верно: '+got.filter(function(g,k){return g===Q[k].a}).length;
  }
  $('#qz-nx').onclick=function(){ if(i===Q.length-1){ got=Q.map(function(){return -1}); i=0; } else i++; render(); };
  $('#qz-pv').onclick=function(){ if(i>0){ i--; render(); } };
  render();
})();

var h=parseInt((location.hash||'').slice(1),10);
slides[0].classList.add('on');
go(h>=1&&h<=N?h-1:0);
RM.addEventListener&&RM.addEventListener('change',function(){ go(cur,true); });
})();
"""

ICON_L = '<svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>'
ICON_R = '<svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>'

def render():
    out = ['<!doctype html><html lang="ru"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
           '<title>Глава 8. Транспортный уровень</title><style>' + CSS + '</style></head><body>'
           '<div id="prog"><i></i></div><main id="deck">']
    for label, kick, title, body, cls in S:
        head = "" if not title else f'<header class="sh">{"<div class=kick>"+kick+"</div>" if kick else ""}<h2>{title}</h2></header>'
        anim = 'loop' if label in ANIM_LOOP else 'once' if label in ANIM_ONCE else ''
        out.append(f'<section class="slide {cls}" data-label="{label}" data-anim="{anim}"><div class="sc"><div class="wrap">{head}{body}</div></div></section>')
    out.append('</main>')
    out.append('<nav id="nav" aria-label="Навигация по слайдам">'
               f'<button id="b-prev" type="button" aria-label="Назад">{ICON_L}</button>'
               '<span id="ind" aria-live="polite"></span>'
               f'<button id="b-next" type="button" aria-label="Вперёд">{ICON_R}</button>'
               '<span class="nsep"></span>'
               
               '<button id="b-play" type="button" title="Клавиша R"><svg viewBox="0 0 24 24"><path d="M7 5l11 7-11 7z"/></svg><span class="lbl2">Повторить</span></button>'
               '<span class="seg"><button type="button" data-speed="0.5">0.5×</button><button type="button" data-speed="1">1×</button><button type="button" data-speed="2">2×</button></span>'
               '<button id="b-ov" type="button" title="Esc"><svg viewBox="0 0 24 24"><path d="M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z"/></svg><span class="lbl2">Содержание</span></button>'
               '</nav>')
    out.append('<div id="ov" hidden><h2>Содержание</h2><div class="ovg"></div></div>')
    js = JS.replace("__PORTS__", json.dumps(PORTS, ensure_ascii=False)).replace("__QUIZ__", json.dumps(QUIZ, ensure_ascii=False))
    out.append('<script>' + js + '</script></body></html>')
    OUT.write_text("".join(out), encoding="utf-8")
    print(len(S), "slides", OUT.stat().st_size, "bytes")

# ==== доработка по ЛК8: схемы из pptx, Wireshark, анимация по месту ====
import base64, io, glob
from PIL import Image as _Im
DL = r"C:/Users/anank/Downloads/"
PP = r"C:/Users/anank/AppData/Local/Temp/claude/p8/"
def _jpg(path, w=2400, q=92):
    if not pathlib.Path(path).exists(): return ""   # слайд всё равно заменяется вёрсткой ниже
    im = _Im.open(path).convert("RGB")
    if im.width > w: im = im.resize((w, round(im.height*w/im.width)), _Im.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True, progressive=True, subsampling=0)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
def _dl(pref): return glob.glob(DL + pref + "*.jpg")[0]
def figslide(label, kick, title, src, cap=""):
    c = f'<p class="p sm figcap">{cap}</p>' if cap else ""
    return (label, kick, title, f'<figure class="figx"><img src="{_jpg(src)}" alt="{title}"></figure>{c}', "figs")
FIGS = [("Сегментация", figslide("Сегментация: схема", "Сегменты и потоки", "Сегментация файла 300 КБ", _dl("HLFbfQPm"))),
 ("Мультиплексирование", figslide("Мультиплексирование: схема", "Сегменты и потоки", "Мультиплексирование потоков", _dl("e7Medrg8"))),
  ("Сокеты", figslide("Сокеты: схема", "Порты и сокеты", "Обмен данными в сети: IP-адреса и порты", _dl("iY880CSX"))),
  ("Флаги 1", figslide("Флаги в Wireshark", "Протокол TCP", "Флаги TCP-заголовка в Wireshark", PP + "s12_1.png", "При установке соединения в заголовке TCP выставлен флаг SYN, остальные флаги сброшены.")),
 ("Рукопожатие", figslide("Рукопожатие: схема", "Установка соединения", "Трёхстороннее рукопожатие во времени", _dl("4xVcPsGf"))),
 ("Рукопожатие: номера", figslide("Рукопожатие: заголовки", "Установка соединения", "Трёхстороннее рукопожатие: IP- и TCP-заголовки", _dl("lLmE7XF3"))),
  ("Окно: принцип", ("Окно: схема", "Надёжность TCP", "Установление TCP-соединения и передача данных",
   '<div class="card dgcard bigdg">' + TCPFLOW + '</div>' + TCPFLOW_LEG, "figs")),
 ("Окно: пример", figslide("Окно: обмен", "Надёжность TCP", "Обмен данными между двумя узлами: окно 3000 байт", _dl("MlkLqTqd"))),
 ("Потеря данных", figslide("Потеря: схема", "Надёжность TCP", "Обмен данными: ожидание подтверждения", _dl("ZyaE-uFR"))),
 ("Завершение сеанса", figslide("Завершение: схема", "Надёжность TCP", "Выключение TCP: четырёхстороннее квитирование", _dl("lf2Fo-i-"))),
 ("Завершение: детали", ("Завершение: номера", "Надёжность TCP", "Выключение TCP: четырёхстороннее квитирование",
   '<div class="card dgcard bigdg">' + FINFLOW + '</div>', "figs")),
 ("UDP: датаграммы", figslide("UDP: заголовок", "Протокол UDP", "Структура UDP-датаграммы", _dl("RChew0hT"))),
]
WSX = [("Первый этап рукопожатия (SYN)", PP + "s16_1.png", [
  "Сам пакет, который мы рассмотрим изнутри.",
  "Клиент отправляет запрос на сервер: порт источника — частный <b class='mono'>54824</b>, порт назначения — общеизвестный <b class='mono'>443</b> (HTTPS).",
  "<b class='mono'>Sequence Number: 0</b> — относительный номер от начала сессии (его формирует Wireshark для удобства). <b class='mono'>Sequence Number (raw): 3638817700</b> — настоящий номер в сети. <b class='mono'>Next Sequence Number: 1</b> — следующий ожидаемый. <b class='mono'>Acknowledgment number</b> равен 0: ACK ещё не поступал.",
  "Флаг <b>SYN</b> — начало синхронизации, запрос на соединение с сервером.",
  "<b class='mono'>Window 64240</b> — размер окна приёма: сколько байт принимающая сторона может принять сейчас."]),
 ("Второй этап рукопожатия (SYN, ACK)", PP + "s17_1.png", [
  "Сам пакет, который мы рассмотрим изнутри.",
  "Сервер отвечает клиенту: порт источника <b class='mono'>443</b>, порт назначения <b class='mono'>54824</b> — в ответе порты меняются местами.",
  "<b class='mono'>Sequence Number: 0</b> — первая последовательность со стороны сервера, <b class='mono'>raw: 1565342372</b>. <b class='mono'>Acknowledgment number: 1</b> и <b class='mono'>raw: 3638817701</b> — это +1 к начальному номеру клиента.",
  "Флаг <b>ACK</b> — подтверждение принятых данных.",
  "Флаг <b>SYN</b> — начало синхронизации со стороны сервера.",
  "<b class='mono'>Window 65160</b> — размер окна изменился: работает механизм «скользящего окна»."]),
 ("Третий этап рукопожатия (ACK)", PP + "s18_1.png", [
  "Сам пакет, который мы рассмотрим изнутри.",
  "Порты снова поменялись местами: это данные от клиента для сервера.",
  "<b class='mono'>Sequence Number: 1</b>, <b class='mono'>raw: 3638817701</b> — закономерное +1. <b class='mono'>Acknowledgment number: 1</b> и <b class='mono'>raw: 1565342373</b> — +1 к начальному номеру сервера.",
  "Флаг <b>ACK</b> — подтверждение принятых данных.",
  "<b class='mono'>Window 502</b> — окно меняется каждый раз в зависимости от сторон и загруженности сети."])]
def _ws(i, t, src, items):
    li = "".join(f'<li><span class="badge">{k+1}</span><span>{x}</span></li>' for k, x in enumerate(items))
    return (f"Wireshark {i}", "Установка соединения", "Установка TCP-соединения в Wireshark",
      f'<div class="wsx"><figure class="figx"><img src="{_jpg(src, 1600, 80)}" alt="{t}"></figure><div><h3 class="wsh">{t}</h3><ol class="steps sm">{li}</ol></div></div>', "figs")
_new = []
for it in S:
    _new.append(it)
    if it[0] == "Wireshark":
        _new += [_ws(i+1, *w) for i, w in enumerate(WSX)]
    for a, f in FIGS:
        if a == it[0]: _new.append(f)
S[:] = _new
# ==== Wireshark вёрсткой (в стиле ARP-слайда) ====
def _b(n): return f'<span class="wn">{n}</span>'
def _hl(txt, n=None): return f'<span class="whl">{_b(n) if n else ""}{txt}</span>'
_PK = [("4836","23.948769626","10.25.200.60","62.109.1.166","TCP","74","54824 → 443 [SYN] Seq=0 Win=64240 Len=0"),
       ("4845","23.993051706","62.109.1.166","10.25.200.60","TCP","74","443 → 54824 [SYN, ACK] Seq=0 Ack=1 Win=65160 Len=0"),
       ("4846","23.993083306","10.25.200.60","62.109.1.166","TCP","66","54824 → 443 [ACK] Seq=1 Ack=1 Win=502 Len=0"),
       ("4847","23.993585209","10.25.200.60","62.109.1.166","TLSv1.3","2137","Client Hello")]
def _flags(syn, ack, nsyn=None, nack=None):
    rows = [("000. .... ....", "Reserved: Not set"), ("...0 .... ....", "Nonce: Not set"),
            (".... 0... ....", "Congestion Window Reduced (CWR): Not set"), (".... .0.. ....", "ECN-Echo: Not set"),
            (".... ..0. ....", "Urgent: Not set"),
            (f".... ...{1 if ack else 0} ....", f"Acknowledgment: {'Set' if ack else 'Not set'}"),
            (".... .... 0...", "Push: Not set"), (".... .... .0..", "Reset: Not set"),
            (f".... .... ..{1 if syn else 0}.", f"Syn: {'Set' if syn else 'Not set'}"), (".... .... ...0", "Fin: Not set")]
    out = ""
    for bits, t in rows:
        line = f"{bits} = {t}"
        if t.startswith("Syn") and syn: line = _hl(line, nsyn)
        if t.startswith("Acknowledgment") and ack: line = _hl(line, nack)
        out += f'<div class="wl i3">{line}</div>'
    return out
def wshark(sel, src, dst, sp, dp, seq, seqraw, nxt, ackn, ackraw, flagcode, syn, ack, win, marks):
    rows = ""
    for i, r in enumerate(_PK):
        c = ' class="sel"' if i == sel else ""
        info = (_b(1) + r[6]) if i == sel else r[6]
        rows += f'<tr{c}><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td><td>{info}</td></tr>'
    fl = "SYN" if syn and not ack else "SYN, ACK" if syn else "ACK"
    d = (f'<div class="wl">▸ Frame {_PK[sel][0]}: {_PK[sel][5]} bytes on wire, {_PK[sel][5]} bytes captured</div>'
         f'<div class="wl">▸ Internet Protocol Version 4, Src: {src}, Dst: {dst}</div>'
         f'<div class="wl">▾ Transmission Control Protocol, Src Port: {sp}, Dst Port: {dp}, Seq: {seq}</div>'
         f'<div class="wl i1">{_hl(f"Source Port: {sp}", 2)}</div><div class="wl i1">{_hl(f"Destination Port: {dp}")}</div>'
         f'<div class="wl i1">{_hl(f"Sequence Number: {seq}  (relative sequence number)", 3)}</div>'
         f'<div class="wl i1">{_hl(f"Sequence Number (raw): {seqraw}")}</div>'
         f'<div class="wl i1">{_hl(f"[Next Sequence Number: {nxt}  (relative sequence number)]")}</div>'
         f'<div class="wl i1">{_hl(f"Acknowledgment Number: {ackn}")}</div><div class="wl i1">{_hl(f"Acknowledgment number (raw): {ackraw}")}</div>'
         f'<div class="wl i1 dim">1010 .... = Header Length: 40 bytes (10)</div>'
         f'<div class="wl i1">▾ Flags: {flagcode} ({fl})</div>' + _flags(syn, ack, marks.get("syn"), marks.get("ack")) +
         f'<div class="wl i1">{_hl(f"Window: {win}", marks["win"])}</div>')
    return ('<div class="wsk"><table class="wst"><thead><tr><th>No.</th><th>Time</th><th>Source</th><th>Destination</th><th>Protocol</th><th>Length</th><th>Info</th></tr></thead>'
            f'<tbody>{rows}</tbody></table><div class="wsd">{d}</div></div>')
WSV = [wshark(0,"10.25.200.60","62.109.1.166",54824,443,0,3638817700,1,0,0,"0x002",True,False,64240,{"syn":4,"win":5}),
       wshark(1,"62.109.1.166","10.25.200.60",443,54824,0,1565342372,1,1,3638817701,"0x012",True,True,65160,{"ack":4,"syn":5,"win":6}),
       wshark(2,"10.25.200.60","62.109.1.166",54824,443,1,3638817701,1,1,1565342373,"0x010",False,True,502,{"ack":4,"win":5})]
for k, it in enumerate(S):
    if it[0].startswith("Wireshark ") and it[0][-1].isdigit():
        i = int(it[0][-1]) - 1
        t, _src, items = WSX[i]
        li = "".join(f'<li><span class="badge wbad">{n+1}</span><span>{x}</span></li>' for n, x in enumerate(items))
        S[k] = (it[0], it[1], it[2], f'<div class="wsx">{WSV[i]}<div><h3 class="wsh">{t}</h3><ol class="steps sm">{li}</ol></div></div>', "figs")
    if it[0] == "Флаги в Wireshark":
        S[k] = (it[0], it[1], it[2], '<div class="wsk" style="max-width:62rem;margin:0 auto"><div class="wsd">'
                '<div class="wl">▾ Flags: 0x002 (SYN)</div>' + _flags(True, False, 1) + '</div></div>'
                '<p class="p sm figcap">При установке соединения в заголовке TCP выставлен только флаг SYN, остальные флаги сброшены.</p>', "figs")

ANIM_LOOP = set()
ANIM_ONCE = {"Мультиплексирование", "Адресация", "Сегментация", "Сокеты", "Рукопожатие", "Рукопожатие: номера", "Рукопожатие: числа", "Передача: Seq и Ack", "Передача: числовой пример", "Окно: принцип", "Окно: пример", "Потеря данных", "Завершение сеанса", "Завершение: детали", "Управление потоком", "UDP: функции", "UDP: датаграммы", "Окно: схема", "Завершение: номера"}

render()
