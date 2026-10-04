# -*- coding: utf-8 -*-
"""Слайды по референсам p001-p018 (режимы CLI, документация, горячие клавиши, панели)."""
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


def svg_lbl(x, y, t, s, anchor="middle"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" data-s="{s}" font-family="var(--mono)" '
            f'font-size="27" font-weight="600" fill="var(--navy)">{t}</text>')


# ======================================================= режимы CLI (p001/p016)
def modes(title, prompts, fn_cmd, cards, warn=None):
    o = [f'<h1 class="t ab ctr-x" style="top:34px;width:1560px">{title}</h1>']

    def box(top, name, cmd, cls, s):
        return (f'<div class="card {cls}" data-s="{s}" style="{ab(300, top, 860)}padding:20px 26px;text-align:center">'
                f'<div style="font-size:31px;font-weight:800;color:var(--navy);text-transform:uppercase">{name}</div>'
                f'<div class="chip mono" style="margin-top:12px;font-size:29px;color:var(--blue);'
                f'border-color:rgba(120,160,230,.5)">{cmd}</div></div>')

    names = ["Пользовательский режим", "Привилегированный режим",
             "Режим глобального конфигурирования", "Режим конфигурирования функционала"]
    for i, (name, cmd, cls) in enumerate(zip(names, prompts, ["solid", "cream", "mint", "solid"])):
        o.append(box(140 + i * 240, name, cmd, cls, 1 + i * 2))

    top = 150
    for j, (cmd, txt) in enumerate(cards):
        o.append(f'<div class="card" data-s="{2 + j * 3}" style="{ab(1320, top, 540)}display:flex;gap:20px;'
                 f'align-items:flex-start;padding:22px 26px">{ico("term", "sm")}<div>'
                 f'<div class="mono" style="font-size:32px;font-weight:700;color:var(--navy)">{cmd}</div>'
                 f'<p class="b sm dim" style="margin-top:8px">{txt}</p></div></div>')
        top += 230
    if warn:
        o.append(f'<div class="card" data-s="8" style="{ab(1320, top, 540)}display:flex;gap:20px;'
                 f'align-items:center;padding:22px 26px">{ico("warn", "sm")}'
                 f'<p class="b sm">{warn}</p></div>')

    parts = []
    for (y0, y1, down, s_down, s_up) in [(272, 376, "enable", 2, 3), (512, 616, "config", 4, 5),
                                         (752, 856, fn_cmd, 6, 7)]:
        parts += [arrow_svg(560, y0, 560, y1, s_down), svg_lbl(470, (y0 + y1) / 2 + 10, down, s_down, "end"),
                  arrow_svg(860, y1, 860, y0, s_up), svg_lbl(900, (y0 + y1) / 2 + 10, "exit", s_up, "start")]
    parts += ['<path class="dr" data-s="8" pathLength="1" d="M1130 856 L1130 500" stroke="var(--blue)" '
              'stroke-width="4" fill="none"/>', arrow_svg(1130, 500, 1130, 470, 8),
              svg_lbl(1175, 690, "end", 8, "start")]
    o.append(layer(*parts))
    return "".join(o)


SLIDES.append(("p001", "Навигация между режимами (ESR)", modes(
    "Навигация между режимами",
    ["esr&gt;", "esr#", "esr(config)#", "esr(config-if-gi)#"], "int gi &lt;num&gt;",
    [("enable", "Переход из пользовательского режима в привилегированный"),
     ("exit", "Выход на один уровень назад; в привилегированном режиме закрывает сеанс"),
     ("end", "Переход из любого режима сразу в привилегированный")],
    warn="Для команды <b class=\"mono\">enable</b> необходимо назначить пароль")))

SLIDES.append(("p016", "Переключение между режимами (MES)", modes(
    "Переключение между режимами",
    ["console&gt;", "console#", "console(config)#", "console(config-if)#"], "int vlan &lt;num&gt;",
    [("enable", "Переход из пользовательского режима в привилегированный. Для команды необходимо назначить пароль."),
     ("exit", "Выход на один уровень назад. В привилегированном режиме закрывает сеанс."),
     ("end", "Переход из любого режима сразу в привилегированный.")])))


# ======================================================= документация (p002)
def docs():
    o = ['<div class="tag ab ctr-x" style="top:30px;border-radius:30px">Официальные материалы Элтекс</div>',
         '<h1 class="t ab ctr-x" style="top:92px;width:1600px">Документация для маршрутизаторов <span class="lt">ESR</span></h1>']

    def pdf_ico(l, t):
        return (f'<div class="ab" style="left:{l}px;top:{t}px;width:96px;height:112px;border-radius:14px;'
                f'background:linear-gradient(160deg,#4a86ff,#2a4fd0);box-shadow:0 10px 24px rgba(40,80,190,.3)">'
                f'<div style="position:absolute;right:0;top:0;width:30px;height:30px;background:#c9ddff;'
                f'clip-path:polygon(100% 0,0 0,100% 100%)"></div>'
                f'<div class="mono" style="position:absolute;left:0;right:0;bottom:16px;text-align:center;'
                f'color:#fff;font-weight:800;font-size:20px">PDF</div></div>')

    def block(l, cover, title, feats, url, s, extra_mid=""):
        h = [f'<div class="card ab" data-s="{s}" style="{ab(l, 230, 830)}height:620px;padding:34px 36px">',
             f'<img class="ph ab" src="assets/{cover}" style="left:36px;top:34px;width:300px">',
             pdf_ico(l0 := 380, 34),
             f'<div class="ab" style="left:500px;top:34px;width:290px;font-size:34px;font-weight:800;'
             f'color:var(--navy);text-transform:uppercase;line-height:1.15">{title}</div>',
             f'<div class="tag ab" style="left:500px;top:150px;font-size:21px;padding:7px 18px">Версия 1.40</div>']
        y = 230
        for icn, txt in feats:
            h.append(f'<div class="ab" style="left:380px;top:{y}px;width:420px;display:flex;gap:16px;align-items:center">'
                     f'{ico(icn, "sm")}<p class="b sm">{txt}</p></div>')
            y += 86
        h.append(extra_mid)
        h.append('<div class="ab" style="left:36px;top:430px;width:300px;display:flex;gap:12px;align-items:center;'
                 'justify-content:center">' + ico("doc", "sm") + '<span class="b sm">PDF, бесплатно</span></div>')
        h.append(f'<div class="ab mono" style="left:36px;top:510px;width:760px;background:rgba(255,255,255,.85);'
                 f'border:1.5px solid var(--line);border-radius:14px;padding:14px 18px;font-size:19px;'
                 f'color:var(--dim);text-align:center">{url}</div>')
        h.append('</div>')
        return "".join(h)

    ctrl_f = ('<div class="ab" style="left:380px;top:430px;width:420px;display:flex;gap:14px;align-items:center;'
              'justify-content:center">'
              '<span class="chip key" style="font-size:26px;padding:14px 22px">CTRL</span>'
              '<span style="font-size:26px;color:var(--dim)">+</span>'
              '<span class="chip key" style="font-size:26px;padding:14px 26px">F</span>'
              '<span class="b sm dim">Поиск по документу</span></div>')

    o.append(block(80, "p002_cli_cover.jpg", "Справочник команд CLI",
                   [("term", "Полный синтаксис команд"), ("gear", "Параметры и ключевые слова")],
                   "eltex.ru/storage/upload_center/files/16/ESR-Series_CLI_1.40.pdf", 1, ctrl_f))
    o.append(block(990, "p002_man_cover.jpg", "Руководство по эксплуатации",
                   [("gear", "Минимальные настройки технологий и протоколов"), ("list", "Пошаговые примеры конфигурации")],
                   "eltex.ru/storage/upload_center/files/52/ESR-Series_User_manual_1.40.pdf", 2))
    return "".join(o)


SLIDES.append(("p002", "Документация для маршрутизаторов ESR", docs()))


# ======================================================= горячие клавиши MES (p003)
def hotkeys_mes():
    o = ['<h1 class="t ab ctr-x" style="top:34px;width:1700px">Горячие клавиши и быстрые команды <span class="lt">MES</span></h1>',
         '<div class="ch ab" style="left:90px;top:130px;font-size:34px">Горячие клавиши</div>']
    left = [("A", "Вернуться к началу строки."), ("E", "Вернуться к концу строки."),
            ("F", "Продвинуться вперёд на один символ."), ("B", "Продвинуться назад на один символ."),
            ("D", "Удалить данный символ."), ("U, X", "Удалить начало строки до символа.")]
    right = [("K", "Удалить конец строки до символа."), ("W", "Удалить предыдущее слово."),
             ("T", "Переместить предыдущий символ."), ("P", "Перейти к предыдущей строке в истории команд."),
             ("N", "Перейти к следующей строке в истории команд."), ("Z", "Возврат к корневому режиму CLI.")]

    def row(l, t, key, txt, s):
        return (f'<div class="ab" data-s="{s}" style="{ab(l, t, 860)}display:flex;gap:16px;align-items:center">'
                f'<span class="chip key" style="font-size:24px;padding:12px 20px">Ctrl</span>'
                f'<span style="font-size:24px;color:var(--dim)">+</span>'
                f'<span class="chip key" style="font-size:24px;padding:12px 22px;min-width:64px">{key}</span>'
                f'<span style="width:2px;height:34px;background:var(--line)"></span>'
                f'<p class="b sm" style="flex:1">{txt}</p></div>')

    for i, (k, t) in enumerate(left):
        o.append(row(90, 200 + i * 78, k, t, 1))
    for i, (k, t) in enumerate(right):
        o.append(row(980, 200 + i * 78, k, t, 2))

    def card(l, icn, title, body, s, cls="card"):
        return (f'<div class="{cls}" data-s="{s}" style="{ab(l, 700, 560)}height:300px">'
                f'<div style="display:flex;gap:16px;align-items:center;margin-bottom:16px">{ico(icn, "sm")}'
                f'<div style="font-size:28px;font-weight:800;color:var(--navy);text-transform:uppercase">{title}</div></div>'
                f'{body}</div>')

    o.append(card(90, "gear", "Привилегированный режим",
                  '<p class="b sm">Команды диагностики, мониторинга и очистки процессов выполняются из привилегированного режима.</p>'
                  '<p class="b sm dim" style="margin-top:14px">Примеры команд:</p>'
                  '<div style="display:flex;gap:12px;margin-top:10px;flex-wrap:wrap">'
                  + "".join(f'<span class="chip mono" style="font-size:21px;padding:8px 16px">{c}</span>'
                            for c in ["ping", "traceroute", "show", "clear"]) + '</div>', 3))
    o.append(card(680, "term", "Ключ do",
                  '<p class="b sm">Ключ <b class="mono">do</b> ставится перед командой и позволяет выполнить '
                  'привилегированную команду из любого режима.</p>'
                  '<p class="b sm dim" style="margin-top:14px">Примеры:</p>'
                  '<div class="mono" style="font-size:20px;line-height:1.6;margin-top:8px;color:var(--navy)">'
                  'console(config)# <b style="color:var(--blue)">do show interfaces</b><br>'
                  'console(config-if)# <b style="color:var(--blue)">do ping 10.0.0.1</b></div>', 4))
    o.append(card(1270, "warn", "Исключение",
                  '<p class="b sm">Команды <b class="mono">dir</b> и <b class="mono">copy</b> не работают с ключом '
                  '<b class="mono">do</b>. Они выполняются только из привилегированного режима.</p>', 5, "card rose"))
    return "".join(o)


SLIDES.append(("p003", "Горячие клавиши и быстрые команды MES", hotkeys_mes()))


# ======================================================= горячие клавиши ESR (p006)
def hotkeys_esr():
    o = ['<h1 class="t ab ctr-x" style="top:34px;width:1700px">Горячие клавиши и быстрые команды <span class="lt">ESR</span></h1>']

    o.append(f'<div class="card" data-s="1" style="{ab(80, 140, 860)}height:380px">'
             '<div class="ch">Сокращение команд</div>'
             '<div style="display:flex;gap:18px;align-items:center">'
             '<div class="card solid" style="flex:1;padding:18px 22px">'
             '<div class="b sm dim" style="margin-bottom:10px">Полная команда</div>'
             '<div class="mono" style="font-size:23px;color:var(--navy)">esr(config)# interface<br>gigabitethernet 1/0/1</div></div>'
             + '<svg width="70" height="40" style="overflow:visible">' + arrow_svg(0, 20, 56, 20, 1, col="var(--blue)") + '</svg>'
             + '<div class="card solid" style="flex:1;padding:18px 22px">'
             '<div class="b sm dim" style="margin-bottom:10px">Сокращённая команда</div>'
             '<div class="mono" style="font-size:23px;color:var(--navy)">esr(config)# int gi 1/0/1</div></div></div>'
             '<div class="note" style="margin-top:24px">' + ico("info", "sm") +
             '<p class="b sm">Сокращение допустимо, если командная строка однозначно распознаёт команду.</p></div></div>')

    keys = [("Tab", "", "Завершает частично набранную команду или ключевое слово"),
            ("Ctrl", "Z", "Выход из режима конфигурации в привилегированный режим; аналог команды end"),
            ("Ctrl", "C", "Прерывает текущую команду"),
            ("Ctrl", "N", "Листает историю команд вперёд"),
            ("Ctrl", "P", "Листает историю команд назад")]
    o.append(f'<div class="card" data-s="2" style="{ab(980, 140, 860)}height:380px">'
             '<div class="ch">Горячие клавиши</div>'
             + "".join(
                 f'<div style="display:flex;gap:14px;align-items:center;margin-bottom:14px">'
                 + (f'<span class="chip key" style="font-size:22px;padding:10px 18px">{a}</span>'
                    f'<span style="font-size:22px;color:var(--dim)">+</span>'
                    f'<span class="chip key" style="font-size:22px;padding:10px 20px">{b}</span>' if b else
                    f'<span class="chip key" style="font-size:22px;padding:10px 26px">{a}</span>'
                    f'<span style="width:118px"></span>')
                 + f'<span style="width:2px;height:30px;background:var(--line)"></span>'
                   f'<p class="b sm" style="flex:1">{t}</p></div>'
                 for a, b, t in keys) + '</div>')

    o.append(f'<div class="card" data-s="3" style="{ab(80, 560, 860)}height:330px">'
             '<div class="ch">История команд</div>'
             '<div class="cmd mono" style="font-size:24px">esr# show history</div>'
             '<p class="b sm" style="margin-top:14px">Показывает список ранее выполненных команд. '
             'По умолчанию хранится 50 команд.</p>'
             '<div class="cmd mono" style="font-size:24px;margin-top:16px">esr(config)# history size [10-1000]</div>'
             '<p class="b sm" style="margin-top:12px">Изменяет размер буфера истории.</p>'
             '<div class="card solid ab" style="left:560px;top:90px;width:270px;padding:18px 20px">'
             '<div class="b sm dim" style="margin-bottom:8px">Пример вывода:</div>'
             '<div class="mono" style="font-size:20px;line-height:1.6;color:var(--navy)">'
             '1&nbsp;&nbsp;config<br>2&nbsp;&nbsp;int gi 1/0/1<br>3&nbsp;&nbsp;end<br>4&nbsp;&nbsp;show history</div></div></div>')

    o.append(f'<div class="card" data-s="4" style="{ab(980, 560, 860)}height:330px">'
             '<div class="ch">Ключ do</div>'
             '<div class="cmd mono" style="font-size:24px">do &lt;команда&gt;</div>'
             '<p class="b sm" style="margin-top:14px">Позволяет запускать команды привилегированного режима из любого режима.</p>'
             '<div class="mono" style="font-size:20px;line-height:1.7;margin-top:14px;color:var(--navy)">'
             'esr(config)# <b style="color:var(--blue)">do show interfaces</b><br>'
             'esr(config-if-gi)# <b style="color:var(--blue)">do ping 10.0.0.1</b></div>'
             '<div class="ab" style="left:560px;top:90px;width:270px">'
             '<div class="b sm dim">Часто используемые команды:</div>'
             '<p class="b sm" style="margin-top:12px">Диагностика: <b class="mono">ping</b>, <b class="mono">traceroute</b></p>'
             '<p class="b sm" style="margin-top:8px">Мониторинг: <b class="mono">show</b></p>'
             '<p class="b sm" style="margin-top:8px">Очистка процессов: <b class="mono">clear</b></p></div></div>')

    o.append(f'<div class="card rose" data-s="5" style="{ab(80, 930, 1760)}display:flex;gap:20px;align-items:center;padding:20px 30px">'
             + ico("warn", "sm") +
             '<div style="font-size:26px;font-weight:800;color:var(--navy);text-transform:uppercase">Исключение</div>'
             '<p class="b sm" style="flex:1">Команды <b class="mono">dir</b> и <b class="mono">copy</b> не работают с ключом '
             '<b class="mono">do</b> и выполняются только из привилегированного режима.</p></div>')
    return "".join(o)


SLIDES.append(("p006", "Горячие клавиши и быстрые команды ESR", hotkeys_esr()))


# ======================================================= контекстная подсказка (p009)
def context_help():
    o = ['<h1 class="t ab ctr-x" style="top:30px;width:1600px">Контекстная подсказка в <span class="lt">CLI</span></h1>',
         f'<div class="card ab ctr-x" style="top:112px;width:900px;display:flex;gap:20px;align-items:center;padding:18px 26px">'
         f'<span class="card solid" style="width:64px;height:64px;display:grid;place-items:center;border-radius:16px;'
         f'font-size:34px;font-weight:800;color:var(--blue)">?</span>'
         f'<div><div style="font-size:27px;font-weight:700;color:var(--navy)">Введите <b class="mono">?</b> в любом месте командной строки</div>'
         f'<p class="b sm dim" style="margin-top:4px">Символ не отображается и Enter нажимать не требуется</p></div></div>']

    def card(l, t, title, cmd, note, cols, s):
        body = "".join(
            f'<div style="flex:1"><div class="mono" style="font-size:21px;line-height:1.7;color:var(--navy)">{c}</div></div>'
            for c in cols)
        return (f'<div class="card" data-s="{s}" style="{ab(l, t, 840)}height:330px">'
                f'<div style="display:flex;gap:18px;align-items:center;margin-bottom:16px">{ico("term", "sm")}'
                f'<div style="font-size:27px;font-weight:800;color:var(--navy);text-transform:uppercase">{title}</div></div>'
                f'<div class="cmd mono" style="font-size:24px">{cmd}</div>'
                f'<p class="b sm dim" style="margin:12px 0 16px">{note}</p>'
                f'<div style="display:flex;gap:30px">{body}</div></div>')

    o.append(card(80, 250, "Список доступных команд", "esr# ?", "Показывает команды, доступные в текущем режиме.",
                  ["boot&nbsp;&nbsp;&nbsp;&nbsp;— загрузка<br>clear&nbsp;&nbsp;&nbsp;— очистка<br>"
                   "commit&nbsp;&nbsp;— применить изменения<br>configure — режим конфигурации",
                   "show&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;— системная информация<br>ssh&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;— SSH-клиент<br>"
                   "traceroute — поиск маршрута"], 1))
    o.append(card(1000, 250, "Поиск по первой букве", "esr# d?", "Показывает команды, начинающиеся с введённой буквы.",
                  ["debug<br>delete<br>dir<br>disable"], 2))
    o.append(card(80, 610, "Подсказка по продолжению команды", "esr# show interfaces ?",
                  "Показывает доступные ключевые слова и параметры.",
                  ["bridge<br>counters<br>description<br>port-channel", "sfp<br>status<br>switch-port"], 3))
    o.append(card(1000, 610, "Поиск созданных объектов", "esr(config)# object-group service ?",
                  "Показывает текстовые переменные и объекты, созданные в системе.",
                  ["any&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;— зарезервировано<br>object1 — созданный объект<br>obtest&nbsp;&nbsp;— созданный объект"], 4))

    steps = [("1", "Введите начало команды"), ("2", "Добавьте <b class=\"mono\">?</b>"), ("3", "Выберите вариант из списка")]
    o.append(f'<div class="card" data-s="5" style="{ab(80, 960, 1760)}display:flex;gap:40px;align-items:center;padding:18px 30px">'
             '<div style="font-size:27px;font-weight:800;color:var(--navy);text-transform:uppercase">Как использовать</div>'
             + "".join(f'<div style="display:flex;gap:14px;align-items:center"><span class="badge">{n}</span>'
                       f'<p class="b sm">{t}</p></div>' for n, t in steps) + '</div>')
    return "".join(o)


SLIDES.append(("p009", "Контекстная подсказка в CLI", context_help()))


# ======================================================= параметры commit (p011)
def commit_params():
    o = ['<h1 class="t ab ctr-x" style="top:34px;width:1600px">Дополнительные параметры <span class="lt">commit</span></h1>',
         '<div class="cmd mono ab ctr-x" data-s="1" style="top:120px;font-size:32px">esr# commit ?</div>']

    def block(l, n, title, cmd, txt, tag, val, icn, s):
        return (f'<div class="card" data-s="{s}" style="{ab(l, 250, 830)}height:560px;padding:34px 38px">'
                f'<div style="display:flex;gap:24px;align-items:center">'
                f'<span class="num" style="font-size:72px">{n}</span>'
                f'<span style="width:2px;height:60px;background:var(--line)"></span>'
                f'<div style="font-size:32px;font-weight:800;color:var(--navy);text-transform:uppercase">{title}</div></div>'
                f'<div class="card solid" style="margin-top:26px;padding:16px 24px;text-align:center">'
                f'<span class="mono" style="font-size:30px;color:var(--navy)">{cmd}</span></div>'
                f'<div style="display:flex;gap:24px;align-items:center;margin-top:26px">{ico(icn)}'
                f'<div style="flex:1"><p class="b sm">{txt}</p>'
                f'<div class="tag" style="margin-top:14px;font-size:21px;padding:8px 18px">{tag}</div></div></div>'
                f'<div class="card solid" style="margin-top:24px;padding:14px 22px">'
                f'<span class="mono" style="font-size:26px;color:var(--navy)">{val}</span></div></div>')

    o.append(block(80, "01", "Комментарий", "commit comment",
                  "Добавляет комментарий к резервной копии конфигурации", "До 31 символа", "WORD(1-31)", "doc", 2))
    o.append(block(1010, "02", "Таймер подтверждения", "commit confirm-timeout",
                  "Задаёт время ожидания команды confirm", "От 120 до 86400 секунд", "120-86400", "clock", 3))

    flow = [("commit", 160), ("ожидание confirm", 700), ("confirm", 1300)]
    o.append(f'<div class="card ab" data-s="4" style="{ab(80, 860, 1760)}height:140px"></div>')
    for i, (t, x) in enumerate(flow):
        sub = '<div class="b sm dim" style="text-align:center">Идёт защитный интервал</div>' if i == 1 else ""
        o.append(f'<div class="ab" data-s="4" style="left:{x}px;top:{895}px;width:460px;text-align:center">'
                 f'<div class="mono" style="font-size:30px;font-weight:700;color:var(--navy)">{t}</div>{sub}</div>')
    o.append(layer(arrow_svg(640, 925, 700, 925, 4), arrow_svg(1180, 925, 1250, 925, 4)))
    return "".join(o)


SLIDES.append(("p011", "Дополнительные параметры commit", commit_params()))
