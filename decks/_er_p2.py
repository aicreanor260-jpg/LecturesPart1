# -*- coding: utf-8 -*-
"""Дека «Маршрутизаторы ESR» (2.3 доп.): слайды pptx 21–37. Вызывается из _er_deck.build() по порядку pptx.
Текст pptx — дословно, но разбит на смысловые блоки; рядом — схема, сцена по шагам или разметка вывода CLI."""
from _sw_lib import card, p, li, slide, sc, head, grow, col, step, scene, _esc
from _dk_kit import pslide, full, term, txt
import _er_fig as F
import _er_intro as I
from _er_fig import t, pill, wire, dot, router, pc, server, cloud, env, note, arr, fig, INK, SOFT, VI, BL, MG, GR, AM, RD
from _er_deck import conf, syn, pic, info

# локальные пиктограммы (префикс b_), добавляются в общий словарь только в памяти
I.PIC.update({
    "b_far": '<circle cx="12" cy="30" r="6"/><circle cx="38" cy="14" r="6"/><path d="M17 27c6-4 10-8 15-10" stroke-dasharray="4 4"/>'
             '<path d="M8 42h8M34 26v8"/>',
    "b_term": '<rect x="5" y="8" width="38" height="32" rx="4"/><path d="M12 19l6 5-6 5M22 30h10"/>',
    "b_open": '<rect x="10" y="22" width="28" height="20" rx="3"/><path d="M16 22v-6a8 8 0 0 1 15-3"/>',
    "b_lock": '<rect x="10" y="22" width="28" height="20" rx="3"/><path d="M16 22v-6a8 8 0 0 1 16 0v6"/><path d="M24 30v5"/>',
    "b_ok": '<path d="M10 25l9 9 19-20"/>',
    "b_clock": '<circle cx="24" cy="24" r="17"/><path d="M24 13v11l8 5"/>',
    "b_flag": '<path d="M10 42V6M10 8h24l-5 8 5 8H10"/>',
    "b_eye": '<path d="M4 24s8-13 20-13 20 13 20 13-8 13-20 13S4 24 4 24z"/><circle cx="24" cy="24" r="6"/>',
    "b_search": '<circle cx="20" cy="20" r="12"/><path d="M29 29l12 12"/>',
    "b_ping": '<path d="M6 18h30l-6-6M42 30H12l6 6"/>',
    "b_x": '<circle cx="24" cy="24" r="17"/><path d="M17 17l14 14M31 17L17 31"/>',
    "b_ttl": '<path d="M14 6h20M14 42h20M16 6c0 10 16 12 16 18S16 32 16 42M32 6c0 10-16 12-16 18s16 8 16 18"/>',
    "b_redir": '<path d="M8 38V20a8 8 0 0 1 8-8h22M32 6l6 6-6 6"/>',
    "b_info": '<circle cx="24" cy="24" r="17"/><path d="M24 22v12M24 15v1"/>',
})
tile, pico = I.tile, I.pico


def lay(label, title, left, right, cls="ixg2", sub="", sz=""):
    """Слева — стопка смысловых блоков, справа — схема / вывод CLI. Всё появляется по шагам."""
    L = "".join(step(b) for b in left)
    R = "".join(step(b) for b in right)
    slide(label, sc(head(title, sub), '<div class="g grow %s %s"><div class="col ixstack">%s</div><div class="col b-r">%s</div></div>'
                    % (cls, sz, L, R)))


def vis(body, vb):
    return F.wrap(fig(body, vb))


def chips(parts):
    """Команда, разобранная на части: [(текст, подпись, тон)]."""
    return '<div class="b-cmd">%s</div>' % "".join(
        '<span class="t-%s"><code>%s</code><i>%s</i></span>' % (tn, c, cap) for c, cap, tn in parts)


def callouts(lines, marks, title=""):
    """Вывод CLI с подсветкой строк и выносками справа: marks = {номер строки: (подпись, тон)}."""
    rows = []
    for i, ln in enumerate(lines):
        m = marks.get(i)
        if m:
            rows.append('<div class="b-ln on t-%s"><pre>%s</pre><em>%s</em></div>' % (m[1], _esc(ln) or " ", m[0]))
        else:
            rows.append('<div class="b-ln"><pre>%s</pre></div>' % (_esc(ln) or " "))
    h = '<div class="clih">%s</div>' % _esc(title) if title else ""
    return '%s<div class="b-out">%s</div>' % (h, "".join(rows))


# ====================================================================== сцены и схемы
def _remote_scene():
    o = [wire(150, 300, 400, 300), wire(600, 300, 850, 300)]
    o.append(cloud(500, 300, 260, 170, "Интернет", size=22))
    o += [pc(120, 200, "Администратор", w=130), router(900, 300, "ESR", 60)]
    o += [t(120, 150, "другой город / страна", 17, SOFT, 800), pill(900, 380, "IP-адрес + логин", BL, 16)]
    o += [t(500, 470, "", 1)]
    # telnet — открытый текст
    o.append('<g data-ph="1">%s%s</g>' % (pill(300, 110, "telnet: password = eltex123", RD, 17, mono=True),
                                         t(300, 150, "данные в открытом виде", 16, RD, 800)))
    o.append(env(170, 270, 860, 270, 1, RD))
    o.append('<g data-ph="2">%s%s%s</g>' % (
        '<circle cx="500" cy="500" r="34" style="fill:#2a2f55"/>',
        t(500, 512, "☠", 34, "#fff", 900), note(40, 470, 380, ["злоумышленник читает трафик:", "пароль виден!"], RD, size=17)))
    o.append('<g data-ph="3">%s%s</g>' % (pill(720, 110, "ssh: 9f#Qz!e7@Lm…", GR, 17, mono=True),
                                         t(720, 150, "данные зашифрованы", 16, GR, 800)))
    o.append(env(170, 330, 860, 330, 3, GR))
    o.append(note(560, 470, 380, ["перехват бесполезен:", "видна только шифровка"], GR, 3, True, 17))
    return scene(fig("".join(o), "0 60 1000 520"), [
        "Администратор подключается к ESR удалённо — по IP-адресу и логину.",
        "telnet: пароль уходит открытым текстом.",
        "Перехватив трафик, злоумышленник получает пароль.",
        "ssh: данные передаются в зашифрованном виде."], "b_remote")


def _clients():
    o = []
    for x, nm, sub, ic in ((150, "PuTTY", "Windows", "b_term"), (500, "ssh", "терминал Linux", "b_term"), (850, "встроенный", "клиент ОС", "b_term")):
        o.append('<rect x="%g" y="40" width="260" height="170" rx="18" style="fill:#fff;stroke:#c9c5f5" stroke-width="2" filter="url(#erSh)"/>' % (x - 130))
        o.append('<g transform="translate(%g 62)" style="color:%s"><svg width="64" height="64" viewBox="0 0 48 48" fill="none" '
                 'stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">%s</svg></g>'
                 % (x - 32, BL, I.PIC[ic]))
        o += [t(x, 160, nm, 24, INK, 900), t(x, 190, sub, 16, SOFT, 700)]
        o.append(arr(x, 215, 500 + (x - 500) * .25, 300, VI, "a", 3, flow=True))
    o += [router(500, 340, "ssh-сервер ESR", 64)]
    return vis("".join(o), "0 20 1000 400")


def _date_break():
    parts = (("17:23:55", "TIME", "HH:MM:SS", BL), ("09", "DAY", "1..31", VI), ("October", "MONTH", "January…December", MG),
             ("2023", "YEAR", "2001..2037", GR))
    x = 250
    o = ['<text x="30" y="110" font-size="30" font-weight="800" style="fill:%s;font-family:JetBrains Mono,Consolas,monospace">set date</text>' % SOFT]
    for s_, k, rng, c in parts:
        w = len(s_) * 19 + 34
        o.append('<rect x="%g" y="70" width="%g" height="58" rx="12" style="fill:#fff;stroke:%s" stroke-width="3"/>' % (x, w, c))
        o.append(t(x + w / 2, 110, s_, 30, INK, 900, mono=True))
        o.append('<path d="M%g 140v24" style="stroke:%s" stroke-width="3"/>' % (x + w / 2, c))
        o.append(pill(x + w / 2, 186, "&lt;%s&gt;" % k, c, 17, mono=True))
        o.append(t(x + w / 2, 230, rng, 16, SOFT, 800))
        x += w + 18
    o += ['<path d="M250 260h%g" style="stroke:#c9c5f5" stroke-width="2"/>' % (x - 268),
          t(250 + (x - 268) / 2, 290, "[ ] — необязательные: без даты меняется только время", 16, SOFT, 700)]
    return vis("".join(o), "10 50 1000 260")


def _tz():
    o = ['<path d="M60 150H940" style="stroke:#9aa0d8" stroke-width="4" stroke-linecap="round"/>']
    for k in range(-12, 13):
        x = 500 + k * 36
        big = k in (-12, 0, 7, 12)
        o.append('<path d="M%g %gv%g" style="stroke:%s" stroke-width="%g"/>' % (x, 150 - (14 if big else 7), 28 if big else 14,
                                                                             VI if k == 7 else "#9aa0d8", 4 if k == 7 else 2))
        if big:
            o.append(t(x, 205, ("gmt %+d" % k).replace("+0", "0") if k else "GMT", 17, VI if k == 7 else INK, 900, mono=True))
    o += ['<circle cx="500" cy="150" r="11" style="fill:%s"/>' % BL, '<circle cx="752" cy="150" r="13" style="fill:%s"/>' % VI,
          '<path d="M500 110 Q626 40 752 110" style="stroke:%s" stroke-width="3" fill="none" marker-end="url(#era)" class="flow"/>' % VI,
          pill(626, 58, "+7 часов", VI, 18)]
    o += [note(150, 250, 300, ["UTC (Greenwich)", "Mon 17:53"], BL, size=19), note(560, 250, 330, ["clock timezone gmt +7", "Tue 00:53"], VI, size=19)]
    return vis("".join(o), "40 30 920 330")


def _banner_flow():
    o = []
    steps = (("подключение", "ssh admin@…", SOFT), ("banner login", "Router-esr-200", BL), ("пароль", "Password:", SOFT),
             ("banner exec", "Connect_Router_esr-200", VI), ("доступ", "esr-200#", GR))
    for i, (a, b, c) in enumerate(steps):
        y = 60 + i * 96
        o.append('<rect x="80" y="%g" width="840" height="70" rx="16" style="fill:%s;stroke:%s" stroke-width="2.5"/>'
                 % (y, "#fff" if c == SOFT else "rgba(255,255,255,.96)", c))
        o.append('<circle cx="80" cy="%g" r="24" style="fill:%s"/>' % (y + 35, c) + t(80, y + 43, str(i + 1), 22, "#fff", 900))
        o += [t(130, y + 44, a, 24, c if c != SOFT else INK, 900, "start"), t(890, y + 44, b, 21, INK, 800, "end", mono=True)]
        if i < 4:
            o.append(arr(80, y + 60, 80, y + 92, "#9aa0d8", "k", 2.5))
    return vis("".join(o), "40 40 920 500")


def _space_rule():
    o = ['<rect x="20" y="20" width="460" height="120" rx="16" style="fill:#eafaf0;stroke:%s" stroke-width="3"/>' % GR,
         t(250, 72, "banner login Router-esr-200", 22, INK, 800, mono=True), t(250, 112, "✓ без пробелов", 20, GR, 900),
         '<rect x="520" y="20" width="460" height="120" rx="16" style="fill:#fff0f2;stroke:%s" stroke-width="3"/>' % RD,
         t(750, 72, "banner login Router esr 200", 22, INK, 800, mono=True), t(750, 112, "✗ пробел недопустим", 20, RD, 900)]
    return vis("".join(o), "0 0 1000 160")


def _show_cards():
    data = (("show running-config", "Команда <b>show running-config</b> представляет информацию о текущих настройках.", "b_doc", "b"),
            ("show interfaces status", "", "b_eye", "v"),
            ("show arp", "Команда <b>show arp</b> дает доступ к содержимому кэша ARP-таблицы.", "table", "g"),
            ("show ip route", "Команда <b>show ip route</b> предоставляет информацию о текущей таблице маршрутизации с лучшими "
                              "маршрутами, а с ключом «all» - со всеми маршрутами.", "path", "a"),
            ("show version", "", "b_info", "m"))
    return '<div class="b-show">%s</div>' % "".join(
        '<div class="ixt t-%s">%s<div><b class="ixk b-mono">%s;</b><p>%s</p></div></div>'
        % (tn, pico(ic if ic in I.PIC else "b_term"), c, d or '<span class="b-dim">подробно — на следующем слайде</span>')
        for c, d, ic, tn in data)


def _if_card():
    o = ['<rect x="40" y="30" width="920" height="330" rx="24" style="fill:#fff;stroke:#c9c5f5" stroke-width="2" filter="url(#erSh)"/>',
         '<rect x="70" y="60" width="210" height="270" rx="18" fill="url(#erSb)"/>',
         t(175, 150, "gi1/0/1", 36, "#fff", 900, mono=True), t(175, 190, "routerport", 18, "#cfe0ff", 700)]
    for i, (k, v) in enumerate((("Operational", "Up"), ("Administrative", "Up"))):
        o += ['<circle cx="110" cy="%g" r="9" style="fill:#3ee08a"/>' % (240 + i * 40), t(128, 246 + i * 40, "%s: %s" % (k, v), 15, "#fff", 700, "start")]
    rows = (("MTU", "1500"), ("MAC", "de:93:87:98:56:0a"), ("broadcast / multicast", "Yes / Yes"), ("Last change", "6 days, 25 min"))
    for i, (k, v) in enumerate(rows):
        y = 100 + i * 64
        o += [t(320, y, k, 18, SOFT, 800, "start"), t(930, y, v, 22, INK, 900, "end", mono=True),
              '<path d="M320 %gH930" style="stroke:#e3e1fa" stroke-width="2"/>' % (y + 22)]
    return vis("".join(o), "20 10 960 370")


def _icmp_funcs():
    data = (("b_ping", "Подтверждение узла;", "b"), ("b_x", "Назначение или услуга недоступны;", "r"),
            ("b_ttl", "Истечение времени;", "a"), ("b_redir", "Переадресация маршрутов;", "v"))
    return '<div class="b-4">%s</div>' % "".join(step('<div class="ixt t-%s">%s<p>%s</p></div>' % (tn, pico(ic), s)) for ic, s, tn in data)


def _ping_mini():
    o = [pc(110, 70, "Источник", w=120), pc(890, 70, "Назначение", w=120)]
    for i in range(3):
        y = 240 + i * 110
        o += [arr(190, y, 810, y, BL, "b", 3.4), arr(810, y + 34, 190, y + 34, GR, "g", 3.4)]
        o += [t(500, y - 10, "Echo Request", 17, BL, 800), t(500, y + 62, "Echo Reply", 17, GR, 800)]
        o.append(pill(910, y + 17, "%d ms" % (2 + i), VI, 17))
    o += [pill(300, 590, "размер", AM, 18), pill(500, 590, "количество", AM, 18), pill(700, 590, "время ожидания", AM, 18)]
    return vis("".join(o), "30 40 960 590")


def _unreach():
    o = [wire(170, 200, 470, 200), wire(530, 200, 760, 200, "#c3c6e6", 3, True)]
    o += [pc(110, 120, "Источник", w=120), router(500, 200, "R1", 56), cloud(860, 200, 200, 130, "сеть ?", "#e23b5a", "rgba(255,236,240,.9)", 20)]
    o += ['<path d="M610 170l40 40M650 170l-40 40" style="stroke:%s" stroke-width="7" stroke-linecap="round"/>' % RD]
    o += [env(180, 180, 450, 180, 1), env(460, 250, 180, 250, 2, RD)]
    o.append(note(240, 300, 520, ["ICMP «Назначение недоступно»", "Type 3 + код причины"], RD, 2, size=19))
    return scene(fig("".join(o), "40 60 960 380"), [
        "Пакет уходит к узлу в недоступной сети.",
        "R1 не может доставить пакет и сообщает источнику: «Назначение недоступно» с кодом ошибки."], "b_unr")


def _ttl0():
    o = [wire(170, 200, 430, 200), wire(570, 200, 830, 200, "#c3c6e6", 3, True)]
    o += [pc(110, 120, "Источник", w=120), router(500, 200, "R1", 56), server(890, 140, "Узел", 90)]
    o += [env(180, 175, 440, 175, 1), pill(300, 130, "TTL = 1", BL, 18, n=1),
          '<g data-ph="2">%s%s</g>' % (pill(500, 110, "TTL 1 → 0", RD, 20),
                                       '<path d="M470 150l60 60M530 150l-60 60" style="stroke:%s" stroke-width="6"/>' % RD),
          env(450, 250, 180, 250, 3, AM), pill(300, 300, "ICMP Time Exceeded", AM, 18, n=3)]
    return scene(fig("".join(o), "40 80 960 270"), [
        "Пакет приходит на маршрутизатор со значением TTL = 1.",
        "TTL уменьшается до 0 — маршрутизатор отбрасывает пакет.",
        "Источнику уходит сообщение об истечении времени жизни пакета."], "b_ttl0")


def _tracert_scene():
    xs = (330, 520, 710)
    o = [wire(170, 260, 330, 260)] + [wire(xs[i], 260, xs[i + 1], 260) for i in range(2)] + [wire(710, 260, 860, 260)]
    o += [pc(110, 180, "Источник", w=120), server(910, 190, "Назначение", 90)]
    o += [router(x, 260, "R%d" % (i + 1), 48) for i, x in enumerate(xs)]
    for k in range(3):
        n = 1 + k * 2
        o.append(env(180, 225, xs[k] - 30, 225, n))
        o.append(pill((180 + xs[k]) / 2, 180 - k * 0, "TTL = %d" % (k + 1), BL, 18, n=n, only=True))
        o.append(env(xs[k] - 30, 305, 180, 305, n + 1, AM))
        o.append(pill(xs[k], 360, "TTL Timeout · %d" % (k + 1), AM, 16, n=n + 1))
    o += [env(180, 225, 860, 225, 7, GR), pill(520, 180, "TTL = 4", GR, 18, n=7, only=True),
          note(320, 410, 420, ["Путь: R1 → R2 → R3 → узел", "+ время каждого перехода"], VI, 8, size=18)]
    return scene(fig("".join(o), "40 120 960 400"), [
        "Источник и узел назначения разделены тремя маршрутизаторами.",
        "Первый пакет: TTL = 1.", "R1: TTL истёк → ICMP TTL Timeout с меткой времени.",
        "Второй пакет: TTL = 2.", "R2: TTL истёк → ICMP TTL Timeout.",
        "Третий пакет: TTL = 3.", "R3: TTL истёк → ICMP TTL Timeout.",
        "TTL = 4 — пакет достигает узла назначения.",
        "Источник знает каждый маршрутизатор пути и время приёма-передачи."], "b_trc")


def _ping_summary():
    o = [pc(90, 40, "Источник", w=110), pc(910, 40, "Назначение", w=110)]
    rows = (("reply", "3 ms", GR), ("reply", "2 ms", GR), ("timeout", "нет ответа", RD), ("reply", "4 ms", GR))
    for i, (k, v, c) in enumerate(rows):
        y = 200 + i * 52
        o.append(arr(170, y, 820 if k == "reply" else 560, y, BL, "b", 3))
        if k == "reply":
            o.append(arr(820, y + 18, 170, y + 18, GR, "g", 3))
        else:
            o += ['<rect x="580" y="%g" width="34" height="56" rx="5" style="fill:#ffd9df;stroke:%s" stroke-width="2.5"/>' % (y - 24, RD),
                  t(597, y + 46, "МЭ", 13, RD, 900)]
        o.append(pill(905, y + 9, v, c, 15))
    o.append(note(260, 410, 480, ["Сводка: отправлено 4 · получено 3", "min 2 · avg 3 · max 4 ms"], VI, size=18))
    return vis("".join(o), "30 20 960 470")


def _gw_flow():
    def box(x, y, w, s, c, sub=""):
        return ('<rect x="%g" y="%g" width="%g" height="66" rx="14" style="fill:#fff;stroke:%s" stroke-width="3" filter="url(#erSh)"/>'
                % (x - w / 2, y, w, c) + t(x, y + (30 if sub else 41), s, 19, INK, 900) + (t(x, y + 54, sub, 15, SOFT, 700) if sub else ""))
    o = [box(500, 20, 420, "ping шлюза по умолчанию", BL),
         arr(500, 88, 500, 128, "#9aa0d8", "k", 3), box(500, 130, 380, "Ответил?", VI),
         arr(690, 163, 820, 163, GR, "g", 3), t(755, 152, "да", 16, GR, 900), box(860, 130, 180, "связь есть", GR),
         arr(500, 198, 500, 238, RD, "r", 3), t(520, 225, "нет", 16, RD, 900, "start"),
         box(500, 240, 460, "ping другого узла в локальной сети", AM),
         arr(500, 308, 500, 348, "#9aa0d8", "k", 3), box(500, 350, 380, "Узлы отвечают?", VI),
         arr(310, 383, 230, 440, GR, "g", 3), arr(690, 383, 770, 440, GR, "g", 3),
         box(230, 442, 380, "настройки узла", BL, "IP-адрес шлюза по умолчанию"),
         box(770, 442, 380, "маршрутизатор", RD, "межсетевой экран не отключен")]
    return vis("".join(o), "20 10 960 510")


def _remote_checks():
    o = [wire(150, 220, 330, 220), wire(330, 220, 520, 220), wire(520, 220, 710, 220), wire(710, 220, 870, 220)]
    o += [pc(110, 140, "Источник", w=110)]
    s, _ = F.switch(330, 220, "SW", 4, 130)
    o += [s, router(520, 220, "Шлюз", 50), router(710, 220, "R2", 50), server(900, 160, "Назначение", 80)]
    marks = ((240, "1", "локальная сеть", BL), (520, "2", "шлюз по умолчанию", VI), (710, "3", "маршрутизаторы пути", AM),
             (900, "4", "узел назначения", GR))
    for x, n, s_, c in marks:
        o += ['<circle cx="%g" cy="80" r="24" style="fill:%s"/>' % (x, c), t(x, 88, n, 22, "#fff", 900),
              '<path d="M%g 104v60" style="stroke:%s" stroke-width="2.5" stroke-dasharray="6 5"/>' % (x, c), t(x, 60 - 10, s_, 16, c, 900)]
    o += ['<rect x="830" y="330" width="140" height="50" rx="10" style="fill:#ffd9df;stroke:%s" stroke-width="2.5"/>' % RD,
          t(900, 362, "правила ICMP", 15, RD, 900)]
    return vis("".join(o), "40 20 960 380")


def _trace_why():
    o = [pc(90, 90, "Источник", w=110), server(910, 90, "Получатель", 80)]
    xs = (280, 420, 560, 700)
    o += [wire(150, 170, 250, 170)] + [wire(xs[i], 170, xs[i + 1], 170) for i in range(3)] + [wire(730, 170, 860, 170)]
    o += [router(x, 170, "?", 40) for x in xs]
    o += [arr(150, 300, 860, 300, BL, "b", 3.5), t(505, 290, "ping: только «доступен / нет»", 18, BL, 900),
          arr(150, 370, 860, 370, VI, "a", 3.5), t(505, 360, "traceroute: каждый промежуточный узел", 18, VI, 900)]
    for x in xs:
        o.append('<circle cx="%g" cy="370" r="9" style="fill:#fff;stroke:%s" stroke-width="3"/>' % (x, VI))
    return vis("".join(o), "30 40 960 360")


# ====================================================================== слайды
def build():
    # ---------------------------------------------------------------- pptx 21
    T21 = "Удаленное управление <em>маршрутизатором</em>"
    lay("Удаленное управление", T21, [
        tile("b_far", "Поскольку не всегда может быть прямой доступ к маршрутизаторам и другим сетевым устройствам, например, "
                      "через консольный провод, существуют протоколы удаленного доступа, позволяющие по IP-адресу и логину "
                      "получить доступ для конфигурирования сетевых устройств, находясь в другом месте, в том числе другом "
                      "городе или стране.", "b", "Удалённый доступ"),
        tile("b_term", "Маршрутизаторы ESR поддерживают работу с протоколами удаленного терминального управления <b>telnet</b> "
                       "и <b>ssh</b>.", "v", "telnet и ssh"),
        tile("b_open", "Протокол telnet на сегодняшний день является небезопасным, так как данные передаются в открытом или "
                       "незашифрованном виде. Тем самым, если злоумышленник заполучит и проанализирует трафик, он может "
                       "получить пароль, переданный открытым текстом.", "r", "telnet"),
        tile("b_lock", "Учитывая недостатки протокола telnet, рекомендовано использовать протокол ssh, который производит "
                       "передачу данных в зашифрованном виде. Для применения и подтверждения настроек требуется ввести "
                       "соответствующие команды commit и confirm.", "g", "ssh")],
        [_remote_scene()], sz="b-sm")
    lay("SSH-сервер и клиенты", T21, [
        syn(["[no] ip ssh server [ vrf ]"]), conf(["esr-200(config)# ip ssh server"], "SSH-сервер"),
        tile("b_open", "Аналогичным образом вместо ssh-сервера можно настроить telnet-сервер и производить подключение к "
                       "устройству по протоколу telnet, но недостатки данного протокола описаны выше.", "r", "telnet-сервер"),
        tile("b_ok", "После настройки ssh-сервера необходимо проверить его доступность с помощью ssh-клиентов. Это "
                     "специализированные приложения, способные подключаться к ssh-серверам по протоколу ssh.", "g", "Проверка")],
        [tile("b_term", "К таким приложениям можно отнести приложение PuTTY, также в операционных системах могут быть свои "
                        "встроенные ssh-клиенты, в качестве примера продемонстрируем процесс подключения из терминала "
                        "операционной системы Linux по протоколу ssh к маршрутизатору.", "v", "ssh-клиенты"),
         _clients()])
    full("PuTTY", T21, step(F.putty()))
    # ---------------------------------------------------------------- pptx 22
    lay("Подключение по ssh", T21, [
        tile("b_term", "По сравнению с графическими приложениями, где необходимо заполнить определенные указанные поля, "
                       "консольный клиент протокола ssh имеет следующий синтаксис: <b>ssh &lt;имя учетной записи&gt;@&lt;ip-адрес "
                       "интерфейса маршрутизатора&gt;</b>.", "b", "Синтаксис"),
        chips((("ssh", "клиент", "b"), ("admin", "имя учетной записи", "v"), ("@", "", "b"),
               ("172.16.100.12", "ip-адрес интерфейса", "g"))),
        tile("b_lock", "После ввода данных, если успешно все настроено, пользователь получит приглашение к вводу пароля от "
                       "учетной записи с именем admin.", "v", "Пароль"),
        tile("b_eye", "Символы ввода пароля обычно экранируются, это делается для того, чтобы ограничить подсмотр количества "
                      "символов, содержащихся в пароле.", "a", "Скрытый ввод"),
        tile("b_ok", "При успешном вводе пароля пользователь получает доступ к консоли управления устройством.", "g", "Доступ")],
        [callouts(["user@user-System-Product-Name:~$ ssh admin@172.16.100.12", "(admin@172.16.100.12) Password:", "",
                   "*" * 45, "*                Welcome to vESR                *", "*" * 45, "", "vesr# █"],
                  {0: ("команда ssh", "b"), 1: ("ввод скрыт", "a"), 4: ("приветствие", "v"), 7: ("консоль", "g")},
                  "Терминал Linux")])
    # ---------------------------------------------------------------- pptx 23
    T23 = "Настройка <em>даты и времени</em>"
    lay("Дата и время", T23, [
        tile("b_clock", "Маршрутизаторы ESR имеют функционал по получению настроек даты и времени.", "b", "Дата и время"),
        tile("globe", "Это может осуществляться как путем запросов к предварительно заданному ntp-серверу,", "v", "NTP"),
        tile("b_term", "так и путем ввода администратором сети данных вручную. Установка времени и даты вручную производится "
                       "из привилегированного режима в формате ЧЧ:ММ:СС [число месяца] [месяц] [год] командой.", "g", "Вручную")],
        [syn(["set date <TIME> [<DAY> <MONTH> [ <YEAR> ] ]"]), _date_break(),
         '<div class="b-cap">Параметры</div><div class="b-4">%s</div>' % "".join(
             '<div class="ixt t-%s"><p>%s</p></div>' % (tn, x) for tn, x in (
                 ("b", "&lt;TIME&gt; – устанавливаемое системное время, задаётся в виде HH:MM:SS, где: HH – часы, принимает "
                       "значение [0..23]; MM – минуты, принимает значение [0 .. 59]; SS – секунды, принимает значение [0 .. 59]."),
                 ("v", "&lt;DAY&gt; – день месяца, принимает значения [1..31];"),
                 ("m", "&lt;MONTH&gt; – месяц, принимает значения [ January/February/March/April/May/June/July/August/"
                       "September/October/November/December];"),
                 ("g", "&lt;YEAR&gt; – год, принимает значения [2001..2037]")))], sz="b-sm")
    lay("Дата и время: set date", T23, [
        conf(["esr-200# set date 17:23:55 09 October 2023",
              "2023-10-09T17:23:55+00:00 %TIME-I-INFO: System time was changed by user admin", "Mon Oct 9 17:23:55 UTC 2023"],
             "Установка даты"),
        tile("b_ok", "После требуется применить и подтвердить соответствующую настройку.", "g", "commit · confirm"),
        tile("b_eye", "И просмотр текущих времени и даты осуществляется командой из привилегированного режима "
                      "<b>show date</b>.", "v", "Проверка")],
        [conf(["esr-200# show date", "\"Monday 17:27:46 UTC October 09 2023\"", "esr-200#"], "show date"),
         '<div class="b-flow"><span class="t-b">set date</span><b>→</b><span class="t-g">commit</span><b>→</b>'
         '<span class="t-g">confirm</span><b>→</b><span class="t-v">show date</span></div>'], "b-g11", sz="b-lg")
    # ---------------------------------------------------------------- pptx 24
    lay("Часовой пояс", T23, [
        tile("b_clock", "После установки времени и даты выполним настройку часового пояса.", "b", "Шаг 2"),
        tile("globe", "Часовой пояс устанавливается в режиме глобального конфигурирования командой <b>clock timezone "
                      "&lt;обозначение временной зоны&gt;</b>. Обозначение зоны представляет собой сдвиг в часах относительно "
                      "Greenwich Mean Time, принимает значения [gmt -12 … gmt +12].", "v", "clock timezone"),
        tile("b_eye", "После настройки часового пояса выведем текущее время с маршрутизатора на экран.", "g", "Проверка"),
        conf(["esr-200# show date", "\"Tuesday 00:53:22 GMT+7 October 10 2023\""], "show date")],
        [_tz(),
         conf(["esr-200# configure", "esr-200(config)# clock timezone gmt +7", "esr-200(config)# exit", "esr-200# commit",
               "Configuration has been successfully applied and saved to flash. Commit timer started, 600 seconds.",
               "2023-10-10T00:47:26+07:00 %CLI-I-CRIT: user admin from ssh 10.25.8.59 input: commit",
               "esr-200# confirm",
               "Configuration has been confirmed. Commit timer canceled.",
               "2023-10-10T00:47:27+07:00 %CLI-I-CRIT: user admin from ssh 10.25.8.59 input: confirm",
               "esr-200#"], "Часовой пояс")])
    # ---------------------------------------------------------------- pptx 25
    T25 = "Баннерные <em>сообщения</em>"
    lay("Баннеры", T25, [
        tile("b_flag", "Баннерные сообщения предназначены для оповещения подключившихся пользователей к оборудованию. "
                       "Содержание баннерных сообщений может варьироваться, передавая различные информационные послания.",
             "b", "Зачем"),
        tile("msg", "Например, по умолчанию может быть установлено сообщение «Добро пожаловать!».", "g", "Приветствие"),
        tile("b_x", "В некоторых случаях размещают сообщения, призывающие пользователей внимательно обдумывать свои действия "
                    "при настройке оборудования.", "r", "Предупреждение"),
        tile("b_clock", "В баннерном сообщении также можно предоставить информацию о расписании проведения технических работ, "
                        "которые могут повлечь временную неработоспособность системы.", "a", "Регламент")],
        [card("На маршрутизаторах ESR существует 2 типа баннерных сообщений:", li([
            "<b>banner login</b> - сообщение, выведенное перед авторизацией;",
            "<b>banner exec</b> - сообщение, которое выводится после авторизации."]), "mg"),
         _banner_flow()])
    lay("Баннеры: настройка", T25, [
        tile("b_term", "Эти два типа баннерных сообщений настраиваются из режима глобальной конфигурации.", "b", "Где"),
        tile("b_x", "При написании баннерных сообщений не допускается использование пробелов.", "r", "Без пробелов"),
        tile("b_ok", "Не стоит забывать, что после ввода настроек требуется их применить и подтвердить.", "g", "commit · confirm"),
        _space_rule()],
        [conf(["esr-200#", "esr-200# configure", "esr-200(config)# banner login Router-esr-200",
               "esr-200(config)# banner exec Connect_Router_esr-200", "esr-200(config)#"], "Баннеры"),
         syn(["banner exec", "no banner exec", "banner login", "no banner login"])], "b-g11", sz="b-lg")
    lay("Баннеры при входе", T25, [
        tile("b_flag", "После конфигурации баннерных сообщений при попытке авторизации пользователь увидит имя устройства, "
                       "к которому он подключается,", "b", "banner login"),
        tile("b_ok", "а после успешной авторизации - сообщение об успешном подключении к этому устройству.", "v", "banner exec")],
        [callouts(["user@user-System-Product-Name:~$ ssh admin@172.16.100.12", "Router-esr-200", "(admin@172.16.100.12) Password:",
                   "Connect_Router_esr-200", "esr-200#"],
                  {1: ("banner login", "b"), 2: ("авторизация", "a"), 3: ("banner exec", "v")}, "Подключение по ssh")], "b-g11", sz="b-lg")
    # ---------------------------------------------------------------- pptx 26
    T26 = "Проверка <em>соединения</em>"
    lay("Команда show", T26, [
        tile("b_search", "Для диагностики, выявления причины неполадок, связанных с работой сети, и их устранения, требуется "
                         "произвести проверку работы устройств.", "b", "Диагностика"),
        tile("b_eye", "Основной командой для просмотра информации является команда <b>show</b>. Данная команда выполняется из "
                      "привилегированного режима.", "v", "show"),
        tile("b_info", "Для получения доступных опций после ввода команды show, используйте символ &lt;?&gt;.", "a", "Подсказка"),
        term(["esr-200#", "esr-200# show", "aaa                  Show aaa information", "alarm                Show alarm information",
              "alarms               Show alarms information", "archive              Show archive information",
              "arp                  Show the entries information in the ARP cache", "bfd                  Show BFD",
              "bgp                  Show BGP information", "bootvar              Show boot parameters",
              "candidate-config     Show the configuration that is currently"], "show ?")],
        ['<div class="b-cap">К наиболее известным или часто используемым командам можно отнести:</div>', _show_cards()], "b-g11")
    # ---------------------------------------------------------------- pptx 27
    lay("show interfaces status", T26, [
        tile("b_info", "Команда <b>show version</b> информирует о версии программного обеспечения.", "m", "show version"),
        tile("b_eye", "Команда <b>show interfaces status</b> предоставляет информацию обо всех интерфейсах маршрутизатора, "
                      "включая физические и виртуальные, размере окна, MAC-адресах и времени последнего изменения.", "v",
             "show interfaces status"),
        tile("b_search", "Для отображения информации о конкретном интерфейсе требуется ввести команду <b>show interfaces status "
                         "&lt;интерфейс&gt;</b>. Список доступных интерфейсов на маршрутизаторе можно увидеть, введя знак "
                         "вопроса &lt;?&gt; после команды show interfaces status.", "g", "Один интерфейс")],
        [term(["esr-200# show interfaces status ?", "bridge                 Show bridge interface's state",
               "e1                     Show e1 interface's state",
               "fortygigabitethernet   Show fortygigabitethernet interface's state",
               "gigabitethernet        Show gigabitethernet interface's state",
               "loopback               Show loopback interface's state", "modem                  Show modem interface's state",
               "multilink              Show multilink interface's state",
               "port-channel           Show port-channel interface's state",
               "tengigabitethernet     Show tengigabitethernet interface's state"])], "b-g11", sz="b-lg")
    full("Вывод show interfaces status", T26, step(term(["Interface          Admin  Link   MTU    MAC address         Last change                  Mode",
               "                   State  State",
               "-----------------  -----  -----  -----  ------------------  ---------------------------  -----------",
               "gi1/0/1            Up     Up     1500   de:93:87:98:56:0a   6 days, 17 minutes and 51    routerport",
               "                                                            seconds", "",
               "gi1/0/1.70         Up     Up     1500   de:93:87:98:56:0a   20 hours, 34 minutes and     routerport",
               "                                                            9 seconds", "",
               "gi1/0/1.70.420     Up     Up     1500   de:93:87:98:56:0a   20 hours, 34 minutes and     routerport",
               "                                                            9 seconds", "",
               "gi1/0/2            Up     Up     1500   7a:b6:74:0d:64:a1   6 days, 17 minutes and 51    routerport",
               "                                                            seconds", "",
               "gi1/0/3            Up     Up     1500   e2:c0:7b:48:ed:a1   6 days, 17 minutes and 51    routerport",
               "                                                            seconds", "",
               "lo1                Up     Up     1500   f6:04:9d:a3:64:45   20 hours, 34 minutes and     routerport",
               "                                                            9 seconds"], "show interfaces status")))
    # ---------------------------------------------------------------- pptx 28
    lay("Интерфейс gi1/0/1", T26, [
        tile("b_search", "Выведем информацию об интерфейсе gi1/0/1. Для этого введем команду <b>show interfaces status "
                         "gigabitethernet 1/0/1</b>.", "b", "Один интерфейс"),
        conf(["esr-200# show interfaces status gigabitethernet 1/0/1"], "Команда"), _if_card()],
        [callouts(["Interface 'gi1/0/1' status information:", "Description:            --", "Operational state:      Up",
                   "Administrative state:   Up", "Track ID:               --", "Supports broadcast:     Yes",
                   "Supports multicast:     Yes", "MTU:                    1500", "MAC address:            de:93:87:98:56:0a",
                   "Last change:            6 days, 25 minutes and 42 seconds", "Mode:                   routerport"],
                  {2: ("работает", "g"), 3: ("включен", "g"), 7: ("MTU", "b"), 8: ("MAC", "v"), 10: ("режим", "a")})], "b-g11")
    # ---------------------------------------------------------------- pptx 29
    T29 = "Сообщения <em>ICMPv4</em>"
    slide("Сообщения ICMPv4", sc(head(T29), '<div class="g grow"><div class="col ixstack b-lg">%s%s%s%s</div></div>' % (
        step(tile("b_info", "Протокол <b>ICMP</b> (Internet Control Message Protocol) предназначен для получения уведомлений "
                            "об ошибках передачи или успешной доставке пакетов.", "b", "ICMP")),
        '<div class="b-cap">ICMP-сообщения включают в себя следующие функции:</div>', _icmp_funcs(),
        step(F.icmp_format()))))
    lay("ICMP: содержимое полей", T29, [
        tile("table", "Формат сообщения ICMP зависит от полей Тип и Код. Поле Тип указывает на тип сообщения, а поле Код "
                      "содержит параметр, сопоставленный с типом сообщения. Поле Контрольная сумма используется для проверки "
                      "на ошибки.", "b", "Тип · Код · Контрольная сумма"),
        tile("msg", "Поле Содержание сообщения ICMP. Если это поле не используется, то 32 бита обычно заполняются 0.", "v",
             "Содержание"),
        tile("b_redir", "В сообщении перенаправления ICMP в этом поле указывается IP-адрес шлюза. Хост перенаправляет пакеты на "
                        "указанный шлюз, которому присваивается этот IP-адрес.", "a", "Redirect"),
        tile("b_ping", "В сообщении эхо-запроса это поле содержит идентификатор и последовательный номер. Источник ассоциирует "
                       "полученный эхо-ответ с эхо-запросом, отправленным локальной стороной на основе идентификаторов и "
                       "последовательных номеров, передаваемых в сообщениях. Когда источник отправляет несколько эхо-запросов "
                       "на адрес назначения, каждый эхо-ответ должен иметь такие же идентификатор и последовательный номер, "
                       "как в эхо-запросе.", "g", "Echo")],
        [F.icmp_codes()], "b-g11")
    info(29, T29)
    # ---------------------------------------------------------------- pptx 30
    T30 = "Тестирование <em>локального узла</em>"
    lay("Подтверждение узла", T30, [
        tile("b_ping", "<b>Подтверждение узла</b> - ICMP-запрос, используемый для определения доступности узла. "
                       "Узел-отправитель отправляет узлу получателю ICMP эхо-запрос. Если узел-получатель доступен, то "
                       "производится отправка эхо-ответа.", "b", "Эхо-запрос → эхо-ответ"),
        tile("b_term", "Такое использование эхо-запросов по протоколу ICMP заложено в основу служебной программы проверки "
                       "связи.", "v", "Основа ping"),
        tile("b_clock", "Эхо-сообщения ICMP используются для проверки сетевого соединения между источником и назначением и "
                        "предоставления прочей информации, например времени приема-передачи.", "g", "Время"),
        tile("gear", "В команде ping могут быть указаны различные параметры, такие как размер сообщений ICMP, количество "
                     "сообщений ICMP, отправляемых одновременно, и период времени ожидания ответа. Устройства формируют "
                     "сообщения ICMP на основе параметров и выполняют тесты ping.", "a", "Параметры")],
        [tile("b_search", "Типичным применением протокола ICMP является тестирование командой <b>ping</b>. <b>Ping</b> - это "
                          "распространенный инструмент, используемый для проверки подключения к сети и сбора другой связанной "
                          "информации.", "a", "ping"),
         _ping_mini()], sz="b-sm")
    slide("Сцена: пример ping", sc(head(T30, "Пример команды Ping — эхо-запрос и эхо-ответ по шагам."),
                                   grow("g", col(F.ping_scene()))))
    info(30, T30)
    # ---------------------------------------------------------------- pptx 31
    T31 = "Переадресация <em>маршрутов</em>"
    lay("Redirect ICMP", T31, [
        tile("b_redir", "Сообщение перенаправления (<b>Redirect</b>) ICMP - это тип управляющего сообщения ICMP.", "b", "Redirect"),
        tile("b_search", "Когда маршрутизатор обнаруживает, что хост использует неоптимальный маршрут в определенном сценарии, "
                         "маршрутизатор отправляет хосту сообщение переадресации ICMP, чтобы хост изменил маршрут.", "v",
             "Когда"),
        tile("b_info", "Это сообщение может использоваться только в том случае, если узел-источник находится в той же "
                       "физической сети, что и шлюзы", "a", "Условие")],
        [F.redirect_scene()], "b-g12")
    info(31, T31)
    # ---------------------------------------------------------------- pptx 32
    T32 = "Назначение или <em>услуга недоступны</em>"
    lay("Назначение недоступно", T32, [
        tile("b_search", "В ICMP определены различные сообщения об ошибках для диагностики проблем с сетевыми соединениями. "
                         "Отправитель может определить причину неисправности передачи данных на основе полученных сообщений "
                         "об ошибке.", "b", "Сообщения об ошибках"),
        tile("b_x", "Например, когда сетевое устройство, получив пакет, не имеет доступ к сети, где находится устройство "
                    "назначения, оно автоматически отправляет ICMP сообщение отправителю о недоступности узла назначения.",
             "r", "Пример"),
        tile("b_info", "При получении узлом или шлюзом пакета, который невозможно доставить, используются ICMP-сообщения типа "
                       "«Назначение недоступно», сообщая источнику о том, что место назначения или услуга является "
                       "недоступной. Такое сообщение содержит в себе код ошибки, который сообщает, по какой причине доставка "
                       "пакета не может быть выполнена.", "a", "Код ошибки")],
        [_unreach()])
    info(32, T32)
    # ---------------------------------------------------------------- pptx 33
    T33 = "Истечение <em>времени</em>"
    lay("Истечение времени", T33, [
        tile("b_ttl", "Сообщение об истечении времени используется протоколом ICMPv4 для указания маршрутизаторам на то, что "
                      "пакет невозможно переслать из-за изменения значения в поле TTL в IP-пакете на 0.", "a", "TTL = 0"),
        tile("b_x", "При получении пакета со значением TTL, равным 1, и изменением значения в поле TTL IPv4-пакета на ноль, "
                    "маршрутизатор отбрасывает пакет и отправляет на узел источника сообщение об истечении времени жизни "
                    "пакета.", "r", "Отбрасывает")],
        [_ttl0(),
         tile("b_search", "<b>Tracert</b> является типичным применением ICMP. Tracert проверяет доступность каждого узла на пути "
                          "передачи на основе значения TTL, переданного в заголовке пакета.", "v", "Tracert")])
    lay("Tracert по шагам", T33, [
        tile("b_ttl", "При тестировании доступности конкретного адреса назначения с помощью Tracert отправитель сначала "
                      "устанавливает в пакете значение TTL равным 1. Когда пакет достигает первого маршрутизатора, значение "
                      "TTL истекает (становится равным 0). Поэтому первый маршрутизатор отправляет источнику сообщение ICMP TTL "
                      "Timeout, содержащее метку времени.", "b", "TTL = 1"),
        tile("b_ttl", "Затем отправитель перед отправкой следующего тестового пакета устанавливает в нем значение TTL равное 2. "
                      "Когда пакет достигает второго маршрутизатора на пути к получателю, значение TTL истекает. Второй "
                      "маршрутизатор также возвращает сообщение ICMP TTL Timeout.", "v", "TTL = 2"),
        tile("b_ok", "Процесс повторяется до тех пор, пока пакет не достигнет узла назначения. Таким образом, источник может "
                     "отслеживать каждый маршрутизатор, через который проходит пакет, на основе информации в возвращенном "
                     "пакете, и рассчитывать время приема-передачи на основе меток времени.", "g", "До узла назначения")],
        [_tracert_scene()], sub="Пример команды Tracert")
    # ---------------------------------------------------------------- pptx 34
    lay("Проверка ping в сегменте", T30, [
        tile("b_ping", "Для проверки сетевой связности между узлами, расположенными в одном сегменте локальной сети, "
                       "воспользуемся утилитой ping. Можно проверить наличие сетевой связности между устройствами путем "
                       "отправки и приема эхо-запросов.", "b", "ping в сегменте"),
        tile("b_clock", "После получения каждого эхо-ответа служба тестирования предоставляет данные о времени, прошедшем между "
                        "отправкой запроса и получением ответа. Это позволяет измерить производительность сети.", "g", "Время"),
        tile("b_x", "Поскольку время для получения эхо-ответа ограничено, если по прошествии временного промежутка эхо-ответ не "
                    "получен, узлу отправителю сообщается, что ответа от указанного сетевого адреса не поступает. Это часто "
                    "указывает на наличие проблемы, возможно, вызванной межсетевым экраном, который блокирует неразрешенный "
                    "трафик, включая эхо-запросы.", "r", "Нет ответа"),
        tile("table", "После отправки всех запросов пользователю предоставляется сводная информация, включая количество успешно "
                      "доставленных пакетов и информации о минимальном, максимальном и среднем времени прохождения запроса от "
                      "узла источника к узлу назначения.", "v", "Сводка")],
        [_ping_summary()], "b-g11", sz="b-sm")
    info(34, T30)
    # ---------------------------------------------------------------- pptx 35
    lay("Ping шлюза по умолчанию", T30, [
        tile("b_ping", "Для проверки сетевой связности инициировать отправку эхо-запроса можно не только по адресам оконечных "
                       "устройств, но также с использованием адреса шлюза по умолчанию.", "b", "ping шлюза"),
        tile("b_x", "Если по каким-то причинам пришел запрос, но устройство не ответило, требуется произвести проверку с любым "
                    "другим оконечным узлом в локальной сети.", "r", "Нет ответа"),
        tile("b_search", "Если устройства отвечают на эхо-запросы, следует проверить настройки узла, возможно, был некорректно "
                         "задан IP-адрес шлюза по умолчанию, или на маршрутизаторе интерфейс функционирует исправно, но не "
                         "отключен межсетевой экран, который не позволяет пропускать трафик.", "a", "Что проверить")],
        [_gw_flow()])
    info(35, T30)
    # ---------------------------------------------------------------- pptx 36
    T36 = "Тестирование <em>удаленного узла</em>"
    checks = ("Возможность передачи трафика в рамках локальной сети;", "Работу маршрутизатора в качестве шлюза по умолчанию;",
              "Взаимодействие и работу других маршрутизаторов, которые являются составными частями маршрута от "
              "узла-источника к узлу-назначения и обратно;",
              "Подтверждение работы узла назначения. Если отправитель по каким-то причинам не получил ответ, одной из "
              "причин могут являться правила, настроенные системным администратором, которые запрещают прием "
              "ICMP-сообщений в сеть получателя. Применение таких методов обеспечения безопасности может стать "
              "причиной отсутствия эхо-ответов.")
    lay("Удаленный узел", T36, [
        tile("globe", "Кроме возможности проверки связности между локальными узлами для обмена данными по сети, существует "
                      "также возможность проверки связности с узлами в удаленных сетях путем отправки эхо-запросов. Можно "
                      "проверить сразу несколько моментов:", "b", "Удалённая сеть")]
        + ['<div class="ixt t-%s b-num"><u>%d</u><p>%s</p></div>' % (tn, i + 1, c)
           for i, (c, tn) in enumerate(zip(checks, ("b", "v", "a", "g")))],
        [_remote_checks()], sz="b-sm")
    info(36, T36)
    # ---------------------------------------------------------------- pptx 37
    T37 = "Тестирование <em>пути</em>"
    lay("Тестирование пути", T37, [
        tile("b_ping", "Мы рассмотрели положительные стороны использования эхо-запросов для проверки сетевой связности "
                       "устройств.", "b", "ping"),
        tile("b_x", "Но пользователь не получает информации об устройствах, которые находятся на пути между отправителем и "
                    "получателем. По всему маршруту между отправителем и получателем может быть расположено множество "
                    "маршрутизаторов.", "r", "Чего не видно"),
        tile("path", "Для отображения всех промежуточных устройств на пути между отправителем и получателем используется "
                     "команда <b>tracert</b> (ОС Windows) или <b>traceroute</b> (Unix-подобные системы), которая выводит "
                     "список всех промежуточных устройств, через которые прошел запрос от отправителя к получателю.", "v",
             "tracert / traceroute"),
        tile("b_term", "Чтобы посмотреть маршрут следования пакета от компьютера к серверу с доменным именем eltex-co.ru, "
                       "требуется ввести в терминале команду <b>traceroute eltex-co.ru</b>.", "g", "Пример")],
        [_trace_why()])
    slide("Сцена: traceroute", sc(head(T37, "Возможный маршрут следования пакета от источника к получателю по сети Интернет."),
                                  grow("g", col(F.trace_scene()))))
    lay("Результат traceroute", T37, [
        callouts(["user@user-System-Product-Name:~$ traceroute eltex-co.ru",
                  "traceroute to eltex-co.ru (62.109.1.166), 30 hops max, 60 byte packets",
                  " 1  _gateway (10.25.8.1)  3.237 ms  4.995 ms  6.546 ms",
                  " 2  10.25.0.18 (10.25.0.18)  2.292 ms  3.928 ms  4.944 ms",
                  " 3  10.25.0.22 (10.25.0.22)  2.254 ms  3.302 ms  4.276 ms",
                  " 4  10.25.0.26 (10.25.0.26)  2.996 ms  3.407 ms  3.951 ms",
                  " 5  10.220.220.1 (10.220.220.1)  3.687 ms  4.862 ms  6.153 ms",
                  " 6  router.eltex.loc (172.16.0.1)  0.228 ms  0.320 ms  0.381 ms",
                  " 7  b-internet.92.125.152.57.snt.ru (92.125.152.57)  26.585 ms  25.444 ms  25.425 ms",
                  " 8  * * *",
                  " 9  5.143.250.114 (5.143.250.114)  43.638 ms  42.997 ms  43.062 ms",
                  "10  msk-m9-cr5.ae667-3004.rascom.as20764.net (80.64.97.58)  66.939 ms  43.367 ms  42.746 ms",
                  "11  msk-m9-cr5.ae666-3004.rascom.as20764.net (80.64.97.59)  42.425 ms  42.541 ms  42.866 ms",
                  "12  msk-m9-cr3.xe-10-1-12-2993.rascom.as20764.net (80.64.102.134)  43.288 ms  43.093 ms  43.055 ms",
                  "13  FRT.msk-m9-cr2.rascom.as20764.net (80.64.102.135)  43.029 ms  57.898 ms  57.802 ms",
                  "14  * * *", "15  * * *",
                  "16  new.eltex-co.ru (62.109.1.166)  44.438 ms  43.901 ms  43.682 ms",
                  "user@user-System-Product-Name:~$ █"],
                 {2: ("шлюз", "b"), 8: ("провайдер", "v"), 9: ("ICMP фильтруется", "r"), 15: ("* * *", "r"),
                  16: ("* * *", "r"), 17: ("получатель", "g")}, "traceroute eltex-co.ru")],
        [tile("b_x", "Если при каком-то из переходов возникают проблемы при передаче данных, указывается адрес последнего "
                     "ответившего маршрутизатора, где возникла проблема.", "r", "Проблема"),
         tile("shield", "Звездочками в процессе трассировки в данном случае отмечены те устройства, у которых в настройках "
                        "безопасности настроена фильтрация ICMP-запросов (пакетов, которые остались без ответа или были "
                        "потеряны).", "a", "* * *"),
         tile("b_search", "Полученную информацию о маршруте прохождения пакета, можно использовать для диагностики состояния "
                          "маршрута, с указанием порядка прохождения пакетом промежуточных устройств и времени прохождения "
                          "каждого из них.", "g", "Диагностика")], "b-g21", sz="b-sm")
    info(37, T37)


CSS = r"""
.b-g11{grid-template-columns:1fr 1fr!important;gap:22px!important}
.b-g12{grid-template-columns:.7fr 1.5fr!important;gap:22px!important}
.b-g21{grid-template-columns:1.35fr .9fr!important;gap:22px!important}
.b-sm .ixt p,.b-sm .c li{font-size:clamp(12px,.98vw,19px)!important;line-height:1.35}.b-sm .ixk{font-size:clamp(12px,.98vw,19px)!important}
.b-sm .ixt{padding:9px 12px!important}
.b-lg>.col{justify-content:center}.b-lg .ixt p{font-size:clamp(16px,1.7vw,32px)!important}.b-lg .ixk{font-size:clamp(16px,1.55vw,30px)!important}
.slide>.sc>.g.grow.b-sm .c ul.li li,.b-sm .c ul.li li{font-size:clamp(12px,1vw,19px)!important;line-height:1.35}
.b-lg pre.cli{font-size:clamp(15px,1.55vw,30px)!important}.b-lg pre.cli.term{font-size:clamp(12px,1.1vw,21px)!important}
.b-lg .ericmp{font-size:clamp(16px,1.75vw,34px)!important;margin-top:18px}.b-lg .ericmp span{padding:14px 22px}.b-lg .b-ln pre{font-size:clamp(12px,1.15vw,22px)}
.b-lg .b-4{grid-template-columns:repeat(4,minmax(0,1fr))}.b-lg .b-4 .ixp{width:clamp(44px,4vw,76px);height:clamp(44px,4vw,76px)}
.b-r{gap:12px!important;justify-content:flex-start}
.b-r>.step>.figwrap,.b-r>.step>.scene{width:100%}
.b-cmd{display:flex;flex-wrap:wrap;gap:8px;align-items:flex-end;padding:12px 14px;border-radius:16px;background:#141838}
.b-cmd span{display:flex;flex-direction:column;align-items:center;gap:6px}
.b-cmd code{font:800 clamp(16px,1.6vw,30px)/1 "JetBrains Mono",Consolas,monospace;color:#fff;padding:8px 12px;border-radius:10px;
 background:color-mix(in srgb,var(--tc) 55%,#141838);border:2px solid var(--tc)}
.b-cmd i{font:700 clamp(10px,.8vw,15px)/1.1 "Golos Text",sans-serif;font-style:normal;color:#c9cdf5;min-height:1em}
.b-out{background:#141838;border:1.5px solid #5a62c8;border-radius:12px;padding:10px 8px;overflow:hidden}
.b-ln{display:flex;align-items:center;gap:10px;border-radius:7px;padding:0 6px}
.b-ln pre{margin:0;flex:1;font:500 clamp(10px,.92vw,18px)/1.5 "JetBrains Mono",Consolas,monospace;color:#e6e9ff;white-space:pre;overflow:hidden;text-overflow:ellipsis}
.b-ln.on{background:color-mix(in srgb,var(--tc) 30%,#141838);box-shadow:inset 4px 0 0 var(--tc)}
.b-ln em{flex:0 0 auto;font:800 clamp(10px,.82vw,16px)/1 "Golos Text",sans-serif;font-style:normal;color:#fff;background:var(--tc);
 padding:5px 9px;border-radius:8px}
.b-flow{display:flex;flex-wrap:wrap;align-items:center;gap:10px;padding:16px;border-radius:16px;background:rgba(255,255,255,.88);border:1.5px solid #fff}
.b-flow span{font:800 clamp(14px,1.3vw,25px)/1 "JetBrains Mono",Consolas,monospace;color:#fff;background:var(--tc);padding:10px 14px;border-radius:12px}
.b-flow b{color:#6a70a8;font-size:clamp(16px,1.5vw,28px)}
.b-cap{font:800 clamp(14px,1.25vw,24px)/1.3 var(--fd);color:#141a5c;padding:4px 2px}
.b-show{display:grid;grid-template-columns:1fr;gap:10px}
.b-show .ixt{padding:12px 14px}.b-mono{font-family:"JetBrains Mono",Consolas,monospace!important}
.b-dim{color:#6a70a8;font-style:italic;font-weight:600}
.b-4{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.b-4 p{overflow-wrap:anywhere}
.b-4 .ixt{align-items:center;padding:12px 14px}.b-4 .ixt p{font-weight:800}
.b-num{align-items:center}
.b-num u{flex:0 0 auto;text-decoration:none;display:grid;place-items:center;width:clamp(30px,2.6vw,48px);height:clamp(30px,2.6vw,48px);
 border-radius:50%;background:var(--tc);color:#fff;font:900 clamp(15px,1.4vw,26px)/1 var(--fd)}
"""
