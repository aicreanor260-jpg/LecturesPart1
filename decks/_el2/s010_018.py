# -*- coding: utf-8 -*-
"""Слайды по референсам p010, p012, p013, p014, p015, p017, p018."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from _el2_lib import ico, arrow_svg

SLIDES = []


def ab(l, t, w=None, extra=""):
    s = f"position:absolute;left:{l}px;top:{t}px;"
    if w: s += f"width:{w}px;"
    return s + extra


def layer(*parts):
    return ('<svg class="ab" style="left:0;top:0;width:1920px;height:1080px;overflow:visible" '
            'viewBox="0 0 1920 1080">' + "".join(parts) + '</svg>')


def tile(l, t, w, icn, text, s, dl=0, h=150, fs=18):
    return (f'<div class="card" data-s="{s}" style="{ab(l, t, w)}height:{h}px;padding:16px;text-align:center;--dl:{dl}ms">'
            f'<div style="display:flex;justify-content:center">{ico(icn, "sm")}</div>'
            f'<div style="margin-top:10px;font-size:{fs}px;font-weight:700;color:var(--navy);'
            f'text-transform:uppercase;line-height:1.25">{text}</div></div>')


# ======================================================= модели MES (p010)
def mes_models():
    o = ['<h1 class="t ab ctr-x" style="top:26px;width:1700px">Модели MES и их характеристики</h1>',
         '<div class="sub ab ctr-x" style="top:104px">Коммутаторы доступа</div>']

    feats = [("expand", "Компактные размеры"), ("temp", "Расширенный температурный диапазон"),
             ("shield", "Надёжность и отказоустойчивость"), ("bolt", "Безопасность и защита от скачков")]
    for i, (icn, t) in enumerate(feats):
        o.append(f'<div class="ab" data-s="1" style="left:{150 + i * 420}px;top:168px;width:390px;display:flex;'
                 f'gap:16px;align-items:center;--dl:{i * 70}ms">{ico(icn, "sm")}'
                 f'<div style="font-size:19px;font-weight:700;color:var(--navy);text-transform:uppercase;'
                 f'line-height:1.25">{t}</div></div>')

    def dev(l, t, w, img, name, s, imgw=None):
        return (f'<div class="card" data-s="{s}" style="{ab(l, t, w)}height:260px;padding:20px">'
                f'<img class="cut" src="assets/{img}" style="width:{imgw or 100}{"px" if imgw else "%"};'
                f'display:block;margin:0 auto">'
                f'<div class="ab" style="left:0;right:0;bottom:-22px;display:flex;justify-content:center">'
                f'<span class="tag mono" style="font-size:25px">{name}</span></div></div>')

    o += [dev(80, 260, 560, "p010_mes1428.jpg", "MES1428", 2),
          dev(680, 260, 560, "p010_mes2300.jpg", "MES2300-08", 3),
          dev(1280, 260, 560, "p010_mes2420.jpg", "MES2420B-24D", 4),
          dev(290, 600, 620, "p010_mes2408.jpg", "MES2408", 5),
          dev(1010, 600, 620, "p010_mes2408b.jpg", "MES2408B", 6)]
    return "".join(o)


SLIDES.append(("p010", "Модели MES: коммутаторы доступа", mes_models()))


# ======================================================= функционал ESR (p012)
def esr_functions():
    o = ['<h1 class="t ab ctr-x" style="top:26px;width:1820px;font-size:56px">Основной функционал маршрутизаторов ESR</h1>',
         '<div class="sub n ab ctr-x" style="top:96px;font-size:21px">'
         'Возможности зависят от модели, версии ПО и установленных лицензий</div>']

    steps = [("globe", "eltex-co.ru"), ("doc", "Каталог, маршрутизаторы ESR"), ("router", "Выбрать нужную модель"),
             ("list", "Документы и файлы"), ("doc", "Руководство по эксплуатации или Справочник команд CLI")]
    o.append(f'<div class="card" data-s="1" style="{ab(70, 150, 380)}height:620px">'
             '<div class="ch sm">Где посмотреть функции модели</div>'
             + "".join(f'<div style="display:flex;gap:14px;align-items:center;margin-bottom:22px">'
                       f'<span class="badge o" style="width:38px;height:38px;font-size:20px">{i + 1}</span>'
                       f'{ico(icn, "sm")}<p class="b sm" style="flex:1">{t}</p></div>'
                       for i, (icn, t) in enumerate(steps)) + '</div>')

    groups = [("net", "Интерфейсы и VLAN", ["Сетевые интерфейсы", "VLAN"]),
              ("arrows", "Коммутация и маршрутизация", ["L2, LAG/LACP", "RIP, OSPF, IS-IS, BGP"]),
              ("lock", "Туннели и VPN", ["MPLS, GRE, DMVPN", "IPsec, OpenVPN", "WireGuard, PPTP, L2TP"]),
              ("gear", "Сетевые сервисы", ["NAT и DHCP", "QoS"]),
              ("shield", "Безопасность", ["ACL и Firewall", "IPS/IDS", "Защита от DoS/DDoS"]),
              ("chart", "Резервирование и мониторинг", ["VRRP, MultiWAN, кластер 1+1", "SNMP, Syslog, NetFlow", "Zabbix и SLA"])]
    o.append(f'<div class="ch sm ab" style="left:490px;top:150px">Основные группы функций</div>')
    for i, (icn, title, items) in enumerate(groups):
        l = 490 + (i % 3) * 300
        t = 200 + (i // 3) * 290
        o.append(f'<div class="card" data-s="{2 + i}" style="{ab(l, t, 280)}height:260px;padding:18px 20px;text-align:center">'
                 f'<div style="display:flex;justify-content:center">{ico(icn, "sm")}</div>'
                 f'<div style="margin-top:10px;font-size:18px;font-weight:800;color:var(--navy);text-transform:uppercase;'
                 f'line-height:1.2">{title}</div>'
                 + "".join(f'<p class="b sm dim" style="margin-top:10px;font-size:17px">{x}</p>' for x in items)
                 + '</div>')

    crit = [("speed", "Количество и скорость портов"), ("chart", "Производительность маршрутизации"),
            ("shield", "Производительность Firewall и VPN"), ("stack", "Поддерживаемые протоколы"),
            ("lock", "Безопасность"), ("reload", "Резервирование")]
    o.append('<div class="ch sm ab" style="left:1420px;top:150px">Ключевые критерии выбора</div>')
    for i, (icn, t) in enumerate(crit):
        o.append(tile(1420 + (i % 2) * 230, 200 + (i // 2) * 200, 210, icn, t, 8 + i // 2, dl=(i % 2) * 80, h=180, fs=16))

    o.append(f'<img class="ph ab" data-s="11" src="assets/p012_scene.jpg" style="{ab(70, 800, 1780)}">')
    return "".join(o)


SLIDES.append(("p012", "Основной функционал маршрутизаторов ESR", esr_functions()))


# ======================================================= внешние точки доступа (p013)
def outdoor_ap():
    o = ['<h1 class="t ab ctr-x" style="top:24px;width:1700px">Внешние точки доступа <span class="lt">Eltex</span></h1>',
         '<div class="sub ab ctr-x" style="top:100px;font-size:20px;letter-spacing:6px">'
         'Надёжные беспроводные сети в любых условиях</div>']

    devs = [("p013_wop30li.jpg", "WOP-30LI"), ("p013_wop12ac.jpg", "WOP-12ac"),
            ("p013_wop50l.jpg", "WOP-50L"), ("p013_wop3lex.jpg", "WOP-3L-EX")]
    for i, (img, name) in enumerate(devs):
        o.append(f'<div class="card" data-s="{1 + i}" style="{ab(70 + i * 450, 160, 420)}height:480px;padding:20px">'
                 f'<img class="cut" src="assets/{img}" style="width:100%;max-height:360px;object-fit:contain">'
                 f'<div class="mono ab" style="left:0;right:0;bottom:24px;text-align:center;font-size:30px;'
                 f'font-weight:800;color:var(--navy)">{name}</div></div>')

    caps = [("wifi", "2,4 и 5 ГГц"), ("net", "PoE"), ("lock", "WPA2/WPA3"),
            ("layers", "VLAN и несколько SSID"), ("wifi", "Бесшовный роуминг"), ("mon", "Централизованное управление")]
    o.append(f'<div class="card" data-s="5" style="{ab(70, 670, 1780)}height:180px;padding:20px 30px">'
             '<div class="ab" style="left:34px;top:54px;width:170px;font-size:26px;font-weight:800;color:var(--navy);'
             'text-transform:uppercase;line-height:1.15">Общие возможности</div>'
             + "".join(f'<div class="ab" style="left:{240 + i * 262}px;top:28px;width:250px;text-align:center">'
                       f'<div style="display:flex;justify-content:center">{ico(icn, "sm")}</div>'
                       f'<div style="margin-top:10px;font-size:19px;font-weight:600;color:var(--navy);line-height:1.25">{t}</div></div>'
                       for i, (icn, t) in enumerate(caps)) + '</div>')

    apps = [("snow", "Парки и стадионы"), ("wifi", "Направленное покрытие"),
            ("gear", "Промышленные объекты"), ("warn", "Взрывоопасные зоны")]
    o.append(f'<div class="card" data-s="6" style="{ab(70, 880, 1780)}height:160px;padding:20px 30px">'
             '<div class="ab" style="left:34px;top:46px;width:170px;font-size:26px;font-weight:800;color:var(--navy);'
             'text-transform:uppercase;line-height:1.15">Сферы применения</div>'
             + "".join(f'<div class="ab" style="left:{250 + i * 400}px;top:50px;width:380px;display:flex;gap:16px;'
                       f'align-items:center">{ico(icn, "sm")}'
                       f'<div style="font-size:20px;font-weight:600;color:var(--navy)">{t}</div></div>'
                       for i, (icn, t) in enumerate(apps)) + '</div>')
    return "".join(o)


SLIDES.append(("p013", "Внешние точки доступа Eltex", outdoor_ap()))


# ======================================================= индикаторы интерфейсов (p014)
def indicators():
    o = ['<div class="ab" style="left:80px;top:46px;width:700px">'
         '<div class="big" style="font-size:70px;line-height:1.05">Индикаторы<br><span class="lt">интерфейсов</span></div></div>',
         '<p class="b sm ab" style="left:80px;top:230px;width:640px">Маршрутизаторы имеют несколько интерфейсов, '
         'которые используются для подключения к нескольким сетям. Каждый интерфейс является участником отдельной '
         'IP-сети. Для каждого интерфейса необходимо настроить IP-адрес и маску подсети соответствующей сети.</p>',
         f'<img class="ab" src="assets/dev/esr-3150.webp" style="{ab(820, 110, 1020)}'
         f'filter:drop-shadow(0 14px 26px rgba(110,100,165,.22))">']

    o.append(f'<div class="card" data-s="1" style="{ab(80, 380, 480)}height:470px">'
             '<div class="ch sm" style="justify-content:center">Разъём RJ-45</div>'
             '<div style="display:flex;justify-content:space-between;padding:0 40px">'
             '<span class="b sm" style="color:#1d8a5b;font-weight:700">LINK/ACT</span>'
             '<span class="b sm" style="color:#d08a1b;font-weight:700">SPEED</span></div>'
             '<img class="cut ab" src="assets/p014_rj45.jpg" style="left:95px;top:120px;width:290px">'
             '<p class="b sm dim ab" style="left:30px;top:390px;width:420px;text-align:center">'
             'Расположение индикаторов разъёма RJ-45</p></div>')

    o.append(f'<div class="card" data-s="2" style="{ab(600, 380, 420)}height:470px">'
             '<div class="ch sm" style="justify-content:center;font-size:21px">Индикаторы оптических интерфейсов</div>'
             '<img class="cut ab" src="assets/p014_sfp.jpg" style="left:110px;top:110px;width:200px">'
             '<div class="ab" style="left:30px;top:330px;width:360px;display:flex;justify-content:space-around">'
             '<span class="mono b sm" style="font-weight:700;color:#1d8a5b">RX/ACT</span>'
             '<span class="mono b sm" style="font-weight:700;color:#d2662a">TX/ACT</span></div>'
             '<p class="b sm dim ab" style="left:30px;top:385px;width:360px;text-align:center">'
             'Расположение индикаторов оптических интерфейсов</p></div>')

    rows = [("Выключен", "Выключен", "Порт выключен или соединение не установлено"),
            ("Выключен", "Горит постоянно", "Установлено соединение на скорости 10/100 Мбит/с"),
            ("Горит постоянно", "Горит постоянно", "Установлено соединение на скорости 1000 Мбит/с"),
            ("X", "Мигание", "Идёт передача данных")]
    tr = "".join(f'<tr><td style="text-align:center">{a}</td><td style="text-align:center">{b}</td><td>{c}</td></tr>'
                 for a, b, c in rows)
    o.append(f'<div class="card" data-s="3" style="{ab(1060, 380, 790)}height:470px">'
             '<div class="ch sm">Состояние интерфейса</div>'
             '<table class="tbl" style="font-size:19px"><thead><tr>'
             '<th style="background:#c8803a;text-align:center">Индикатор<br>SPEED</th>'
             '<th class="b2" style="text-align:center">Индикатор<br>LINK/ACT</th>'
             '<th class="b3">Состояние интерфейса</th></tr></thead>'
             f'<tbody>{tr}</tbody></table></div>')

    def ind(l, color, name, txt, s):
        return (f'<div class="card" data-s="{s}" style="{ab(l, 880, 740)}height:170px;padding:20px 26px;'
                f'display:flex;gap:20px;align-items:flex-start">'
                f'<svg width="44" height="40" viewBox="0 0 44 40"><polygon points="22,34 4,6 40,6" fill="{color}" '
                f'stroke="#2b3f6b" stroke-width="1.5"/></svg>'
                f'<div><div class="mono" style="font-size:26px;font-weight:800;color:{color}">{name}</div>'
                f'<p class="b sm" style="margin-top:8px">{txt}</p></div></div>')

    o += [ind(80, "#1d8a5b", "RX/ACT (приём)",
              "Индикатор загорается или мигает при наличии оптического сигнала на приёмном интерфейсе (RX). "
              "Мигание указывает на приём данных.", 4),
          ind(860, "#d2662a", "TX/ACT (передача)",
              "Индикатор загорается или мигает на передающем интерфейсе (TX). Мигание указывает на передачу данных.", 5)]
    return "".join(o)


SLIDES.append(("p014", "Индикаторы интерфейсов", indicators()))


# ======================================================= MES1428 задняя панель (p015)
def mes1428_back():
    o = ['<div class="ab" style="left:96px;top:56px"><div class="big">MES1428</div>'
         '<div class="kick" style="margin-top:6px">Задняя панель</div></div>',
         f'<img class="cut ab" src="assets/p015_mes1428_back.jpg" style="{ab(190, 320, 1540)}">']

    def call(l, n, title, txt, icn, s):
        return (f'<div class="card" data-s="{s}" style="{ab(l, 650, 520)}display:flex;gap:18px;align-items:flex-start">'
                f'<span class="badge">{n}</span><div style="flex:1">'
                f'<div style="font-size:24px;font-weight:800;color:var(--navy);text-transform:uppercase">{title}</div>'
                f'<div style="display:flex;gap:16px;align-items:center;margin-top:12px">{ico(icn, "sm")}'
                f'<p class="b sm dim">{txt}</p></div></div></div>')

    o += [call(330, 2, "Вентиляционные отверстия", "Обеспечивают теплообмен и охлаждение компонентов", "fan", 1),
          call(1070, 1, "Клемма заземления", "Подключение корпуса устройства к контуру защитного заземления", "ground", 2)]
    o.append(layer(
        '<path class="dr" data-s="1" pathLength="1" d="M420 520 L420 600 L590 600 L590 650" stroke="var(--blue)" stroke-width="4" fill="none"/>',
        '<path class="dr" data-s="1" pathLength="1" d="M1240 520 L1240 600 L590 600" stroke="var(--blue)" stroke-width="4" fill="none"/>',
        '<path class="dr" data-s="2" pathLength="1" d="M1650 520 L1650 600 L1330 600 L1330 650" stroke="var(--blue)" stroke-width="4" fill="none"/>'))

    others = [("power", "Разъём питания переменного тока"), ("bolt", "Разъём аккумуляторной батареи"),
              ("fan", "Вентиляторные модули")]
    o.append(f'<div class="card" data-s="3" style="{ab(620, 850, 900)}height:190px;padding:20px 30px">'
             '<div style="text-align:center;font-size:26px;font-weight:800;color:var(--navy);text-transform:uppercase;'
             'margin-bottom:16px">На других моделях</div>'
             + "".join(f'<div class="ab" style="left:{40 + i * 290}px;top:76px;width:260px;text-align:center">'
                       f'<div style="display:flex;justify-content:center">{ico(icn, "sm")}</div>'
                       f'<p class="b sm dim" style="margin-top:8px">{t}</p></div>'
                       for i, (icn, t) in enumerate(others)) + '</div>')
    return "".join(o)


SLIDES.append(("p015", "MES1428: задняя панель", mes1428_back()))


# ======================================================= WOP-12ac (p017)
def wop12ac():
    o = ['<div class="ab" style="left:80px;top:60px"><div class="big" style="font-size:92px">WOP-12ac</div>'
         '<div class="kick" style="margin-top:8px">Внешняя точка доступа</div></div>',
         f'<img class="cut ab" src="assets/p017_wop12ac.jpg" style="{ab(1010, 60, 860)}">']

    specs = [("wifi", "2,4 и 5 ГГц"), ("speed", "До 1300 + 450 Мбит/с"), ("net", "PoE+, IEEE 802.3at"),
             ("user", "До 64 устройств в кластере"), ("wifi", "Бесшовный роуминг"), ("temp", "От −40 до +65 °C")]
    for i, (icn, t) in enumerate(specs):
        o.append(f'<div class="card" data-s="{1 + i // 3}" style="'
                 f'{ab(80 + (i % 3) * 300, 300 + (i // 3) * 250, 280)}height:220px;padding:20px;text-align:center;'
                 f'--dl:{(i % 3) * 90}ms">'
                 f'<div style="display:flex;justify-content:center">{ico(icn)}</div>'
                 f'<div style="margin-top:14px;font-size:21px;font-weight:700;color:var(--navy);text-transform:uppercase;'
                 f'line-height:1.25">{t}</div></div>')

    apps = [("snow", "Парки"), ("stack", "Стадионы"), ("gear", "Промышленные объекты")]
    for i, (icn, t) in enumerate(apps):
        o.append(f'<div class="card" data-s="3" style="{ab(80 + i * 300, 830, 280)}height:140px;padding:18px;'
                 f'display:flex;gap:16px;align-items:center;--dl:{i * 90}ms">{ico(icn, "sm")}'
                 f'<div style="font-size:20px;font-weight:700;color:var(--navy);text-transform:uppercase">{t}</div></div>')
    return "".join(o)


SLIDES.append(("p017", "WOP-12ac: внешняя точка доступа", wop12ac()))


# ======================================================= справка в CLI MES (p018)
def help_mes():
    o = ['<h1 class="t ab ctr-x" style="top:90px;width:1500px">Справка в командной строке <span class="lt">MES</span></h1>']

    def card(l, n, title, mid, txt, s):
        return (f'<div class="card solid" data-s="{s}" style="{ab(l, 230, 540)}height:620px;padding:40px 42px;'
                f'display:flex;flex-direction:column;gap:26px">'
                f'<div style="display:flex;gap:20px;align-items:center">'
                f'<span class="mono" style="background:var(--blue);color:#fff;border-radius:14px;padding:6px 18px;'
                f'font-size:40px;font-weight:800">{n}</span>'
                f'<div style="font-size:31px;font-weight:800;color:var(--navy);text-transform:uppercase;line-height:1.1">{title}</div></div>'
                f'<div style="flex:1;display:grid;place-items:center">{mid}</div>'
                f'<p class="b">{txt}</p></div>')

    q = ('<div class="card" style="width:170px;height:170px;display:grid;place-items:center;border-radius:30px">'
         '<span style="font-size:104px;font-weight:800;color:var(--blue);line-height:1">?</span></div>')
    term = ('<div style="width:260px;border-radius:22px;overflow:hidden;box-shadow:var(--sh)">'
            '<div style="background:#dbe8ff;padding:12px 16px;display:flex;gap:9px">'
            + "".join('<i style="width:13px;height:13px;border-radius:50%;background:#fff;display:block"></i>' for _ in range(3))
            + '</div><div style="background:#fff;padding:30px 24px;display:flex;align-items:center;justify-content:space-between">'
              '<span class="mono" style="font-size:48px;font-weight:800;color:var(--navy)">&gt;_</span>'
              '<span style="display:grid;place-items:center;width:58px;height:58px;border-radius:50%;background:var(--blue);'
              'color:#fff;font-size:30px">&#10003;</span></div></div>')
    keys = ('<div style="display:flex;gap:22px">'
            '<span class="chip key" style="font-size:32px;padding:20px 30px">CTRL</span>'
            '<span class="chip key" style="font-size:32px;padding:20px 30px">TAB</span></div>')
    o += [card(140, "01", "Контекстная подсказка", q, "Показывает доступные команды и параметры в текущем режиме.", 1),
          card(690, "02", "Проверка синтаксиса", term, "Помогает обнаружить ошибку в введённой команде.", 2),
          card(1240, "03", "Горячие клавиши", keys, "Ускоряют ввод, редактирование и работу с командами.", 3)]
    return "".join(o)


SLIDES.append(("p018", "Справка в командной строке MES", help_mes()))
