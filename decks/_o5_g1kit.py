# -*- coding: utf-8 -*-
"""Элементы группы g1 (обзор, принцип, недостатки, стоимость, Дейкстра 1–2): иконки и предметы в SVG.
Дополняет _o5_ikit, ничего в нём не меняя."""
from _o5_ikit import ICO, ICOFILL, puck, cross, line, chip  # noqa: F401

G1ICO = dict(ICO)
G1ICO.update({
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/>',
    "sync": '<path d="M19.5 9A8 8 0 0 0 5.2 7.2M4.5 15a8 8 0 0 0 14.3 1.8"/><path d="M5 3v4.5h4.5M19 21v-4.5h-4.5"/>',
    "weight": '<circle cx="12" cy="6" r="2.4"/><path d="M7.5 9h9l3 11.5h-15z"/>',
    "router": '<ellipse cx="12" cy="11" rx="8.5" ry="3.5"/><path d="M3.5 11v3.5c0 1.9 3.8 3.5 8.5 3.5s8.5-1.6 8.5-3.5V11M12 3v4.5"/>',
    "edge": '<circle cx="6" cy="18" r="2.8"/><circle cx="18" cy="6" r="2.8"/><path d="M8 16 16 8"/>',
    "book": '<path d="M3 5.5c3-1.3 6-1.3 9 .8 3-2.1 6-2.1 9-.8v13c-3-1.3-6-1.3-9 .8-3-2.1-6-2.1-9-.8z"/><path d="M12 6.3v13"/>',
    "calc": '<rect x="5" y="3" width="14" height="18" rx="2.4"/><path d="M8 7h8M8.5 11.5h.1M12 11.5h.1M15.5 11.5h.1M8.5 15h.1M12 15h.1M15.5 15h.1M8.5 18h.1M12 18h.1M15.5 18h.1"/>',
    "bulb": '<path d="M9 17.5h6M10 20.5h4M8.6 14.5A6 6 0 1 1 15.4 14.5c-.8.7-1.4 1.6-1.4 3h-4c0-1.4-.6-2.3-1.4-3z"/>',
    "check": '<circle cx="12" cy="12" r="8.6"/><path d="m8 12.2 2.8 2.8 5.4-5.6"/>',
    "arrow": '<path d="M4 12h15M13.5 6.5 19 12l-5.5 5.5"/>',
    "table": '<rect x="3.5" y="4.5" width="17" height="15" rx="2"/><path d="M3.5 9.5h17M9 9.5v10"/>',
    "swap": '<path d="M4 8.5h15M15 4.5l4 4-4 4M20 15.5H5M9 11.5l-4 4 4 4"/>',
    "ram": '<rect x="2.5" y="6" width="19" height="8" rx="1.4"/><path d="M6 9v2M9.5 9v2M14.5 9v2M18 9v2M4 14v3M8 14v3M12 14v3M16 14v3M20 14v3"/>',
    "doc": '<path d="M6 3h8.5L19 7.5V21H6z"/><path d="M14 3v5h5M9 12h7M9 15.5h7M9 19h4.5"/>',
    "net": '<rect x="9" y="3" width="6" height="5" rx="1"/><rect x="3" y="16" width="6" height="5" rx="1"/>'
           '<rect x="15" y="16" width="6" height="5" rx="1"/><path d="M12 8v4M6 16v-4h12v4"/>',
})


def g1icon(name, x, y, d=96, tone="p", ink="#1f1a33"):
    """Кружок-иконка (HTML-элемент), как icon() из _o5_ikit, но с расширенным набором."""
    fill = ICOFILL.get(tone, tone)
    return ('<svg class="ab" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx" viewBox="0 0 96 96">'
            '<circle cx="48" cy="48" r="46" style="fill:%s"/><g transform="translate(22 22) scale(2.15)" fill="none" '
            'stroke="%s" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">%s</g></svg>'
            % (x, y, d, d, fill, ink, G1ICO[name]))


def g1ico_svg(name, cx, cy, d=60, fill="#ff8fbf", ink="#1f1a33"):
    """Та же иконка, но внутри общего SVG-холста (центр cx, cy)."""
    s = d / 96.0
    return ('<g transform="translate(%.1f %.1f) scale(%.3f)"><circle cx="48" cy="48" r="46" style="fill:%s"/>'
            '<g transform="translate(22 22) scale(2.15)" fill="none" stroke="%s" stroke-width="1.9" '
            'stroke-linecap="round" stroke-linejoin="round">%s</g></g>' % (cx - d / 2, cy - d / 2, s, fill, ink, G1ICO[name]))


def g1t(x, y, text, fs=18, col="#1f1a33", anchor="middle", weight=700, extra=""):
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%.1f" font-weight="%d" style="fill:%s"%s>%s</text>'
            % (x, y, anchor, fs, weight, col, extra, text))


def g1xpuck(x, y, w=110, tone="b", label=None, fs=None):
    """Шайба, перечёркнутая красным крестом (посещённая вершина)."""
    return puck(x, y, w, tone, label, fs) + cross(x, y + w * .08, w * .3, "#e8245e", max(6, int(w * .07)))


def g1antpuck(x, y, w=150, tone="p", label=None):
    """Шайба с двумя антеннами (как роутеры на артах автора)."""
    top = {"p": "#f7a9c9", "b": "#9fcaf3"}[tone]
    out = {"p": "#e05a97", "b": "#3f86d8"}[tone]
    a = ""
    for k in (-1, 1):
        ax = x + k * w * .36
        a += ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" style="fill:%s;stroke:%s" stroke-width="2"/>'
              % (ax - w * .035, y - w * .5, w * .07, w * .55, w * .035, top, out))
    return a + puck(x, y, w, tone, label)


def g1cyl(x, y, w=80, h=100, fill="#e9ecf4", edge="#6b7385", band="#3f86d8"):
    """База данных — цилиндр с тремя секциями (левый верх x, y)."""
    ry = w * .18
    s = ('<path d="M%.1f %.1f v%.1f a%.1f %.1f 0 0 0 %.1f 0 v%.1f" style="fill:%s;stroke:%s" stroke-width="2.4"/>'
         % (x, y + ry, h - 2 * ry, w / 2, ry, w, -(h - 2 * ry), fill, edge))
    for k in (1, 2):
        yy = y + ry + (h - 2 * ry) * k / 3.0
        s += ('<path d="M%.1f %.1f a%.1f %.1f 0 0 0 %.1f 0" fill="none" style="stroke:%s" stroke-width="2.4"/>'
              % (x, yy, w / 2, ry, w, edge))
    s += ('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" style="fill:%s;stroke:%s" stroke-width="2.4"/>'
          % (x + w / 2, y + ry, w / 2, ry, band, edge))
    return s


def g1ram(x, y, w=150, h=34, fill="#ff8fbf", rot=0):
    """Планка памяти."""
    chips = "".join('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" style="fill:#2a2f3d"/>'
                    % (x + 10 + i * (w - 20) / 5.0, y + 6, (w - 20) / 5.0 - 6, h * .5) for i in range(5))
    pins = "".join('<rect x="%.1f" y="%.1f" width="3" height="6" style="fill:#e9b93a"/>' % (x + 8 + i * 8, y + h - 7)
                   for i in range(int((w - 14) / 8)))
    return ('<g transform="rotate(%d %.1f %.1f)"><rect x="%.1f" y="%.1f" width="%d" height="%d" rx="4" '
            'style="fill:%s;stroke:#2a2f3d" stroke-width="2"/>%s%s</g>' % (rot, x + w / 2, y + h / 2, x, y, w, h, fill, chips, pins))


def g1cpu(cx, cy, s=110):
    """Процессор с ножками и подсветкой."""
    h = s / 2.0
    pins = ""
    for i in range(7):
        o = -h * .75 + i * h * .25
        pins += ('<path d="M%.1f %.1f v-12M%.1f %.1f v12M%.1f %.1f h-12M%.1f %.1f h12"/>'
                 % (cx + o, cy - h, cx + o, cy + h, cx - h, cy + o, cx + h, cy + o))
    return ('<g style="stroke:#ff6fb0" stroke-width="4" stroke-linecap="round">%s</g>'
            '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="12" style="fill:#3a3f55;stroke:#2a2f3d" stroke-width="2.5"/>'
            '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" style="fill:#c9ced9"/>'
            '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%.1f" font-weight="900" style="fill:#6b7385">CPU</text>'
            % (pins, cx - h, cy - h, s, s, cx - h * .62, cy - h * .62, s * .62, s * .62, cx, cy + s * .08, s * .2))


def g1env(cx, cy, w=40, fill="#ffd6e7", edge="#e05a97", rot=0):
    """Конверт-пакет."""
    h = w * .68
    return ('<g transform="rotate(%d %.1f %.1f)"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" '
            'style="fill:%s;stroke:%s" stroke-width="2.2"/><path d="M%.1f %.1f l%.1f %.1f l%.1f %.1f" fill="none" '
            'style="stroke:%s" stroke-width="2.2"/></g>'
            % (rot, cx, cy, cx - w / 2, cy - h / 2, w, h, fill, edge, cx - w / 2, cy - h / 2, w / 2, h * .55, w / 2, -h * .55, edge))


def g1warn(cx, cy, s=60):
    return ('<path d="M%.1f %.1f l%.1f %.1f h%.1f z" style="fill:#ff4f7f" stroke-linejoin="round"/>'
            '<path d="M%.1f %.1f v%.1f M%.1f %.1f v1" style="stroke:#fff" stroke-width="%.1f" stroke-linecap="round"/>'
            % (cx, cy - s * .5, s * .55, s * .9, -s * 1.1, cx, cy - s * .18, s * .3, cx, cy + s * .26, s * .1))


def g1clock(cx, cy, r=26):
    return ('<circle cx="%.1f" cy="%.1f" r="%.1f" style="fill:#fff;stroke:#3f86d8" stroke-width="4"/>'
            '<path d="M%.1f %.1f v%.1f l%.1f %.1f" fill="none" style="stroke:#1f1a33" stroke-width="3.5" stroke-linecap="round"/>'
            % (cx, cy, r, cx, cy - r * .6, r * .6, r * .4, r * .25))


def g1graph(ox, oy, s=1.0, col="#ff8fbf", edge="#8cc4f5"):
    """Мини-граф из 6 узлов (декор мониторов/карточек)."""
    P = [(0, 30), (50, 0), (100, 25), (35, 75), (90, 85), (140, 55)]
    E = [(0, 1), (1, 2), (0, 3), (1, 3), (2, 4), (3, 4), (2, 5), (4, 5)]
    p = [(ox + a * s, oy + b * s) for a, b in P]
    return ("".join('<path d="M%.1f %.1f L%.1f %.1f" style="stroke:%s" stroke-width="%.1f"/>'
                    % (p[a][0], p[a][1], p[b][0], p[b][1], edge, 2.5 * s) for a, b in E)
            + "".join('<circle cx="%.1f" cy="%.1f" r="%.1f" style="fill:%s;stroke:#fff" stroke-width="%.1f"/>'
                      % (x, y, 8 * s, col if i % 2 == 0 else "#b9a4f2", 2 * s) for i, (x, y) in enumerate(p)))


def g1monitor(x, y, w=260, h=170, body=""):
    """Монитор (левый верх x, y), body — содержимое экрана в тех же координатах."""
    return ('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="12" style="fill:#3a3f55"/>'
            '<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="6" style="fill:#2a3350"/>%s'
            '<path d="M%.1f %.1f h%.1f l10 26 h%.1f z" style="fill:#5b6178"/>'
            % (x, y, w, h, x + 10, y + 10, w - 20, h - 20, body, x + w / 2 - 22, y + h, 44, -64))


# маска персонажа: растворяет все четыре края вырезки
G1FADE = ("-webkit-mask:radial-gradient(ellipse 52% 54% at 50% 52%,#000 68%,transparent 100%);"
          "mask:radial-gradient(ellipse 52% 54% at 50% 52%,#000 68%,transparent 100%)")
