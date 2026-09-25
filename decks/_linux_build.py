# -*- coding: utf-8 -*-
# Сборка decks/linux-basics.html — «Linux: дистрибутивы и работа в терминале»
# Структура — по linux.pptx (37 слайдов), вёрстка — по инфографикам слайдов.
import _lx_lib as L
from _lx_lib import *
from _lx_info import *
from _lx_info import _ic_key

OUT = HERE / "linux-basics.html"
CR = lambda n, i, w=620: crop(f"image{n}.png", load(n)["art"][i]["bbox"], w)
BLK = lambda n: load(n)["blocks"]

def two(left, right, cls="two"):
    return f'<div class="{cls}"><div class="col">{left}</div><div class="col">{right}</div></div>'

# =============================================================== 1. Титул
slide("Титул", f"""
<div class="title">
  <div>
    <span class="tag" data-s="1">LINUX</span>
    <h1 data-s="1">Работа<br>в <span class="o">Linux</span></h1>
    <p class="lead" data-s="1">Дистрибутивы, файловая система и основные команды терминала</p>
    {term([{"p": "kali@kali:~$", "cmd": "whoami"}, {"out": "student"}, {"p": "kali@kali:~$", "cmd": "echo \"Hello Linux\""}, {"out": "Hello Linux"}], cls="big-t")}
    <p class="authors mt2" data-s="1">Ананко Софья Михайловна<br>Качур Анна Юрьевна</p>
  </div>
  {art(CR(2, 0, 760), "lg")}
</div>""", "tslide")

# =============================================================== 2. Введение
slide("Введение в Linux", head([("ВВЕДЕНИЕ", "w"), ("В LINUX", "o")], "Бесплатная система с открытым исходным кодом", "LINUX") + two(
    P("Linux основан на операционной системе <o>UNIX</o>, многопользовательской и многозадачной платформе, разработанной в 1970-х годах в AT&amp;T Bell Labs, которая стала основой для многих современных операционных систем.",
      "Linux — бесплатная операционная система с <o>открытым исходным кодом</o>, которая способствует глобальному сотрудничеству и инновациям, обеспечивая при этом высокий уровень безопасности, гибкость и надёжную производительность на различных устройствах и в различных отраслях.", cls="p lg"),
    '<div class="g2">' + "".join(card(f'<div class="bigic">{ICON[i]}</div><p class="t">{t}</p>') for i, t in [
        ("shield", "Обеспечивает высокий уровень безопасности и стабильности, что делает её подходящей для серверов и сред разработки."),
        ("code", "Позволяет пользователям свободно использовать, модифицировать и распространять операционную систему."),
        ("gear", "Поддерживает настройку под различные требования пользователей и отраслевые приложения."),
        ("users", "Поддерживается большим глобальным сообществом и широким спектром программных продуктов.")]) + '</div>'))

# =============================================================== 3. Дистрибутивы
d1 = load(1)
DIST_TXT = [("Ubuntu", "удобный для новичков дистрибутив Linux, который используется для настольных компьютеров, серверов и облачных вычислений."),
    ("Debian", "стабильный и надежный дистрибутив Linux, широко используемый для серверов."),
    ("Kali Linux", "дистрибутив Linux, ориентированный на безопасность, который используется для этичного взлома и тестирования на проникновение."),
    ("MX Linux", "легковесный дистрибутив Linux, подходящий для старого оборудования."),
    ("Manjaro", "удобный дистрибутив Linux на основе Arch с непрерывными обновлениями."),
    ("Linux Mint", "простой и удобный для новичков дистрибутив Linux для пользователей Windows."),
    ("Solus", "современный дистрибутив Linux, ориентированный на производительность и простоту работы на настольных компьютерах."),
    ("Fedora", "дистрибутив Linux, ориентированный на разработчиков и использующий новейшие технологии."),
    ("openSUSE", "мощный дистрибутив Linux, используемый для разработки и корпоративных сред."),
    ("Deepin", "визуально привлекательный дистрибутив Linux с простым в использовании интерфейсом.")]
slide("Дистрибутивы: определение", head([("ДИСТРИБУТИВЫ", "w"), ("LINUX", "o")], "Одна идея — разные возможности", "LINUX") +
    P("<o>Дистрибутив Linux</o> (дистрибутив) — это полноценная операционная система, построенная на основе ядра Linux, а также системных инструментов, библиотек и приложений. Различные дистрибутивы предназначены для разных целей, таких как использование на настольных компьютерах, серверах, в сфере кибербезопасности и разработки.", cls="p lg")
    + defs([(a, b) for a, b in DIST_TXT], "words c2"))

def dist_card(i, b):
    lg = f'<figure class="art logo"><img src="{CR(1, i + 1, 200)}" alt="Логотип {b["title"]}"></figure>'
    tg = b.get("tag") or {}
    return card(f'<div class="dhead"><span class="nb">{b["num"]}</span>{lg}</div><h3 class="dn">{b["title"]}</h3><p class="t sm">{rich(b["text"])}</p>'
                f'<div class="pillrow">{tagpill(icon_key(tg.get("icon")), tg.get("text", ""))}</div>', cls="dist")
def icon_key(d): return _ic_key(d)
cards = [b for b in d1["blocks"] if b["type"] == "card"]
slide("Дистрибутивы: 10 систем", '<div class="tl2">' + '<div class="col">' + header(d1) + P(d1["intro"], cls="p") + '</div>'
    + '<div class="col">' + art(CR(1, 0, 760), "") + info("Один Linux — много возможностей!", "q") + '</div></div>'
    + '<div class="g5 mt">' + "".join(dist_card(i, b) for i, b in enumerate(cards)) + '</div>', "dense")

# =============================================================== 4. Архитектура
slide("Архитектура: компоненты", head([("АРХИТЕКТУРА", "o"), ("LINUX", "w")], "Многоуровневая структура операционной системы", "LINUX") + two(
    P("<o>Архитектура Linux</o> — это многоуровневая структура операционной системы Linux, которая определяет, как взаимодействуют такие компоненты, как ядро, оболочка, системные библиотеки и аппаратное обеспечение, для управления ресурсами и эффективного выполнения программ. Она состоит из следующих компонентов:", cls="p lg"),
    defs([("Ядро", "Основной компонент Linux, который управляет аппаратными ресурсами, процессами и системными операциями."),
          ("Системные библиотеки", "Системные библиотеки предоставляют функции, которые помогают приложениям взаимодействовать с ядром Linux."),
          ("Оболочка", "Это интерфейс командной строки, который интерпретирует и выполняет пользовательские команды."),
          ("Аппаратный уровень", "Аппаратный уровень включает в себя физические компоненты, такие как центральный процессор, оперативная память, хранилище и устройства ввода/вывода."),
          ("Системные утилиты", "Системные утилиты — это встроенные инструменты, используемые для управления, настройки и обслуживания системы.")], "words")))

LAYERS = [("user", "Приложения", "Пользователь", ["браузер", "редактор", "IDE"]),
          ("gear", "Системные утилиты", "", ["systemctl", "apt", "top", "ls", "grep", "…"]),
          ("terminal", "Оболочка (Shell)", "", ["bash", "zsh", "sh", "…"]),
          ("disk", "Системные библиотеки", "", ["glibc", "libm", "libpthread", "…"]),
          ("cpu", "Ядро Linux", "", ["Управление процессами", "Управление памятью", "Драйверы", "Системные вызовы", "…"]),
          ("server", "Аппаратный уровень", "", ["ЦПУ", "ОЗУ", "Хранилище", "Устройства ввода/вывода"])]
stack = '<div class="stack">' + "".join(
    (f'<div class="sarrow" data-s="1"><span></span></div>' if i else "") +
    f'<div class="slab s{i}" data-s="1">{ICON[ic]}<div><b>{n}</b><div class="chips">' + "".join(f'<span>{c}</span>' for c in ch) + '</div></div></div>'
    for i, (ic, n, _, ch) in enumerate(LAYERS)) + '</div>'
arch_cards = [b for b in BLK(2) if b["type"] == "card"]
slide("Архитектура: уровни", '<div class="tl2"><div class="col">' + head([("АРХИТЕКТУРА", "o"), ("LINUX", "w")], load(2)["subtitle"]) + '</div>'
    + art(CR(2, 0, 520), "sm") + '</div>' + two(stack, '<div class="col lc">' + "".join(
        card(f'<p class="t sm">{rich(b["text"])}</p>', b["num"], b["title"], cls=f"lc{i}") for i, b in enumerate(arch_cards)) + '</div>', "two arch")
    + '<div class="mt">' + info(BLK(2)[-1]["text"], "q") + '</div>', "dense")

# =============================================================== 5. Приложения
d3 = load(3)
slide("Применение Linux", '<div class="tl2"><div class="col">' + header(d3) + P(d3["intro"], cls="p") + '</div><div class="col">'
    + art(CR(3, 0, 780)) + '</div></div>' + '<div class="g4 mt">' + "".join(
    card(f'<figure class="art cardart"><img src="{CR(3, i + 1, 460)}" alt=""></figure><p class="t sm">{rich(b["text"])}</p>'
         f'<span class="sq">{ICON[_ic_key(b["tag"]["icon"]) if _ic_key(b["tag"]["icon"]) != "dot" else ("server" if i == 5 else "grad")]}</span>',
         b["num"], b["title"], cls="appc") for i, b in enumerate([x for x in d3["blocks"] if x["type"] == "card"]))
    + f'<figure class="art globe" data-s="1"><img src="{CR(3, 8, 360)}" alt=""></figure></div>', "dense")

# =============================================================== 6. VirtualBox
slide("VirtualBox: что это", head([("УСТАНОВКА LINUX", "w"), ("В ВИРТУАЛЬНОЙ МАШИНЕ", "o")], "Oracle VirtualBox", "VIRTUALIZATION") + two(
    P("<o>Oracle VirtualBox</o> — это инструмент виртуализации, который позволяет пользователям запускать другие операционные системы на основной ОС. Например, вы можете установить Ubuntu в своей системе Windows 11 виртуально, с помощью VirtualBox.",
      "Чтобы скачать VirtualBox, перейдите на сайт VirtualBox и выберите версию, подходящую для вашей ОС.", cls="p lg")
    + '<div class="chiprow">' + "".join(tagpill(i, t) for i, t in [("check", "Бесплатно"), ("shield", "Безопасно"), ("gear", "Просто в использовании"), ("list", "Поддержка множества ОС")]) + '</div>',
    art(CR(4, 0, 800))))
d4 = load(4); c4 = [b for b in d4["blocks"] if b["type"] == "card"]
vm_form = ('<div class="vmf"><div><span>Имя:</span><b>Ubuntu</b></div><div><span>Тип:</span><b>Linux ▾</b></div><div><span>Версия:</span><b>Ubuntu (64-bit) ▾</b></div>'
           '<div><span>ОЗУ:</span><i class="bar"><u></u></i><b>4096 МБ</b></div></div>')
vm_list = ('<div class="vml"><div class="on">Ubuntu <em>Работает</em></div><div>Windows 11 <em>Выключена</em></div><div>Kali Linux <em>Выключена</em></div></div>')
dl_mock = '<div class="brow"><span>https://www.virtualbox.org</span></div>'
inst = '<div class="prog"><i style="--w:60%"></i></div><span class="pill sm">Установить</span>'
iso = f'<div class="prog"><i style="--w:50%"></i></div><p class="t sm dim">Установка… Загрузите ISO-образ</p>'
mocks = [dl_mock, inst, vm_form, iso, vm_list]
slide("VirtualBox: пошагово", header(d4) + '<div class="g4 mt">' + "".join(
    card(f'<p class="t sm">{rich(b.get("text"))}</p>{mocks[i] if i < 5 else ""}' + (info(b["info"]) if b.get("info") else "")
         + (bullets([x.rsplit(" (", 1)[0] for x in b["bullets"]], "sm") if b.get("bullets") else ""), b["num"], b["title"])
    for i, b in enumerate(c4)) + f'<div class="col">{art(CR(4, 5, 460), "sm")}{info("Больше чем одна ОС — в одном компьютере!", "q")}</div></div>', "dense")

# =============================================================== 7. Файловая система: 3 уровня
d5 = load(5)
FS3 = [("1. Логическая файловая система", "Обеспечивает простое и единообразное взаимодействие приложений с файлами без необходимости беспокоиться о деталях хранения.", 2),
       ("2. Виртуальная файловая система (VFS)", "Обеспечивает единообразие и совместимость файловых операций независимо от формата базовой файловой системы.", 4),
       ("3. Физическая файловая система", "Обеспечивает надежное хранение данных, обработку ошибок и низкоуровневое управление данными.", 6)]
slide("Файловая система: три уровня", head([("ФАЙЛОВАЯ СИСТЕМА", "w"), ("LINUX", "o")], d5["subtitle"], "LINUX")
    + P("Архитектура файловой системы Linux состоит из трёх важных уровней, каждый из которых отвечает за определённые функции. Эти уровни работают вместе, обеспечивая беспрепятственный доступ к файлам, их хранение и управление ими.", cls="p lg")
    + '<div class="g3">' + "".join(card(f'<p class="t">{t}</p>' + bullets(d5["blocks"][k]["items"], "sm"), None, n, cls="hot" if k == 4 else "")
                                   for n, t, k in FS3) + '</div>')
flow = ('<div class="vfs">'
        '<div class="vbox" data-s="1"><b>Пользовательские приложения</b><div class="tiles">' + "".join(f'<span>{ICON[i]}</span>' for i in ("terminal", "folder", "file", "globe")) + '</div></div>'
        '<div class="ops" data-s="1"><span>Открыть</span><span>Читать</span><span>Записать</span><span>Закрыть</span><i class="pk"></i></div>'
        '<div class="vbox hot" data-s="1"><b class="big">VFS</b><span class="dim">(Virtual File System)</span></div>'
        '<div class="ops arr" data-s="1"><i class="pk d2"></i></div>'
        '<div class="vbox" data-s="1"><b>Конкретные файловые системы</b><div class="fss">' + "".join(f'<span>{x}</span>' for x in ("ext4", "XFS", "Btrfs", "FAT32", "NTFS", "…")) + '</div></div>'
        '<div class="ops arr" data-s="1"><i class="pk d3"></i></div>'
        f'<div class="disk" data-s="1"><img src="{CR(5, 1, 420)}" alt=""><b>Дисковое хранилище</b></div></div>')
slide("Файловая система: схема", '<div class="tl2">' + head([("ФАЙЛОВАЯ СИСТЕМА", "w"), ("LINUX", "o")], d5["subtitle"], "LINUX") + info(d5["blocks"][0]["text"], "q") + '</div>'
    + '<div class="fs3">' + '<div class="col">' + "".join(card(f'<p class="t sm">{rich(b["text"])}</p>', b["num"], b["title"], cls="hot" if b["num"] == "02" else "") for b in d5["blocks"] if b["type"] == "card") + '</div>'
    + flow + '<div class="col">' + "".join(card(bullets(d5["blocks"][k]["items"], "sm"), cls="hot" if k == 4 else "") for k in (2, 4, 6)) + '</div></div>'
    + '<div class="fsfoot" data-s="1"><span>FILES / SYSTEM / LINUX</span><span>НАДЁЖНОСТЬ • ГИБКОСТЬ • СВОБОДА</span></div>', "dense")

# =============================================================== 8. Характеристики ФС
d6 = load(6); c6 = [b for b in d6["blocks"] if b["type"] == "card"]
slide("Характеристики ФС", head([("ХАРАКТЕРИСТИКИ", "w"), ("ФАЙЛОВОЙ СИСТЕМЫ", "o")], "Файловая система Linux", "LINUX")
    + P("Файловая система определяет структуру, правила и методы организации, хранения, доступа и управления данными на устройстве хранения.", cls="p lg")
    + defs([("Управление пространством", "управляет распределением блоков, отслеживанием свободного пространства и контролем фрагментации для оптимизации эффективности хранения."),
            ("Имя файла", "обеспечивает соблюдение правил именования, включая наборы символов, ограничения по длине и чувствительность к регистру для идентификации файлов."),
            ("Каталог", "реализует иерархические структуры индексирования для эффективной организации и поиска файлов."),
            ("Метаданные", "хранят атрибуты файлов, такие как информация о владельце, разрешениях, временных метках, размере и типе файла."),
            ("Утилиты", "обеспечивают операции системного уровня для создания, удаления, резервного копирования, восстановления файлов и управления доступом к ним."),
            ("Архитектура", "определяет архитектурные ограничения и механизмы, которые влияют на масштабируемость, надёжность и производительность файловой системы.")], "words"))
meta = '<div class="meta">' + "".join(f'<div><span>{k}</span><b>{v}</b></div>' for k, v in d6["blocks"][5]["rows"]) + '</div>'
ART6 = {0: 1, 1: 2, 2: 3, 5: 4}
def c6card(i, b):
    extra = meta if i == 3 else (f'<figure class="art mini"><img src="{CR(6, ART6[i], 260)}" alt=""></figure>' if i in ART6 else
            '<div class="btn4">' + "".join(f'<span>{ICON[x]}</span>' for x in ("pen", "trash", "refresh", "gear")) + '</div>')
    return card(f'<div class="c6"><p class="t sm">{rich(b["text"])}</p>{extra}</div>', b["num"], b["title"], big=False)
slide("Характеристики ФС: схема", '<div class="tl2">' + header(d6) + info(d6["blocks"][0]["text"], "q") + '</div>'
    + '<div class="fs6"><div class="col">' + "".join(c6card(i, b) for i, b in enumerate(c6[:3])) + '</div>'
    + art(CR(6, 0, 560), "soft") + '<div class="col">' + "".join(c6card(i + 3, b) for i, b in enumerate(c6[3:])) + '</div></div>', "dense")

# =============================================================== 9. Иерархия
d7 = load(7)
slide("Иерархия каталогов", head([("СТРУКТУРА", "o"), ("ФАЙЛОВОЙ ИЕРАРХИИ", "w")], "Файловая иерархия Linux", "LINUX") + two(
    bullets(["В файловой иерархии все файлы и каталоги находятся в корневом каталоге <c>/</c>, даже если они хранятся на разных физических или виртуальных устройствах.",
             "Некоторые из этих каталогов существуют только в определённых системах, если в них установлены определённые подсистемы, например система X Window.",
             "Большинство этих каталогов существуют во всех операционных системах UNIX и, как правило, используются примерно одинаково.",
             "Однако приведённые здесь описания каталогов используются специально для файловой иерархии и не считаются авторитетными для других платформ, кроме Linux."]),
    art(CR(7, 0, 420), "sm") + info(d7["blocks"][2]["text"], "q")))
IC7 = {"terminal": "terminal", "gear": "gear", "device": "chip", "file": "file", "home": "user", "books": "book", "usb": "download", "drive": "disk",
       "package": "files", "server": "server", "clock": "clock", "users": "users", "chart": "list"}
rows7 = d7["blocks"][1]["rows"]
tree7 = ('<div class="dtree"><div class="droot" data-s="1">' + ICON["folder"] + '<b>/</b></div><div class="dlist">' + "".join(
    f'<div class="drow" data-s="1" style="--dl:{i*45}ms"><span class="dpill">{ICON["folder"]}{r[0]}</span><span class="dsc">{ICON[IC7.get(r[1], "dot")]}<b>{r[2]}</b><em>{r[3]}</em></span></div>'
    for i, r in enumerate(rows7)) + '</div></div>')
slide("Иерархия: дерево", '<div class="tl2">' + header(d7) + info(d7["blocks"][3]["text"], "q") + '</div>' + tree7, "dense")

# =============================================================== 10. Как проверить каталоги
d8 = load(8)["blocks"][0]["terminal"]
slide("Каталоги из корня: шаги", head([("КАК ПРОВЕРИТЬ", "w"), ("КАТАЛОГИ", "o")], "Из корневого каталога ( / )", "TERMINAL") + two(
    '<div class="col">' + "".join(card(f'<div class="stp">{circle(i+1)}<div><h3>{a}</h3><p>{b}</p></div></div>') for i, (a, b) in enumerate([
        ("Открыть терминал", "Запустить терминал из меню приложений или с помощью сочетания клавиш."),
        ("Переключиться на пользователя root", "Выполнить команду <c>sudo -s</c> и ввести системный пароль, чтобы получить права пользователя root."),
        ("Перейти в корневой каталог", "Изменить текущий рабочий каталог на корневой (<c>/</c>)."),
        ("Список всех каталогов в корневом каталоге", "Отображение всех доступных каталогов в базовом каталоге."),
        ("Просмотр структуры каталогов", "Ознакомьтесь с перечисленными каталогами, такими как системные, пользовательские, конфигурационные и виртуальные каталоги.")])) + '</div>',
    term([{"p": "kali@kali:~$", "cmd": "sudo -s"}, {"out": "[sudo] password for kali:"}, {"p": "root@kali:/home/kali#", "cmd": "cd /"}, {"p": "root@kali:/#", "cmd": "ls"},
          {"ls": [x for x in d8[1]["ls"] if x], "cols": 5, "allblue": True}], "root@kali: /", "big-t")))
slide("Каталоги из корня: вывод ls", head([("ВЫВОД", "w"), ("ls", "o l")], "Содержимое корневого каталога", "TERMINAL")
    + term([{"p": "root@geeksforgeeks:/#", "cmd": "ls"}, {"ls": d8[1]["ls"], "cols": 9, "allblue": True}, {"p": "root@geeksforgeeks:/#", "cmd": ""}], "root@geeksforgeeks: /", "big-t wide")
    + '<div class="mt">' + info("Синим выделены каталоги. Здесь видны все каталоги верхнего уровня: <c>bin</c>, <c>boot</c>, <c>dev</c>, <c>etc</c>, <c>home</c>, <c>proc</c>, <c>usr</c>, <c>var</c> и другие.") + '</div>')

# =============================================================== 11–12. /dev и /boot
d9 = load(9)
dtree = ('<div class="ntree">'
    '<div class="nd root" data-s="1">' + ICON["folder"] + '<b>/</b><em>(корень файловой системы)</em></div>'
    '<div class="nbr"><div class="ncol"><div class="nd" data-s="1">' + ICON["folder"] + '<b>/boot</b><em>Файлы загрузчика</em></div>'
    '<div class="nd hot" data-s="1">' + ICON["file"] + '<b>/boot/vmlinux</b><em>Образ ядра Linux</em></div></div>'
    '<div class="ncol"><div class="nd" data-s="1">' + ICON["folder"] + '<b>/dev</b><em>Файлы устройств</em></div>'
    '<div class="nrow">' + "".join(f'<div class="nd {c}" data-s="1">{ICON[i]}<b>{a}</b><em>{b}</em></div>' for i, a, b, c in [
        ("disk", "/dev/hda", "Первый IDE/SATA жёсткий диск", ""), ("disk", "/dev/hdc", "Второй IDE/SATA жёсткий диск", ""),
        ("x", "/dev/null", "Специальное устройство «пустота» (отбрасывает все данные)", "hot")]) + '</div></div></div></div>')
slide("Каталоги /boot и /dev", '<div class="tl2"><div class="col">' + header(d9) + P(d9["intro"]) + info(d9["blocks"][0]["text"], "q") + '</div>'
    + render_card(d9["blocks"][2]) + '</div>' + '<div class="tr2 mt">' + art(CR(9, 0, 380), "sm") + dtree + '</div>'
    + '<div class="g4 mt">' + "".join(render_card(b) for b in d9["blocks"][3:7]) + '</div><div class="mt">' + info(d9["blocks"][7]["text"], "q") + '</div>', "dense")
slide("Ядро и файлы устройств", head([("ИЗУЧЕНИЕ", "o"), ("КАТАЛОГОВ", "w")], "и их возможностей", "LINUX")
    + P("В системе Linux для каждого процесса доступны чётко определённые файлы конфигурации, двоичные файлы и справочные страницы.", cls="p lg")
    + '<div class="g2">' + card(defs([("/boot/vmlinux", "Файл ядра Linux."), ("/boot/grub/grub.cfg", "основной сгенерированный файл конфигурации, который фактически используется при загрузке GRUB.")]), None, "Файл ядра Linux")
    + card(defs([("/dev/hda", "Файл устройства для первого жёсткого диска IDE."), ("/dev/null", "Псевдоустройство (символьное устройство), которое отбрасывает все записанные в него данные и при чтении возвращает признак конца файла (EOF).")]), None, "Файлы устройств") + '</div>'
    + '<div class="g2 mt">' + term([{"p": "kali@kali:~$", "cmd": "ls /boot"}, {"ls": ["grub", "vmlinuz", "initrd.img", "config"], "cols": 4}]) +
    term([{"p": "kali@kali:~$", "cmd": "echo \"мусор\" > /dev/null"}, {"p": "kali@kali:~$", "cmd": "cat /dev/null"}, {"p": "kali@kali:~$", "cmd": ""}]) + '</div>')

# =============================================================== 13. /etc
d10 = load(10); b10 = d10["blocks"]; c10 = [b for b in b10 if b["type"] == "card"]
slide("Файлы /etc", '<div class="tr2"><div class="col">' + header(d10) + P(d10["intro"]) + art(CR(10, 0, 460), "sm") + info(b10[1]["text"], "q") + '</div>'
    + '<div class="g3 etc">' + "".join(card(f'<div class="fi">{icon_for(b.get("icon"), "file")}<div><h3 class="mono">{b["title"]}</h3><p class="t sm">{rich(b.get("text"))}</p></div></div>', cls="flat") for b in c10) + '</div></div>'
    + '<div class="mt">' + info(b10[-1]["text"], "q") + '</div>', "dense")

# =============================================================== 14. /usr
d11 = load(11); b11 = d11["blocks"]; c11 = [b for b in b11 if b["type"] == "card"]
def ex_chips(items):
    return '<div class="exs"><span class="sl">Примеры:</span>' + "".join(f'<code>{esc(x)}</code>' for x in items) + '</div>'
slide("Файлы /usr", '<div class="tr2"><div class="col">' + header(d11) + P(d11["intro"]) + art(CR(11, 0, 460), "sm") + '</div><div class="col">'
    + '<div class="nd root big" data-s="1">' + ICON["folder"] + '<b>/usr</b><em>' + rich(c11[0]["text"]) + '</em></div><div class="bus" data-s="1"></div>'
    + '<div class="g5">' + "".join(card(f'<span class="fold f{i}">{ICON["folder"]}</span><h3 class="mono">{b["title"]}</h3><p class="t sm">{rich(b.get("text"))}</p>'
        + ex_chips(b.get("bullets") or []), cls="usrc") for i, b in enumerate(c11[1:])) + '</div></div></div>'
    + '<div class="mt">' + info(b11[-1]["text"], "q") + '</div>', "dense")

# =============================================================== 15. /proc
d12 = load(12); b12 = d12["blocks"]; c12 = [b for b in b12 if b["type"] == "card"]
def panel_out(t):
    return '<pre class="pan">' + esc("\n".join(x.get("out", "") for x in t)) + '</pre>' if t else ""
slide("Файлы /proc", '<div class="tr2"><div class="col">' + header(d12) + P(d12["intro"]) + art(CR(12, 0, 460), "sm") + '</div>'
    + '<div class="col"><div class="g3">' + "".join(card(f'<div class="fi">{icon_for(b.get("icon"), "cpu")}<div><h3 class="mono">{b["title"]}</h3><p class="t sm">{rich(b.get("text"))}</p></div></div>' + panel_out(b.get("terminal")), cls="flat") for b in c12[:-1]) + '</div>'
    + card(f'<div class="fi">{icon_for(c12[-1].get("icon"), "list")}<div><h3 class="mono">{c12[-1]["title"]}</h3><p class="t sm">{rich(c12[-1].get("text"))}</p></div></div>' + panel_out(c12[-1].get("terminal")), cls="flat")
    + '</div></div><div class="mt">' + info(b12[-1]["text"], "q") + '</div>', "dense")

# =============================================================== 16. Журналы
d13 = load(13); b13 = d13["blocks"]; c13 = [b for b in b13 if b["type"] == "card"]
slide("Файлы журналов", '<div class="tr2"><div class="col">' + header(d13) + P(d13["intro"]) + art(CR(13, 0, 520), "") + '</div><div class="col">'
    + "".join(card(f'<div class="logc"><div class="fi">{icon_for(b.get("icon"), "log")}<div><h3 class="mono">{rich(b["title"])}</h3><p class="t">{rich(b.get("text"))}</p></div></div>{panel_out(b.get("terminal"))}</div>', cls="flat") for b in c13)
    + '</div></div><div class="mt">' + info(b13[-1]["text"], "q") + '</div>', "dense")

exec(open(HERE / "_linux_build2.py", encoding="utf-8").read())
