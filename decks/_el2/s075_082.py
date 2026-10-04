# -*- coding: utf-8 -*-
"""Слайды по референсам p075-p082."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from _el2_lib import ico, arrow_svg, icon

SLIDES = []


def px(v):
    return round(v * 1920 / 900)


def py(v):
    return round(v * 1080 / 506)


def pz(v):
    return round(v * 1080 / 600)


def R(x0, y0, x1, y1, fy=py):
    return (f"position:absolute;left:{px(x0)}px;top:{fy(y0)}px;"
            f"width:{px(x1) - px(x0)}px;height:{fy(y1) - fy(y0)}px;")


def layer(*parts):
    return ('<svg class="ab" style="left:0;top:0;width:1920px;height:1080px;overflow:visible" '
            'viewBox="0 0 1920 1080">' + "".join(parts) + '</svg>')


def led(color, size=44):
    g = {"g": ("#d4ffdc", "#31d05a", "#15993c", "60,200,100"),
         "r": ("#ffd6d6", "#f0494b", "#b92024", "240,70,75")}[color]
    return (f'<span style="display:block;flex:none;width:{size}px;height:{size}px;border-radius:50%;'
            f'background:radial-gradient(circle at 35% 30%,{g[0]},{g[1]} 55%,{g[2]});'
            f'box-shadow:0 0 0 {size // 4}px rgba({g[3]},.16),0 0 22px rgba({g[3]},.45)"></span>')


def dot(color):
    c = {"g": "#34c759", "o": "#ff9f1a", "gr": "#9aa6bd", "r": "#f0494b", "b": "#2a6bf2"}[color]
    return f'<i style="display:block;flex:none;width:10px;height:10px;border-radius:50%;background:{c};margin-top:7px"></i>'


def bl(color, text, fs=15):
    return (f'<div style="display:flex;gap:8px;align-items:flex-start;font-size:{fs}px;line-height:1.3;'
            f'color:var(--ink)">{dot(color)}<span>{text}</span></div>')


HEAD = 'font-weight:800;color:var(--navy);text-transform:uppercase;'


# ======================================================= p075 справочник CLI MES
def p075():
    o = ['<h1 class="t ab ctr-x" style="top:34px;width:1700px">Справочник команд CLI</h1>',
         '<div class="ab ctr-x" style="top:128px;display:flex;gap:26px;align-items:center;font-size:25px;'
         'font-weight:700;color:var(--blue);letter-spacing:4px;text-transform:uppercase;white-space:nowrap">'
         '<span style="width:90px;height:2px;background:var(--blue)"></span>'
         'Руководство по эксплуатации MES<span style="width:90px;height:2px;background:var(--blue)"></span></div>']
    o.append(f'<div class="card" data-s="1" style="{R(55, 98, 347, 418)}padding:0;overflow:hidden">'
             '<img src="assets/p075_cover.jpg" style="display:block;width:100%;height:100%;object-fit:cover"></div>')
    pdf = ('<div class="ab" style="left:28px;top:26px;width:112px;height:130px;border-radius:16px;'
           'background:linear-gradient(160deg,#4a86ff,#2a4fd0);box-shadow:0 10px 24px rgba(40,80,190,.3)">'
           '<div style="position:absolute;right:0;top:0;width:34px;height:34px;background:#c9ddff;'
           'clip-path:polygon(100% 0,0 0,100% 100%)"></div>'
           '<div class="mono" style="position:absolute;left:0;right:0;bottom:22px;text-align:center;color:#fff;'
           'font-weight:800;font-size:24px">PDF</div></div>')
    items = [("server", "Назначение оборудования"), ("doc", "Технические характеристики"),
             ("gear", "Начальная настройка"), ("chart", "Конфигурация и мониторинг"),
             ("reload", "Обновление программного обеспечения")]
    lst = "".join(f'<div class="ab" style="left:28px;top:{300 + i * 78}px;width:560px;display:flex;gap:26px;'
                  f'align-items:center">{ico(ic, "sm hex")}<p class="b" style="font-size:22px">{t}</p></div>'
                  for i, (ic, t) in enumerate(items))
    o.append(f'<div class="card" style="{R(368, 98, 878, 418)}padding:0">'
             f'<div class="ab" data-s="2" style="left:0;top:0;width:100%;height:290px">{pdf}'
             f'<div class="ab" style="left:190px;top:34px;{HEAD}font-size:38px;white-space:nowrap">Руководство по эксплуатации</div>'
             '<div class="tag ab" style="left:190px;top:100px;font-size:21px;padding:6px 20px;font-weight:600">Версия ПО 10.4.5</div>'
             '<p class="b ab" style="left:190px;top:150px;width:800px;font-size:23px">Официальный документ Элтекс для настройки и '
             'эксплуатации коммутаторов серии MES.</p></div>'
             '<div class="ab" style="left:28px;top:272px;width:1030px;height:2px;background:var(--line)"></div>'
             f'<div class="ab" data-s="3" style="left:0;top:0;width:100%;height:100%">{lst}</div>'
             f'<div class="card solid ab" data-s="4" style="left:640px;top:296px;width:448px;height:322px;padding:24px 26px">'
             f'<div style="display:flex;gap:20px;align-items:center">{ico("term", "sm")}'
             f'<div style="{HEAD}font-size:29px;line-height:1.1">Синтаксис<br>команд CLI</div></div>'
             '<p class="b sm" style="margin-top:14px;font-size:20px">Команды, параметры, ключевые слова и примеры настройки.</p>'
             '<div style="display:flex;gap:18px;align-items:center;margin-top:16px">'
             '<span class="chip key" style="font-size:26px;padding:14px 22px;min-width:150px">CTRL</span>'
             '<span style="font-size:26px;color:var(--dim)">+</span>'
             '<span class="chip key" style="font-size:26px;padding:14px 26px;min-width:100px">F</span></div>'
             '<p class="b sm" style="margin-top:12px;font-size:20px">Поиск команды в документе</p></div></div>')
    o.append(f'<div class="card" data-s="5" style="{R(115, 437, 785, 485)}display:flex;align-items:center;gap:22px;'
             f'padding:0 0 0 34px">{ico("doc", "sm")}<span class="mono" style="font-size:26px;font-weight:800;color:var(--navy)">PDF</span>'
             '<span style="width:2px;height:60px;background:var(--line)"></span>'
             f'<span style="color:var(--blue)">{ico("link", "sm")}</span>'
             '<span class="mono" style="font-size:23px;color:var(--dim)">eltex.ru/storage/upload_center/files/60/MES_Series_user_manual_10.4.5.pdf</span></div>')
    return "".join(o)


SLIDES.append(("p075", "Справочник команд CLI: руководство MES", p075()))


# ======================================================= p076 радиоинтерфейсы
def p076():
    o = ['<h1 class="t left ab" style="left:75px;top:30px;width:1700px">Настройка радиоинтерфейсов</h1>',
         '<img class="ph ab" data-s="1" src="assets/p076_webui.jpg" style="left:38px;top:130px;width:1046px;border-radius:22px;'
         'box-shadow:0 14px 38px rgba(26,52,120,.16)">']

    def hd(icn, t):
        return (f'<div style="display:flex;gap:22px;align-items:center;margin-bottom:12px">{ico(icn, "sm hex")}'
                f'<div style="{HEAD}font-size:31px">{t}</div></div>')

    def pill(t, light=False):
        bg = "#6f98e8" if light else "#19b6e8"
        return (f'<span style="display:inline-block;min-width:130px;text-align:center;background:{bg};color:#fff;'
                f'border-radius:8px;padding:9px 14px;font-size:21px;font-weight:600;flex:none">{t}</span>')

    def prow(a, b, light=False):
        return ('<div style="display:flex;gap:20px;align-items:center;background:rgba(255,255,255,.8);border-radius:10px;'
                f'padding:7px 10px;margin-top:8px">{pill(a, light)}<span style="font-size:21px;color:var(--ink)">{b}</span></div>')

    o.append(f'<div class="card" data-s="2" style="{R(533, 65, 878, 160)}padding:20px 26px">{hd("gear", "Режим работы")}'
             + prow("2,4 ГГц", "802.11ax; 802.11b/g/n; 802.11b/g/n/ax")
             + prow("5 ГГц", "802.11ax; 802.11a/n/ac; 802.11a/n/ac/ax", True) + '</div>')
    o.append(f'<div class="card" data-s="3" style="{R(533, 168, 878, 293)}padding:20px 26px">{hd("wifi", "Выбор канала")}'
             f'<div style="display:flex;gap:18px;align-items:center;margin-bottom:10px">{ico("check", "sm")}'
             '<p class="b sm"><b>Автоматический</b> — точка выбирает наименее загруженный канал</p></div>'
             f'<div style="display:flex;gap:18px;align-items:center">{ico("gear", "sm")}'
             '<p class="b sm"><b>Статический</b> — канал задаётся вручную</p></div></div>')
    o.append(f'<div class="card" data-s="4" style="{R(533, 300, 878, 393)}padding:20px 26px">{hd("chart", "Доступные каналы")}'
             + prow("2,4 ГГц", "1 – 13 &nbsp;&nbsp;Оптимальны: 1, 6 и 11")
             + prow("5 ГГц", "36 – 64, 132 – 144, 149 – 165", True) + '</div>')

    def small(x0, x1, icn, title, body, s):
        return (f'<div class="card" data-s="{s}" style="{R(x0, 405, x1, 495)}padding:16px 22px">'
                f'<div style="display:flex;gap:16px;align-items:center">{ico(icn, "sm hex")}'
                f'<div style="{HEAD}font-size:22px;line-height:1.1">{title}</div></div>{body}</div>')

    w1 = ('<p class="b ab" style="left:24px;top:86px;font-size:20px;font-weight:600">20 или 40 МГц</p>'
          '<svg class="ab" style="left:40px;top:128px" width="380" height="60" viewBox="0 0 380 60">'
          '<path d="M30 56 L50 32 L110 32 L130 56Z" fill="#6f98e8" opacity=".8"/>'
          '<path d="M180 56 L210 14 L320 14 L350 56Z" fill="#2a6bf2" opacity=".85"/>'
          '<text x="80" y="52" font-size="14" fill="#12245e" text-anchor="middle" font-weight="600">20 МГц</text>'
          '<text x="265" y="48" font-size="14" fill="#fff" text-anchor="middle" font-weight="600">40 МГц</text></svg>')
    w2 = ('<p class="b ab" style="left:24px;top:84px;font-size:20px;line-height:1.6"><b>Upper</b> — верхний<br><b>Lower</b> — нижний</p>'
          '<svg class="ab" style="left:250px;top:84px" width="190" height="90" viewBox="0 0 190 90">'
          '<path d="M30 2 L160 2 L180 38 L10 38Z" fill="#6f98e8" opacity=".85"/>'
          '<path d="M10 46 L180 46 L160 84 L30 84Z" fill="#2a6bf2" opacity=".9"/>'
          '<text x="95" y="26" font-size="15" fill="#fff" text-anchor="middle">Upper</text>'
          '<text x="95" y="72" font-size="15" fill="#fff" text-anchor="middle">Lower</text></svg>')
    w3 = ('<p class="b ab" style="left:24px;top:98px;font-size:20px">от 6 до 16 дБм</p>'
          '<svg class="ab" style="left:210px;top:78px" width="190" height="100" viewBox="0 0 190 100">'
          + "".join(f'<rect x="{12 + i * 26}" y="{88 - 14 * (i + 1)}" width="16" height="{14 * (i + 1)}" rx="3" '
                    f'fill="{"#2a6bf2" if i > 1 else "#6f98e8"}"/>' for i in range(6)) + '</svg>')
    w4 = ('<p class="b ab" style="left:22px;top:86px;width:230px;font-size:17px;line-height:1.3">Изолирует трафик клиентов '
          'разных VAP и радиоинтерфейсов</p>'
          f'<div class="ab" style="left:262px;top:90px;display:flex;gap:14px;align-items:center">{ico("user", "sm")}'
          f'<span style="color:#e24b4b;font-size:34px;font-weight:800">×</span>{ico("user", "sm")}</div>')
    o.append(small(15, 220, "wifi", "Ширина канала", w1, 5))
    o.append(small(228, 440, "layers", "Основной канал", w2, 6))
    o.append(small(450, 632, "chart", "Мощность сигнала", w3, 7))
    o.append(small(640, 878, "shield", "Глобальная изоляция", w4, 8))
    return "".join(o)


SLIDES.append(("p076", "Настройка радиоинтерфейсов", p076()))


# ======================================================= p077 системные индикаторы
def p077():
    Y = pz
    o = ['<div class="ab" style="left:53px;top:60px;width:640px;font-size:78px;font-weight:800;line-height:1.02;'
         'text-transform:uppercase;color:var(--navy)">Системные<br><span style="color:#6c8fd6">индикаторы</span></div>',
         '<div class="ab" style="left:53px;top:260px;width:440px;height:3px;background:linear-gradient(90deg,var(--blue),transparent)"></div>',
         '<div class="ab" style="left:53px;top:290px;width:600px;font-size:22px;line-height:1.5;color:var(--ink)">'
         '<p data-s="1">Системные индикаторы средних моделей содержат индикаторы: <b>Status, Alarm, Power и FAN.</b> '
         'Эти индикаторы отражают текущее состояние устройства.</p>'
         '<p data-s="2" style="margin-top:20px">В младших моделях не все из этих индикаторов используются, зависит от конкретной модели.</p>'
         '<p data-s="3" style="margin-top:20px">Системные индикаторы старших моделей, в отличие от средних, имеют не 4, а 8 значений индикаторов. '
         'К имеющимся <b>Status, Alarm, Power</b> и <b>FAN</b> добавляются ещё: <b>VPN, Mastr, RPS</b> и <b>Flash.</b></p></div>',
         '<img class="ab" data-s="1" src="assets/p077_device.jpg" style="left:0;top:706px;width:691px;'
         'filter:drop-shadow(0 12px 22px rgba(30,60,130,.2))">']
    o.append(f'<div class="card" data-s="1" style="{R(313, 40, 572, 405, Y)}padding:0">'
             '<div class="ab" style="left:28px;top:20px;font-size:30px;font-weight:800;color:var(--blue);text-transform:uppercase">Средние модели</div>'
             '<div class="ab" style="left:28px;top:62px;font-size:20px;color:var(--dim)">4 основных индикатора</div>'
             '<img class="ab" src="assets/p077_mid.jpg" style="right:22px;top:26px;width:150px"></div>')
    x1_of = {313: 572, 585: 880}

    def row(x0, y0, y1, c, name, desc, bullets, s, lamp=None):
        h = pz(y1) - pz(y0)
        w = px(x1_of[x0]) - px(x0) - 36
        lamp = lamp or led(c, 42)
        return (f'<div class="card solid" data-s="{s}" style="position:absolute;left:{px(x0) + 18}px;top:{pz(y0)}px;width:{w}px;'
                f'height:{h}px;padding:0 16px;display:flex;align-items:center;border-radius:16px">'
                f'<div style="display:flex;gap:14px;align-items:center;width:37%;flex:none">{lamp}'
                f'<div><div style="font-size:21px;font-weight:800;color:var(--navy)">{name}</div>'
                f'<div style="font-size:15px;color:var(--dim);line-height:1.25">{desc}</div></div></div>'
                f'<div style="display:flex;flex-direction:column;gap:5px;flex:1">{"".join(bullets)}</div></div>')

    pw = [bl("g", "Основной источник питания в норме."),
          bl("o", "Неработоспособность основного источника питания, авария или отсутствие первичной сети."),
          bl("gr", "Отказ внутренних источников питания.")]
    fan = [bl("g", "Все вентиляторы исправны."), bl("r", "Отказ одного/нескольких вентиляторов.")]
    st = [bl("g", "Работает нормально."), bl("o", "Состояние загрузки ПО.")]
    al = [bl("gr", "Выключен<br>Устройство работает в безаварийном режиме.")]
    mid = [(100, 168, "g", "Status", "Текущее состояние устройства", st),
           (176, 244, "r", "Alarm", "Наличие и уровень аварии устройства", al),
           (252, 326, "g", "Power", "Электропитание", pw),
           (334, 398, "g", "FAN", "Состояние вентиляторов", fan)]
    for i, (a, b, c, n, d, bu) in enumerate(mid):
        o.append(row(313, a, b, c, n, d, bu, 2 + i // 2))
    o.append(f'<div class="card" data-s="4" style="{R(585, 40, 880, 530, Y)}padding:0">'
             '<div class="ab" style="left:28px;top:20px;font-size:30px;font-weight:800;color:var(--blue);text-transform:uppercase">Старшие модели</div>'
             '<div class="ab" style="left:28px;top:62px;font-size:20px;color:var(--dim)">8 индикаторов</div>'
             '<img class="ab" src="assets/p077_senior.jpg" style="right:22px;top:14px;width:120px"></div>')

    def bic(icn):
        return ('<span class="ico sm" style="width:46px;height:46px;background:#2f6be0;border-color:#2f6be0;color:#fff;'
                f'border-radius:12px;flex:none"><svg viewBox="0 0 24 24" style="width:26px;height:26px">{icon(icn)[len("<svg viewBox=" + chr(34) + "0 0 24 24" + chr(34) + ">"):-6]}</svg></span>')

    sen = [(97, 137, "g", "Status", "Текущее состояние устройства", st, None),
           (141, 180, "r", "Alarm", "Наличие и уровень аварии устройства", al, None),
           (185, 265, "g", "Power", "Электропитание", pw, None),
           (270, 306, "g", "FAN", "Состояние вентиляторов", fan, None),
           (312, 348, None, "VPN", "Наличие активных VPN-сессий", [bl("gr", "-")], "shield"),
           (352, 390, None, "Mastr", "Работа устройства в failover-режимах.", [bl("gr", "-")], "server"),
           (396, 462, None, "RPS", "Режим работы резервного источника питания.",
            [bl("g", "Резервный источник питания установлен и исправен."),
             bl("o", "Отсутствие первичного питания резервного источника и его неисправность."),
             bl("gr", "Резервный источник не установлен.")], "power"),
           (468, 526, None, "Flash", "Активность обмена с накопителем: SD-картой/USB Flash.",
            [bl("g", "Выполнение операций чтение и записи по команде «copy».")], "sd")]
    for i, (a, b, c, n, d, bu, icn) in enumerate(sen):
        o.append(row(585, a, b, c, n, d, bu, 5 + i // 4, bic(icn) if icn else None))
    o.append(f'<div class="card solid" data-s="7" style="{R(297, 500, 515, 567, Y)}padding:16px 22px;display:flex;gap:16px;align-items:center;border-radius:18px">'
             '<span style="font-size:60px;line-height:.6;color:var(--blue);font-weight:800;font-family:Georgia,serif">&ldquo;</span>'
             '<p class="b sm" style="font-size:19px">Индикаторы помогают быстро оценить состояние устройства и своевременно выявить неисправности.</p></div>')
    return "".join(o)


SLIDES.append(("p077", "Системные индикаторы", p077()))



# ======================================================= p078 установка в стойку
def p078():
    o = ['<h1 class="t ab ctr-x" style="top:26px;width:1700px;font-size:60px">Установка коммутаторов <span class="lt">MES</span> в стойку</h1>']
    steps = [(25, 318, "1.", "Установить кронштейны", "p078_step1.jpg",
              "Кронштейны и винты входят в комплект поставки. Закрепите кронштейны на корпусе устройства."),
             (330, 590, "2.", "Разместить в стойке", "p078_step2.jpg",
              "Совместите отверстия кронштейнов с направляющими стойки."),
             (598, 878, "3.", "Закрепить устройство", "p078_step3.jpg", "Надёжно закрепите устройство с обеих сторон.")]
    for i, (x0, x1, n, t, img, txt) in enumerate(steps):
        w = px(x1) - px(x0)
        o.append(f'<div class="card" data-s="{1 + i}" style="{R(x0, 80, x1, 265)}padding:0;overflow:hidden">'
                 f'<div style="height:78px;background:linear-gradient(90deg,#d9e6fb,#eef4ff);display:flex;align-items:center;gap:16px;padding:0 14px">'
                 f'<span style="display:grid;place-items:center;min-width:92px;height:62px;background:#1f55c8;color:#fff;'
                 f'font-size:44px;font-weight:800;border-radius:12px">{n}</span>'
                 f'<span style="{HEAD}font-size:30px;white-space:nowrap">{t}</span></div>'
                 f'<img class="ab" src="assets/{img}" style="left:10px;top:92px;width:{w - 20}px;height:206px;'
                 f'object-fit:contain"></div>'
                 + f'<p class="b ab" data-s="{1 + i}" style="left:{px(x0) + 28}px;top:{py(224)}px;width:{w - 56}px;font-size:21px">{txt}</p>')
    o.append(layer(*[f'<path data-s="{s}" d="M{x} 340 L{x + 34} 366 L{x} 392Z" fill="#2a6bf2"/>' for x, s in ((680, 2), (1252, 3))]))
    o.append('<div class="ab ctr-x" data-s="4" style="top:572px;display:flex;gap:24px;align-items:center;white-space:nowrap">'
             '<span style="width:460px;height:2px;background:var(--line)"></span>'
             f'<span style="{HEAD}font-size:34px">Требования безопасности</span>'
             '<span style="width:460px;height:2px;background:var(--line)"></span></div>')

    def bcard(x0, x1, s):
        return f'<div class="card" data-s="{s}" style="{R(x0, 305, x1, 492)}padding:0;overflow:hidden">'

    o.append(bcard(15, 315, 4) +
             '<div class="ab" style="left:20px;top:16px;display:flex;gap:20px;align-items:center">'
             '<span class="ico sm" style="background:#e5484d;border-color:#e5484d;color:#fff;width:64px;height:64px">'
             f'<svg viewBox="0 0 24 24" style="width:36px;height:36px">{icon("warn")[24:-6]}</svg></span>'
             f'<span style="{HEAD}font-size:26px;white-space:nowrap">Не перекрывать вентиляцию</span></div>'
             '<img class="ab" src="assets/p078_vent.jpg" style="left:20px;top:100px;width:580px">'
             '<p class="b ab" style="left:20px;top:276px;width:600px;font-size:19px">Не закрывайте вентиляционные отверстия и вентиляторы посторонними предметами.</p>'
             '<div class="ab" style="left:20px;top:340px;width:600px;background:#fde4e6;border-radius:12px;padding:10px 14px;'
             'display:flex;gap:14px;align-items:center;font-size:18px;color:#c5313a">'
             f'<span style="width:34px;color:#e5484d"><svg viewBox="0 0 24 24" style="width:34px;height:34px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round">{icon("temp")[24:-6]}</svg></span>'
             'Перекрытие потока воздуха вызывает перегрев и нарушение работы.</div></div>')
    o.append(bcard(320, 590, 5) +
             f'<div class="ab" style="left:18px;top:16px;display:flex;gap:18px;align-items:center">{ico("gear", "sm hex")}'
             f'<span style="{HEAD}font-size:26px;white-space:nowrap">Вертикальная установка</span></div>'
             '<img class="ab" src="assets/p078_vert.jpg" style="left:20px;top:84px;width:200px">'
             '<p class="b ab" style="left:260px;top:100px;width:270px;font-size:19px">Модели <b class="mono">MES3710P</b> и <b class="mono">MES3708P</b> '
             'устанавливаются вертикально.<br><br>Боковые панели обеспечивают теплоотвод.</p></div>')
    o.append(bcard(598, 878, 6) +
             f'<div class="ab" style="left:18px;top:16px;display:flex;gap:18px;align-items:center">{ico("power", "sm hex")}'
             f'<span style="{HEAD}font-size:26px;white-space:nowrap">Подключение питания</span></div>'
             '<img class="ab" src="assets/p078_tools.jpg" style="left:16px;top:100px;width:540px">'
             '<p class="b ab" style="left:20px;top:268px;width:560px;font-size:19px">Электропитание должен подключать квалифицированный специалист.</p></div>')
    return "".join(o)


SLIDES.append(("p078", "Установка коммутаторов MES в стойку", p078()))


# ======================================================= p079 MES1428 передняя панель
def p079():
    o = ['<div class="ab" style="left:75px;top:20px"><div style="font-size:70px;font-weight:800;color:var(--navy);'
         'text-transform:uppercase;line-height:1">Конструктивное исполнение</div>'
         '<div style="font-size:26px;font-weight:700;color:var(--blue);text-transform:uppercase;margin-top:10px">Передняя панель MES1428</div></div>',
         '<img class="ab" src="assets/p079_front.jpg" style="left:58px;top:497px;width:1786px;filter:drop-shadow(0 16px 26px rgba(30,60,130,.18))">']

    def box(x0, y0, x1, y1, n, title, body, s):
        return (f'<div class="card" data-s="{s}" style="{R(x0, y0, x1, y1)}padding:0">'
                f'<span class="badge ab" style="left:14px;top:12px;width:62px;height:62px;font-size:40px;border-radius:14px;font-family:var(--f)">{n}</span>'
                f'<div class="ab" style="left:98px;top:20px;{HEAD}font-size:{26 if len(title) < 20 else 22}px;white-space:nowrap">{title}</div>{body}</div>')

    def img(name, left, top, w):
        return f'<img class="ab" src="assets/{name}" style="left:{left}px;top:{top}px;width:{w}px">'

    def txt(left, top, w, t):
        return f'<p class="b ab" style="left:{left}px;top:{top}px;width:{w}px;font-size:21px;line-height:1.35">{t}</p>'

    o.append(box(42, 108, 285, 188, 1, "Разъём питания",
                 img("p079_ic_plug.jpg", 24, 102, 62) + txt(120, 98, 380, "Подключение к источнику переменного тока"), 1))
    o.append(box(315, 108, 565, 188, 3, "Консольный интерфейс",
                 img("p079_ic_con.jpg", 24, 100, 76) + txt(124, 104, 340, "Локальное управление устройством"), 3))
    o.append(box(598, 108, 855, 188, 5, "Ethernet-интерфейсы",
                 img("p079_ic_eth.jpg", 24, 100, 76) + txt(124, 104, 420, "Порты 10/100BASE-TX (RJ-45)"), 5))
    o.append(box(35, 372, 290, 472, 2, "Индикаторы",
                 '<div class="ab" style="left:36px;top:96px;width:480px;font-size:21px;line-height:1.35">'
                 + bl("b", "<b>Power</b> — индикатор питания устройства", 21)
                 + '<div style="height:8px"></div>' + bl("b", "<b>Alarm</b> — индикатор перегрева", 21) + '</div>', 2))
    o.append(box(315, 372, 565, 472, 4, "Функциональная кнопка F",
                 '<span class="ab" style="left:30px;top:106px;width:60px;height:60px;border-radius:50%;background:#1f55c8;'
                 'box-shadow:0 0 0 7px #fff inset,0 0 0 3px #1f55c8;border:0"><i style="position:absolute;inset:18px;border-radius:50%;background:#1f55c8"></i></span>'
                 + txt(116, 90, 380, "Менее 10 секунд — перезагрузка<br>Более 10 секунд — перезагрузка и сброс настроек"), 4))
    o.append(box(598, 372, 855, 472, 6, "Combo-порты",
                 img("p079_ic_combo.jpg", 24, 102, 76) + txt(124, 98, 420, "Порты 10/100/1000BASE-T (RJ-45)"), 6))

    def ln(path, s, dots=()):
        d = "".join(f'<circle data-s="{s}" cx="{px(cx)}" cy="{py(cy)}" r="7" fill="#2a6bf2"/>' for cx, cy in dots)
        return f'<path class="dr" data-s="{s}" pathLength="1" d="{path}" stroke="var(--blue)" stroke-width="3" fill="none"/>' + d

    P = lambda *pts: "M" + " L".join(f"{px(x)} {py(y)}" for x, y in pts)
    o.append(layer(
        ln(P((95, 188), (95, 262)), 1, [(95, 262)]),
        ln(P((320, 142), (320, 200), (228, 262), (228, 286)), 3, [(320, 142), (228, 286)]),
        ln(P((355, 244), (355, 236), (548, 236), (548, 244)), 5),
        ln(P((452, 236), (452, 210), (620, 210), (620, 188)), 5, [(620, 188)]),
        ln(P((180, 372), (180, 326)), 2, [(180, 326)]),
        ln(P((263, 372), (263, 326)), 4, [(263, 326)]),
        ln(P((700, 346), (700, 354), (840, 354), (840, 346)), 6),
        ln(P((765, 354), (765, 372)), 6, [(765, 372)])))
    return "".join(o)


SLIDES.append(("p079", "Конструктивное исполнение: передняя панель MES1428", p079()))


# ======================================================= p080 точки доступа outdoor
def p080():
    o = ['<h1 class="t left ab" style="left:75px;top:50px;width:1200px;font-size:62px">Точки доступа: <span class="lt">Outdoor</span></h1>',
         '<img class="ab" data-s="1" src="assets/p080_scene.jpg" style="left:0;top:167px;width:1920px;'
         '-webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 50px,#000 92%,transparent 100%);'
         'mask-image:linear-gradient(to bottom,transparent 0,#000 50px,#000 92%,transparent 100%)">']
    for i, (x0, x1, icn, t) in enumerate([(15, 292, "wifi", "Уличное покрытие"), (305, 560, "bolt", "Питание PoE"),
                                          (573, 878, "server", "Централизованное управление")]):
        o.append(f'<div class="card" data-s="{2 + i}" style="{R(x0, 410, x1, 495)}display:flex;gap:26px;align-items:center;padding:0 30px">'
                 f'{ico(icn, "hex")}<span style="{HEAD}font-size:30px;line-height:1.15">{t}</span></div>')
    return "".join(o)


SLIDES.append(("p080", "Точки доступа: Outdoor", p080()))


# ======================================================= p081 устройство коммутаторов MES
def p081():
    o = ['<div class="ab" style="left:53px;top:60px;width:700px;font-size:47px;font-weight:800;line-height:1.1;'
         'text-transform:uppercase;color:var(--navy)">Устройство<br>коммутаторов <span style="color:var(--blue)">MES</span></div>',
         '<div class="ab" style="left:53px;top:178px;font-size:24px;font-weight:600;color:var(--blue);text-transform:uppercase;'
         'letter-spacing:1px">Конструктивное исполнение</div>',
         '<img class="ab" data-s="1" src="assets/p081_board.jpg" style="left:601px;top:0;width:689px;'
         'filter:drop-shadow(0 14px 22px rgba(30,60,130,.2))">',
         '<div class="ab" data-s="1" style="left:496px;top:318px;background:#dfe9fb;border-radius:8px;padding:2px 12px;'
         f'{HEAD}font-size:21px;color:var(--navy)">Интерфейсы</div>']

    o.append(f'<div class="card" data-s="2" style="{R(607, 12, 880, 75)}display:flex;gap:22px;align-items:center;padding:0 24px">'
             '<img src="assets/p081_sw.jpg" style="width:100px;height:auto;border-radius:8px;flex:none">'
             '<p class="b sm" style="font-size:19px;line-height:1.35"><b>Коммутатор</b> — специализированный компьютер с процессором, '
             'памятью, операционной системой и сетевыми интерфейсами.</p></div>')
    o.append(f'<div class="card" data-s="2" style="{R(607, 82, 790, 133)}display:flex;gap:18px;align-items:center;padding:0 20px">'
             f'{ico("gear", "sm")}<div><div style="{HEAD}font-size:21px;color:var(--blue)">Чип коммутации</div>'
             '<p class="b sm" style="font-size:16px;line-height:1.3">Быстро обрабатывает и пересылает кадры по простому алгоритму.</p></div></div>')
    o.append(f'<div class="card" data-s="3" style="{R(795, 80, 880, 134)}padding:10px 14px">'
             f'<div style="{HEAD}font-size:18px;margin-bottom:6px">Уровни работы</div>'
             '<div style="font-size:16px;line-height:1.3"><b style="color:var(--blue)">L2</b> — коммутация<br>'
             '<b style="color:var(--blue)">L3</b> — коммутация и маршрутизация</div></div>')
    o.append(f'<div class="card" data-s="3" style="{R(607, 140, 880, 184)}display:flex;gap:20px;align-items:center;padding:0 22px">'
             f'{ico("gear", "sm")}<p class="b sm" style="font-size:19px;line-height:1.3"><b>ОС на базе Linux:</b> инициализация системы, '
             'управление, функции коммутации и маршрутизации.</p></div>')

    # ОЗУ
    def mi(icn, t, d):
        return (f'<div style="display:flex;gap:10px;align-items:flex-start;flex:1">{ico(icn, "sm")}'
                f'<div><div style="font-size:18px;font-weight:700;color:var(--navy);line-height:1.15;white-space:nowrap">{t}</div>'
                f'<div style="font-size:15px;color:var(--dim);line-height:1.25;margin-top:3px">{d}</div></div></div>')

    o.append(f'<div class="card" data-s="4" style="{R(15, 198, 437, 438)}padding:0">'
             f'<div class="ab" style="left:22px;top:18px;display:flex;gap:16px;align-items:center">{ico("db", "sm")}'
             f'<span style="{HEAD}font-size:29px">Оперативная память (ОЗУ)</span></div>'
             '<div class="ab" style="right:26px;top:16px;width:300px;display:flex;gap:12px">'
             f'<span style="color:var(--blue)"><svg viewBox="0 0 24 24" style="width:32px;height:32px;fill:none;stroke:currentColor;stroke-width:1.8">{icon("bolt")[24:-6]}</svg></span>'
             '<div><div style="font-size:19px;font-weight:800;color:var(--navy)">Энергозависимая</div>'
             '<div style="font-size:15px;color:var(--dim);line-height:1.25">Данные сохраняются только при наличии электропитания</div></div></div>'
             '<div class="ab" style="left:22px;top:100px;width:824px;display:flex;gap:14px">'
             + mi("doc", "running-config", "текущая конфигурация") + mi("layers", "Буфер обмена", "временное хранение пакетов")
             + mi("net", "Таблица ARP", "соответствия IP- и MAC-адресов") + mi("list", "Таблица маршрутизации", "") + '</div>'
             '<img class="ab" src="assets/p081_ddr3.jpg" style="left:34px;top:240px;width:330px;border-radius:6px">'
             '<img class="ab" src="assets/p081_ddr4.jpg" style="left:430px;top:240px;width:330px;border-radius:6px"></div>')
    o.append(f'<div class="card rose" data-s="5" style="{R(30, 392, 422, 428)}display:flex;gap:16px;align-items:center;padding:0 22px">'
             f'<span style="color:#e5484d">{ico("warn", "sm")}</span>'
             '<span style="font-size:23px;font-weight:700;color:#c5313a">При отключении питания содержимое ОЗУ теряется.</span></div>')

    # ПЗУ
    nand_b = ["startup-config — /mnt/config", "Образы firmware — image-1 / image-2", "Дополнительные данные — /mnt/data",
              "Критические журналы — /mnt/critlog", "Boot-лицензия"]
    spi_b = ["U-Boot и переменные окружения", "Factory-параметры: S/N, MAC, HW rev.", "Параметры инициализации DDR-памяти"]

    def mem(x0, x1, title, img, bullets, imgw):
        w = px(x1) - px(x0)
        return (f'<div class="card solid ab" style="{R(x0, 280, x1, 430)}padding:0;border-radius:16px">'
                f'<div class="ab" style="left:22px;top:14px;display:flex;gap:12px;align-items:center">{ico("gear", "sm")}'
                f'<span style="{HEAD}font-size:23px">{title}</span></div>'
                f'<div class="ab" style="left:22px;top:84px;width:{w - 44}px;display:flex;flex-direction:column;gap:6px">'
                + "".join(bl("b", b, 16) for b in bullets) + '</div>'
                f'<img class="ab" src="assets/{img}" style="right:14px;bottom:8px;width:{imgw}px"></div>')

    o.append(f'<div class="card" data-s="6" style="{R(450, 198, 885, 438)}padding:0">'
             f'<div class="ab" style="left:22px;top:18px;display:flex;gap:16px;align-items:center">{ico("db", "sm")}'
             f'<span style="{HEAD}font-size:29px">Постоянная память (ПЗУ)</span></div>'
             '<div class="ab" style="right:24px;top:14px;width:280px;display:flex;gap:12px">'
             f'<span style="color:var(--blue)"><svg viewBox="0 0 24 24" style="width:32px;height:32px;fill:none;stroke:currentColor;stroke-width:1.8">{icon("shield")[24:-6]}</svg></span>'
             '<div><div style="font-size:19px;font-weight:800;color:var(--navy)">Энергонезависимая</div>'
             '<div style="font-size:15px;color:var(--dim);line-height:1.25">Данные сохраняются после отключения питания</div></div></div>'
             f'<div class="ab" style="left:22px;top:96px;width:{px(885) - px(450) - 44}px;background:rgba(255,255,255,.8);border-radius:10px;'
             'padding:8px 14px;text-align:center;font-size:20px;color:var(--ink)">Загрузочные инструкции &bull; POST &bull; конфигурации &bull; прошивки</div></div>')
    o.append(f'<div data-s="7" style="position:absolute;left:0;top:0;width:1920px;height:1080px;pointer-events:none">'
             f'<div style="pointer-events:auto">{mem(462, 660, "SPI NOR Flash", "p081_spi.jpg", spi_b, 190)}'
             f'{mem(668, 875, "NAND Flash", "p081_nand.jpg", nand_b, 170)}</div></div>')

    def pw(x0, x1, col, label, txt, icn, s):
        return (f'<div class="card" data-s="{s}" style="{R(x0, 443, x1, 495)}display:flex;gap:20px;align-items:center;padding:0 22px">'
                f'<span style="display:grid;place-items:center;width:60px;height:60px;border-radius:50%;background:{col};color:#fff">'
                f'<svg viewBox="0 0 24 24" style="width:34px;height:34px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round">{icon("power")[24:-6]}</svg></span>'
                f'<span style="{HEAD}font-size:23px;color:{col};white-space:nowrap">{label}</span>'
                f'<svg width="64" height="24" viewBox="0 0 64 24"><path d="M2 12 H52" stroke="#2a6bf2" stroke-width="3"/><path d="M44 4 L58 12 L44 20Z" fill="#2a6bf2"/></svg>'
                f'<span style="font-size:21px;color:var(--ink);line-height:1.25;flex:1">{txt}</span>{ico(icn, "sm")}</div>')

    o.append(pw(15, 437, "#1f9a4f", "Питание включено", "ОЗУ хранит рабочие данные", "list", 8))
    o.append(pw(450, 885, "#d93a3f", "Питание выключено", "ПЗУ сохраняет загрузочные файлы и конфигурации", "db", 8))
    return "".join(o)


SLIDES.append(("p081", "Устройство коммутаторов MES", p081()))


# ======================================================= p082 WB-2P-LR5
def p082():
    o = ['<img class="ab" data-s="1" src="assets/p082_sceneA.jpg" style="left:0;top:221px;width:1920px;'
         '-webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 40px,#000 90%,transparent 100%);'
         'mask-image:linear-gradient(to bottom,transparent 0,#000 40px,#000 90%,transparent 100%)">',
         '<img class="ab" data-s="1" src="assets/p082_sceneB.jpg" style="left:0;top:0;width:595px;'
         '-webkit-mask-image:linear-gradient(to bottom,#000 88%,transparent 100%);mask-image:linear-gradient(to bottom,#000 88%,transparent 100%)">']
    tiles = [("wifi", "5 ГГц · IEEE 802.11a/n/ac"), ("net", "MIMO 2×2"), ("chart", "Мощность до 28 дБм"),
             ("wifi", "Антенна 12 дБ"), ("link", "PoE-инжектор 24 В"), ("power", "Кнопка Reset на инжекторе")]
    for i, (icn, t) in enumerate(tiles):
        o.append(f'<div class="card solid" data-s="2" style="position:absolute;left:{608 + i * 208}px;top:64px;width:190px;height:149px;'
                 f'padding:14px 8px;text-align:center;border-radius:18px;--dl:{i * 70}ms">'
                 f'<div style="display:flex;justify-content:center">{ico(icn, "sm")}</div>'
                 f'<div style="margin-top:12px;font-size:16px;font-weight:700;color:var(--navy);text-transform:uppercase;line-height:1.25">{t}</div></div>')
    arts = [("p082_art1.jpg", 15, 292, "Дальняя беспроводная связь", "wifi", 3, 560),
            ("p082_art2.jpg", 305, 585, "Доступ к домашней сети", "server", 4, 430),
            ("p082_art3.jpg", 598, 878, "Фиксированный ШПД", "globe", 5, 290)]
    for img, x0, x1, t, icn, s, iw in arts:
        w = px(x1) - px(x0)
        o.append(f'<div class="card" data-s="{s}" style="{R(x0, 378, x1, 495)}padding:0;overflow:hidden">'
                 f'<div class="ab" style="left:20px;top:18px;display:flex;gap:18px;align-items:center">{ico(icn, "sm hex")}'
                 f'<span style="{HEAD}font-size:24px">{t}</span></div>'
                 f'<img class="ab" src="assets/{img}" style="left:{(w - iw) // 2}px;bottom:8px;width:{iw}px;opacity:.95"></div>')
    return "".join(o)


SLIDES.append(("p082", "WB-2P-LR5: абонентская станция и базовая станция", p082()))
