# -*- coding: utf-8 -*-
"""Окно анализатора трафика (pptx 9–11): скриншоты Wireshark перерисованы окном в стиле деки.
Строки — дословно со скриншотов; красные рамки pptx — подсвеченные блоки с номерами из текста слайда."""
from _sw_lib import _esc


def ws(row, lines, marks=None, title="Wireshark"):
    """row: (No, Time, Source, Destination, Protocol, Length, Info);
    lines: строки дерева, отступ — пробелами, '>'/'v' в начале — свёрнуто/развёрнуто;
    marks: {номер строки: метка} — подсветка (рамка pptx); метка 'row' — строка списка пакетов.
    Строки с одинаковой меткой подряд объединяются в один блок."""
    marks = marks or {}
    head = "".join("<th>%s</th>" % h for h in ("No.", "Time", "Source", "Destination", "Protocol", "Length", "Info"))
    cells = "".join("<td>%s</td>" % _esc(c) for c in row[:6])
    rm = marks.get("row")
    info = '<td class="%s">%s%s</td>' % ("wsm" if rm else "", _esc(row[6]), '<i class="wsn">%s</i>' % rm if rm else "")
    out, prev = [], None
    for i, ln in enumerate(lines):
        m = marks.get(i)
        k = len(ln) - len(ln.lstrip(" "))
        s = ln.strip()
        arr = ""
        if s[:2] in ("> ", "v "):
            arr = '<span class="wsa">%s</span>' % ("›" if s[0] == ">" else "⌄")
            s = s[2:]
        cls = "wsl"
        if m:
            cls += " wsh"
            if m != prev:
                cls += " wsh0"
        nxt = marks.get(i + 1)
        if m and nxt != m:
            cls += " wsh1"
        badge = '<i class="wsn">%s</i>' % m if m and m != prev else ""
        out.append('<div class="%s" style="padding-left:%gem">%s%s%s</div>' % (cls, .6 + k * .55, arr, _esc(s), badge))
        prev = m
    return ('<div class="wswin"><div class="wsbar"><i></i><i></i><i></i><span>%s</span></div>'
            '<table class="wslist"><thead><tr>%s</tr></thead><tbody><tr class="wssel">%s%s</tr></tbody></table>'
            '<div class="wstree">%s</div></div>' % (title, head, cells, info, "".join(out)))


CSS = r"""
.wswin{background:#0a1230;border:1.5px solid rgba(92,190,255,.75);border-radius:12px;overflow:hidden;
 box-shadow:0 0 22px rgba(58,160,255,.3);font:500 clamp(11px,.86vw,16.5px)/1.32 var(--m);color:#dfe9ff}
.wsbar{display:flex;align-items:center;gap:6px;padding:6px 10px;background:#16224d;color:#cfd8ff;font:700 13px/1 var(--m)}
.wsbar i{width:11px;height:11px;border-radius:50%;background:#ff5f57}.wsbar i+i{background:#febc2e}.wsbar i+i+i{background:#28c840}
.wsbar span{margin-left:8px}
.wslist{width:100%;border-collapse:collapse}
.wslist th{background:#111c42;color:#9fb6e8;text-align:left;font-weight:700;padding:4px 8px;font-size:.92em}
.wslist td{padding:4px 8px;white-space:nowrap}
.wssel{background:#1d4f9a;color:#fff}
.wslist td.wsm{outline:2.5px solid #ff5a6a;outline-offset:-3px;position:relative}
.wstree{padding:6px 0 8px;border-top:1px solid #1f2d5c}
.wsl{white-space:pre;position:relative;padding-right:46px}
.wsa{display:inline-block;width:1.1em;color:#7ea4e8}
.wsh{border-left:2.5px solid #ff5a6a;border-right:2.5px solid #ff5a6a;background:rgba(255,90,106,.10)}
.wsh0{border-top:2.5px solid #ff5a6a}.wsh1{border-bottom:2.5px solid #ff5a6a}
.wsn{position:absolute;right:6px;top:50%;transform:translateY(-50%);font:900 .95em/1 var(--f);font-style:normal;
 background:#ffc94a;color:#08142e;border-radius:50%;width:1.6em;height:1.6em;display:grid;place-items:center}
"""
