# -*- coding: utf-8 -*-
"""Вводные слайды pptx 3–5 «Маршрутизаторы ESR»: текст pptx разбит на смысловые блоки и показан схемами —
настоящее фото ESR-200 (паспорт Eltex), лестница OSI, путь пакета, интерфейсы, домашняя сеть, плитки функций.
Инфографики автора — во весь слайд."""
import base64
import os

from _sw_lib import slide, sc, head, step, scene
import _er_fig as F
from _er_fig import t, pill, wire, dot, router, pc, server, phone, cloud, env, note, fig, INK, SOFT, VI, BL, MG, GR, AM, RD

HERE = os.path.dirname(os.path.abspath(__file__))


def _img(name):
    with open(os.path.join(HERE, "_er_assets", name), "rb") as fh:
        return "data:image/webp;base64," + base64.b64encode(fh.read()).decode()


# пиктограммы 48×48, линия currentColor
PIC = {
    "swap": '<path d="M8 16h30l-7-7M40 32H10l7 7"/>',
    "nets": '<circle cx="12" cy="14" r="6"/><rect x="30" y="8" width="12" height="12" rx="2"/><path d="M18 34l6-8 6 8z"/>'
            '<path d="M18 14h12M15 19l6 9M33 20l-6 8"/>',
    "gear": '<circle cx="24" cy="24" r="6"/><path d="M24 6v6M24 36v6M6 24h6M36 24h6M11 11l4 4M33 33l4 4M37 11l-4 4M15 33l-4 4"/>',
    "cut": '<circle cx="13" cy="24" r="8"/><circle cx="35" cy="24" r="8"/><path d="M24 6v36" stroke-dasharray="4 4"/>',
    "msg": '<path d="M8 10h32v20H20l-8 7v-7H8z"/>',
    "music": '<path d="M18 34V12l20-4v22"/><circle cx="14" cy="34" r="4"/><circle cx="34" cy="30" r="4"/>',
    "video": '<rect x="6" y="12" width="28" height="24" rx="3"/><path d="M34 20l9-5v18l-9-5"/>',
    "cart": '<path d="M5 9h6l5 21h22l4-15H14"/><circle cx="19" cy="38" r="3"/><circle cx="35" cy="38" r="3"/>',
    "mail": '<rect x="6" y="11" width="36" height="26" rx="3"/><path d="M6 13l18 13 18-13"/>',
    "table": '<rect x="6" y="8" width="36" height="32" rx="3"/><path d="M6 17h36M6 26h36M18 17v23"/>',
    "path": '<circle cx="9" cy="24" r="4"/><circle cx="24" cy="10" r="4"/><circle cx="24" cy="38" r="4"/><circle cx="39" cy="24" r="4"/>'
            '<path d="M12 21l9-8M27 13l9 8" stroke-width="4.5"/><path d="M12 27l9 8M27 35l9-8" stroke-dasharray="3 4"/>',
    "send": '<path d="M6 24h28M26 14l12 10-12 10"/><rect x="6" y="14" width="12" height="9" rx="2"/>',
    "bcast": '<circle cx="12" cy="24" r="9"/><circle cx="36" cy="24" r="9"/><path d="M24 10v28" stroke-width="5"/>'
             '<path d="M12 18v-3M12 30v3M6 24H3M18 24h3"/>',
    "globe": '<circle cx="24" cy="24" r="17"/><path d="M7 24h34M24 7c-8 9-8 25 0 34M24 7c8 9 8 25 0 34"/>',
    "nat": '<rect x="4" y="16" width="16" height="16" rx="3"/><rect x="28" y="16" width="16" height="16" rx="3"/><path d="M20 24h8M25 21l3 3-3 3"/>',
    "shield": '<path d="M24 5l16 6v11c0 10-7 17-16 20C15 39 8 32 8 22V11z"/><path d="M17 24l5 5 9-10"/>',
    "home": '<path d="M7 22L24 8l17 14M12 19v20h24V19"/><path d="M20 39V28h8v11"/>',
    "wifi": '<path d="M6 18c10-9 26-9 36 0M12 25c7-6 17-6 24 0M18 32c4-3 8-3 12 0"/><circle cx="24" cy="38" r="2.5"/>',
}


def pico(name):
    return ('<svg class="ixp" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="3.2" '
            'stroke-linecap="round" stroke-linejoin="round">%s</svg>' % PIC[name])


def tile(icon, html, tone="b", key=""):
    k = '<b class="ixk">%s</b>' % key if key else ""
    return '<div class="ixt t-%s">%s<div>%s<p>%s</p></div></div>' % (tone, pico(icon), k, html)


def bleed(n, label):
    """Инфографика автора во весь слайд, без рамки и заголовка (заголовок уже на картинке)."""
    slide("Инфографика · слайд %d · %s" % (n, label),
          '<div class="ixbleed"><img src="%s" alt="" loading="lazy"></div>' % _img("p%02d.webp" % n))


# ====================================================================== pptx 3
def router_slide(title):
    left = (step('<div class="ixdef"><span class="ixtag">Определение</span><p><b>Маршрутизатор (Router)</b> - это '
                 'специализированное устройство, которое пересылает пакеты между различными сегментами сети на основе '
                 'правил и таблицы маршрутизации.</p></div>')
            + '<div class="ixtiles">'
            + step(tile("nets", "Маршрутизатор может связывать разнородные сети различных архитектур.", "v", "Связывает"))
            + step(tile("gear", "Для принятия решений о пересылке пакетов используются информация о топологии сети и "
                                "определённые правила, заданные администратором.", "b", "Решает"))
            + step(tile("cut", "Маршрутизатор также делит широковещательные домены и области коллизии.", "g", "Разделяет"))
            + "</div>")
    photo = ('<figure class="ixphoto"><img src="%s" alt="ESR-200, передняя панель">'
             '<figcaption><b>Eltex ESR-200</b> · 4×RJ-45 · 4 combo (RJ-45/SFP) · Console · USB · SD</figcaption></figure>'
             % _img("esr200.webp"))
    osi = ('<div class="ixosi">'
           '<div class="ixl l3"><u>3</u><span><b>Маршрутизаторы</b> работают на <b>сетевом уровне</b> многоуровневой '
           'сетевой модели OSI,</span></div>'
           '<div class="ixl l2"><u>2</u><span>в то время как <b>коммутаторы</b> функционируют на втором уровне,</span></div>'
           '<div class="ixl l1"><u>1</u><span>а <b>концентраторы (Hub)</b> - на первом уровне модели OSI, '
           '<i>но они не применяются в современных сетях.</i></span></div></div>')
    slide("Маршрутизатор", sc(head(title), '<div class="g grow ixg3"><div class="col">%s</div><div class="col">%s%s</div></div>'
                              % (left, step(photo), step(osi))))


# ====================================================================== pptx 4
def _path_scene():
    xs = (330, 520, 710, 900)
    o = [cloud(615, 300, 760, 260, "", "#b9c0ff", "rgba(236,238,255,.55)")]
    o += [wire(150, 300, xs[0], 300)] + [wire(xs[i], 300, xs[i + 1], 300) for i in range(3)] + [wire(xs[-1], 300, 1060, 300)]
    o += [pc(110, 230, "Клиент", w=120), server(1100, 220, "Сервер", 100)]
    o += [router(x, 300, "R%d" % (i + 1), 44) for i, x in enumerate(xs)]
    o.append(t(615, 205, "Интернет", 24, SOFT, 800))
    o += [env(150, 268, xs[0], 268, 2), env(xs[0], 268, xs[1], 268, 2), env(xs[1], 268, xs[2], 268, 2),
          env(xs[2], 268, xs[3], 268, 2), env(xs[3], 268, 1060, 268, 2)]
    o += [env(1060, 335, xs[3], 335, 3, MG), env(xs[3], 335, xs[0], 335, 3, MG), env(xs[0], 335, 150, 335, 3, MG)]
    for i, x in enumerate(xs):
        o.append(pill(x, 380, str(i + 1), AM, 18, n=4))
    o.append(note(380, 430, 470, ["Где физически сервер?", "Сколько маршрутизаторов на пути?"], AM, 4, size=18))
    o += [pill(250, 80, "сообщения", BL, 17, n=1), pill(420, 80, "музыка", BL, 17, n=1), pill(570, 80, "видео", BL, 17, n=1),
          pill(730, 80, "покупки", BL, 17, n=1), pill(890, 80, "почта", BL, 17, n=1)]
    return scene(fig("".join(o), "0 0 1200 540"), [
        "Клиент и сервер — где-то в Интернете.",
        "Пользователь пользуется сервисами: сообщения, музыка, видео, покупки, почта.",
        "Запрос идёт к серверу через цепочку маршрутизаторов.",
        "Ответ сервера возвращается обратно — тоже через маршрутизаторы.",
        "Пользователь не задумывается, сколько маршрутизаторов на пути."], "er_path")


def internet_slide(title):
    services = "".join('<span>%s%s</span>' % (pico(i), s) for i, s in (
        ("msg", "сообщения"), ("music", "музыка"), ("video", "видео"), ("cart", "покупки"), ("mail", "почта")))
    left = (step('<div class="ixdef"><p>Сегодня выход в сеть Интернет имеет множество пользователей. В Интернете пользователи '
                 'общаются с помощью сервисов передачи мгновенных текстовых сообщений, прослушивают музыку онлайн и '
                 'просматривают видео, используя различные платформы. Производят покупки в онлайн магазинах, посещая '
                 'web-сайты, и отправляют сообщения по электронной почте.</p><div class="ixsrv">%s</div></div>' % services))
    q = step('<div class="ixq"><span>?</span><p>Большинство пользователей при этом не задумывается о том, где физически '
             'располагаются сервера и сколько маршрутизаторов проходит пакет от клиента до сервера и обратно.</p></div>')
    slide("Маршрутизатор в Интернете", sc(head(title), '<div class="g grow ixg2"><div class="col">%s</div><div class="col">%s%s</div></div>'
                                          % (left, step(_path_scene()), q)))


def _if_scene():
    o = [wire(600, 270, 250, 140), wire(600, 270, 250, 420), wire(600, 270, 960, 270, AM, 4.5)]
    o += [cloud(160, 140, 250, 130, "LAN 1", size=22), cloud(160, 420, 250, 130, "LAN 2", size=22),
          cloud(1060, 270, 250, 150, "WAN", "#e8b25a", "rgba(255,244,225,.9)", 24)]
    o += [t(160, 200, "192.168.1.0/24", 16, INK, 800, mono=True), t(160, 480, "192.168.2.0/24", 16, INK, 800, mono=True),
          t(1060, 336, "Интернет", 16, INK, 800)]
    o.append(router(600, 270, "R1", 70))
    o += [pill(420, 170, "gi1/0/1", BL, 17, mono=True), pill(420, 375, "gi1/0/2", BL, 17, mono=True),
          pill(800, 238, "gi1/0/3", AM, 17, mono=True)]
    o += [dot(530, 228), dot(530, 312), dot(672, 270)]
    o += [env(270, 150, 525, 230, 2)]
    o.append(note(470, 380, 270, ["Куда переслать?", "→ интерфейс gi1/0/3"], VI, 3, size=17))
    o.append(env(680, 270, 930, 270, 4, AM))
    o += [pill(160, 60, "отдельный интерфейс на каждую сеть", GR, 16, n=5),
          pill(900, 140, "LAN — локальные · WAN — глобальная", GR, 16, n=5)]
    return scene(fig("".join(o), "0 0 1200 540"), [
        "У R1 три интерфейса, каждый — в своей IP-сети.",
        "IP-пакет приходит на интерфейс gi1/0/1.",
        "R1 решает, через какой интерфейс доставить пакет получателю.",
        "Пакет уходит через gi1/0/3 — по пути к сети назначения.",
        "Каждой сети — свой интерфейс: LAN объединяют, WAN подключает к глобальной сети."], "er_if")


def interfaces_slide(title):
    left = (step(tile("nets", "У маршрутизатора может быть множество интерфейсов, каждый из которых может принадлежать "
                              "разной IP-сети.", "b", "Много интерфейсов"))
            + step(tile("swap", "Задача маршрутизатора при получении IP-пакета с одного интерфейса - принять решение о выборе "
                                "необходимого интерфейса, на который необходимо переслать пакет для доставки получателю.",
                        "v", "Задача"))
            + step(tile("path", "Интерфейс маршрутизатора может являться как узлом-получателем, так и промежуточной точкой "
                                "по пути к сети назначения.", "b", "Роль интерфейса"))
            + step(tile("cut", "Каждая подключенная к маршрутизатору сеть требует наличия отдельного интерфейса "
                               "маршрутизатора для этой сети.", "g", "Сеть = интерфейс"))
            + step(tile("globe", "Интерфейсы маршрутизатора могут быть подключены как для объединения локальных сетей (LAN), "
                                 "так и для подключения к глобальной сети (WAN).", "a", "LAN и WAN")))
    slide("Интерфейсы маршрутизатора", sc(head(title), '<div class="g grow ixg2"><div class="col ixstack">%s</div>'
                                          '<div class="col">%s</div></div>' % (left, step(_if_scene()))))


def _home_fig():
    o = [wire(600, 300, 1000, 300, AM, 4.5)]
    for x, y in ((180, 130), (180, 300), (180, 470)):
        o.append('<path d="M%g %gQ%g %g 545 300" style="stroke:#7d8be0" stroke-width="3" stroke-dasharray="8 7" fill="none" class="flow"/>'
                 % (x + 60, y, 420, y))
    o.append(cloud(1060, 300, 260, 170, "Интернет", "#e8b25a", "rgba(255,244,225,.9)", 26))
    o += [pc(170, 75, "ПК", w=110), phone(180, 270, "Телефон", 64), F.server(180, 430, "NAS", 70)]
    o.append(router(600, 300, "Wi-Fi", 76))
    o.append('<g transform="translate(565 165)" style="color:#2f6bff">%s</g>'
             % ('<svg width="70" height="70" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="3.6" '
                'stroke-linecap="round">%s</svg>' % PIC["wifi"]))
    for i, s in enumerate(("Wi-Fi", "DHCP", "NAT", "межсетевой экран")):
        o.append(pill(600, 400 + i * 34, s, VI, 15))
    o.append(t(380, 560, "домашняя сеть", 20, SOFT, 800))
    return F.wrap(fig("".join(o), "0 20 1200 560"))


def home_slide(title):
    left = (step(tile("home", "Сегодня каждый пользователь сети Интернет имеет у себя дома маршрутизатор.", "b", "Дома"))
            + step(tile("gear", "В домашней сети маршрутизатор представляет собой специализированное устройство, объединяющее "
                                "в себе множество функций и сервисов для работы в сети", "v", "Всё в одном"))
            + step(tile("globe", "и связывающее пользователей домашней сети с сетью Интернет.", "a", "Выход в Интернет")))
    slide("Домашний маршрутизатор", sc(head(title), '<div class="g grow ixg2"><div class="col ixstack">%s</div>'
                                       '<div class="col">%s</div></div>' % (left, step(_home_fig()))))


# ====================================================================== pptx 5
def _mr(x, y, r=17):
    """Мини-маршрутизатор для плиток функций."""
    return ('<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="url(#erRb)"/><ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="url(#erRt)" '
            'style="stroke:#c9d8ff" stroke-width="1.5"/><path d="M%g %gl%g %gM%g %gl%g %g" style="stroke:#fff" stroke-width="2.4" '
            'stroke-linecap="round"/>' % (x, y + 5, r, r * .42, x, y, r, r * .4, x - r * .5, y - 3, r, 6, x + r * .5, y - 3, -r, 6))


def _ico(x, y, size, name, col):
    return ('<g transform="translate(%g %g)" style="color:%s"><svg width="%g" height="%g" viewBox="0 0 48 48" fill="none" '
            'stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">%s</svg></g>'
            % (x, y, col, size, size, PIC[name]))


def _mini(kind):
    """Мини-схема под текстом функции: показывает, что функция делает."""
    o = []
    if kind == "table":
        o.append('<rect x="4" y="4" width="252" height="96" rx="9" style="fill:#f3f6ff;stroke:#b9c6ff" stroke-width="1.5"/>')
        for i, (c, n, v) in enumerate((("C", "192.168.1.0/24", "gi1/0/1"), ("C", "192.168.2.0/24", "gi1/0/2"),
                                       ("S", "10.0.0.0/8", "via 3.2"))):
            y = 32 + i * 27
            o.append(t(16, y, c, 15, BL, 900, "start", True) + t(38, y, n, 13, INK, 700, "start", True)
                     + t(246, y, v, 12, SOFT, 700, "end", True))
    elif kind == "path":
        pts = {"A": (22, 46), "B": (95, 16), "C": (95, 76), "D": (170, 46), "E": (240, 46)}
        for a, b, hl in (("A", "B", 1), ("B", "D", 1), ("A", "C", 0), ("C", "D", 0), ("D", "E", 1)):
            (x1, y1), (x2, y2) = pts[a], pts[b]
            o.append('<path d="M%g %gL%g %g" style="stroke:%s" stroke-width="%g" stroke-linecap="round"%s/>'
                     % (x1, y1, x2, y2, VI if hl else "#c3c6e6", 5 if hl else 3, ' class="flow"' if hl else ' stroke-dasharray="5 5"'))
        o += [_mr(x, y, 13) for x, y in pts.values()]
        o.append(t(130, 100, "лучший путь — по метрике", 12, SOFT, 700))
    elif kind == "send":
        o += [wire(10, 50, 250, 50, "#8f9ad8", 3), _mr(130, 46, 20)]
        o.append('<g class="ixmv"><rect x="0" y="36" width="34" height="24" rx="4" style="fill:#fff;stroke:%s" stroke-width="2.6"/>'
                 '<path d="M3 39l14 10 14-10" style="stroke:%s" stroke-width="2" fill="none"/></g>' % (BL, BL))
        o += [t(26, 92, "вход", 12, SOFT, 700), t(130, 94, "решение", 12, VI, 800), t(234, 92, "выход", 12, SOFT, 700)]
    elif kind == "bcast":
        o += ['<ellipse cx="60" cy="48" rx="56" ry="40" style="fill:rgba(24,167,90,.10);stroke:%s" stroke-width="2" stroke-dasharray="6 5"/>' % GR,
              '<ellipse cx="200" cy="48" rx="56" ry="40" style="fill:rgba(47,107,255,.08);stroke:%s" stroke-width="2" stroke-dasharray="6 5"/>' % BL]
        for x in (30, 60, 90):
            o.append('<path d="M60 56L%g 30" style="stroke:%s" stroke-width="2"/><circle cx="%g" cy="30" r="5" style="fill:%s"/>' % (x, GR, x, GR))
        o += ['<circle cx="60" cy="58" r="6" style="fill:%s"/>' % GR, _mr(130, 44, 18),
              '<path d="M150 30l14 14M164 30l-14 14" style="stroke:%s" stroke-width="3.4" stroke-linecap="round"/>' % RD,
              t(60, 102, "broadcast", 12, GR, 800), t(200, 102, "не доходит", 12, BL, 800)]
    elif kind == "globe":
        o += [wire(60, 48, 200, 48, AM, 3.5), _mr(130, 44, 20), _ico(16, 24, 44, "home", BL), _ico(200, 22, 48, "globe", AM),
              t(38, 98, "LAN", 13, BL, 800), t(224, 98, "WAN", 13, AM, 800)]
    elif kind == "nat":
        o += [wire(100, 48, 160, 48, "#8f9ad8", 3), _mr(130, 44, 18),
              '<rect x="2" y="32" width="96" height="30" rx="8" style="fill:#f1f4ff;stroke:%s" stroke-width="1.8"/>' % BL,
              t(50, 52, "192.168.1.10", 12, INK, 800, mono=True),
              '<rect x="162" y="32" width="96" height="30" rx="8" style="fill:#fbefff;stroke:%s" stroke-width="1.8"/>' % MG,
              t(210, 52, "85.12.4.7", 12, INK, 800, mono=True), t(50, 90, "частный", 12, BL, 800), t(210, 90, "публичный", 12, MG, 800)]
    elif kind == "shield":
        o += [wire(10, 50, 250, 50, "#8f9ad8", 3), _mr(160, 50, 20),
              '<path d="M160 4l22 8v14c0 13-10 21-22 24-12-3-22-11-22-24V12z" style="fill:rgba(226,59,90,.12);stroke:%s" stroke-width="2.4"/>' % RD,
              '<rect x="30" y="38" width="34" height="24" rx="4" style="fill:#fff;stroke:%s" stroke-width="2.6"/>' % RD,
              '<path d="M96 42l14 14M110 42l-14 14" style="stroke:%s" stroke-width="3.6" stroke-linecap="round"/>' % RD,
              t(47, 92, "чужой пакет", 12, RD, 800), t(225, 92, "защищено", 12, GR, 800)]
    return '<svg class="ixmini" viewBox="0 0 260 106">%s</svg>' % "".join(o)


FUNCS = (
    ("table", "Поддержка таблицы маршрутизации и маршрутной информации", "b"),
    ("path", "Определение наилучшего маршрута для передачи пакетов к удаленным сетям", "v"),
    ("send", "Пересылка пакетов к месту назначения.", "b"),
    ("bcast", "Изоляция широковещательного домена", "g"),
    ("globe", "Доступ к глобальной сети", "a"),
    ("nat", "Преобразование сетевых адресов", "m"),
    ("shield", "Специальные функции обеспечения безопасности.", "r"),
)
_MINI = ("table", "path", "send", "bcast", "globe", "nat", "shield")


def functions_slide(title):
    cells = "".join(step('<div class="ixf t-%s"><u>%d</u><div class="ixfh">%s<p>%s</p></div>%s</div>'
                         % (tn, i + 1, pico(ic), txt, _mini(_MINI[i])))
                    for i, (ic, txt, tn) in enumerate(FUNCS))
    centre = ('<div class="ixfc"><img src="%s" alt="ESR-200"><b>Основные функции маршрутизаторов</b></div>' % _img("esr200.webp"))
    slide("Основные функции", sc(head(title), '<div class="ixfg">%s%s</div>' % (step(centre), cells)))


CSS = r"""
.ixbleed{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:10px 10px 62px}
.ixbleed img{max-width:100%;max-height:100%;width:auto;height:auto;border-radius:16px;box-shadow:0 16px 44px rgba(70,60,190,.28)}
.ixg3{grid-template-columns:1.05fr 1fr!important;gap:22px!important}.ixg2{grid-template-columns:.78fr 1.4fr!important;gap:22px!important}
.ixg3>.col:last-child{display:flex;flex-direction:column}.ixg3>.col:last-child>.step:last-child{flex:1;display:flex}
.ixstack .ixt{padding:10px 14px}.ixstack .ixt p{font-size:clamp(13px,1.1vw,21px)}.ixstack .ixk{font-size:clamp(13px,1.05vw,20px)}
.ixdef{background:var(--panel);border:1.5px solid #fff;border-radius:18px;padding:20px 24px;box-shadow:0 10px 30px rgba(70,60,190,.16)}
.ixdef p{font:600 clamp(16px,1.55vw,30px)/1.42 "Golos Text",sans-serif;color:#141a5c;margin:0}
.ixdef b,.ixt b,.ixl b{color:#2a3ad0;-webkit-text-fill-color:#2a3ad0}
.ixtag{display:inline-block;margin-bottom:10px;padding:5px 12px;border-radius:9px;background:linear-gradient(90deg,#2f6bff,#6a4cff);
 color:#fff;font:800 clamp(11px,.85vw,16px)/1 var(--fd);letter-spacing:.04em;text-transform:uppercase}
.ixtiles{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:14px}
.ixtiles .ixt{flex-direction:column;height:100%}
.ixstack{gap:12px!important}
.ixt{display:flex;gap:14px;align-items:flex-start;background:rgba(255,255,255,.88);border:1.5px solid #fff;border-radius:16px;padding:14px 16px;
 box-shadow:0 8px 24px rgba(70,60,190,.13);border-top:5px solid var(--tc,#2f6bff)}
.ixt p{margin:0;font:600 clamp(14px,1.28vw,25px)/1.38 "Golos Text",sans-serif;color:#141a5c}
.ixk{display:block;margin-bottom:4px;font:800 clamp(14px,1.25vw,24px)/1.1 var(--fd);color:var(--tc)!important;-webkit-text-fill-color:var(--tc)!important}
.ixp{flex:0 0 auto;width:clamp(34px,3.2vw,60px);height:clamp(34px,3.2vw,60px);color:var(--tc,#2f6bff);
 background:color-mix(in srgb,var(--tc,#2f6bff) 12%,#fff);border-radius:14px;padding:6px}
.t-b{--tc:#2f6bff}.t-v{--tc:#6a4cff}.t-g{--tc:#18a75a}.t-a{--tc:#e08a00}.t-m{--tc:#c03ad6}.t-r{--tc:#e23b5a}
.ixphoto{margin:0;background:linear-gradient(160deg,#fff,#eef0ff);border:1.5px solid #fff;border-radius:18px;padding:16px 16px 12px;
 box-shadow:0 14px 36px rgba(70,60,190,.2)}
.ixphoto img{display:block;width:100%;height:auto;filter:drop-shadow(0 10px 14px rgba(40,40,120,.25))}
.ixphoto figcaption{margin-top:10px;font:600 clamp(12px,1vw,19px)/1.3 "Golos Text",sans-serif;color:#3e4688;text-align:center}
.ixphoto figcaption b{color:#141a5c}
.ixosi{flex:1;display:flex;flex-direction:column;gap:10px;margin-top:14px}.ixosi .ixl{flex:1}
.ixl{display:flex;align-items:center;gap:14px;border-radius:14px;padding:10px 14px;background:rgba(255,255,255,.85);border:1.5px solid #fff}
.ixl u{flex:0 0 auto;text-decoration:none;display:grid;place-items:center;width:clamp(34px,3vw,56px);height:clamp(34px,3vw,56px);border-radius:12px;
 font:900 clamp(18px,1.8vw,34px)/1 var(--fd);color:#fff;background:#8f95c8}
.ixl span{font:600 clamp(14px,1.25vw,24px)/1.35 "Golos Text",sans-serif;color:#141a5c}
.ixl.l3{background:linear-gradient(90deg,#dfe6ff,#efe9ff);border-color:#9fb0ff;box-shadow:0 8px 22px rgba(60,80,230,.2);transform:translateX(-8px)}
.ixl.l3 u{background:linear-gradient(135deg,#2f6bff,#6a4cff)}.ixl.l2 u{background:#6a74c8}
.ixl.l1{opacity:.78}.ixl.l1 i{color:#e23b5a;font-style:normal;font-weight:700}
.ixsrv{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
.ixsrv span{display:flex;align-items:center;gap:8px;padding:6px 12px 6px 6px;border-radius:12px;background:#eef1ff;
 font:700 clamp(13px,1.1vw,21px)/1 "Golos Text",sans-serif;color:#2a3ad0}
.ixsrv .ixp{width:clamp(28px,2.4vw,44px);height:clamp(28px,2.4vw,44px);padding:4px}
.ixq{display:flex;gap:16px;align-items:center;margin-top:14px;padding:16px 20px;border-radius:18px;background:linear-gradient(90deg,#fff4dc,#fff);
 border:1.5px solid #f2c46a;box-shadow:0 10px 26px rgba(200,140,20,.16)}
.ixq span{flex:0 0 auto;display:grid;place-items:center;width:clamp(40px,3.6vw,68px);height:clamp(40px,3.6vw,68px);border-radius:50%;
 background:#e89a10;color:#fff;font:900 clamp(22px,2.4vw,44px)/1 var(--fd)}
.ixq p{margin:0;font:600 clamp(15px,1.4vw,27px)/1.4 "Golos Text",sans-serif;color:#3a2a00}
.ixfg{flex:1;display:grid;grid-template-columns:repeat(4,1fr);grid-template-rows:1fr 1fr;gap:16px;min-height:0}
.ixfc{height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:18px;padding:20px;border-radius:20px;
 background:radial-gradient(circle at 50% 40%,#fff,#e4e6ff);border:1.5px solid #fff;box-shadow:0 14px 36px rgba(70,60,190,.2)}
.ixfc img{width:100%;height:auto;filter:drop-shadow(0 10px 14px rgba(40,40,120,.25))}
.ixfc b{font:800 clamp(16px,1.6vw,30px)/1.2 var(--fd);color:#141a5c;text-align:center}
.ixf{position:relative;height:100%;display:flex;flex-direction:column;gap:10px;padding:18px;border-radius:18px;background:rgba(255,255,255,.9);
 border:1.5px solid #fff;border-top:6px solid var(--tc);box-shadow:0 10px 26px rgba(70,60,190,.14)}
.ixf u{position:absolute;top:12px;right:14px;text-decoration:none;font:900 clamp(20px,2vw,38px)/1 var(--fd);color:var(--tc);opacity:.35}
.ixf p{margin:0;font:700 clamp(15px,1.35vw,26px)/1.3 "Golos Text",sans-serif;color:#141a5c}
.ixfh{display:flex;gap:12px;align-items:flex-start;padding-right:34px}
.ixmini{margin-top:auto;width:100%;flex:1;min-height:0;max-height:62%;background:color-mix(in srgb,var(--tc) 6%,#fff);border-radius:12px;padding:6px}
.ixmini text{font-family:"Golos Text",sans-serif}
.ixmv{animation:ixmv 2.8s linear infinite}
@keyframes ixmv{0%{transform:translateX(0)}42%,58%{transform:translateX(113px)}100%{transform:translateX(220px)}}
"""
