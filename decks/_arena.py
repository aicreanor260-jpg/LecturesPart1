# -*- coding: utf-8 -*-
"""Инфографики автора (тема «арена») — вёрсткой и SVG с анимацией вместо картинок.

Слайд = подзаголовок-лента + свиток-пояснение + сцена SVG (коммутаторы-«сундуки», ПК, кабели, конверты-кадры,
MAC-таблицы, которые заполняются по ходу анимации) + карточки шагов 1-2-3 + нижняя плашка.
"""
import itertools

_ID = itertools.count(1)
GOLD, NAVY, BLUE, PURP, LIL = "#e8b84a", "#13286b", "#3570dd", "#6a35c9", "#d8c8f5"
CAB = {"b": "#36b9ff", "y": "#ffc93c", "p": "#b46bff", "r": "#ff4d4d", "g": "#4cd964", "w": "#cfd8e3"}


# ------------------------------------------------------------------ спрайты
def sw(x, y, name, w=170, ports=5, crown=True):
    h2 = w // 2
    pw = (w - 40) / ports
    g = ['<g transform="translate(%d,%d)">' % (x, y),
         '<polygon points="%d,-20 %d,-46 %d,-46 %d,-20" fill="#4d86ee" stroke="%s" stroke-width="3" stroke-linejoin="round"/>'
         % (-h2, -h2 + 20, h2 - 20, h2, GOLD),
         '<rect x="%d" y="-20" width="%d" height="58" rx="7" fill="#1f3f9c" stroke="%s" stroke-width="3"/>' % (-h2, w, GOLD)]
    if crown:
        g.append('<path d="M-14,-30 l5,-10 l9,7 l9,-7 l5,10 z" fill="%s" stroke="#8a5a10" stroke-width="1.2"/>' % GOLD)
    for i in range(ports):
        px = -h2 + 20 + i * pw
        g.append('<rect x="%.1f" y="-6" width="%.1f" height="22" rx="2" fill="#0c1430" stroke="#9fb3d9" stroke-width="1.2"/>' % (px + 2, pw - 5))
        g.append('<circle cx="%.1f" cy="22" r="2.6" fill="#5dff7a"><animate attributeName="opacity" values="1;.25;1" dur="%.1fs" '
                 'repeatCount="indefinite" begin="%.1fs"/></circle>' % (px + pw / 2, 0.7 + (i % 3) * 0.35, i * 0.17))
    g.append('<rect x="-42" y="44" width="84" height="28" rx="7" fill="%s" stroke="%s" stroke-width="2.4"/>'
             '<text x="0" y="64" text-anchor="middle" fill="#fff" font-weight="900" font-size="18">%s</text></g>' % (NAVY, GOLD, name))
    return "".join(g)


def rack(x, y, w=260, ports=10, name=""):
    """Широкий коммутатор (для пучков из 4–9 линков)."""
    h2 = w // 2
    g = ['<g transform="translate(%d,%d)">' % (x, y),
         '<polygon points="%d,-24 %d,-50 %d,-50 %d,-24" fill="#4d86ee" stroke="%s" stroke-width="3"/>' % (-h2, -h2 + 22, h2 - 22, h2, GOLD),
         '<rect x="%d" y="-24" width="%d" height="70" rx="8" fill="#1f3f9c" stroke="%s" stroke-width="3"/>' % (-h2, w, GOLD),
         '<path d="M-14,-34 l5,-10 l9,7 l9,-7 l5,10 z" fill="%s"/>' % GOLD]
    pw = (w - 30) / ports
    for i in range(ports):
        px = -h2 + 15 + i * pw
        g.append('<rect x="%.1f" y="-8" width="%.1f" height="22" rx="2" fill="#0c1430" stroke="#9fb3d9"/>' % (px + 2, pw - 5))
        g.append('<circle cx="%.1f" cy="24" r="2.6" fill="#5dff7a"><animate attributeName="opacity" values="1;.3;1" dur="%.1fs" '
                 'repeatCount="indefinite"/></circle>' % (px + pw / 2, 0.6 + (i % 4) * 0.3))
    if name:
        g.append('<rect x="-44" y="52" width="88" height="28" rx="7" fill="%s" stroke="%s" stroke-width="2.4"/>'
                 '<text x="0" y="72" text-anchor="middle" fill="#fff" font-weight="900" font-size="18">%s</text>' % (NAVY, GOLD, name))
    g.append("</g>")
    return "".join(g)


def rack_ports(x, w=260, ports=10):
    pw = (w - 30) / ports
    return [x - w // 2 + 15 + i * pw + pw / 2 for i in range(ports)]


def pc(x, y, name):
    return ('<g transform="translate(%d,%d)">'
            '<rect x="-44" y="-70" width="88" height="62" rx="7" fill="#2b5fd0" stroke="%s" stroke-width="3"/>'
            '<rect x="-36" y="-63" width="72" height="47" rx="3" fill="#8fd3ff"/>'
            '<path d="M-10,-38 l4,-8 l6,5 l6,-5 l4,8 z" fill="%s"/>'
            '<rect x="-8" y="-8" width="16" height="10" fill="#1f3f9c"/><rect x="-30" y="2" width="60" height="7" rx="2" fill="#1f3f9c" stroke="%s" stroke-width="1.5"/>'
            '<rect x="-38" y="16" width="76" height="26" rx="7" fill="%s" stroke="%s" stroke-width="2.4"/>'
            '<text x="0" y="35" text-anchor="middle" fill="#fff" font-weight="900" font-size="17">%s</text></g>'
            % (x, y, GOLD, GOLD, GOLD, NAVY, GOLD, name))


def pill(x, y, text, kind="n", size=14, anchor="middle"):
    """Подпись-плашка: n — тёмная (порт), g — золотая, p — фиолетовая, w — белая, r — красная."""
    fill, col, st = {"n": (NAVY, "#fff", "#7f9be0"), "g": ("#fff3c4", "#3a2a00", GOLD), "p": (PURP, "#fff", "#c9a8ff"),
                     "w": ("#ffffff", "#13286b", "#9fb3d9"), "r": ("#ffe3e3", "#b00000", "#ff6b6b"), "y": ("#ffd43b", "#3a2a00", "#a07415")}[kind]
    w = int(len(text) * size * 0.58) + 18
    x0 = x - w / 2 if anchor == "middle" else x
    return ('<rect x="%.0f" y="%d" width="%d" height="%d" rx="%d" fill="%s" stroke="%s" stroke-width="1.8"/>'
            '<text x="%.0f" y="%d" text-anchor="middle" fill="%s" font-weight="800" font-size="%d">%s</text>'
            % (x0, y - size - 2, w, size + 12, (size + 12) // 2, fill, st, x0 + w / 2, y + 3, col, size, text))


def cable(d, c="b", w=7, flow=True, dash=False, op=1):
    col = CAB.get(c, c)
    s = ('<path d="%s" fill="none" stroke="%s" stroke-width="%d" stroke-linecap="round" opacity="%.2f" filter="url(#glw)" %s/>'
         % (d, col, w, op * .55, 'stroke-dasharray="14 10"' if dash else ""))
    s += '<path d="%s" fill="none" stroke="%s" stroke-width="%d" stroke-linecap="round" opacity="%.2f" %s/>' % (
        d, col, max(w - 3, 2), op, 'stroke-dasharray="14 10"' if dash else "")
    if flow:
        s += ('<path d="%s" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="6 16" opacity=".85">'
              '<animate attributeName="stroke-dashoffset" from="44" to="0" dur="1s" repeatCount="indefinite"/></path>' % d)
    return s


def _kt(t0, t1, T):
    return max(0.0, min(t0 / T, 1.0)), max(0.0, min(t1 / T, 1.0))


def env(path, t0, d, T, red=False, label=""):
    """Конверт-кадр едет по path в интервале [t0, t0+d] цикла T секунд."""
    s, e = _kt(t0, t0 + d, T)
    fill = "#ff8f8f" if red else "#ffd166"
    lab = ('<text x="0" y="-16" text-anchor="middle" font-size="12" font-weight="800" fill="#3a2a00">%s</text>' % label) if label else ""
    return ('<g opacity="0"><animate attributeName="opacity" calcMode="discrete" values="0;1;0" keyTimes="0;%.4f;%.4f" dur="%ss" repeatCount="indefinite"/>'
            '<animateMotion dur="%ss" repeatCount="indefinite" calcMode="linear" keyPoints="0;0;1;1" keyTimes="0;%.4f;%.4f;1" path="%s"/>'
            '<g transform="translate(-17,-12)" filter="url(#glw)"><rect width="34" height="24" rx="3" fill="%s" stroke="#9a6b10" stroke-width="2"/>'
            '<path d="M2,2 L17,13 L32,2" fill="none" stroke="#9a6b10" stroke-width="2"/></g>%s</g>'
            % (s, e, T, T, s, e, path, fill, lab))


def show(t0, T, t1=None, inner=""):
    """Группа видна с t0 до t1 (или до конца цикла)."""
    s = t0 / T
    if t1 is None:
        return ('<g opacity="0"><animate attributeName="opacity" calcMode="discrete" values="0;1" keyTimes="0;%.4f" dur="%ss" '
                'repeatCount="indefinite"/>%s</g>' % (s, T, inner))
    return ('<g opacity="0"><animate attributeName="opacity" calcMode="discrete" values="0;1;0" keyTimes="0;%.4f;%.4f" dur="%ss" '
            'repeatCount="indefinite"/>%s</g>' % (s, t1 / T, T, inner))


def mactab(x, y, title, rows, w=300, T=6, note=""):
    """MAC-таблица: rows — [(mac, порт, t_появления|None, t_зачёркивания|None, выделить)]"""
    R = 31
    n = max(len(rows), 1)
    g = ['<g transform="translate(%d,%d)">' % (x, y),
         '<rect x="0" y="0" width="%d" height="%d" rx="10" fill="#2a1466" stroke="%s" stroke-width="3"/>' % (w, 72 + R * n + (24 if note else 0), GOLD),
         '<text x="%d" y="27" text-anchor="middle" fill="#fff" font-weight="900" font-size="19">%s</text>' % (w // 2, title),
         '<rect x="8" y="38" width="%d" height="26" fill="%s"/>' % (w - 16, LIL),
         '<text x="%d" y="57" text-anchor="middle" font-size="15" font-weight="800" fill="#2a1466">MAC-адрес</text>' % ((w - 16) * 0.33 + 8),
         '<text x="%d" y="57" text-anchor="middle" font-size="15" font-weight="800" fill="#2a1466">Порт</text>' % ((w - 16) * 0.83 + 8)]
    if not rows:
        g.append('<rect x="8" y="66" width="%d" height="%d" fill="#fff"/><text x="%d" y="87" text-anchor="middle" font-size="16" fill="#555" '
                 'font-weight="800">Пусто</text>' % (w - 16, R - 2, w // 2))
    for k, (mac, port, t_on, t_x, hl) in enumerate(rows):
        yy = 66 + k * R
        cell = ('<rect x="8" y="%d" width="%d" height="%d" fill="#fff"/><rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
                '<text x="%d" y="%d" text-anchor="middle" font-size="16" font-weight="800" fill="#13286b">%s</text>'
                '<text x="%d" y="%d" text-anchor="middle" font-size="17" font-weight="900" fill="#13286b">%s</text>'
                % (yy, w - 16, R - 2, int((w - 16) * 0.66) + 8, yy, int((w - 16) * 0.34), R - 2, "#ffd43b" if hl else "#eef2ff",
                   (w - 16) * 0.33 + 8, yy + 20, mac, (w - 16) * 0.83 + 8, yy + 20, port))
        if t_x is not None:
            cell += show(t_x, T, None, '<path d="M12,%d h%d" stroke="#e03131" stroke-width="3"/><rect x="8" y="%d" width="%d" height="%d" '
                                       'fill="#ff6b6b" opacity=".25"/>' % (yy + 14, w - 24, yy, w - 16, R - 2))
        g.append(show(t_on, T, None, cell) if t_on is not None else cell)
    if note:
        g.append('<text x="%d" y="%d" text-anchor="middle" font-size="14" font-weight="800" fill="#ffd43b">%s</text>' % (w // 2, 86 + R * n, note))
    g.append("</g>")
    return "".join(g)


def ring(x, y, h=86, label="Po1", T=None):
    return ('<ellipse cx="%d" cy="%d" rx="22" ry="%d" fill="#b46bff" fill-opacity=".18" stroke="#c48bff" stroke-width="4" filter="url(#glw)">'
            '<animate attributeName="stroke-opacity" values="1;.45;1" dur="1.6s" repeatCount="indefinite"/></ellipse>' % (x, y, h // 2)
            + pill(x, y + 5, label, "p", 14))


def tube(x1, x2, y, h=44, label=""):
    s = ('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="#b46bff" fill-opacity=".22" stroke="#d3a6ff" stroke-width="3" filter="url(#glw)">'
         '<animate attributeName="fill-opacity" values=".15;.35;.15" dur="2s" repeatCount="indefinite"/></rect>' % (x1, y - h // 2, x2 - x1, h, h // 2))
    if label:
        s += pill((x1 + x2) / 2, y - h // 2 - 12, label, "p", 14)
    return s


def xmark(x, y, T=None, t0=0, s=14):
    m = '<path d="M%d,%d l%d,%d m0,-%d l-%d,%d" stroke="#ff2d2d" stroke-width="6" stroke-linecap="round" filter="url(#glw)"/>' % (
        x - s, y - s, 2 * s, 2 * s, 2 * s, 2 * s, 2 * s)
    return show(t0, T, None, m) if T else m


def scene(w, h, inner):
    i = next(_ID)
    inner = inner.replace('url(#glw)', 'url(#glw%d)' % i)
    return ('<div class="ar-scene"><svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" '
            'font-family="Nunito,Segoe UI,sans-serif"><defs><filter id="glw%d" filterUnits="userSpaceOnUse" x="-2000" y="-2000" width="6000" height="6000">'
            '<feGaussianBlur stdDeviation="3.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
            '%s</svg></div>' % (w, h, i, inner))


# ------------------------------------------------------------------ вёрстка слайда
def steps(items):
    """items — [(заголовок, текст)] → карточки на свитках с номерами-щитами, появляются по шагам."""
    out = []
    for k, (t, d) in enumerate(items, 1):
        out.append('<div class="ar-st step"><b class="ar-n">%d</b><div><h4>%s</h4>%s</div></div>' % (k, t, "<p>%s</p>" % d if d else ""))
    return '<div class="ar-steps n%d">%s</div>' % (len(items), "".join(out))


def layout(sub="", scroll="", scn="", st=None, foot="", note="", extra=""):
    h = ""
    if sub:
        h += '<div class="ar-sub">%s</div>' % sub
    if scroll:
        h += '<div class="ar-scroll">%s</div>' % scroll
    h += scn + extra
    if st:
        h += steps(st)
    if foot or note:
        h += '<div class="ar-foot step">%s%s</div>' % ('<span class="ar-fi">♛</span><b>%s</b>' % foot if foot else "",
                                                      '<small>%s</small>' % note if note else "")
    return '<div class="ar">%s</div>' % h


def table(head, rows, marks=None):
    """Таблица в стиле инфографики; marks — [True/False/None] по строкам: зелёная ✓ / красная ✗."""
    tr = []
    for k, r in enumerate(rows):
        m = marks[k] if marks else None
        cls = ' class="ok"' if m is True else (' class="no"' if m is False else "")
        cells = "".join("<td>%s</td>" % c for c in r)
        if m is not None:
            cells = cells[:-5] + "</td>"
            ic = '<i class="ar-ok">✔</i>' if m else '<i class="ar-no">✘</i>'
            cells = "".join("<td>%s</td>" % c for c in r[:-1]) + "<td>%s %s</td>" % (ic, r[-1])
        tr.append("<tr%s>%s</tr>" % (cls, cells))
    return '<table class="ar-tab"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % ("".join("<th>%s</th>" % x for x in head), "".join(tr))


CSS = r"""
.ar{display:flex;flex-direction:column;align-items:stretch;gap:calc(8px*var(--fz,1));height:100%;min-height:0}
.ar-sub{align-self:center;background:linear-gradient(180deg,#7b45e0,#5420b0);color:#fff;font:900 calc(clamp(15px,1.45vw,26px)*var(--fz,1))/1.15 var(--fh,var(--f));
 padding:7px 30px;border:3px solid #e8b84a;border-radius:12px;box-shadow:0 4px 0 #2a0f6a,0 8px 18px rgba(0,0,0,.35);text-align:center;letter-spacing:.2px}
.ar-scroll{align-self:center;background:linear-gradient(180deg,#fff6dc,#f1dcab);color:#3a2a10;font:800 calc(clamp(13px,1.08vw,19px)*var(--fz,1))/1.3 var(--f);
 padding:6px 26px;border:2px solid #c9962e;border-radius:10px;box-shadow:0 3px 10px rgba(0,0,0,.25);text-align:center;max-width:92%}
.ar-scene{flex:1 1 auto;min-height:0;display:flex;justify-content:center;background:rgba(10,40,60,.22);border:2px solid rgba(232,184,74,.55);
 border-radius:16px;padding:4px;box-shadow:inset 0 0 30px rgba(0,0,0,.25)}
.ar-scene svg{width:100%;height:100%;max-height:56vh;display:block}
.ar-steps{display:grid;gap:12px;grid-template-columns:repeat(3,1fr)}
.ar-steps.n2{grid-template-columns:repeat(2,1fr)}.ar-steps.n4{grid-template-columns:repeat(4,1fr)}
.ar-steps.n5{grid-template-columns:repeat(5,1fr)}.ar-steps.n6{grid-template-columns:repeat(3,1fr);gap:8px}
.ar-steps.n6 .ar-st{padding:4px 10px}.ar-steps.n6 .ar-n{width:calc(30px*var(--fz,1));height:calc(32px*var(--fz,1));font-size:calc(17px*var(--fz,1))}.ar-steps.n1{grid-template-columns:1fr}
.ar-st{display:flex;gap:10px;align-items:center;background:linear-gradient(180deg,#fff7df,#f0d9a2);border:3px solid #c9962e;border-radius:12px;
 padding:8px 12px;box-shadow:0 4px 0 #8a5a10,0 8px 16px rgba(0,0,0,.3);position:relative}
.ar-st h4{margin:0;color:#13286b;font:900 calc(clamp(13px,1.12vw,20px)*var(--fz,1))/1.15 var(--fh,var(--f))}
.ar-st p{margin:3px 0 0!important;color:#3a2a10;font:700 calc(clamp(11.5px,.92vw,16px)*var(--fz,1))/1.25 var(--f)}
.ar-n{flex:0 0 auto;width:calc(40px*var(--fz,1));height:calc(44px*var(--fz,1));display:grid;place-items:center;color:#fff;font:900 calc(22px*var(--fz,1))/1 var(--fh,var(--f));
 background:linear-gradient(180deg,#3d6fe0,#13286b);border:3px solid #e8b84a;border-radius:10px 10px 50% 50%;box-shadow:0 3px 0 #8a5a10}
.ar-steps:not(.n6):not(.n5) .ar-st+.ar-st::before{content:"➜";position:absolute;left:-17px;top:50%;transform:translateY(-50%);color:#e8b84a;
 font-size:22px;text-shadow:0 2px 0 #8a5a10}
.ar-foot{display:flex;align-items:center;gap:14px;background:linear-gradient(180deg,#1d3a8f,#0f2160);color:#fff;border:3px solid #e8b84a;border-radius:14px;
 padding:8px 18px;box-shadow:0 4px 0 #8a5a10;font:800 calc(clamp(13px,1.1vw,20px)*var(--fz,1))/1.25 var(--f)}
.ar-foot b{flex:1}.ar-foot small{flex:0 1 34%;font:700 calc(clamp(10.5px,.82vw,14px)*var(--fz,1))/1.3 var(--f);color:#ffe9a8;border-left:2px solid rgba(232,184,74,.6);padding-left:12px}
.ar-fi{color:#ffd43b;font-size:1.6em;line-height:1}
.ar-tab{width:100%;border-collapse:separate;border-spacing:0;border:3px solid #c9962e;border-radius:12px;overflow:hidden;box-shadow:0 4px 0 #8a5a10;
 font:800 calc(clamp(13px,1.1vw,20px)*var(--fz,1))/1.25 var(--f)}
.ar-tab th{background:linear-gradient(180deg,#2f5fd0,#13286b);color:#fff;padding:7px 12px;text-align:left}
.ar-tab td{background:#fff8e6;color:#13286b;padding:6px 12px;border-top:1px solid #e3cf9a}
.ar-tab tr.ok td:last-child{background:#dcf7d6;color:#1b6e1b}.ar-tab tr.no td:last-child{background:#ffdede;color:#a10f0f}
.ar-ok{color:#1fae3b;font-style:normal}.ar-no{color:#e03131;font-style:normal}
.ar-two{display:grid;grid-template-columns:1fr 1fr;gap:12px;flex:1 1 auto;min-height:0}
.ar-card{background:linear-gradient(180deg,#fff7df,#f0d9a2);border:3px solid #c9962e;border-radius:14px;padding:10px 14px;box-shadow:0 4px 0 #8a5a10;color:#13286b}
.ar-card h4{margin:0 0 6px;font:900 calc(clamp(14px,1.2vw,22px)*var(--fz,1))/1.15 var(--fh,var(--f))}
.ar-card p,.ar-card li{color:#3a2a10;font:700 calc(clamp(12px,1vw,18px)*var(--fz,1))/1.3 var(--f)}
.ar-goals{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;flex:1 1 auto;align-content:center}
.ar-goal{display:flex;gap:16px;align-items:center;background:linear-gradient(180deg,#fff7df,#f0d9a2);border:3px solid #c9962e;border-radius:16px;padding:16px 20px;
 box-shadow:0 5px 0 #8a5a10,0 10px 20px rgba(0,0,0,.3)}
.ar-goal .ar-n{width:calc(54px*var(--fz,1));height:calc(60px*var(--fz,1));font-size:calc(28px*var(--fz,1))}
.ar-goal h4{margin:0;color:#13286b;font:900 calc(clamp(15px,1.35vw,24px)*var(--fz,1))/1.2 var(--fh,var(--f))}
.ar-goal p{margin:4px 0 0!important;color:#3a2a10;font:700 calc(clamp(12px,1vw,18px)*var(--fz,1))/1.3 var(--f)}
"""


# холст сцены подгоняется под рисунок (убираем пустые поля), как только слайд впервые показан
JS = r"""
(function(){function fit(){var left=0;document.querySelectorAll('.ar-scene svg:not([data-fit])').forEach(function(s){
 var b;try{b=s.getBBox();}catch(e){b=null;}if(!b||!b.width){left++;return;}
 var p=Math.max(b.width,b.height)*0.025;s.setAttribute('viewBox',[b.x-p,b.y-p,b.width+2*p,b.height+2*p].map(function(v){return v.toFixed(1);}).join(' '));
 s.setAttribute('data-fit','1');});if(left)setTimeout(fit,400);}
 if(document.readyState!=='loading')fit();else document.addEventListener('DOMContentLoaded',fit);})();
"""
