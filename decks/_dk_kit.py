# -*- coding: utf-8 -*-
"""Блоки дек-спутников, повторяющие содержимое pptx в стиле деки:
кадр из цветных полей, блок-схема прохождения кадра, таблицы MAC, терминал, слайд «как в pptx»."""

from _sw_lib import SL, slide, head, sc, grow, col, card, p, step, cli, _esc

# поле кадра → класс цвета
_FIELD = [("802.1Q", "tg"), ("C-VLAN", "tg"), ("S-VLAN", "ts"), ("TPID", "tg"), ("TCI", "tg"),
          ("EtherType", "et"), ("Данные", "da"), ("FCS", "fc"), ("MAC", "ma")]


def _fcls(name):
    for k, c in _FIELD:
        if k in name:
            return c
    return "ma"


def frame(cells, cap=""):
    """[MAC ПК2 | MAC ПК1 | 802.1Q: VID 10 | EtherType | Данные | FCS] — строка цветных полей."""
    tds = "".join('<span class="fr-%s">%s</span>' % (_fcls(c), c) for c in cells)
    c = '<div class="frcap">%s</div>' % cap if cap else ""
    return '<div class="frw">%s<div class="frm">%s</div></div>' % (c, tds)


def fr(s, cap=""):
    """frame из строки pptx вида '[A | B | C]'."""
    return frame([x.strip() for x in s.strip().strip("[]").split("|")], cap)


def flow(columns):
    """Вертикальная блок-схема: columns = [[{'t': 'device'|'edge', 'text': ...}, ...], ...]."""
    out = []
    for colm in columns:
        items = []
        for it in colm:
            t = _esc(it["text"]).replace("\n", "<br>")
            if it["t"] == "device":
                items.append('<div class="fl-dev">%s</div>' % t)
            else:
                items.append('<div class="fl-edge"><i>↓</i>%s</div>' % t)
        out.append('<div class="fl-col">%s</div>' % "".join(items))
    return '<div class="flow">%s</div>' % "".join(out)


def mtables(tbls, after=""):
    out = []
    for t in tbls:
        th = "".join("<th>%s</th>" % _esc(h) for h in t.get("cols", []))
        rows = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % _esc(str(c)) for c in r) for r in t.get("rows", []))
        ttl = '<div class="mt-t">%s</div>' % _esc(t["title"]) if t.get("title") else ""
        note = '<div class="mt-n">%s</div>' % _esc(t["note"]) if t.get("note") else ""
        out.append('%s<div class="tw mt"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>%s'
                   % (ttl, th, rows, note))
    if after:
        out.append('<div class="mt-n">%s</div>' % _esc(after))
    return '<div class="mtw">%s</div>' % "".join(out)


def term(lines, title=""):
    """Экран консоли из pptx — построчно, как на скриншоте."""
    t = '<div class="clih">%s</div>' % _esc(title) if title else ""
    return '%s<pre class="cli term">%s</pre>' % (t, "\n".join(_esc(l) for l in lines))


def conf(lines, title="Конфигурация"):
    """Команды конфигурации: приглашение приглушено, команда выделена."""
    out = []
    for ln in lines:
        k = ln.find("#")
        if k > 0 and ("(" in ln[:k] or ln[:k].strip() in ("switch", "console")):
            out.append('<span class="p">%s</span><span class="k">%s</span>' % (_esc(ln[:k + 1]), _esc(ln[k + 1:])))
        else:
            out.append(_esc(ln))
    t = '<div class="clih">%s</div>' % _esc(title) if title else ""
    return '%s<pre class="cli">%s</pre>' % (t, "\n".join(out))


def txt(*paras, title="", tone="cy"):
    return card(title, p(*paras), tone)


def pslide(label, title, left, right=None, sub="", layout="g2"):
    """Слайд по pptx: слева текст, справа конфигурация / рисунок. Блоки появляются по шагам."""
    L = col(*[step(b) for b in left])
    if right is None:
        body = grow("g", L)
    else:
        body = grow(layout, L, col(*[step(b) for b in right]))
    slide(label, sc(head(title, sub), body))


def full(label, title, block, sub=""):
    slide(label, sc(head(title, sub), grow("g", col(block))))


CSS = r"""
/* крупный текст: слайды читаются с проектора */
.c p,ul.li li,.ir span{font-size:clamp(14px,1.32vw,26px)!important;line-height:1.42}
.ch h3{font-size:clamp(15px,1.4vw,28px)!important}
pre.cli{font-size:clamp(13px,1.15vw,22px)!important;line-height:1.5}
.clih{font-size:clamp(11px,.8vw,15px)!important}
.tw table{font-size:clamp(13px,1.05vw,20px)!important}
p.sub{font-size:clamp(13px,1.1vw,21px)!important}
.frw{margin:4px 0}
.frcap{font:700 clamp(11px,.8vw,15px)/1.3 var(--f);color:var(--soft);margin-bottom:5px}
.frm{display:flex;gap:4px;flex-wrap:wrap}
.frm span{flex:1 1 auto;text-align:center;padding:9px 10px;font:800 clamp(13px,1.12vw,21px)/1.2 var(--f);color:#1a1030;
 border:3px solid #0a1440;box-shadow:3px 3px 0 rgba(0,0,0,.45);white-space:nowrap}
.fr-ma{background:#9fd3ff}.fr-tg{background:#ffd23a}.fr-ts{background:#ff9a3d}.fr-et{background:#c9a8ff}
.fr-da{background:#ffc1dc}.fr-fc{background:#ff7a7a}
.th-base .frm span{border-color:#2a0a2a;border-radius:4px;transform:skew(-4deg)}
.flow{display:flex;gap:18px;justify-content:center;align-items:flex-start}
.fl-col{display:flex;flex-direction:column;align-items:center;gap:0;min-width:0;flex:1 1 0;max-width:340px}
.fl-dev{width:100%;text-align:center;padding:9px 12px;background:rgba(255,255,255,.95);color:#10183a;
 font:700 clamp(12px,.92vw,17px)/1.35 var(--f);border:3px solid #0a1440;box-shadow:4px 4px 0 rgba(0,0,0,.4)}
.th-base .fl-dev{border-color:#2a0a2a;border-radius:6px;box-shadow:5px 5px 0 #ff2e93}
.fl-edge{display:flex;flex-direction:column;align-items:center;padding:4px 6px;font:700 clamp(11.5px,.85vw,16px)/1.3 var(--f);
 color:var(--ink);text-align:center}
.fl-edge i{font-style:normal;font-size:20px;line-height:1;color:var(--cy)}
.mtw{display:flex;flex-direction:column;gap:6px}
.mt-t{font:800 clamp(11.5px,.85vw,16px)/1.3 var(--f);color:var(--ink);margin-top:4px}
.mt-n{font:600 clamp(11px,.78vw,15px)/1.4 var(--f);color:var(--soft)}
.tw.mt td,.tw.mt th{font-family:var(--m)}
pre.cli.term{background:#05060a;color:#e8e8e8;border-color:#666}
"""
