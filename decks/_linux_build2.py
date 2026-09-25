# -*- coding: utf-8 -*-
# Часть 2: команды терминала и права доступа (pptx 17–37). Выполняется из _linux_build.py.

def cmd_top(d, right, extra_left="", cls="tl2"):
    """Шапка командного слайда: слева заголовок, вводный текст, синтаксис; справа иллюстрация/схема."""
    left = header(d) + (P(d["intro"]) if d.get("intro") else "") + extra_left
    return f'<div class="{cls} ctop"><div class="col">{left}</div><div class="col">{right}</div></div>'

def steps_row(items, arrows=True, cls=None):
    cols = cls or {2: "g2", 3: "g3", 4: "g4", 5: "g5"}.get(len(items), "g3")
    out = []
    for it in items:
        body = f'<div class="stp">{circle(it.get("n", "").lstrip("0") or it.get("n"))}<div><h3>{rich(it.get("title"))}</h3>' + (f'<p>{rich(it.get("text"))}</p>' if it.get("text") else "") + '</div></div>'
        if it.get("terminal"): body += term(it["terminal"])
        if it.get("note") and not it["note"].startswith("as printed") and not it["note"].startswith("prompt"):
            body += f'<div class="foot"><span class="bigic">{icon_for(it.get("icon"), "check")}</span><div>{rich(it["note"])}</div></div>'
        out.append(card(body, cls="stepc"))
    return f'<div class="{cols} mt {"chev" if arrows else ""}">{"".join(out)}</div>'

def sec(t):
    return f'<h3 class="sec" data-s="1">{rich(t)}</h3>'

def cards_row(bs, cols=None):
    cols = cols or {2: "g2", 3: "g3", 4: "g4", 5: "g5"}.get(len(bs), "g3")
    return f'<div class="{cols}">' + "".join(render_card(b) for b in bs) + '</div>'

def bottom(*items):
    return '<div class="bot mt">' + "".join(items) + '</div>'

def fig(src, cls=""):
    return f'<img class="fg {cls}" src="{src}" alt="" decoding="async">'

# =============================================================== 17. pwd / ls / cd
d14 = load(14); b14 = d14["blocks"]
slide("pwd, ls, cd", '<div class="tl2 ctop"><div class="col">' + header(d14)
    + P("Команды для навигации по файловой системе: где я нахожусь, что лежит в папке и как перейти в другую.", cls="p lg") + '</div>' + art(CR(14, 0, 760), "soft") + '</div>'
    + '<div class="g3">' + render_card(b14[0]) + render_card(b14[1])
    + card(f'<p class="t">{rich(b14[2]["text"])}</p>' + art(CR(14, 1, 420), "sm soft"), b14[2]["num"], b14[2]["title"], b14[2]["sub"], big=True) + '</div>'
    + steps_row(b14[3]["items"]), "dense")

# =============================================================== 18. cd по полному пути
d15 = load(15); b15 = d15["blocks"]
def node(src, name, path, hot=False):
    return f'<div class="fnode {"hot" if hot else ""}" data-s="1">{fig(src)}<b>{name}</b><span>{path}</span></div>'
nav = ('<div class="navf">' + node(CR(15, 0, 200), "Home", "/home/kali") + '<i class="fa"></i>' + node(CR(15, 1, 200), "User", "/home/kali")
       + '<i class="fa br"></i><div class="fcol">' + node(CR(15, 2, 200), "Desktop", "/home/kali/Desktop") + node(CR(15, 3, 200), "Downloads", "/home/kali/Downloads")
       + node(CR(15, 4, 200), "Documents", "/home/kali/Documents", True) + '</div></div>')
slide("cd: переход по пути", cmd_top(d15, nav, P("Представьте, что вы сообщаете кому-то полный адрес, чтобы найти свой дом. Точно так же вы можете указать полный путь к папке. Например, вам нужно перейти в папку «Документы» из домашнего каталога.")
    + syntax([("Синтаксис:", "cd", "[directory path]"), ("Пример:", "cd", "/home/username/documents")]), "two")
    + steps_row(b15[1]["items"]) + '<div class="mt">' + info(b15[2]["text"]) + '</div>', "dense")

# =============================================================== 19. mkdir / rmdir
d16 = load(16); b16 = d16["blocks"]
def half_head(b, tag="TERMINAL"):
    t = b["title"].replace("<o>КОМАНДА</o> ", "")
    return head([("КОМАНДА", "o"), (t, "w l")], b.get("sub"), tag)
slide("mkdir", '<div class="tl2 ctop"><div class="col">' + half_head(b16[0]) + P(b16[0]["text"]) + syntax([tuple(r) for r in b16[1]["rows"]]) + '</div>'
    + art(CR(16, 0, 420), "soft") + '</div>' + steps_row(b16[2]["items"]), "dense")
slide("rmdir", '<div class="tl2 ctop"><div class="col">' + half_head(b16[3]) + P(b16[3]["text"]) + syntax([tuple(r) for r in b16[4]["rows"]]) + '</div>'
    + art(CR(16, 1, 420), "soft") + '</div>' + steps_row(b16[5]["items"]) + '<div class="mt">' + info(b16[6]["text"], "w") + '</div>', "dense")

# =============================================================== 20–21. cp / mv — анимация переноса файла
def move_scene(n, a, f, b, la, pa, lb, pb, copy):
    return (f'<div class="mvs {"cp" if copy else "mv"}" data-s="1">'
            f'<div class="mvn">{fig(CR(n, a, 260))}<b>{la}</b><span>{pa}</span></div>'
            f'<div class="mvn mid"><span class="mvghost">{fig(CR(n, f, 160))}</span><span class="mvfile">{fig(CR(n, f, 160))}</span><b>image.jpg</b><svg class="mvarc" viewBox="0 0 300 60" preserveAspectRatio="none"><path d="M10 55 Q150 -25 290 55"/></svg></div>'
            f'<div class="mvn">{fig(CR(n, b, 260))}<b>{lb}</b><span>{pb}</span></div></div>')
d17 = load(17); b17 = d17["blocks"]
slide("cp", cmd_top(d17, info(b17[1]["text"]) + move_scene(17, 0, 1, 2, "Downloads", "~/Downloads", "Pictures", "~/Pictures", True), syntax([tuple(r) for r in b17[0]["rows"]]))
    + steps_row(b17[3]["items"]) + '<div class="mt">' + info(b17[4]["text"]) + '</div>', "dense")
d18 = load(18); b18 = d18["blocks"]
slide("mv", cmd_top(d18, info(b18[1]["text"]) + move_scene(18, 0, 1, 2, "Downloads", "~/Downloads", "Documents", "~/Documents", False), syntax([tuple(r) for r in b18[0]["rows"]]))
    + steps_row(b18[3]["items"]), "dense")

# =============================================================== 22. cat
d19 = load(19); b19 = d19["blocks"]
slide("cat", cmd_top(d19, '<div class="catv">' + art(CR(19, 0, 520), "soft") + art(CR(19, 1, 260), "sm soft") + '</div>' + info(b19[1]["text"]), syntax([tuple(r) for r in b19[0]["rows"]]))
    + steps_row(b19[2]["items"], False, "g3") + '<div class="mt">' + info(b19[3]["text"]) + '</div>', "dense")

# =============================================================== 23. rm — файл уезжает в корзину
d20 = load(20); b20 = d20["blocks"]
rm_scene = (f'<div class="rms" data-s="1"><div class="rmf">{fig(CR(20, 0, 260))}<b>demo.txt</b></div><i class="rma"></i>'
            f'<div class="rmt">{fig(CR(20, 1, 260))}</div></div>')
slide("rm", cmd_top(d20, info(b20[1]["text"], "w") + rm_scene, syntax([tuple(r) for r in b20[0]["rows"]]))
    + steps_row(b20[3]["items"]) + '<div class="mt">' + info(b20[4]["text"]) + '</div>', "dense")

# =============================================================== 24. uname / locate
d21 = load(21); b21 = d21["blocks"]
slide("uname", '<div class="tl2 ctop"><div class="col">' + half_head(b21[0]) + P(b21[0]["text"]) + syntax([tuple(r) for r in b21[1]["rows"]]) + '</div>'
    + art(CR(21, 0, 520), "soft") + '</div>' + sec(b21[2]["title"]) + steps_row(b21[2]["items"], False) + '<div class="mt">' + info(b21[3]["text"]) + '</div>', "dense")
slide("locate", '<div class="tl2 ctop"><div class="col">' + half_head(b21[4]) + P(b21[4]["text"]) + syntax([tuple(r) for r in b21[5]["rows"]]) + '</div>'
    + art(CR(21, 1, 560), "soft") + '</div>' + sec(b21[6]["title"]) + steps_row(b21[6]["items"], False) + '<div class="mt">' + info(b21[7]["text"]) + '</div>', "dense")

# =============================================================== 25. touch
d22 = load(22); b22 = d22["blocks"]
slide("touch", cmd_top(d22, art(crop("image22.png", load(22)["art"][0]["bbox"], 700, erase=[(1100, 95, 1445, 262)]), "") + '<div class="g2">' + info(b22[1]["text"]) + info(b22[2]["text"], "q") + '</div>', syntax([tuple(r) for r in b22[0]["rows"]]))
    + sec("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ") + cards_row(b22[4:8]) + '<div class="mt">' + info(b22[8]["text"]) + '</div>', "dense")

# =============================================================== 26. ln — схема ссылок
d23 = load(23); b23 = d23["blocks"]
ln_d = ('<div class="lnd" data-s="1"><div class="lnf src">' + ICON["file"] + '<b>file1.txt</b></div>'
        '<svg class="lna" viewBox="0 0 300 200" preserveAspectRatio="none"><path class="h" d="M5 100 C120 100 150 40 295 40"/><path class="s" d="M5 100 C120 100 150 160 295 160"/></svg>'
        '<div class="lnr"><div class="lnf">' + ICON["file"] + '<b>hardlink.txt</b><span><b class="o">Жесткая ссылка</b><br>(указатель на тот же файл)</span></div>'
        '<div class="lnf">' + ICON["link"] + '<b>symlink.txt</b><span><b class="o">Символическая ссылка</b><br>(ссылка на путь к файлу)</span></div></div></div>')
slide("ln", cmd_top(d23, ln_d + '<div class="g2">' + info(b23[2]["text"]) + info(b23[3]["text"], "q") + '</div>', syntax([tuple(r) for r in b23[0]["rows"]]))
    + '<div class="mt">' + cards_row(b23[4:8]) + '</div><div class="mt">' + info(b23[8]["text"]) + '</div>', "dense")

# =============================================================== 27. clear — до / после
d24 = load(24); b24 = d24["blocks"]
clr = ('<div class="clr" data-s="1">' + term(b24[3]["terminal"], "до") + '<div class="clra"><code>clear</code><i></i></div>'
       + term(b24[4]["terminal"], "после") + '</div>')
slide("clear", cmd_top(d24, clr + '<div class="clrw">' + info(b24[1]["text"]) + art(CR(24, 0, 300), "xs soft") + '</div>', syntax([tuple(r) for r in b24[0]["rows"]]), "two")
    + sec("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ") + cards_row(b24[6:9]) + bottom(info(b24[9]["text"]), info(b24[10]["text"], "q")), "dense")

# =============================================================== 28. grep
d25 = load(25); b25 = d25["blocks"]
slide("grep", cmd_top(d25, art(CR(25, 0, 620), "soft") + '<div class="g2">' + info(b25[2]["text"], "q") + info(b25[3]["text"]) + '</div>',
    syntax([tuple(r) for r in b25[0]["rows"]]) + term(b25[1]["terminal"], "grep", "big-t"), "two")
    + sec("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ") + cards_row(b25[5:10]) + bottom(info(b25[10]["text"]), info(b25[11]["text"], "q")), "dense")

# =============================================================== 29. echo
d26 = load(26); b26 = d26["blocks"]
slide("echo", cmd_top(d26, '<div class="echo">' + term(b26[1]["terminal"], "echo", "big-t") + '<div class="bub" data-s="1"><b>Hello<br>Linux!</b></div>' + art(CR(26, 0, 520), "sm soft") + '</div>',
    syntax([tuple(r) for r in b26[0]["rows"]]))
    + sec("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ") + cards_row(b26[4:9]) + bottom(info(b26[9]["text"]), info(b26[10]["text"], "q")), "dense")

# =============================================================== 30. sort / wc
d27 = load(27); b27 = d27["blocks"]
UNS = ["banana", "apple", "cherry", "date", "fig"]; SRT = sorted(UNS)
sort_d = ('<div class="srt" data-s="1"><div class="doc">' + "".join(f'<span style="--from:{UNS.index(w)};--to:{SRT.index(w)}">{w}</span>' for w in UNS)
          + '</div><i class="fa"></i><div class="doc res">' + "".join(f'<span style="--i:{i}">{w}</span>' for i, w in enumerate(SRT)) + '</div></div>'
          '<p class="dim cap" data-s="1">После сортировки строки упорядочены по алфавиту.</p>')
def feats(items, icons):
    return '<div class="feats">' + "".join(f'<div class="ft" data-s="1">{ICON[i]}<span>{t.split("] ", 1)[1]}</span></div>' for t, i in zip(items, icons)) + '</div>'
intro_sort, intro_wc = d27["intro"].split("||")
slide("sort", '<div class="tl2 ctop"><div class="col">' + head([("КОМАНДА", "o"), ("sort", "w l")], "(сортировка содержимого файлов)", "TERMINAL") + P(intro_sort.strip())
    + syntax([tuple(r) for r in b27[1]["rows"]]) + '</div><div class="col">' + sort_d + '</div></div>'
    + sec("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ") + cards_row(b27[4:7]) + feats(b27[7]["items"], ["list", "gear", "bolt"]), "dense")
wc_stats = '<div class="wcs" data-s="1">' + "".join(f'<div><span>{k}</span><b>{v}</b></div>' for k, v in b27[10]["rows"]) + '</div>'
slide("wc", '<div class="tl2 ctop"><div class="col">' + head([("КОМАНДА", "o"), ("wc", "w l")], "(подсчёт строк, слов и байтов)", "TERMINAL") + P(intro_wc.strip())
    + syntax([tuple(r) for r in b27[9]["rows"]]) + P("Также можно использовать: <c>wc -m test.txt</c> — опция <c>-m</c> отображает количество символов.") + '</div><div class="col">'
    + '<div class="wcv">' + art(CR(27, 0, 260), "sm soft") + wc_stats + '</div>' + art(CR(27, 1, 420), "sm soft") + '</div></div>'
    + sec("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ") + cards_row(b27[12:16], "g4") + feats(b27[16]["items"], ["file", "list", "check"])
    + bottom(info(b27[17]["text"]), info(b27[18]["text"], "q")), "dense")

# =============================================================== 31. wget
d28 = load(28); b28 = d28["blocks"]
wg = ('<div class="wg" data-s="1"><div class="wgn"><span class="wgg">' + ICON["globe"] + '<em>https://</em></span><b>Интернет (URL)</b></div>'
      '<svg class="wga" viewBox="0 0 300 80" preserveAspectRatio="none"><path d="M5 60 Q150 -20 295 50"/><circle r="6"/></svg>'
      '<div class="wgn"><span class="wgg">' + ICON["file"] + '<i>' + ICON["download"] + '</i></span><b>файл загружен</b></div></div>')
opts = card(render_table({"head": ["Опция", "Назначение"], "rows": [[r[0], r[1].lstrip("— ")] for r in b28[8]["rows"]]}), None, "ПОЛЕЗНЫЕ ОПЦИИ")
slide("wget", cmd_top(d28, '<div class="tr2">' + wg + art(CR(28, 0, 520), "soft") + '</div>' + info(b28[2]["text"], "q"), syntax([tuple(r) for r in b28[0]["rows"]]))
    + sec("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ") + cards_row(b28[4:8], "g4 wgc") + '<div class="g3 mt">' + opts
    + card(bullets(b28[9]["items"], "sm"), None, b28[9]["title"]) + info(b28[10]["text"], "q") + '</div>', "dense")

# =============================================================== 32. Разрешения
d32 = load(32); b32 = d32["blocks"]
slide("Разрешения: основы", head([("РАЗРЕШЕНИЯ", "o"), ("В LINUX", "w")], "Кто и что может делать с файлом", "LINUX")
    + sec("Три основных типа разрешений") + '<div class="g3">' + "".join(card(f'<div class="bigic">{ICON[i]}</div><h3>{a}</h3><p class="t sm">{b}</p>') for i, a, b in [
        ("eye", "Чтение (r)", "Просмотр содержимого файла или списка файлов в каталоге."),
        ("pen", "Запись (w)", "Изменение файла или управление файлами в каталоге."),
        ("gear", "Выполнение (x)", "Запуск файла как программы или вход в каталог.")]) + '</div>'
    + sec("Группы владельцев и разрешений") + P("Разрешения назначаются трём категориям пользователей:") + '<div class="g3">' + "".join(card(f'<div class="bigic">{ICON[i]}</div><h3>{a}</h3><p class="t sm">{b}</p>') for i, a, b in [
        ("user", "Пользователь (владелец)", "Тот, кто создал файл."),
        ("users", "Группа", "Пользователи, входящие в общую группу (например, «developers»)."),
        ("globe", "Остальные", "Все остальные пользователи системы.")]) + '</div>'
    + sec("Права доступа к файлу: схема действий") + render_table(load(31)["blocks"][0]))
ops_tbl = render_table(b32[10])
slide("Права доступа: схема", '<div class="tr2"><div class="col">' + header(d32) + P(d32["intro"]) + art(CR(32, 0, 520), "") + '</div><div class="col">'
    + sec(b32[1]["title"]) + cards_row(b32[2:5]) + sec(b32[5]["title"]) + P(b32[5]["items"][0]) + cards_row(b32[6:9])
    + sec(b32[9]["title"]) + '<div class="g2">' + ops_tbl + '<div class="col">' + term([{"p": "kali@kali:~$", "cmd": "chmod u+x file.txt"}], cls="big-t")
    + info("Пример: добавить право на выполнение для владельца файла") + '</div></div></div></div>'
    + '<div class="mt">' + info(b32[13]["text"], "q") + '</div>', "dense")

# =============================================================== 33. rwx: девять символов
d33 = load(33); b33 = d33["blocks"]
def permrow(s, file=None, labels=True):
    cls = ["ft"] + ["u"] * 3 + ["g"] * 3 + ["ot"] * 3
    boxes = "".join(f'<span class="{c}" style="--i:{i}">{ch}</span>' for i, (c, ch) in enumerate(zip(cls, s)))
    lab = ('<div class="braces"><span></span><span><b>u</b>Пользователь (владелец)</span><span><b>g</b>Группа</span><span><b>o</b>Остальные</span></div>' if labels else "")
    f = f'<span class="pf">{file}</span>' if file else ""
    return f'<div class="permw" data-s="1"><div class="perm">{boxes}{f}</div>{lab}</div>'
slide("Группы разрешений", head([("ГРУППЫ", "o"), ("РАЗРЕШЕНИЙ", "w")], "Девять символов rwx", "LINUX")
    + P("Разрешения представлены девятью символами. Каждый из трёх символов «<o>rwx</o>» обозначает отдельную операцию, которую можно выполнить с файлом.", cls="p lg")
    + '<div class="card hot mt">' + permrow("-rwxrwxrwx") + '</div>'
    + '<div class="g3 mt">' + "".join(card(f'<div class="rwx">{ICON[i]}<b>{L}</b></div><h3>{t}</h3><p class="t sm">{rich(x)}</p>') for i, L, t, x in [
        ("user", "rwx", "user", "права владельца файла"), ("users", "rwx", "group", "права группы файла"), ("globe", "rwx", "other", "права всех остальных")]) + '</div>')
slide("Структура прав доступа", '<div class="tr2"><div class="col">' + header(d33) + P(d33["intro"]) + '</div><div class="card hot">'
    + f'<h3 class="sec" style="margin-top:0"><b class="o">ДЕВЯТЬ СИМВОЛОВ</b> РАЗРЕШЕНИЙ</h3>' + permrow("-rwxrwxrwx") + '<div class="mt">' + card(bullets(b33[1]["items"], "sm"), None, rich(b33[1]["title"])) + '</div></div></div>'
    + sec(b33[2]["title"]) + '<div class="g3">' + "".join(card(f'<div class="rwx">{icon_for(b.get("icon"))}<b>{b["num"]}</b></div><h3>{b["title"]}</h3><p class="t sm">{rich(b["text"])}</p>' + info(b["info"])) for b in b33[3:6]) + '</div>'
    + '<div class="tl2 mt"><div class="col">' + sec(b33[6]["title"]) + render_table(b33[7]) + '</div><div class="col">' + sec("<o>ПРИМЕР</o>")
    + '<div class="term" data-s="1"><div class="tbar"><i></i><i></i><i></i></div><div class="tbody">' + permrow("-rwxr-xr--", "file.txt", False)
    + '<div class="braces sm"><span></span><span><b>u</b>rwx</span><span><b>g</b>r-x</span><span><b>o</b>r--</span></div></div></div>' + info(b33[9]["text"]) + '</div></div>', "dense")

# =============================================================== 34. ls -l
d34 = load(34); b34 = d34["blocks"]
TOK = [("-", 1), ("rw-r--r--", 2), ("1", 3), ("user", 4), ("group", 5), ("46", 6), ("Apr 14 16:37", 7), ("NarX.txt", 8)]
toks = '<div class="toks" data-s="1">' + "".join(f'<div class="tk" style="--i:{i}"><span class="cn">{n}</span><code>{t}</code></div>' for i, (t, n) in enumerate(TOK)) + '</div>'
slide("ls -l: пример из лекции", head([("ВХОДНЫЕ И ВЫХОДНЫЕ", "w"), ("ДАННЫЕ", "o")], "Имя файла по умолчанию — «NarX»", "TERMINAL")
    + two('<div class="col">' + syntax([("Входные данные:", "ls -l", "NarX.txt"), ("Выходные данные:", "-rw-r--r--", "1 user group 46 Apr 14 16:37 NarX.txt")])
          + term([{"p": "kali@kali:~$", "cmd": "ls -l NarX.txt"}, {"out": "-rw-r--r-- 1 user group 46 Apr 14 16:37 NarX.txt"}], cls="big-t") + '</div>',
          card(bullets(["Первый символ '<o>-</o>' указывает на файл, а '<o>d</o>' — на каталог.",
                        "Следующие девять символов (<o>rw-r--r--</o>) показывают права доступа.",
                        "В следующем столбце указан владелец файла.",
                        "В следующем столбце указан владелец из группы (у которой есть специальный доступ к этим файлам).",
                        "В следующем столбце указан размер файла в байтах.",
                        "В следующем столбце указаны дата и время последнего изменения файла."]), None, "Приведённая выше команда содержит следующую информацию")))
slide("ls -l: разбор вывода", cmd_top(d34, '<div class="tl2">' + '<div class="col">' + term(b34[1]["terminal"], "ls -l", "big-t") + info(b34[2]["text"], "q") + '</div>' + art(CR(34, 0, 300), "sm soft") + '</div>',
    syntax([tuple(r) for r in b34[0]["rows"]]), "two")
    + sec("РАЗБОР ВЫВОДА КОМАНДЫ") + toks + '<div class="g4 mt">' + "".join(
        card(f'<div class="stp">{circle(b["num"])}<div><h3>{b["title"]}</h3><p>{rich(b.get("text"))}</p></div></div>' + (bullets(b["bullets"], "sm") if b.get("bullets") else "")
             + f'<span class="bigic cr">{icon_for(b.get("icon"), "file")}</span>') for b in b34[4:12]) + '</div>'
    + bottom(card(bullets(b34[12]["items"], "sm"), None, b34[12]["title"]), info(b34[13]["text"], "q")), "dense")

# =============================================================== 35. chmod
d35 = load(35); b35 = d35["blocks"]
slide("chmod: пошагово", head([("ИЗМЕНЕНИЕ", "w"), ("ПРАВ ДОСТУПА", "o")], "К файлу в Linux", "TERMINAL") + two(
    P("Если вы хотите предоставить пользователю <o>world</o> (то есть всем остальным) разрешение на выполнение файла <c>xyz.txt</c>, начните с ввода следующей команды.")
    + '<div class="build" data-s="1">' + "".join(f'<div class="bl" style="--i:{i}"><code>{c}</code><span>{t}</span></div>' for i, (c, t) in enumerate([
        ("chmod o", "кому: остальные (others)"), ("chmod o+", "«+» — добавляем разрешение"), ("chmod o+x", "«x» — разрешение «выполнять»"), ("chmod o+x xyz.txt", "имя файла")])) + '</div>',
    P("Вы также можете изменить сразу несколько разрешений. Например, чтобы убрать все права, введите команду:")
    + term([{"p": "kali@kali:~$", "cmd": "chmod ugo-rwx xyz.txt"}, {"p": "kali@kali:~$", "cmd": "ls -l xyz.txt"}, {"out": "---------- 1 user group 46 Apr 14 16:37 xyz.txt"}], cls="big-t")
    + info("Приведённый выше код отменяет все разрешения на чтение (<o>r</o>), запись (<o>w</o>) и выполнение (<o>x</o>) для всех пользователей (<o>u</o>), групп (<o>g</o>) и других лиц (<o>o</o>) для файла <c>xyz.txt</c>, в результате чего файл становится недоступным.")))
st35 = b35[3]["items"]; st35[2]["terminal"][1]["out"] = "-rw-r--r-x 1 user  group  46"
slide("chmod: инфографика", cmd_top(d35, '<div class="tl2">' + term(b35[1]["terminal"], "chmod", "big-t") + '<div class="col">' + art(CR(35, 0, 360), "sm soft") + info(b35[2]["text"], "q") + '</div></div>',
    syntax([("Синтаксис:", "chmod", "[OPTIONS] file_name"), ("Пример:", "chmod", "o+x xyz.txt")]), "two")
    + sec(b35[3]["title"]) + steps_row(st35, False, "g5"), "dense")
slide("chmod: обозначения", head([("CHMOD:", "o"), ("СИМВОЛЫ И ЧИСЛА", "w")], "Кто, что и как", "TERMINAL")
    + '<div class="g3">' + "".join(card(bullets(b35[k]["items"]), None, rich(b35[k]["title"].split(" / ")[-1])) for k in (4, 5, 6)) + '</div>'
    + '<div class="two mt"><div class="col">' + sec("ПРИМЕРЫ КОМАНД") + render_table(b35[9]) + '</div><div class="col">' + sec("ЧИСЛОВОЙ ФОРМАТ ПРАВ")
    + render_table(b35[11]) + card(bullets(b35[12]["items"], "sm"), None, rich(b35[12]["title"])) + '</div></div>'
    + bottom(card(bullets(b35[13]["items"], "sm"), None, "ПОЛЕЗНО ЗНАТЬ"), info(b35[14]["text"], "q")))

# =============================================================== 36. примеры chmod
d36 = load(36); b36 = d36["blocks"]
def ex36(c, dg, tb, fname, ic):
    L_ = dg["labels"]
    brk = (f'<div class="brk"><div class="bg"><em>{L_[0]}</em><div><span>{ICON["user"]}<b>u</b>{L_[2]}</span><span>{ICON["users"]}<b>g</b>{L_[4]}</span></div></div>'
           f'<div class="bg"><em>{L_[5]}</em><div><span>{ICON["globe"]}<b>o</b>{L_[7]}</span></div></div></div>')
    fc = card(f'<div class="fi">{ICON[ic]}<h3 class="mono">{fname}</h3></div>' + '<div class="meta">' + "".join(f'<div><span>{a}</span><b>{b}</b></div>' for a, b in tb["rows"]) + '</div>', cls="flat")
    cmd = c["terminal"][0]["cmd"].replace("<o>", "").replace("</o>", "")
    return card(f'<p class="t">{rich(c["text"])}</p><div class="tl2"><div class="col">' + term([{"p": "kali@kali:~$", "cmd": cmd}], cls="big-t") + brk + '</div>' + fc + '</div>', c["num"], c["title"])
slide("chmod: примеры", '<div class="tr2"><div class="col">' + header(d36) + P(d36["intro"]) + info(b36[0]["text"], "q") + art(CR(36, 0, 420), "sm soft") + '</div><div class="col">'
    + ex36(b36[1], b36[2], b36[3], "abc.mp4", "play") + ex36(b36[4], b36[5], b36[6], "abc.c", "code") + '</div></div>', "dense")

# =============================================================== 37. восьмеричная запись + тренажёр
d38 = load(38); b38 = d38["blocks"]
slide("Восьмеричные обозначения", '<div class="tl2 ctop"><div class="col">' + header(d38) + P(d38["intro"]) + '</div><div class="col">' + art(CR(38, 0, 360), "sm soft") + info(b38[0]["text"], "q") + '</div></div>'
    + '<div class="tl2"><div class="col">' + render_table(b38[1]) + '</div><div class="col">' + card(P(b38[2]["items"][0], cls="t") + "".join(
        f'<div class="fi">{icon_for(b.get("icon"), "user")}<div><h3>{rich(b["title"])}</h3><p class="t sm">{rich(b["text"])}</p></div></div>' for b in b38[3:6]), None, rich(b38[2]["title"]))
    + card(P(b38[6]["text"], cls="t") + term([{"p": "kali@kali:~$", "cmd": "chmod 644 file.txt"}]), None, "<o>Пример</o>") + '</div></div>'
    + '<div class="mt">' + info(b38[7]["text"]) + '</div>', "dense")

slide("Тренажёр chmod", head([("ТРЕНАЖЁР", "o"), ("CHMOD", "w")], "Отметьте права — получите команду", "TERMINAL") + two(
    '<div class="card hot"><div class="calc" id="calc">'
    '<span></span><span class="hd">r (4)</span><span class="hd">w (2)</span><span class="hd">x (1)</span>'
    + "".join(f'<span class="rl">{who}</span>' + "".join(f'<label><input type="checkbox" data-w="{k}" data-b="{b}" aria-label="{who} {n}" {"checked" if (k, b) in {(0,4),(0,2),(0,1),(1,4),(1,1),(2,4)} else ""}></label>' for b, n in ((4, "чтение"), (2, "запись"), (1, "выполнение")))
              for k, who in enumerate(("u — владелец", "g — группа", "o — остальные")))
    + '</div><div class="cres"><b id="c-oct">754</b><span id="c-sym">-rwxr-xr--</span></div></div>',
    term([{"p": "kali@kali:~$", "cmd": "chmod 754 file.txt"}], cls="big-t calc-t") + '<div id="c-expl" class="info" data-s="1"><span class="ii">i</span><div></div></div>'
    + '<div class="trow" data-s="1">' + "".join(f'<button class="btn" type="button" data-oct="{o}">{o}</button>' for o in ("644", "755", "700", "600", "777", "000")) + '</div>'))

# =============================================================== тест
QUIZ = [
    {"q": "Какая команда показывает текущий рабочий каталог?", "o": ["ls", "pwd", "cd", "whoami"], "a": 1, "e": "pwd — print working directory, например /home/kali/Templates."},
    {"q": "Что сделает команда rmdir, если каталог не пустой?", "o": ["Удалит каталог вместе с файлами", "Не удалит: rmdir удаляет только пустые каталоги", "Переместит файлы в корзину", "Переименует каталог"], "a": 1, "e": "rmdir удаляет только пустые каталоги; для каталога с файлами используют rm -r."},
    {"q": "Чем mv отличается от cp?", "o": ["Ничем", "mv перемещает — оригинала в исходной папке больше нет", "mv копирует только каталоги", "mv работает только с картинками"], "a": 1, "e": "cp оставляет оригинал, mv переносит (или переименовывает) файл."},
    {"q": "Какая команда создаёт пустой файл test.txt?", "o": ["cat test.txt", "touch test.txt", "mkdir test.txt", "echo test.txt"], "a": 1, "e": "touch создаёт пустой файл или обновляет его временные метки."},
    {"q": "Где хранятся конфигурационные файлы системы?", "o": ["/home", "/etc", "/tmp", "/proc"], "a": 1, "e": "/etc — настройки системы и служб: fstab, hosts, passwd, resolv.conf…"},
    {"q": "Что означает запись -rw-r--r-- ?", "o": ["Каталог, все права у всех", "Файл: владелец читает и пишет, группа и остальные только читают", "Файл: только выполнение", "Символическая ссылка"], "a": 1, "e": "«-» — обычный файл; rw- владелец; r-- группа; r-- остальные."},
    {"q": "Какой восьмеричный код соответствует rwxr-xr-x?", "o": ["644", "755", "777", "700"], "a": 1, "e": "rwx = 4+2+1 = 7, r-x = 4+1 = 5 → 755."},
    {"q": "Что делает chmod o+x xyz.txt?", "o": ["Убирает выполнение у владельца", "Добавляет право выполнения остальным пользователям", "Даёт все права группе", "Удаляет файл"], "a": 1, "e": "o — остальные (others), + — добавить, x — выполнение."},
    {"q": "Как найти строки со словом Python в notes.txt без учёта регистра?", "o": ["grep Python notes.txt", "grep -i \"python\" notes.txt", "find -i python", "cat -i notes.txt"], "a": 1, "e": "Опция -i отключает учёт регистра."},
]
slide("Проверь себя", head([("ПРОВЕРЬ", "o"), ("СЕБЯ", "w")], "Короткий тест по лекции", "LINUX") + '<div class="tl2"><div class="card quiz">'
    '<div class="qtop"><span id="qz-n">1 / 9</span><span id="qz-sc">верно: 0</span></div><div class="tq" id="qz-q"></div>'
    '<div class="opts" id="qz-o"></div><div class="tres" id="qz-e" aria-live="polite"></div>'
    '<div class="trow"><button class="btn" id="qz-pv" type="button">Предыдущий</button><button class="btn pri" id="qz-nx" type="button">Следующий вопрос</button></div></div>'
    + art(CR(13, 0, 460), "sm") + '</div>')

# =============================================================== финал
slide("Спасибо за внимание", f"""
<div class="title fin">
  <div>
    <span class="tag" data-s="1">LINUX</span>
    <h1 data-s="1">Спасибо<br>за <span class="o">внимание</span></h1>
    {term([{"p": "kali@kali:~$", "cmd": "exit"}, {"out": "logout"}], cls="big-t")}
    <p class="authors mt2" data-s="1">Ананко Софья Михайловна<br>Качур Анна Юрьевна</p>
  </div>
  {art(CR(32, 0, 700), "lg")}
</div>""", "tslide")

EXTRA_JS = r"""
(function(){
  var box=$('#calc'); if(!box) return;
  var names=[['чтение','запись','выполнение'],'владелец','группа','остальные'];
  function upd(){
    var d=[0,0,0]; $$('input',box).forEach(function(c){ if(c.checked) d[+c.dataset.w]+=+c.dataset.b; });
    var sym='-'+d.map(function(v){return (v&4?'r':'-')+(v&2?'w':'-')+(v&1?'x':'-')}).join('');
    var oct=d.join(''); $('#c-oct').textContent=oct; $('#c-sym').textContent=sym;
    var t=$('.calc-t .ty'); t.innerHTML='<span class="tc">chmod</span> <span class="tf">'+oct+'</span> <span class="ta">file.txt</span>';
    var who=['владелец','группа','остальные'];
    $('#c-expl div').textContent=d.map(function(v,i){ var p=[]; if(v&4)p.push('чтение'); if(v&2)p.push('запись'); if(v&1)p.push('выполнение');
      return who[i]+': '+(p.length?p.join(', '):'нет прав')+' ('+v+')'; }).join('; ')+'.';
  }
  $$('input',box).forEach(function(c){ c.addEventListener('change',upd); });
  $$('[data-oct]').forEach(function(b){ b.onclick=function(){ var o=b.dataset.oct;
    $$('input',box).forEach(function(c){ c.checked=!!(+o[+c.dataset.w] & +c.dataset.b); }); upd(); }; });
  upd();
})();
(function(){
  var Q=__QUIZ__, i=0, got=Q.map(function(){return -1}); if(!$('#qz-q')) return;
  function sc(){ return got.filter(function(g,k){return g===Q[k].a}).length; }
  function render(){ var q=Q[i]; $('#qz-n').textContent=(i+1)+' / '+Q.length; $('#qz-q').textContent=q.q;
    var o=$('#qz-o'); o.innerHTML=''; var e=$('#qz-e'); e.textContent=''; e.className='tres';
    q.o.forEach(function(t,k){ var b=document.createElement('button'); b.type='button'; b.className='opt'; b.textContent=t; b.onclick=function(){ if(got[i]<0) got[i]=k; show(); }; o.appendChild(b); });
    if(got[i]>=0) show(); $('#qz-sc').textContent='верно: '+sc(); $('#qz-pv').disabled=i===0; $('#qz-nx').textContent=i===Q.length-1?'Начать заново':'Следующий вопрос'; }
  function show(){ var q=Q[i], bs=$$('.opt',$('#qz-o')); bs[q.a].classList.add('ok'); if(got[i]!==q.a) bs[got[i]].classList.add('no');
    var e=$('#qz-e'); e.textContent=(got[i]===q.a?'Верно. ':'Неверно. ')+q.e; e.className='tres '+(got[i]===q.a?'ok':'no'); $('#qz-sc').textContent='верно: '+sc(); }
  $('#qz-nx').onclick=function(){ if(i===Q.length-1){ got=Q.map(function(){return -1}); i=0; } else i++; render(); };
  $('#qz-pv').onclick=function(){ if(i>0){ i--; render(); } };
  render();
})();
""".replace("__QUIZ__", json.dumps(QUIZ, ensure_ascii=False))

L.CSS += (HERE / "_lx_extra.css").read_text(encoding="utf-8")
render(OUT, "Linux: дистрибутивы и работа в терминале", EXTRA_JS)
