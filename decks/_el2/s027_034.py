# -*- coding: utf-8 -*-
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from _el2_lib import ico, arrow_svg

SLIDES = []   # (ref, label, html)
NAVY = "#12245e"
SVG_OPEN = '<svg class="ab" style="left:0;top:0;width:1920px;height:1080px;overflow:visible" viewBox="0 0 1920 1080">'


def A(l, t, w=None, h=None, extra=""):
    s = f"position:absolute;left:{l}px;top:{t}px;"
    if w is not None: s += f"width:{w}px;"
    if h is not None: s += f"height:{h}px;"
    return s + extra


def ds(s):
    return f' data-s="{s}"' if s else ""


def box(l, t, w, h, inner="", cls="card", s=None, extra=""):
    return f'<div class="{cls}"{ds(s)} style="{A(l, t, w, h, extra)}">{inner}</div>'


def txt(l, t, w, text, size=22, weight=400, color="var(--ink)", s=None, extra="", cls=""):
    return (f'<div class="{cls}"{ds(s)} style="{A(l, t, w, None, f"font-size:{size}px;font-weight:{weight};color:{color};line-height:1.25;" + extra)}">{text}</div>')


def path(d, s, col="var(--blue)", w=4):
    return f'<path class="dr" data-s="{s}" pathLength="1" d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def icoS(name, cls, box_px, glyph_px):
    h = ico(name, cls)
    h = h.replace(f'class="ico {cls}"', f'class="ico {cls}" style="width:{box_px}px;height:{box_px}px"', 1)
    return h.replace("<svg ", f'<svg style="width:{glyph_px}px;height:{glyph_px}px" ', 1)


def dot(col, size=15):
    return f'<i style="display:inline-block;width:{size}px;height:{size}px;border-radius:50%;background:{col};flex:none"></i>'


# =========================================================== p027
def p027():
    L, W, H = 150, 1620, 1080

    def tile(x0, y0, x1, y1, s=None):
        return (f'<div{ds(s)} style="{A(L + x0 * W, y0 * H, (x1 - x0) * W, (y1 - y0) * H, "overflow:hidden")}">'
                f'<img src="assets/p027_network.jpg" alt="Схема сети" style="position:absolute;left:{-x0 * W}px;top:{-y0 * H}px;'
                f'width:{W}px;height:{H}px;display:block"></div>')
    return "".join([tile(0, 0, 1, .305), tile(0, .30, .352, 1, 1), tile(.348, .30, .692, 1, 2), tile(.688, .30, 1, 1, 3)])


SLIDES.append(("p027", "Схема сети: интернет и три офиса", p027()))


# =========================================================== p028
def p028():
    o = ['<h1 class="t left ab" style="left:72px;top:44px;width:1000px;font-size:58px;line-height:1.0">Подключение<br>'
         '<span style="color:var(--blue)">к сетевому устройству</span></h1>']
    o.append(txt(75, 168, 840, "Для доступа к сетевому оборудованию можно использовать консольное подключение или удалённый доступ по протоколам Telnet/SSH.",
                 21, 400, "var(--ink)"))
    o.append('<img src="assets/p028_switch_top.jpg" alt="Порты управления коммутатора" style="'
             + A(985, 0, 900, 316, "display:block;object-fit:contain") + '">')

    o.append(box(38, 296, 906, 612, "", "card", 1))
    o.append(box(964, 296, 926, 612, "", "card", 5))

    def head(l, n, title, sub, s):
        return (txt(l + 46, 330, 100, n, 62, 300, "var(--blue)", s, "font-family:var(--mono);line-height:1")
                + txt(l + 142, 322, 700, title, 33, 800, NAVY, s)
                + txt(l + 142, 372, 640, sub, 20, 400, "var(--dim)", s))

    o.append(head(38, "01", "Консольное подключение", "Используется для первоначальной настройки или когда недоступен удалённый доступ.", 1))
    o.append(head(964, "02", "Удалённый доступ (Telnet / SSH)", "Используется для управления устройством через сеть по IP-адресу.", 5))

    def lst(l, w, items, s):
        ys = [490, 548, 606, 668, 730]
        out = [txt(l, 434, 400, "Что необходимо:", 20, 700, NAVY, s)]
        for k, (y, t) in enumerate(zip(ys, items)):
            out.append(f'<div data-s="{s + 1}" style="{A(l, y - 22, w + 60, None, f"display:flex;gap:16px;align-items:center;--dl:{k * 90}ms")}">'
                       f'<span class="badge" style="width:40px;height:40px;border-radius:50%;font-size:20px;flex:none">{k + 1}</span>'
                       f'<span style="font-size:17.5px;line-height:1.3;width:{w}px;color:var(--ink)">{t}</span></div>')
        return "".join(out)

    o.append(lst(70, 360, ["Консольный порт на коммутаторе или маршрутизаторе (разъём RJ-45).",
                           "Консольный кабель (RJ-45 &harr; RS-232).",
                           "Адаптер-переходник RS-232 – USB.",
                           "USB-интерфейс на ПК или ноутбуке администратора сети.",
                           "Программа эмуляции терминала (PuTTY, Tera Term, HyperTerminal, minicom и др.)."], 1))
    o.append(lst(1000, 345, ["Активный интерфейс с IP-адресом на коммутаторе или маршрутизаторе.",
                             "Кабель локальной сети (например, витая пара категории 7, разъём RJ-45).",
                             "Знать логин и пароль администратора.",
                             "ПК или ноутбук администратора сети подключены к локальной сети.",
                             "Программа эмуляции терминала (PuTTY, HyperTerminal, minicom и т.д.)."], 5))
    o.append(f'<img data-s="3" src="assets/p028_console_cable.jpg" alt="Консольный кабель" style="{A(512, 392, 420, 264, "display:block")}">')
    o.append(f'<img data-s="3" src="assets/p028_adapter_laptop.jpg" alt="Адаптер RS-232 – USB и программа эмуляции терминала" style="{A(494, 664, 440, 147, "display:block")}">')
    o.append(f'<img data-s="6" src="assets/p028_putty_laptop.jpg" alt="Окно PuTTY Configuration" style="{A(1420, 430, 455, 335, "display:block")}">')

    o.append(box(66, 800, 860, 96, f'<div style="display:flex;gap:20px;align-items:center;height:100%">{icoS("gear", "", 64, 34)}'
                 '<p class="b" style="font-size:20px;line-height:1.3">При создании консольного подключения в программе эмуляции терминала необходимо установить скорость 115200 бит/с.</p></div>',
                 "card solid", 4, "padding:14px 22px;border-radius:20px"))
    o.append(box(996, 776, 866, 116, f'<div style="display:flex;gap:20px;align-items:center;height:100%">{icoS("gear", "", 64, 34)}'
                 '<p class="b" style="font-size:20px;line-height:1.3">При создании нового подключения в программе эмуляции терминала по протоколам Telnet или SSH необходимо указать IP-адрес, настроенный на интерфейсе маршрутизатора во время выполнения базовой настройки.</p></div>',
                 "card solid", 7, "padding:12px 22px;border-radius:20px"))

    def info(l, w, icn, title, text, s):
        return box(l, 924, w, 140, f'<div style="display:flex;gap:18px;align-items:flex-start">{ico(icn, "sm")}<div>'
                   f'<div style="font-size:19px;font-weight:800;color:var(--blue)">{title}</div>'
                   f'<p class="b dim" style="font-size:15.5px;line-height:1.3;margin-top:4px">{text}</p></div></div>',
                   "card solid", s, "padding:14px 20px;border-radius:18px")
    o.append(info(38, 600, "net", "RJ-45", "Registered Jack («Зарегистрированный разъём») — стандартизированный физический сетевой интерфейс, состоящий из «вилки» и «розетки», а также схемы их взаимодействия.", 8))
    o.append(info(660, 640, "cable", "RS-232", "Recommended Standard 232 (EIA-232) — стандарт физического уровня, поддерживающий последовательный порт персональных компьютеров. Тип разъёма DE-9 (из-за формы в виде буквы «D», E — размер разъёма, 9 контактов). В современных сетях почти вытеснен стандартом USB.", 8))
    o.append(info(1322, 566, "term", "Программы эмуляции терминала", "Бывают платные, бесплатные и условно-бесплатные. Можно скачать в открытом доступе с официального сайта производителя.", 8))
    return "".join(o)


SLIDES.append(("p028", "Подключение к сетевому устройству", p028()))


# =========================================================== p029
def p029():
    o = ['<h1 class="t ab ctr-x" style="top:34px;width:1600px;font-size:74px">Синтаксис команд <span class="lt">ESR</span></h1>']
    GRN, PUR, BLU = "#1a9a55", "#7b3fc4", "#2a6bf2"

    def sp(c, t): return f'<span style="color:{c}">{t}</span>'
    cmd = (sp(NAVY, "esr#") + " " + sp(PUR, "ping") + " " + sp(BLU, "{") + " " + sp(BLU, "&lt;ADDR&gt;") + " " + sp(NAVY, "|") + " "
           + sp(BLU, "&lt;HOSTNAME&gt;") + " " + sp(BLU, "}") + " " + sp(NAVY, "[") + " " + sp(GRN, "packets") + " " + sp(BLU, "&lt;NUM&gt;") + " "
           + sp(NAVY, "]") + " " + sp(NAVY, "[") + " " + sp(GRN, "size") + " " + sp(BLU, "&lt;NUM&gt;") + " " + sp(NAVY, "]") + " "
           + sp(NAVY, "[") + " " + sp(GRN, "detailed") + " " + sp(NAVY, "]"))
    o.append(box(64, 196, 1795, 106, f'<div class="mono" style="font-size:37px;font-weight:700;white-space:nowrap;text-align:center;line-height:60px">{cmd}</div>',
                 "card solid", None, "padding:20px 10px;border-radius:26px"))

    def pill(cx, w, text, bg, col, s):
        return (f'<div data-s="{s}" style="{A(cx - w / 2, 361, w, 58, f"background:{bg};color:{col};border-radius:14px;display:flex;align-items:center;justify-content:center;text-align:center;font-size:21px;font-weight:700;line-height:1.05")}">{text}</div>')
    sv = [SVG_OPEN]
    items = [(139, 138, "Режим", "#dfe6f6", NAVY, NAVY, 2), (262, 156, "Команда", "#e5dbf8", PUR, PUR, 2),
             (1124, 160, "Параметр", "#d8e6fb", BLU, BLU, 4), (1482, 160, "Параметр", "#d8e6fb", BLU, BLU, 4),
             (925, 152, "Ключевое слово", "#d9f3e4", GRN, GRN, 4), (1312, 152, "Ключевое слово", "#d9f3e4", GRN, GRN, 4),
             (1717, 200, "Ключевое слово", "#d9f3e4", GRN, GRN, 4)]
    for cx, w, t, bg, col, ac, s in items:
        o.append(pill(cx, w, t, bg, col, s))
        sv.append(arrow_svg(cx, 304, cx, 352, s, ac, 4))
    o.append(pill(580, 400, "Параметры", "#d6ecfb", BLU, 3))
    sv.append(path("M380 312 L380 322 L780 322 L780 312", 3, BLU, 4))
    sv.append(arrow_svg(580, 322, 580, 352, 3, BLU, 4))
    sv.append("</svg>")
    o.append("".join(sv))

    def big(l, w, icn, title, col, body, s, extra=""):
        return box(l, 470, w, 270, f'<div style="display:flex;gap:26px;align-items:flex-start">{icoS(icn, "hex", 124, 62)}<div>'
                   f'<div style="font-size:36px;font-weight:800;color:{col};text-transform:uppercase;line-height:1.1">{title}</div>'
                   f'<p class="b" style="font-size:24px;margin-top:10px;line-height:1.35">{body}</p></div></div>{extra}', "card solid", s, "padding:30px 32px;border-radius:26px")
    play = ('<div style="position:absolute;left:30px;bottom:18px;right:30px;border-top:1.5px solid var(--line);padding-top:12px;font-size:21px;'
            'display:flex;gap:14px;align-items:center"><span style="width:34px;height:34px;border-radius:50%;background:#dbe6ff;color:var(--blue);display:grid;place-items:center;font-size:14px">&#9654;</span>'
            'Выполнение — нажатием <b>Enter</b></div>')
    o.append(big(47, 597, "term", "Команда", PUR, "Зарезервированное слово или аббревиатура, вводимая после запроса командной строки.", 5, play))
    o.append(big(661, 593, "gear", "Ключевые слова", "#14867a", "Дополнительные настройки в виде зарезервированных слов, уточняющие выполнение команды.", 6))
    o.append(big(1273, 598, "doc", "Параметры", BLU, "Значения или переменные, заданные администратором: адреса, имена и числа.", 7))

    o.append(txt(75, 790, 900, "Условные обозначения", 38, 800, NAVY, 8, "text-transform:uppercase"))

    def small(l, w, glyph, title, body, top, s):
        return box(l, 835, w, 205, f'<div style="position:absolute;left:36px;top:14px;right:20px;text-align:center">{top}</div>'
                   f'<div style="position:absolute;left:26px;top:100px;display:flex;gap:22px;align-items:flex-start;right:20px">'
                   f'{glyph}<div><div style="font-size:26px;font-weight:800;color:{NAVY}">{title}</div>'
                   f'<p class="b" style="font-size:20px;margin-top:6px;line-height:1.3">{body}</p></div></div>', "card solid", s, "padding:0;border-radius:24px")

    def sym(t):
        return f'<span class="ico hex" style="width:96px;height:96px"><span class="mono" style="position:relative;font-size:46px;font-weight:700;color:var(--blue)">{t}</span></span>'
    o.append(small(36, 600, sym("{ }"), "Обязательный выбор", "Фигурные скобки — обязательные элементы. Вертикальная линия — выбрать один вариант.",
                   f'<span class="mono" style="font-size:25px;font-weight:700;color:{NAVY}">{{ <span style="color:{BLU}">&lt;ADDR&gt;</span> | <span style="color:{BLU}">&lt;HOSTNAME&gt;</span> }}</span>', 8))
    o.append(small(657, 629, sym("[ ]"), "Необязательные элементы", "Квадратные скобки — дополнительные параметры или ключевые слова.",
                   f'<span class="mono" style="font-size:20px;font-weight:700;color:{NAVY}">[ <span style="color:{GRN}">packets</span> <span style="color:{BLU}">&lt;NUM&gt;</span> ] [ <span style="color:{GRN}">size</span> <span style="color:{BLU}">&lt;NUM&gt;</span> ] [ <span style="color:{GRN}">detailed</span> ]</span>', 8))
    o.append(box(1297, 835, 584, 205, f'<div style="position:absolute;left:26px;top:34px;display:flex;gap:24px;align-items:flex-start">'
                 f'<span class="ico hex" style="width:96px;height:96px"><span style="position:relative;font-size:42px;font-weight:600;color:{NAVY}">Aa</span></span>'
                 f'<div><div style="font-size:26px;font-weight:800;color:{NAVY}">Начертание текста</div>'
                 '<p class="b" style="font-size:20px;margin-top:12px;line-height:1.35"><b>Жирный</b> — команды и ключевые слова<br><i>Обычный или курсив</i> — значения параметров</p></div></div>',
                 "card solid", 8, "padding:0;border-radius:24px"))
    return "".join(o)


SLIDES.append(("p029", "Синтаксис команд ESR", p029()))


# =========================================================== p030
DOC = ('<svg viewBox="0 0 110 130" style="width:160px;height:190px"><defs><linearGradient id="dg" x1="0" y1="0" x2="1" y2="1">'
       '<stop offset="0" stop-color="#7fa6ff"/><stop offset="1" stop-color="#3c63d8"/></linearGradient></defs>'
       '<path d="M12 6h58l28 28v88a6 6 0 0 1-6 6H12a6 6 0 0 1-6-6V12a6 6 0 0 1 6-6z" fill="url(#dg)"/>'
       '<path d="M70 6l28 28H76a6 6 0 0 1-6-6z" fill="#c9daff"/>'
       '<path d="M28 62h54M28 80h54M28 98h38" stroke="#fff" stroke-width="6" stroke-linecap="round"/></svg>')


def p030():
    o = ['<h1 class="t ab ctr-x" style="top:44px;width:1700px;font-size:70px">Файлы конфигурации <span class="lt">MES</span></h1>']
    TITLE_C = "#1c3f9e"

    def file_card(l, w, name, bullets, cmd, s):
        out = [box(l, 192, w, 490, "", "card", s)]
        out.append(f'<div data-s="{s}" style="{A(l + 70, 255, 170, 200)}">{DOC}</div>')
        out.append(txt(l + 290, 232, w - 300, name, 52, 800, TITLE_C, s))
        for k, b in enumerate(bullets):
            out.append(f'<div data-s="{s + 1}" style="{A(l + 290, 335 + k * 54, w - 310, None, f"display:flex;gap:14px;align-items:flex-start;font-size:22px;line-height:1.2;--dl:{k * 80}ms")}">'
                       f'<i style="width:17px;height:17px;border-radius:50%;background:var(--blue);margin-top:5px;flex:none"></i><span>{b}</span></div>')
        out.append(f'<div class="mono" data-s="{s + 1}" style="{A(l + 90, 572, w - 180, 78, "background:rgba(255,255,255,.9);border:1.5px solid var(--line);border-radius:16px;padding:0 34px;display:flex;align-items:center;font-size:28px;font-weight:500;color:" + NAVY + ";--dl:300ms")}">{cmd}</div>')
        return "".join(out)
    o.append(file_card(26, 917, "running-config", ["Текущая активная конфигурация", "Коммутатор работает по ней сейчас",
                                                   "Хранится в энергозависимой памяти (ОЗУ)", "Удаляется при выключении или перезагрузке"],
                       "console# show running-config", 1))
    o.append(file_card(977, 913, "startup-config", ["Начальная сохранённая конфигурация", "Хранится в виде файла",
                                                    "Загружается после включения или перезагрузки", "Изменения сохраняются только после команды копирования"],
                       "console# show startup-config", 3))

    o.append(box(36, 708, 984, 316, "", "card", 5))

    def blk(l, w, text, bg, s, col=TITLE_C):
        return (f'<div class="mono" data-s="{s}" style="{A(l, 790, w, 70, f"background:{bg};border:1.5px solid var(--line);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:29px;font-weight:700;color:{col}")}">{text}</div>')
    o.append(blk(70, 276, "running-config", "rgba(225,236,255,.95)", 5))
    o.append(blk(414, 214, "copy", "rgba(214,205,250,.95)", 5))
    o.append(blk(702, 276, "startup-config", "rgba(225,236,255,.95)", 5))
    o.append(SVG_OPEN + arrow_svg(352, 826, 408, 826, 5, "var(--blue)", 3) + arrow_svg(634, 826, 696, 826, 5, "var(--blue)", 3) + "</svg>")
    o.append(f'<div class="mono" data-s="6" style="{A(124, 896, 830, 76, "background:rgba(255,255,255,.9);border:1.5px solid var(--line);border-radius:16px;padding:0 30px;display:flex;align-items:center;font-size:27px;color:" + NAVY)}">console# copy running-config startup-config</div>')

    o.append(box(1045, 708, 836, 316, "", "card cream", 7, "background:rgba(253,240,222,.9)"))
    o.append(f'<div data-s="7" style="{A(1090, 738, 90, 80)}"><svg viewBox="0 0 64 60" style="width:84px;height:78px"><path d="M32 4L60 54H4z" fill="#f59a1c" stroke="#f59a1c" stroke-width="6" stroke-linejoin="round"/><path d="M32 22v16M32 45v2" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg></div>')
    o.append(txt(1196, 752, 640, "Очистка конфигурации", 38, 800, NAVY, 7, "text-transform:uppercase"))

    def cb(l, w, text, s):
        return (f'<div class="mono" data-s="{s}" style="{A(l, 843, w, 96, "background:rgba(255,255,255,.92);border:1.5px solid var(--line);border-radius:14px;padding:0 22px;display:flex;align-items:center;font-size:25px;line-height:1.25;color:" + NAVY)}">{text}</div>')
    o.append(cb(1081, 350, "console# delete startup-config", 7))
    o.append(cb(1488, 340, "console# reload", 8))
    o.append(SVG_OPEN + arrow_svg(1436, 891, 1482, 891, 8, "var(--blue)", 3) + "</svg>")
    o.append(txt(1075, 975, 780, "Удаление сохранённой конфигурации и перезагрузка коммутатора.", 21, 400, "var(--ink)", 8, "text-align:center"))
    return "".join(o)


SLIDES.append(("p030", "Файлы конфигурации MES", p030()))


# =========================================================== p031
def p031():
    o = ['<h1 class="t ab ctr-x" style="top:30px;width:1700px;font-size:66px">Обзор коммутаторов MES</h1>']
    leg = [("net", "Доступ"), ("layers", "Агрегация"), ("db", "ЦОД"), ("gear", "Промышленные")]
    xs = [366, 676, 972, 1215]
    o.append(box(341, 117, 1248, 80, "", "card solid", None, "border-radius:22px"))
    for x, (ic, t) in zip(xs, leg):
        o.append(f'<div style="{A(x, 128, None, 56, "display:flex;gap:14px;align-items:center")}">'
                 f'{ico(ic, "sm")}'
                 f'<span style="font-size:22px;font-weight:700;color:{NAVY};letter-spacing:.5px;text-transform:uppercase">{t}</span></div>')

    def card(l, t, w, h, tag, img, iw, ih, il, it, name, s):
        out = [box(l, t, w, h, "", "card", s)]
        out.append(f'<div data-s="{s}" style="{A(l + 14, t - 6, None, None, "background:linear-gradient(90deg,#2f6df0,#4f86f7);color:#fff;font-weight:800;font-size:21px;border-radius:18px;padding:6px 22px;letter-spacing:.5px;box-shadow:0 6px 14px rgba(42,107,242,.3)")}">{tag}</div>')
        out.append(f'<img data-s="{s}" src="assets/{img}" alt="{name}" class="cut" style="{A(il, it, iw, ih, "display:block")}">')
        return "".join(out)

    def lab(cx, y, name, cap, s):
        return (f'<div data-s="{s}" style="{A(cx - 330, y, 660, None, "text-align:center")}"><div style="font-size:42px;font-weight:800;color:{NAVY};line-height:1.1">{name}</div>'
                f'<div style="font-size:21px;color:var(--ink);margin-top:6px">{cap}</div></div>')
    o.append(card(38, 213, 598, 384, "АГРЕГАЦИЯ", "p031_mes5324.jpg", 520, 162, 77, 290, "MES5324", 1))
    o.append(lab(337, 466, "MES5324", "Коммутатор агрегации 10G/40G", 1))
    o.append(card(657, 213, 619, 384, "ДОСТУП", "p031_mes2300.jpg", 570, 160, 681, 292, "MES2300-24", 2))
    o.append(lab(966, 466, "MES2300-24", "Коммутатор доступа", 2))
    o.append(card(1286, 213, 595, 384, "ДОСТУП PoE", "p031_mes2308p.jpg", 540, 152, 1313, 294, "MES2308P", 3))
    o.append(lab(1583, 466, "MES2308P", "Коммутатор доступа с поддержкой PoE", 3))
    o.append(card(96, 614, 843, 431, "ПРОМЫШЛЕННЫЙ", "p031_mes3510s.jpg", 168, 288, 340, 640, "MES3510S-08P", 4))
    o.append(lab(517, 945, "MES3510S-08P", "Промышленный коммутатор", 4))
    o.append(card(964, 614, 834, 431, "ЦОД", "p031_mes5320.jpg", 780, 169, 992, 720, "MES5320-24", 5))
    o.append(lab(1381, 945, "MES5320-24", "Коммутатор для центра обработки данных", 5))
    return "".join(o)


SLIDES.append(("p031", "Обзор коммутаторов MES", p031()))


# =========================================================== p032
def p032():
    o = [f'<div class="ab" style="left:76px;top:22px;font-size:88px;font-weight:800;color:{NAVY};line-height:1;letter-spacing:-1px">MES2424P</div>',
         f'<div class="ab" style="left:78px;top:112px;font-size:34px;font-weight:800;color:#3d72e8;letter-spacing:1px;text-transform:uppercase">Передняя панель</div>']
    o.append('<img src="assets/p032_panel.jpg" alt="Передняя панель MES2424P" class="cut" style="' + A(85, 487, 1777, 210, "display:block") + '">')

    def cardbase(l, t, w, h, n, title, s, inner):
        return (box(l, t, w, h, "", "card solid", s, "border-radius:22px")
                + f'<span class="badge" data-s="{s}" style="{A(l + 20, t + 18, 64, 64, "border-radius:14px;font-size:38px")}">{n}</span>'
                + f'<div data-s="{s}" style="{A(l + 104, t + 30, w - 120, None, f"font-size:27px;font-weight:800;color:{NAVY};text-transform:uppercase;line-height:1.1")}">{title}</div>'
                + f'<div data-s="{s}" style="{A(l, t + 86, w, None)}">{inner}</div>')

    def body(icn, text):
        return (f'<div style="display:flex;gap:20px;align-items:center;padding:0 24px">{icoS(icn, "", 88, 52)}'
                f'<p class="b" style="font-size:21px;line-height:1.3">{text}</p></div>')
    o.append(cardbase(75, 207, 518, 190, 1, "Разъём питания", 1, body("power", "Подключение к источнику переменного тока")))
    leds = [("#2fa84f", "Power", "питание"), ("#2fa84f", "Status", "состояние устройства"), ("#e03030", "Alarm", "авария"), ("#2fa84f", "Fan", "состояние вентиляторов")]
    lt = "".join(f'<div style="display:flex;gap:12px;align-items:center;font-size:19px;line-height:1.38">{dot(c, 14)}<span><b>{a}</b> — {b}</span></div>' for c, a, b in leds)
    o.append(cardbase(693, 207, 561, 190, 2, "Индикаторы состояния", 2,
                      f'<div style="display:flex;gap:22px;align-items:center;padding:0 24px">{icoS("sun", "", 80, 50)}<div>{lt}</div></div>'))
    o.append(cardbase(1318, 207, 527, 190, 3, "Консольный интерфейс", 3, body("mon", "Локальное управление устройством")))

    def bl(items):
        return "".join(f'<div style="display:flex;gap:12px;align-items:flex-start;font-size:19px;line-height:1.3;margin-bottom:6px">{dot("var(--blue)", 11)}<span>{i}</span></div>' for i in items)
    f_icon = '<span class="ico" style="width:88px;height:88px;border-radius:20px"><i style="width:44px;height:44px;border-radius:50%;background:#2a4fd0;display:block"></i></span>'
    o.append(cardbase(100, 779, 578, 218, 4, "Функциональная кнопка F", 4,
                      f'<div style="display:flex;gap:22px;align-items:center;padding:0 24px">{f_icon}<div>{bl(["Менее 10 секунд — перезагрузка", "Более 10 секунд — перезагрузка и сброс настроек"])}</div></div>'))
    o.append(cardbase(732, 779, 516, 218, 5, "Ethernet-интерфейсы", 5, body("net", "Медные порты RJ-45")))
    o.append(cardbase(1322, 779, 523, 218, 6, "Uplink-интерфейсы", 6,
                      f'<div style="display:flex;gap:22px;align-items:center;padding:0 24px">{icoS("cable", "", 88, 52)}<div>{bl(["Подключение к вышестоящим устройствам", "Оптические модули SFP / SFP+"])}</div></div>'))
    sv = [SVG_OPEN,
          path("M160 397 L160 520", 1),
          path("M780 397 L780 462 L486 462 L486 548", 2),
          path("M1414 397 L1414 437 L612 437 L612 610", 3),
          path("M352 779 L352 750 L518 750 L518 672", 4),
          path("M679 716 L679 724 L1418 724 L1418 716 M1048 724 L1048 779", 5),
          path("M1472 722 L1472 732 L1834 732 L1834 722 M1653 732 L1653 779", 6),
          "</svg>"]
    o.append("".join(sv))
    return "".join(o)


SLIDES.append(("p032", "MES2424P: передняя панель", p032()))


# =========================================================== p033
def shield(kind, size=250):
    inner = ('<rect x="62" y="68" width="30" height="24" rx="5" fill="#fff"/><path d="M68 68v-7a9 9 0 0 1 18 0v7" fill="none" stroke="#fff" stroke-width="5"/>' if kind == "lock" else
             '<circle cx="76" cy="82" r="20" fill="#2a6bf2" stroke="#fff" stroke-width="3"/><path d="M66 82l7 7 13-14" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    return (f'<svg viewBox="0 0 110 120" style="width:{size}px;height:{size * 120 / 110:.0f}px;filter:drop-shadow(0 10px 18px rgba(40,80,200,.35))">'
            '<defs><linearGradient id="sh' + kind + '" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8db2ff"/><stop offset="1" stop-color="#3a62dc"/></linearGradient></defs>'
            f'<path d="M45 6l36 12v30c0 26-14 44-36 54C23 92 9 74 9 48V18z" fill="url(#sh{kind})"/>'
            '<path d="M24 38l16 12-16 12M44 66h22" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>' + inner + '</svg>')


def mark(kind, col="var(--blue)", s=44):
    g = '<path d="M7 12.5l3.5 3.5L17 9" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>' if kind == "ok" else '<path d="M7 12h10" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
    return f'<svg viewBox="0 0 24 24" style="width:{s}px;height:{s}px;flex:none"><circle cx="12" cy="12" r="11" fill="{col}"/>{g}</svg>'


def p033():
    o = [f'<div class="ab" style="left:186px;top:58px;font-size:64px;font-weight:800;color:{NAVY};text-transform:uppercase;line-height:1.06">Режимы командной строки</div>',
         '<div class="ab" style="left:186px;top:136px;font-size:56px;font-weight:800;color:#5f8ae6;text-transform:uppercase;line-height:1.06">Уровни привилегий</div>']
    o.append(box(85, 262, 768, 444, "", "card solid", 1, "border-radius:30px"))
    o.append(txt(120, 296, 700, 'Уровни <span style="font-size:84px;color:var(--blue);margin-left:10px;letter-spacing:2px">1&ndash;14</span>', 40, 800, NAVY, 1, "text-transform:uppercase;white-space:nowrap"))
    o.append(f'<div data-s="1" style="{A(120, 430)}">{shield("lock", 250)}</div>')
    o.append(txt(405, 436, 430, "Только доступ", 44, 800, NAVY, 1, "text-transform:uppercase;line-height:1"))
    o.append(f'<div data-s="2" style="{A(405, 506, 440, None, "display:flex;gap:16px;align-items:center;font-size:23px;line-height:1.25")}">{mark("ok")}<span>Разрешён доступ к устройству</span></div>')
    o.append(f'<div data-s="2" style="{A(405, 592, 440, None, "display:flex;gap:16px;align-items:center;font-size:23px;line-height:1.25;--dl:120ms")}">{mark("minus")}<span>Настройка устройства запрещена</span></div>')
    o.append(SVG_OPEN + '<circle data-s="3" cx="900" cy="520" r="9" fill="none" stroke="var(--blue)" stroke-width="4"/><circle data-s="3" cx="1040" cy="372" r="9" fill="none" stroke="var(--blue)" stroke-width="4"/>'
             + path("M912 505 C960 480 1000 450 1030 395", 3, "#4f7df0", 7)
             + '<polygon class="hd" data-s="3" points="1030,380 1018,402 1048,398" fill="#4f7df0"/></svg>')
    o.append(txt(1015, 312, 80, "15", 30, 700, NAVY, 3, "font-family:var(--mono)"))
    o.append(txt(878, 556, 60, "1", 30, 700, NAVY, 3, "font-family:var(--mono);text-align:center"))
    o.append(box(1116, 192, 729, 512, "", "card", 4, "border-radius:30px;background:linear-gradient(135deg,#3e63da,#1a2f9a);border:2px solid rgba(180,205,255,.8);box-shadow:0 0 50px rgba(80,120,255,.45)"))
    o.append(txt(1190, 262, 600, 'Уровень <span style="font-size:90px;margin-left:10px">15</span>', 42, 800, "#fff", 4, "text-transform:uppercase;white-space:nowrap"))
    o.append(f'<div data-s="4" style="{A(1150, 400)}">{shield("gear", 260)}</div>')
    o.append(txt(1429, 400, 420, "Доступ и настройка", 32, 800, "#fff", 4, "text-transform:uppercase;line-height:1.1"))
    o.append(f'<div data-s="5" style="{A(1429, 478, 410, None, "display:flex;gap:16px;align-items:center;font-size:23px;line-height:1.25;color:#fff")}">{mark("ok", "#4f86f7")}<span>Разрешён доступ к устройству</span></div>')
    o.append(f'<div data-s="5" style="{A(1429, 590, 410, None, "display:flex;gap:16px;align-items:center;font-size:23px;line-height:1.25;color:#fff;--dl:120ms")}">{mark("ok", "#4f86f7")}<span>Разрешена настройка устройства</span></div>')
    o.append(box(43, 742, 1834, 314, "", "card", 6, "border-radius:28px"))
    o.append(txt(96, 782, 900, "Переход между режимами", 36, 800, NAVY, 6, "text-transform:uppercase"))
    o.append(f'<div data-s="6" style="{A(970, 858, 3, 160, "background:var(--line)")}"></div>')

    def trans(l, up, title, c1, c2, s, col):
        arrow = (f'<svg viewBox="0 0 60 120" style="width:62px;height:122px"><path d="M30 6l26 30H38v78H22V36H4z" fill="{col}"/></svg>' if up else
                 f'<svg viewBox="0 0 60 120" style="width:62px;height:122px"><path d="M30 114L4 84h18V6h16v78h18z" fill="{col}"/></svg>')
        return (f'<div data-s="{s}" style="{A(l, 840, 90, 130)}">{arrow}</div>'
                + txt(l + 102, 836, 620, title, 23, 800, NAVY, s, "text-transform:uppercase")
                + f'<div class="mono" data-s="{s}" style="{A(l + 102, 888, 612, 98, "background:#16254f;color:#eaf2ff;border-radius:14px;padding:12px 24px;font-size:27px;line-height:1.3;box-shadow:0 6px 18px rgba(16,37,90,.3)")}">{c1}<br>{c2}</div>')
    o.append(trans(176, True, "Получение 15-го уровня", "console&gt; enable", "console#", 7, "#3d72e8"))
    o.append(trans(1052, False, "Возвращение на исходный уровень", "console# disable", "console&gt;", 8, "#6a5ce8"))
    return "".join(o)


SLIDES.append(("p033", "Режимы командной строки: уровни привилегий", p033()))


# =========================================================== p034
def p034():
    o = ['<h1 class="t ab ctr-x" style="top:18px;width:1500px;font-size:56px">Режимы командной строки <span class="lt" style="color:var(--navy)">MES</span></h1>']
    CM = "#1c3f9e"

    def cmds(l, t, items, size=17, lh=23.7, s=None):
        body = "<br>".join(items)
        return f'<div class="mono"{ds(s)} style="{A(l, t, None, None, f"font-size:{size}px;line-height:{lh}px;color:{CM};font-weight:600;white-space:nowrap")}">{body}</div>'

    def prompt(l, t, w, h, text, s, size=26):
        return (f'<div class="mono"{ds(s)} style="{A(l, t, w, h, f"background:rgba(255,255,255,.9);border:1.5px solid var(--line);border-radius:12px;display:flex;align-items:center;padding-left:18px;font-size:{size}px;font-weight:700;color:{CM}")}">{text}</div>')

    def circ(l, t, d, icn, s):
        return (f'<div{ds(s)} style="{A(l, t, d, d, "border-radius:50%;background:radial-gradient(circle,#fff,#d9e6ff);border:2px solid #fff;box-shadow:0 8px 22px rgba(40,80,200,.25);display:grid;place-items:center;color:var(--blue)")}">'
                f'<svg viewBox="0 0 24 24" style="width:{d * .5:.0f}px;height:{d * .5:.0f}px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round">{ICON_PATHS[icn]}</svg></div>')

    def head(l, t, w, text, size, s):
        return txt(l, t, w, text, size, 800, NAVY, s, "text-transform:uppercase;white-space:nowrap")
    o.append(box(70, 100, 1754, 252, "", "card solid", 1, "border-radius:28px"))
    o.append(circ(118, 130, 112, "user", 1))
    o.append(head(252, 128, 1200, "Пользовательский (непривилегированный) режим", 28, 1))
    o.append(prompt(256, 175, 346, 52, "console&gt;", 1, 27))
    o.append(cmds(740, 168, ["clear", "disable", "enable", "exit", "help"], 19, 25.6, 1))
    o.append(cmds(1060, 168, ["logout", "no", "ping", "set", "show"], 19, 25.6, 1))
    o.append(cmds(1344, 168, ["snmpwalk", "ssl", "test"], 19, 25.6, 1))
    o.append(box(70, 353, 1786, 668, "", "card solid", 2, "border-radius:28px"))
    o.append(circ(110, 380, 96, "shield", 2))
    o.append(head(252, 366, 800, "Привилегированный режим", 28, 2))
    o.append(prompt(252, 400, 266, 52, "console#", 2, 27))
    pr = ["backup", "boot", "clear", "clock", "configure", "copy", "debug", "delete", "dir", "disable", "dot1x", "dump", "enable", "end", "erase", "exit",
          "firmware", "help", "ip", "no", "ping", "release", "reload", "..."]
    o.append(cmds(268, 462, pr, 17, 22.8, 2))
    o.append(box(559, 405, 1222, 606, "", "card", 3, "border-radius:26px;background:rgba(236,243,255,.75)"))
    o.append(circ(582, 424, 80, "gear", 3))
    o.append(head(693, 432, 700, "Режим глобального конфигурирования", 22, 3))
    o.append(prompt(693, 468, 340, 42, "console(config)#", 3, 21))
    gl = ["aaa", "arp", "backup", "banner", "class-map", "clear", "clock", "cpu", "crypto", "debug", "default", "dot1x", "dump", "enable", "end", "exit",
          "hostname", "interface", "..."]
    o.append(cmds(714, 533, gl, 17, 23.6, 3))
    o.append(box(1060, 469, 721, 530, "", "card solid", 4, "border-radius:24px"))
    o.append(circ(1086, 484, 70, "net", 4))
    o.append(head(1190, 492, 600, "Режим конфигурирования интерфейса", 20, 4))
    o.append(prompt(1190, 530, 300, 40, "console(config-if)#", 4, 20))
    ifc = ["channel-group", "description", "dot1x", "duplex", "end", "exit", "gvrp", "help", "ip", "l2protocol-tunnel", "lacp", "lldp", "mac", "mdix", "no",
           "port-isolation", "..."]
    o.append(cmds(1216, 595, ifc, 17, 23.9, 4))
    return "".join(o)


ICON_PATHS = {
    "user": '<circle cx="12" cy="8.5" r="3.5"/><path d="M5 20c0-3.6 3.1-6 7-6s7 2.4 7 6"/>',
    "shield": '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/>',
    "gear": '<circle cx="12" cy="12" r="3.2"/><path d="M12 3v2.5M12 18.5V21M3 12h2.5M18.5 12H21M5.6 5.6l1.8 1.8M16.6 16.6l1.8 1.8M18.4 5.6l-1.8 1.8M7.4 16.6l-1.8 1.8"/>',
    "net": '<circle cx="12" cy="5" r="2.2"/><circle cx="5" cy="19" r="2.2"/><circle cx="19" cy="19" r="2.2"/><path d="M12 7.2v6M12 13.2L6.6 17.4M12 13.2l5.4 4.2"/>',
}

SLIDES.append(("p034", "Режимы командной строки MES", p034()))
