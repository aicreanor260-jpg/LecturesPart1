# -*- coding: utf-8 -*-
"""Слайды по референсам p051-p058."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from _el2_lib import ico, arrow_svg

SLIDES = []


def ab(l, t, w=None, extra=""):
    s = f"position:absolute;left:{l}px;top:{t}px;"
    if w:
        s += f"width:{w}px;"
    return s + extra


def layer(*parts):
    return ('<svg class="ab" style="left:0;top:0;width:1920px;height:1080px;overflow:visible" '
            'viewBox="0 0 1920 1080">' + "".join(parts) + '</svg>')


def line_svg(x1, y1, x2, y2, s, col="var(--blue)"):
    return (f'<path class="dr" data-s="{s}" pathLength="1" d="M{x1} {y1} L{x2} {y2}" stroke="{col}" '
            f'stroke-width="4" fill="none" stroke-linecap="round"/>')


NAVY = 'font-weight:800;color:var(--navy);text-transform:uppercase'


# ================================================================ p051 ESR
def esr_intro():
    o = []
    o.append('<svg class="ab" style="left:1330px;top:20px;width:420px;height:420px" viewBox="0 0 420 420">'
             '<defs><radialGradient id="gl51" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#ffffff"/>'
             '<stop offset=".6" stop-color="#cfe0fb"/><stop offset="1" stop-color="#9dbdf0"/></radialGradient></defs>'
             '<circle cx="210" cy="210" r="195" fill="url(#gl51)" opacity=".85"/>'
             '<g fill="none" stroke="#fff" stroke-width="2" opacity=".8"><ellipse cx="210" cy="210" rx="195" ry="70"/>'
             '<ellipse cx="210" cy="210" rx="90" ry="195"/><path d="M15 210h390M210 15v390"/>'
             '<path d="M70 120L180 170 300 110M120 300L200 230 330 290M180 170L200 230"/></g>'
             '<g fill="#fff"><circle cx="70" cy="120" r="5"/><circle cx="180" cy="170" r="6"/><circle cx="300" cy="110" r="5"/>'
             '<circle cx="200" cy="230" r="6"/><circle cx="330" cy="290" r="5"/><circle cx="120" cy="300" r="5"/></g></svg>')
    o.append('<div class="ab" style="left:50px;top:70px;width:640px">'
             '<div style="font-size:78px;font-weight:800;color:var(--navy);line-height:1">СЕРВИСНЫЕ</div>'
             '<div style="font-size:60px;font-weight:800;color:var(--blue);line-height:1.1;margin-top:6px">МАРШРУТИЗАТОРЫ</div>'
             '<div style="font-size:88px;font-weight:800;color:var(--navy);line-height:1.05">ESR</div></div>')
    o.append('<div class="ab" style="left:50px;top:320px;width:560px">'
             '<div style="width:70px;height:3px;background:var(--navy);margin-bottom:14px"></div>'
             '<p class="b" style="font-size:24px;color:var(--navy)">Надёжная основа<br><i>современных сетей</i></p></div>')
    o.append('<div class="card ab" data-s="1" style="left:683px;top:40px;width:540px;height:270px;padding:26px 32px">'
             '<p class="b" style="font-size:21px;line-height:1.5">Сервисные маршрутизаторы Элтекс (ESR) — это современные '
             'устройства, которые пересылают пакеты между элементами сети, основываясь на правилах или таблицах маршрутизации. '
             'Линейка ESR включает решения для сетей любого масштаба — от компактных устройств до высокопроизводительных '
             'маршрутизаторов операторского класса.</p></div>')
    o.append('<div class="ab" data-s="1" style="left:1690px;top:100px;width:200px;text-align:left">'
             '<div style="font-size:23px;font-weight:700;color:var(--blue);text-transform:uppercase;line-height:1.3">Сети<br>объединяют<br>возможности</div>'
             '<div style="margin-top:24px;font-size:15px;letter-spacing:1px;color:var(--dim);text-transform:uppercase;line-height:1.9">'
             'Безопасность<br>Производительность<br>Гибкость</div></div>')

    def feats(l, top, w, items, s):
        n = len(items)
        cw = w // n
        h = ''
        for i, (icn, txt) in enumerate(items):
            h += (f'<div class="ab" data-s="{s}" style="left:{l + i * cw}px;top:{top}px;width:{cw}px;text-align:center;'
                  f'--dl:{i * 90}ms"><div style="display:flex;justify-content:center">{ico(icn, "sm")}</div>'
                  f'<p class="b sm" style="margin-top:8px;font-size:17px;line-height:1.3">{txt}</p></div>')
        return h

    def head(l, top, name, desc, s, w=520):
        return (f'<div class="ab" data-s="{s}" style="left:{l}px;top:{top}px;width:{w}px">'
                f'<div style="font-size:40px;font-weight:800;color:var(--navy);line-height:1">{name}</div>'
                f'<p class="b" style="font-size:21px;line-height:1.3;margin-top:6px;color:var(--navy)">{desc}</p></div>')

    o.append('<div class="card ab" data-s="2" style="left:96px;top:515px;width:500px;height:300px"></div>')
    o.append(head(150, 425, "ESR-10", "Компактное решение<br>для небольших сетей", 2))
    o.append('<img class="cut ab" data-s="2" src="assets/p051_esr10.jpg" style="left:170px;top:545px;width:330px">')
    o.append(feats(110, 722, 480, [("expand", "Компактный корпус"), ("gear", "Базовый набор интерфейсов"),
                                   ("chart", "Для небольших офисов и филиалов")], 2))
    o.append('<div class="card ab" data-s="3" style="left:650px;top:470px;width:580px;height:340px"></div>')
    o.append(head(710, 365, "ESR-30", "Оптимальный баланс<br>функциональности", 3))
    o.append('<img class="cut ab" data-s="3" src="assets/p051_esr30.jpg" style="left:680px;top:515px;width:520px">')
    o.append(feats(665, 700, 550, [("layers", "Расширенные возможности"), ("net", "Больше интерфейсов"),
                                   ("stack", "Для корпоративных сегментов")], 3))
    o.append('<div class="card ab" data-s="4" style="left:1290px;top:430px;width:590px;height:380px"></div>')
    o.append(head(1312, 355, "ESR-1700", "Высокая производительность<br>для крупных сетей", 4, 560))
    o.append('<img class="cut ab" data-s="4" src="assets/p051_esr1700.jpg" style="left:1320px;top:465px;width:540px">')
    o.append(feats(1305, 690, 560, [("speed", "Высокая производительность"), ("server", "Многоядерный процессор"),
                                    ("db", "Для операторов и крупных компаний")], 4))
    o.append('<div class="card ab" data-s="5" style="left:40px;top:830px;width:640px;height:200px;padding:22px 30px">'
             '<div style="font-size:24px;font-weight:800;color:var(--navy);text-transform:uppercase;margin-bottom:14px">Ключевые отличия моделей</div>'
             '<div style="display:flex;gap:20px;justify-content:space-between">'
             + "".join(f'<div style="flex:1;display:flex;flex-direction:column;gap:8px">{ico(i, "sm")}'
                       f'<p class="b sm" style="font-size:17px;line-height:1.3">{t}</p></div>'
                       for i, t in [("net", "Набор интерфейсов"), ("server", "Центральный процессор"), ("chart", "Производительность")])
             + '</div></div>')
    o.append('<div class="card ab" data-s="6" style="left:715px;top:840px;width:650px;height:190px;display:flex;gap:26px;'
             'align-items:center;padding:22px 34px">' + ico("layers") +
             '<p class="b" style="font-size:21px;line-height:1.45">Все устройства серии ESR имеют единый набор функциональных '
             'возможностей. Разница между моделями заключается в объёме трафика, который они могут обрабатывать.</p></div>')
    o.append('<div class="ab" data-s="6" style="left:1500px;top:995px;width:380px;text-align:right;font-size:16px;letter-spacing:1px;'
             'color:var(--dim);text-transform:uppercase;line-height:1.5">От небольших офисов<br>до масштабных сетей</div>')
    return "".join(o)


SLIDES.append(("p051", "Сервисные маршрутизаторы ESR", esr_intro()))


# ================================================================ p052 справка
def help_slide():
    o = ['<h1 class="t ab ctr-x" style="top:50px;width:1700px">Справка в командной строке <span class="lt">ESR</span></h1>']

    def card(l, n, title, art, txt, s):
        return (f'<div class="card" data-s="{s}" style="{ab(l, 230, 590)}height:634px;padding:30px 34px">'
                f'<div style="display:flex;gap:26px;align-items:center">'
                f'<span class="badge" style="width:92px;height:92px;font-size:46px;border-radius:16px">{n}</span>'
                f'<div style="{NAVY};font-size:33px;line-height:1.15">{title}</div></div>'
                f'<div style="height:230px;margin-top:34px;display:flex;justify-content:center;align-items:center">{art}</div>'
                f'<p class="b" style="font-size:25px;line-height:1.4;margin-top:34px;padding-left:10px">{txt}</p></div>')

    q = ('<div class="card solid" style="width:210px;height:200px;display:grid;place-items:center;border-radius:30px;'
         'font-size:120px;font-weight:800;color:var(--navy)">?</div>')
    term = ('<div style="width:460px;height:200px;border-radius:18px;background:#fff;border:2px solid var(--line);'
            'box-shadow:var(--sh);overflow:hidden;position:relative">'
            '<div style="height:44px;background:linear-gradient(180deg,#4f86f5,#2a5fd6);display:flex;gap:10px;align-items:center;padding-left:22px">'
            + "".join('<i style="width:13px;height:13px;border-radius:50%;background:#fff;display:block"></i>' for _ in range(3)) +
            '</div><div class="mono" style="position:absolute;left:28px;top:80px;font-size:50px;font-weight:700;color:var(--navy)">&gt;_</div>'
            '<span style="position:absolute;right:30px;top:88px;width:64px;height:64px;border-radius:50%;background:var(--blue);'
            'display:grid;place-items:center"><svg viewBox="0 0 24 24" width="38" height="38" fill="none" stroke="#fff" stroke-width="3" '
            'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span></div>')
    keys = ('<div style="display:flex;gap:22px">'
            '<span class="chip key" style="font-size:30px;width:250px;height:150px;border-radius:26px;justify-content:center">CTRL</span>'
            '<span class="chip key" style="font-size:30px;width:220px;height:150px;border-radius:26px;justify-content:center">TAB</span></div>')
    o.append(card(43, "01", "Контекстная<br>подсказка", q, "Показывает доступные команды и параметры в текущем режиме", 1))
    o.append(card(665, "02", "Проверка<br>синтаксиса", term, "Помогает обнаружить ошибку в введённой команде", 2))
    o.append(card(1286, "03", "Горячие<br>клавиши", keys, "Ускоряют ввод, редактирование и работу с командами", 3))
    o.append('<div class="card ab" data-s="4" style="left:160px;top:895px;width:1600px;height:84px;display:flex;gap:24px;'
             'align-items:center;padding:0 40px">' + ico("info", "sm") +
             '<span style="width:2px;height:40px;background:var(--line)"></span>'
             '<p class="b" style="font-size:25px">Справка зависит от текущего режима командной строки</p></div>')
    return "".join(o)


SLIDES.append(("p052", "Справка в командной строке ESR", help_slide()))


# ================================================================ p053 VAP
def vap():
    o = ['<h1 class="t left ab" style="left:80px;top:24px;width:1700px;font-size:62px">Настройка '
         '<span class="lt">виртуальной</span> точки доступа</h1>']
    o.append('<img class="ph ab" data-s="1" src="assets/p053_webui.jpg" style="left:43px;top:138px;width:1010px">')

    def card(top, h, icn, title, txt, s, extra=""):
        return (f'<div class="card" data-s="{s}" style="{ab(1088, top, 796)}height:{h}px;padding:22px 30px;display:flex;'
                f'gap:24px;align-items:center">{ico(icn, "hex")}<div style="flex:1">'
                f'<div style="{NAVY};font-size:32px;margin-bottom:6px">{title}</div>'
                f'<p class="b" style="font-size:19px;line-height:1.35">{txt}</p></div>{extra}</div>')

    wifi_chip = ('<div style="text-align:center;flex:none">' + ico("wifi") +
                 '<div class="chip mono" style="font-size:16px;padding:6px 12px;margin-top:8px">WEP-3ax_Portal</div></div>')
    o.append(card(139, 190, "check", "Включено", "Флаг включает виртуальную точку доступа. Без флага VAP отключена.", 2,
                  '<div style="flex:none">' + ico("router") + '</div>'))
    o.append(card(345, 222, "net", "VLAN ID", "Определяет VLAN для трафика клиентов. При передаче клиенту метка снимается, "
                  "обратный трафик получает указанный VLAN ID.", 3,
                  '<div class="mono" style="flex:none;font-size:30px;font-weight:800;color:var(--blue);text-align:center">VLAN<br>1000</div>'))
    o.append(card(582, 228, "wifi", "SSID", "Имя беспроводной сети, по которому устройства находят нужную Wi-Fi-сеть. "
                  "SSID чувствителен к регистру и должен совпадать во всех устройствах сети.", 4, wifi_chip))

    o.append('<div class="card ab" data-s="5" style="left:139px;top:840px;width:1642px;height:160px"></div>')

    def cell(l, w, inner, s):
        return (f'<div class="ab" data-s="{s}" style="left:{l}px;top:855px;width:{w}px;height:130px;display:flex;'
                f'align-items:center;justify-content:center;gap:20px">{inner}</div>')

    o.append(cell(190, 360, ico("db") + '<div class="mono" style="font-size:34px;font-weight:800;color:var(--navy)">VLAN<br>1000</div>', 5))
    o.append(cell(700, 330, ico("router") + '<div style="font-size:30px;font-weight:800;color:var(--navy)">VAP</div>', 6))
    o.append(cell(1110, 340, ico("wifi") + '<div class="mono" style="font-size:25px;font-weight:700;color:var(--navy)">SSID:<br>WEP-3ax_Portal</div>', 7))
    o.append(cell(1480, 280, ico("pc") + ico("phone") + ico("mon"), 8))
    o.append(layer(arrow_svg(560, 920, 690, 920, 6), arrow_svg(1040, 920, 1100, 920, 7), arrow_svg(1440, 920, 1490, 920, 8)))
    o.append('<p class="b ab ctr-x" data-s="8" style="top:1018px;font-size:20px;color:var(--navy);text-align:center;width:1400px">'
             'Одна VAP объединяет клиентов с общими параметрами беспроводной сети.</p>')
    return "".join(o)


SLIDES.append(("p053", "Настройка виртуальной точки доступа", vap()))


# ================================================================ p054 режимы ESR
def cli_modes():
    o = ['<h1 class="t ab ctr-x" style="top:14px;width:1700px;font-size:58px">Режимы командной строки</h1>']
    M = 'font-family:var(--mono);font-weight:600;color:#3a4fa0'

    def lst(l, t, items, size, lh):
        return (f'<div class="ab" style="left:{l}px;top:{t}px;{M};font-size:{size}px;line-height:{lh}px">'
                + "<br>".join(items) + '</div>')

    def side(l, t, txts):
        return (f'<div class="ab" style="left:{l}px;top:{t}px;width:190px;font-size:15px;line-height:1.7;letter-spacing:1px;'
                f'color:var(--dim);text-transform:uppercase;border-left:2px solid var(--line);padding-left:16px">'
                + "<br>".join(txts) + '</div>')

    def prompt(l, t, w, txt, size=26, s=None):
        at = f' data-s="{s}"' if s else ""
        return (f'<div class="chip mono ab"{at} style="left:{l}px;top:{t}px;width:{w}px;font-size:{size}px;justify-content:flex-start;'
                f'padding:12px 20px;background:rgba(255,255,255,.9);color:var(--navy)">{txt}</div>')

    o.append('<div class="card ab" data-s="1" style="left:160px;top:107px;width:1606px;height:217px"></div>')
    o.append(f'<div class="ab" data-s="1" style="left:185px;top:132px">{ico("user")}</div>')
    o.append('<div class="ab" data-s="1" style="left:290px;top:134px;width:1100px;font-size:30px;font-weight:800;'
             'color:var(--navy);text-transform:uppercase">Пользовательский (непривилегированный) режим</div>')
    o.append(prompt(290, 190, 310, "esr&gt;", 26, 1))
    o.append('<div class="ab" data-s="1" style="left:785px;top:170px;width:3px;height:140px;background:var(--line)"></div>')
    o.append('<div data-s="1">' + lst(810, 181, ["clear", "dir", "enable", "exit", "help"], 21, 26)
             + lst(1024, 181, ["history", "logout", "no", "ping", "show"], 21, 26)
             + lst(1280, 181, ["ssh", "telnet", "terminal", "traceroute", "uptime"], 21, 26)
             + side(1520, 200, ["Доступ", "Проверка", "Диагностика"]) + '</div>')

    o.append('<div class="card ab" data-s="2" style="left:60px;top:352px;width:1779px;height:651px"></div>')
    o.append(f'<div class="ab" data-s="2" style="left:85px;top:375px">{ico("shield")}</div>')
    o.append('<div class="ab" data-s="2" style="left:210px;top:393px;width:900px;font-size:30px;font-weight:800;'
             'color:var(--navy);text-transform:uppercase">Привилегированный режим</div>')
    o.append('<div class="ab" data-s="2" style="left:1480px;top:382px;font-size:15px;letter-spacing:1px;color:var(--dim);'
             'text-transform:uppercase;width:340px;text-align:right">Полный доступ к системе</div>')
    o.append(prompt(214, 442, 260, "esr#", 26, 2))
    o.append('<div data-s="2">' + lst(214, 515, ["boot", "clear", "commit", "config", "confirm", "copy", "debug", "delete", "dir", "...", "verify"],
                                     22, 28) + '</div>')
    o.append('<div class="card solid ab" data-s="2" style="left:85px;top:900px;width:420px;height:76px;display:flex;gap:16px;'
             'align-items:center;padding:0 20px">' + ico("lock", "sm") +
             '<span class="mono" style="font-size:15px;color:var(--navy);line-height:1.3">admin / password &nbsp;•&nbsp; уровень привилегий 15</span></div>')

    o.append('<div class="card ab" data-s="3" style="left:523px;top:437px;width:1307px;height:548px;background:rgba(255,255,255,.5)"></div>')
    o.append(f'<div class="ab" data-s="3" style="left:545px;top:455px">{ico("gear", "sm")}</div>')
    o.append('<div class="ab" data-s="3" style="left:625px;top:462px;width:900px;font-size:25px;font-weight:800;'
             'color:var(--navy);text-transform:uppercase">Режим глобального конфигурирования</div>')
    o.append(prompt(625, 524, 330, "esr(config)#", 20, 3))
    o.append('<div data-s="3">' + lst(800, 515, ["aaa", "banner", "boot", "bridge", "clock", "do", "enable", "end", "exit", "hostname", "interface",
                                                 "line", "object-group", "port-channel", "privilege", "router", "security", "syslog", "system",
                                                 "tunnel", "username", "vlan", "...", "zabbix-proxy"], 17, 19.4)
             + '<div class="ab" style="left:560px;top:690px;width:200px;font-size:15px;letter-spacing:1px;color:var(--dim);'
               'text-transform:uppercase;line-height:1.7">Конфигурация<br>системы<br>управление<br>ресурсами</div></div>')

    def sub(top, h, icn, title, prm, items, side_t, s):
        h_ = (f'<div class="card solid ab" data-s="{s}" style="left:1002px;top:{top}px;width:810px;height:{h}px;background:rgba(255,255,255,.7)"></div>'
              f'<div class="ab" data-s="{s}" style="left:1020px;top:{top + 14}px">{ico(icn, "sm")}</div>'
              f'<div class="ab" data-s="{s}" style="left:1090px;top:{top + 18}px;width:700px;font-size:17px;font-weight:800;'
              f'color:var(--navy);text-transform:uppercase">{title}</div>')
        if prm:
            h_ += prompt(1090, top + 56, 280, prm, 17, s)
        if items:
            h_ += (f'<div data-s="{s}">' + lst(1385, top + 40, items, 16, 19.5) +
                   f'<div class="ab" style="left:1630px;top:{top + 56}px;width:170px;font-size:13px;letter-spacing:1px;color:var(--dim);'
                   f'text-transform:uppercase;line-height:1.6;border-left:2px solid var(--line);padding-left:12px">{side_t}</div></div>')
        return h_

    o.append(sub(506, 160, "gear", "Конфигурирование интерфейса", "esr(config-if-gi)#",
                 ["channel-group", "do", "ip", "mode", "mtu", "...", "wan"], "Настройка<br>интерфейсов", 4))
    o.append(sub(678, 160, "net", "Конфигурирование маршрутизации", "esr(config-ospf)#",
                 ["area", "do", "enable", "preference", "...", "router-id"], "Настройка<br>протоколов<br>маршрутизации", 5))
    o.append(sub(849, 122, "layers", "Конфигурирование функционала", "", None, "", 6))
    o.append('<div class="ab mono" data-s="6" style="left:1020px;top:906px;width:620px;font-size:17px;font-weight:600;color:var(--navy);'
             'background:rgba(255,255,255,.9);border:1.5px solid var(--line);border-radius:12px;padding:10px 14px;white-space:nowrap">'
             '(config-user)# &nbsp;•&nbsp; (config-gre)# &nbsp;•&nbsp; (config-line-ssh)#</div>')
    o.append('<div class="ab" data-s="6" style="left:1660px;top:895px;width:150px;font-size:13px;color:var(--dim);'
             'letter-spacing:1px;text-transform:uppercase;line-height:1.5;border-left:2px solid var(--line);padding-left:12px">'
             'Настройка дополнительных функций</div>')
    return "".join(o)


SLIDES.append(("p054", "Режимы командной строки", cli_modes()))


# ================================================================ p055 ошибки
def errors():
    o = ['<h1 class="t ab ctr-x" style="top:30px;width:1700px;font-size:58px">Ошибки в командной строке <span class="lt" style="color:var(--navy)">ESR</span></h1>']
    T = ('background:#101c3d;border-radius:12px;padding:16px 18px;font-family:var(--mono);color:#eaf2ff;font-size:19px;line-height:1.5')

    def card(l, cls, bord, icol, name, ru, cause_i, cause, ex1, ex2, fix, s):
        return (f'<div class="card {cls}" data-s="{s}" style="{ab(l, 160, 590)}height:578px;padding:20px 24px;'
                f'border:2px solid {bord}">'
                f'<div style="display:flex;gap:18px;align-items:center">'
                f'<span style="width:84px;height:84px;border-radius:50%;background:{icol};display:grid;place-items:center;flex:none;'
                f'box-shadow:0 8px 20px rgba(0,0,0,.18)"><svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="#fff" '
                f'stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"><path d="M12 3.5l9.5 16.5h-19z"/><path d="M12 10v4.5M12 17.2h.01"/></svg></span>'
                f'<div><div style="font-size:31px;font-weight:800;color:var(--navy);text-transform:uppercase;line-height:1.1">{name}</div>'
                f'<div style="font-size:26px;font-weight:600;color:#5a74b8">{ru}</div></div></div>'
                f'<div class="card solid" style="margin-top:20px;padding:16px 20px;display:flex;gap:18px;align-items:center">{ico(cause_i, "sm")}'
                f'<div><div style="font-size:22px;font-weight:800;color:var(--navy)">Причина:</div>'
                f'<p class="b" style="font-size:19px;line-height:1.3">{cause}</p></div></div>'
                f'<div style="margin-top:16px;font-size:20px;font-weight:800;color:var(--navy)">Пример в командной строке:</div>'
                f'<div style="{T};margin-top:8px"><div>esr# {ex1}</div>'
                f'<div style="margin-top:6px;border:2.5px solid #e53935;padding:5px 10px;border-radius:3px;font-size:18px">Syntax error: {ex2}</div></div>'
                f'<div class="card solid" style="margin-top:16px;padding:16px 20px;display:flex;gap:18px;align-items:center">{ico("wrench", "sm")}'
                f'<div><div style="font-size:22px;font-weight:800;color:var(--navy)">Что исправить:</div>'
                f'<p class="b" style="font-size:19px;line-height:1.3">{fix}</p></div></div></div>')

    o.append(card(38, "cream", "#f2c26b", "linear-gradient(160deg,#ffbf3c,#f08a00)", "Incompleted command", "Незаконченная команда", "doc",
                  "Введены не все ключевые слова или параметры.", "set", "Incompleted command",
                  "Дополнить команду: <b class=\"mono\">set date</b> и указать необходимые параметры.", 1))
    o.append(card(657, "rose", "#f0a7c6", "linear-gradient(160deg,#ff5a6a,#d3173c)", "Unknown command", "Неизвестная команда", "gear",
                  "Командная строка не распознала введённую команду.", "s", "Unknown command",
                  "Проверить написание и ввести полное имя команды.", 2))
    o.append(card(1276, "", "#9cc0f2", "linear-gradient(160deg,#ff5a6a,#d3173c)", "Illegal parameter", "Недопустимый параметр", "list",
                  "Введено значение, которое команда не может принять.", "set date 22:44:33 15 1", "Illegal parameter",
                  "Вместо <b class=\"mono\">1</b> указать название месяца, например <b class=\"mono\">January</b>.", 3))

    o.append('<div class="card ab" data-s="4" style="left:38px;top:757px;width:1843px;height:290px"></div>')
    o.append('<div class="ab" data-s="4" style="left:100px;top:775px;font-size:33px;font-weight:800;color:var(--navy);'
             'text-transform:uppercase">Как обрабатывается команда</div>')
    steps = [("doc", "1.", "Ввод команды"), ("reload", "2.", "Нажатие Enter"), ("search", "3.", "Анализ слева направо"),
             ("gear", "4.", "Проверка синтаксиса"), ("check", "5.", "Выполнение или сообщение об ошибке")]
    xs = [255, 585, 935, 1285, 1640]
    for i, ((ic, n, t), x) in enumerate(zip(steps, xs)):
        o.append(f'<div class="ab" data-s="{5 + i}" style="left:{x - 150}px;top:830px;width:300px;text-align:center">'
                 f'<div style="display:flex;justify-content:center">{ico(ic)}</div>'
                 f'<p class="b" style="font-size:19px;margin-top:12px;color:var(--navy)"><b>{n}</b> {t}</p></div>')
    o.append(layer(*[arrow_svg(xs[i] + 90, 870, xs[i + 1] - 100, 870, 6 + i) for i in range(4)]))
    o.append('<div class="note ab ctr-x" data-s="10" style="top:965px;width:1250px;font-size:20px;padding:12px 22px">' + ico("info", "sm") +
             '<p class="b" style="font-size:20px;align-self:center">Если команда распознана, она выполняется, затем командная '
             'строка ожидает следующий ввод.</p></div>')
    return "".join(o)


SLIDES.append(("p055", "Ошибки в командной строке ESR", errors()))


# ================================================================ p056 доступ
def access():
    o = ['<h1 class="t left ab" style="left:60px;top:62px;width:520px;font-size:62px;line-height:1.1">Доступ к сетевому устройству</h1>']
    o.append('<p class="b ab" style="left:80px;top:285px;width:500px;font-size:20.5px;line-height:1.4">Для доступа к сетевому устройству есть '
             'несколько способов подключения: по консольному порту с помощью консольного кабеля и через протоколы удалённого доступа '
             'Telnet или SSH.</p>')
    o.append('<img class="cut ab" data-s="1" src="assets/p056_device.jpg" style="left:595px;top:95px;width:900px">')
    o.append('<div class="card solid ab" data-s="2" style="left:843px;top:105px;width:310px;padding:10px 16px;text-align:center;border-radius:16px">'
             '<p class="b sm" style="font-size:19px;color:var(--navy);line-height:1.25">Порты для подключения<br>(Telnet / SSH)</p></div>')
    o.append('<div class="card solid ab" data-s="3" style="left:1248px;top:150px;width:260px;padding:10px 16px;text-align:center;border-radius:16px">'
             '<p class="b sm" style="font-size:19px;color:var(--navy);line-height:1.25">Консольный порт<br>(Console)</p></div>')
    o.append(layer('<g data-s="2"><path d="M1000 175 L920 300" stroke="var(--blue)" stroke-width="3" fill="none"/><circle cx="920" cy="300" r="8" fill="var(--blue)"/></g>',
                   '<g data-s="3"><path d="M1380 220 L1210 345" stroke="var(--blue)" stroke-width="3" fill="none"/><circle cx="1210" cy="345" r="8" fill="var(--blue)"/></g>'))
    o.append('<div class="card ab" style="left:1610px;top:63px;width:275px;height:272px;padding:12px 22px">'
             + "".join(f'<div style="display:flex;gap:14px;align-items:center;height:62px">{ico(i, "sm")}'
                       f'<span style="font-size:15px;letter-spacing:1px;color:var(--dim);text-transform:uppercase">{t}</span></div>'
                       for i, t in [("gear", "Настройка"), ("shield", "Управление"), ("chart", "Мониторинг"), ("wrench", "Обслуживание")])
             + '</div>')

    def col(l, w, n, title, sub, art, items, s):
        h = (f'<div class="card" data-s="{s}" style="{ab(l, 418, w)}height:625px;padding:16px 22px">'
             f'<div style="display:flex;gap:18px;align-items:center">'
             f'<span class="num" style="font-size:54px;color:#a9c0ea">{n}</span>'
             f'<div style="font-size:35px;font-weight:800;color:var(--navy);text-transform:uppercase;line-height:1.05;flex:1">{title}</div>'
             f'<div style="font-size:15px;color:var(--dim);text-align:left;width:130px;line-height:1.3">{sub}</div></div>'
             f'<div style="height:160px;margin-top:6px;position:relative">{art}</div>')
        for ic, t in items:
            h += (f'<div style="display:flex;gap:14px;align-items:center;margin-top:8px">{ico(ic, "sm")}'
                  f'<p class="b" style="font-size:15.5px;line-height:1.22;flex:1">{t}</p></div>')
        return h + '</div>'

    def term(txt):
        return ('<div class="ab" style="left:0;top:10px;width:290px;height:140px;border-radius:12px;background:#fff;border:2px solid var(--line);'
                'box-shadow:var(--sh);padding:14px 14px"><div class="mono" style="font-size:14px;color:var(--navy);line-height:1.4">'
                + txt + '</div></div>')

    art1 = '<img class="ph ab" src="assets/p056_console.jpg" style="left:2px;top:10px;width:380px">'
    art2 = (term("C:\\&gt; telnet 192.168.1.1<br><span style='color:var(--blue)'>_</span>") +
            '<div class="ab" style="left:290px;top:60px;width:92px;height:50px;border-radius:25px;background:rgba(255,255,255,.8);'
            'border:1.5px solid var(--line);display:grid;place-items:center;font-weight:700;color:var(--navy)">TCP</div>'
            '<div class="ab" style="left:400px;top:50px;text-align:center">' + ico("globe") +
            '<div style="font-weight:700;font-size:16px;color:var(--navy);margin-top:6px">Telnet<br>(порт 23)</div></div>')
    art3 = (term("C:\\&gt; ssh admin@192.168.1.1<br><span style='color:var(--blue)'>_</span>") +
            '<div class="ab" style="left:300px;top:55px">' + ico("lock") + '</div>'
            '<div class="ab" style="left:400px;top:50px;text-align:center">' + ico("globe") +
            '<div style="font-weight:700;font-size:16px;color:var(--navy);margin-top:6px">SSH<br>(порт 22)</div></div>')
    o.append(col(47, 590, "01", "Консольное<br>подключение", "Консольный порт<br>(Console)", art1, [
        ("gear", "Консольный порт (Console) — это интерфейс управления устройством, использует внеполосный доступ подключения."),
        ("layers", "Внеполосный доступ (out-of-band) — доступ к устройству через специальный выделенный канал, предназначенный только для администрирования и технического обслуживания устройства."),
        ("doc", "Позволяет выполнить первоначальное конфигурирование или может быть единственным способом доступа, если доступ по протоколам удалённого подключения невозможен или запрещён."),
        ("check", "Консольное подключение не зависит от наличия каких-либо настроек на сетевом устройстве.")], 4))
    o.append(col(657, 602, "02", "Telnet", "Удалённый незащищённый доступ", art2, [
        ("mon", "Telnet — это протокол для установления удалённого незащищённого подключения к интерфейсу командной строки (CLI)."),
        ("link", "Подключение по Telnet считается внутриполосным доступом (in-band) — через общий канал."),
        ("flag", "Требует наличия минимум одного настроенного IP-адреса и включения возможности использования протокола Telnet на сетевом устройстве (<span class=\"mono\">ip telnet server</span>)."),
        ("gear", "Если необходимо использовать нестандартный номер порта, то используется команда <span class=\"mono\">ip telnet port</span>."),
        ("shield", "В случае маршрутизатора дополнительно необходима настройка правил разрешения межсетевого экрана для Telnet и настройка взаимодействия между зонами безопасности либо отключение межсетевого экрана на интерфейсе.")], 5))
    o.append(col(1276, 602, "03", "SSH", "Удалённый защищённый доступ", art3, [
        ("mon", "SSH (Secure Shell) — это протокол для установления удалённого защищённого внутриполосного подключения к интерфейсу CLI сетевого устройства."),
        ("lock", "Защищённое подключение возможно благодаря использованию аутентификации на основе пароля и шифрования данных пользователя, но это несёт дополнительную нагрузку на сетевое устройство и канал."),
        ("flag", "Требует наличия минимум одного настроенного IP-адреса и включения возможности использования протокола SSH на сетевом устройстве (<span class=\"mono\">ip ssh server</span>)."),
        ("gear", "Если необходимо использовать нестандартный номер порта, то используется команда <span class=\"mono\">ip ssh port</span>."),
        ("shield", "В случае маршрутизатора дополнительно необходима настройка правил разрешения межсетевого экрана для SSH и настройка взаимодействия между зонами безопасности либо отключение межсетевого экрана на интерфейсе.")], 6))
    return "".join(o)


SLIDES.append(("p056", "Доступ к сетевому устройству", access()))


# ================================================================ p057 индустриальные
def industrial():
    o = ['<h1 class="t ab ctr-x" style="top:16px;width:1700px;font-size:58px">Индустриальные коммутаторы</h1>']
    feats = [(384, "temp", "Широкий диапазон температур"), (661, "shield", "Прочный корпус"), (960, "chart", "Защита от ЭМП"),
             (1248, "bolt", "Защита от скачков"), (1532, "clock", "Надёжность 24/7")]
    for i, (cx, ic, t) in enumerate(feats):
        o.append(f'<div class="ab" data-s="1" style="left:{cx - 140}px;top:108px;width:280px;text-align:center;--dl:{i * 80}ms">'
                 f'<div style="display:flex;justify-content:center">{ico(ic)}</div>'
                 f'<div style="font-size:17px;letter-spacing:.5px;text-transform:uppercase;color:var(--navy);margin-top:6px;line-height:1.2">{t}</div></div>')
    lab = 'text-align:center;font-size:31px;font-weight:800;color:var(--navy)'
    o.append('<div class="card ab" data-s="2" style="left:47px;top:267px;width:849px;height:490px"></div>')
    o.append('<img class="cut ab" data-s="2" src="assets/p057_mes3510.jpg" style="left:100px;top:360px;width:740px">')
    o.append(f'<div class="ab mono" data-s="2" style="left:47px;top:690px;width:849px;{lab}">MES3510DS-24F</div>')
    o.append('<div class="card ab" data-s="3" style="left:921px;top:267px;width:476px;height:490px"></div>')
    o.append('<img class="cut ab" data-s="3" src="assets/p057_mes3500.jpg" style="left:1055px;top:290px;width:210px">')
    o.append(f'<div class="ab mono" data-s="3" style="left:921px;top:700px;width:476px;{lab}">MES3500I-8P8F</div>')
    o.append('<div class="card ab" data-s="4" style="left:1418px;top:267px;width:459px;height:490px"></div>')
    o.append('<img class="cut ab" data-s="4" src="assets/p057_mes3710.jpg" style="left:1565px;top:300px;width:180px">')
    o.append(f'<div class="ab mono" data-s="4" style="left:1418px;top:700px;width:459px;{lab}">MES3710P</div>')
    o.append('<div class="card ab" data-s="5" style="left:47px;top:779px;width:1830px;height:276px"></div>')
    o.append('<div class="ab" data-s="5" style="left:47px;top:796px;width:1830px;text-align:center;font-size:27px;font-weight:800;'
             'color:var(--navy);text-transform:uppercase">Сеть промышленного объекта</div>')
    o.append('<img class="cut ab" data-s="5" src="assets/p057_factory.jpg" style="left:130px;top:845px;width:460px">')
    o.append('<img class="cut ab" data-s="6" src="assets/p057_din.jpg" style="left:880px;top:860px;width:170px">')
    o.append('<img class="cut ab" data-s="7" src="assets/p057_cams.jpg" style="left:1570px;top:830px;width:150px">')
    o.append(layer(line_svg(610, 935, 870, 935, 6), line_svg(1060, 935, 1560, 935, 7)))
    o.append('<div class="ab" data-s="6" style="left:620px;top:900px;font-size:19px;font-weight:600;color:var(--navy)">Ethernet</div>')
    o.append('<div class="ab" data-s="7" style="left:1230px;top:900px;font-size:19px;font-weight:600;color:var(--navy)">Ethernet</div>')
    return "".join(o)


SLIDES.append(("p057", "Индустриальные коммутаторы", industrial()))


# ================================================================ p058 IP на MES
def mes_ip():
    o = ['<h1 class="t ab ctr-x" style="top:42px;width:1800px;font-size:60px">Настройка IP-адреса на интерфейсе <span style="color:var(--navy)">MES</span></h1>']
    CODE = 'font-family:var(--mono);font-weight:600;color:var(--navy);font-size:21px'

    def card(l, w, n, title, txt, code, abbr, icn, s):
        h = (f'<div class="card" data-s="{s}" style="{ab(l, 166, w)}height:453px;padding:20px 24px">'
             f'<div style="display:flex;justify-content:space-between;align-items:flex-start">'
             f'<span style="font-size:84px;font-weight:800;color:#8aa6dc;line-height:1;font-family:var(--mono)">{n}</span>{ico(icn)}</div>'
             f'<div style="{NAVY};font-size:28px;line-height:1.15;margin-top:12px;min-height:64px">{title}</div>'
             f'<p class="b" style="font-size:18px;line-height:1.3;margin-top:12px;min-height:50px">{txt}</p>'
             f'<div class="card solid" style="margin-top:14px;padding:12px 14px;border-radius:12px"><div style="{CODE}">{code}</div></div>')
        if abbr:
            h += (f'<div class="card solid" style="margin-top:12px;padding:8px 14px;border-radius:12px"><span style="font-size:18px;color:var(--dim)">'
                  f'Сокращённо:</span> <b style="{CODE};font-size:20px"> {abbr}</b></div>')
        return h + '</div>'

    B = '<b style="color:var(--blue)">'
    o.append(card(38, 457, "01", "Привилегированный режим", "Переход в режим глобальной конфигурации", f"console# {B}config</b>", "", "term", 1))
    o.append(card(523, 448, "02", "Создание VLAN", "Создание VLAN 10", f"console(config)# {B}vlan 10</b>", "", "db", 2))
    o.append(card(988, 445, "03", "Выбор интерфейса VLAN", "Переход в режим настройки интерфейса VLAN 10",
                  f"console(config)# {B}interface vlan 10</b>", "int vl 10", "gear", 3))
    o.append(card(1455, 429, "04", "Назначение IP-адреса", "Назначение IP-адреса с префиксом /24",
                  f"console(config-if)# {B}ip address 10.0.0.1/24</b>", "ip add 10.0.0.1/24", "net", 4))
    o.append(layer(*[f'<polygon data-s="{s}" points="{x},548 {x + 26},573 {x},598 {x + 4},573" fill="var(--blue)"/>'
                     for s, x in [(2, 500), (3, 965), (4, 1432)]]))

    lines = [("Login: ", "admin"), ("Password: ", "admin"), ("console# ", "config"), ("console(config)# ", "vlan 10"),
             ("console(config)# ", "interface vlan 10"), ("console(config-if)# ", "ip address 10.0.0.1/24")]
    t = ('<div class="ab" data-s="5" style="left:111px;top:725px;width:1698px;height:270px;border-radius:20px;background:#0f1d4a;'
         'box-shadow:0 14px 34px rgba(16,37,90,.35);border:2px solid #3a63c9;overflow:hidden">'
         '<div style="height:50px;background:#16285f;display:flex;align-items:center;justify-content:space-between;padding:0 30px">'
         '<span style="font-size:17px;letter-spacing:3px;color:#cfdcff;text-transform:uppercase">Конфигурация в командной строке</span>'
         '<span style="display:flex;gap:12px">' + "".join('<i style="width:16px;height:16px;border-radius:50%;background:#5b8cff;display:block"></i>' for _ in range(3)) +
         '</span></div><div class="mono" style="position:absolute;left:120px;top:64px;font-size:24px;line-height:1.3;color:#dbe7ff">'
         + "<br>".join(f'{a}<b style="color:#6fa8ff">{b}</b>' for a, b in lines) + '</div>'
         '<div class="mono" style="position:absolute;left:30px;top:70px;font-size:34px;color:#8fb0f5">&gt;_</div></div>')
    o.append(t)
    o.append('<div class="card solid ab ctr-x" data-s="6" style="top:1008px;width:640px;height:60px;display:flex;gap:16px;align-items:center;'
             'justify-content:center;padding:0;border-radius:16px">' + ico("net", "sm") +
             '<span style="font-size:22px;color:var(--navy)">IP-адрес интерфейса: </span>'
             '<b class="mono" style="font-size:27px;color:var(--blue)">10.0.0.1/24</b></div>')
    return "".join(o)


SLIDES.append(("p058", "Настройка IP-адреса на интерфейсе MES", mes_ip()))


# .card задаёт position:relative и перебивает .ab, поэтому для "card ab" добавляем position:absolute инлайном
import re as _re


def _fix_abs(html):
    def rep(m):
        cls = m.group(1)
        if "card" in cls.split() and "ab" in cls.split():
            return m.group(0) + "position:absolute;"
        return m.group(0)
    return _re.sub(r'class="([^"]*)"(?: data-s="\d+")? style="', rep, html)


SLIDES[:] = [(r, l, _fix_abs(h)) for r, l, h in SLIDES]
