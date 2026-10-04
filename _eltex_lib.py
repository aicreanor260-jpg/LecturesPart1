# -*- coding: utf-8 -*-
"""Чистка и разбивка текста, вытащенного из pptx «Сетевые устройства 2.1».

Исходный pptx местами потерял буквы (Tlnt вместо Telnet, Cnsle вместо Console) —
FIXES восстанавливает известные слова. Ничего нового не выдумывается:
только то, что однозначно читается из контекста.
"""
import html
import re

FIXES = [
    ("t-f-b nd", "out-of-band"), ("in-b nd", "in-band"),
    ("tlnt srvr", "telnet server"), ("ssh srvr", "ssh server"),
    ("i telnet server", "ip telnet server"), ("i ssh server", "ip ssh server"),
    ("Tlnt", "Telnet"), ("tlnt", "telnet"), ("srvr", "server"), ("Cnsle", "Console"), ("Cnsl", "Console"),
    ("Eltex Service Rter", "Eltex Service Router"),
    ("Secrit Shell", "Secure Shell"),
    ("Cmm nd Lin Intrf", "Command Line Interface"),
    ("(i telnet srvr)", "(ip telnet server)"), ("(i ssh srvr)", "(ip ssh server)"),
    ("i telnet srvr", "ip telnet server"), ("i ssh srvr", "ip ssh server"),
    ("Tr Trm", "TeraTerm"), ("HrTrminl", "HyperTerminal"), ("mini m", "minicom"),
    ("Rgistrd Jk", "Registered Jack"),
    ("R mmndd Stndrt 232", "Recommended Standard 232"),
    ("]IA232", "EIA-232"), ("D]‑9", "DE-9"), ("D]-9", "DE-9"),
    ("стандартом USE", "стандартом USB"),
    ("flsh‑карт", "flash-карт"), ("flsh", "flash"),
    ("Ulink", "Uplink"), ("u p link", "uplink"),
    ("]SR", "ESR"), ("E SR", "ESR"), ("ESR ‑", "ESR-"), ("ESR -", "ESR-"),
    ("M ES", "MES"), ("МES", "MES"), ("MЕS", "MES"),
    ("неприлигированный", "непривилегированный"),
    ("Incompleted command", "Incomplete command"),
    ("Ctri+N", "Ctrl+N"), ("TRL+F", "CTRL+F"),
    ("сommit", "commit"), ("candidade-config", "candidate-config"),
    ("соpy", "copy"), ("cорy", "copy"), ("сopy", "copy"),
    ("he работают с ключом", "не работают с ключом"),
    ("a pаботают", "а работают"), ("a работают", "а работают"),
    ("Коммуmаmоры доступa", "Коммутаторы доступа"),
    ("aгрегации", "агрегации"),
    ("WEP-Зах", "WEP-3ax"), ("WEP-З", "WEP-3"), ("WPAЗ", "WPA3"),
    ("WОP‑12аc", "WOP-12ac"), ("WOP-12ас", "WOP-12ac"), ("WOP-12aс", "WOP-12ac"),
    ("МIМО", "MIMO"), ("РоЕ", "PoE"), ("ElTEX", "Eltex"),
    ("нетолько", "не только"), ("насклад", "на склад"),
    ("илиформула", "или формула"), ("Впримере", "В примере"),
    ("изданного", "из данного"), ("нодоступны", "но доступны"),
    ("навсех", "на всех"), ("вDRAM", "в DRAM"), ("вскорости", "в скорости"),
    ("необходимоо бязательно", "необходимо обязательно"),
    ("споддержкой", "с поддержкой"), ("Гбит/скаждый", "Гбит/с каждый"),
    ("24ethernet", "24 ethernet"), ("2uplink", "2 uplink"), ("2u plink", "2 uplink"),
    ("48ethernet", "48 ethernet"),
    ("адняя панель коммутаторов", "Задняя панель коммутаторов"),
    ("сновные различия", "Основные различия"),
    ("Точки доступаТочки доступа", "Точки доступа. Точки доступа"),
    ("знергонезависимую", "энергонезависимую"),
    ("набольших расстояниях", "на больших расстояниях"),
    ("набольшихрасстояниях", "на больших расстояниях"),
    ("трафикав обратную", "трафика в обратную"),
    ("будет будет", "будет"),
    ("с это высокопроизводительное", "— это высокопроизводительное"),
    ("Service)тегированных", "Service) тегированных"),
    ("Enterpriseрежим", "Enterprise — режим"),
    ("(Local AreaNetwork)", "(Local Area Network)"),
    ("Usermanual", "User manual"), ("ipaddress", "ip address"),
    ("іp add", "ip add"), ("intvl", "int vlan"),
    ("1/0/1Tab", "1/0/1. Tab"),
    ("50.Все команды", "50. Все команды"),
    ("ops", "ops"),
]

# мусор от нумерации страниц методички, прилипший к тексту
JUNK = re.compile(r"\d{0,3}\s*Академия\s*(Eltex\s*\))?")


def clean(text, slide_no=None):
    t = JUNK.sub(" ", text)
    for a, b in FIXES:
        t = t.replace(a, b)
    if slide_no is not None:
        # «... и т.д. 7 Во-вторых ...» — номер страницы посреди абзаца
        t = re.sub(r"(?<=[\.\;\s])%d(?=\s+[А-ЯA-Z])" % slide_no, " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s+([,;:\.\)])", r"\1", t)
    t = re.sub(r"\(\s+", "(", t)
    return t


CLI_RE = re.compile(r"^(esr|console|Login:|Password:|\(esr\))", re.I)
BULLET = re.compile(r"[•]")
NUMBERED = re.compile(r"(?<![\d/.])([1-9])\.\s+(?=[А-ЯA-Zа-яa-z«])")


def is_cli(line):
    return bool(CLI_RE.match(line.strip()))


def split_sentences(t):
    parts = re.split(r"(?<=[\.\!\?])\s+(?=[А-ЯA-Z«\d])", t)
    return [p.strip() for p in parts if p.strip()]


def group_sentences(sents, per=2):
    out, buf = [], []
    for s in sents:
        buf.append(s)
        if len(buf) >= per:
            out.append(" ".join(buf))
            buf = []
    if buf:
        out.append(" ".join(buf))
    return out


def blocks(paragraph):
    """Абзац методички -> список блоков {'t': p|ul|ol|cli, 'v': ...}."""
    t = paragraph
    if is_cli(t) and len(t) < 160:
        return [{"t": "cli", "v": [t]}]

    # нумерованный список 1. 2. 3.
    if len(NUMBERED.findall(t)) >= 3:
        i = NUMBERED.search(t).start()
        head, body = t[:i].strip(), t[i:]
        items = [x.strip(" ;.") for x in NUMBERED.split(body)]
        items = [x for x in items if len(x) > 2 and not x.isdigit()]
        res = []
        if head:
            res.append({"t": "p", "v": head})
        res.append({"t": "ol", "v": items})
        return res

    if BULLET.search(t):
        head, *rest = BULLET.split(t)
        res = []
        if head.strip():
            res += blocks(head.strip())
        items = [re.sub(r"^\d+[\.\)]\s*", "", x.strip(" ;.")) for x in rest if x.strip(" ;.")]
        if items:
            res.append({"t": "ul", "v": items})
        return res

    # перечисление через точку с запятой
    if t.count(";") >= 3:
        i = t.find(":")
        head, body = (t[: i + 1], t[i + 1:]) if 0 < i < 180 else ("", t)
        items = [x.strip(" ;") for x in body.split(";") if x.strip(" ;")]
        res = []
        if head.strip():
            res.append({"t": "p", "v": head.strip()})
        if len(items) >= 3:
            res.append({"t": "ul", "v": items})
            return res

    sents = split_sentences(t)
    return [{"t": "p", "v": c} for c in group_sentences(sents, 2 if len(t) > 400 else 3)]


TERM = re.compile(
    r"\b(esr(?:\([a-z\-]+\))?[#>]|console(?:\([a-z\-]+\))?[#>]|"
    r"running-config|candidate-config|startup-config|restore-config|default-config|factory-config|"
    r"show running-config|commit|confirm|rollback|restore|enable|disable|configure|exit|end|"
    r"interface gigabitethernet|int gi|ip address|history size|show history|traceroute|ping)\b")


def mark(s):
    """Технические термины -> <code>."""
    s = html.escape(s)
    return TERM.sub(lambda m: "<code>%s</code>" % m.group(0), s)


def render(bl):
    if bl["t"] == "p":
        return '<p class="step">%s</p>' % mark(bl["v"])
    if bl["t"] == "ul":
        li = "".join("<li>%s</li>" % mark(x) for x in bl["v"])
        return '<ul class="step">%s</ul>' % li
    if bl["t"] == "ol":
        li = "".join("<li>%s</li>" % mark(x) for x in bl["v"])
        return '<ol class="step">%s</ol>' % li
    if bl["t"] == "cli":
        return '<div class="cli step">%s</div>' % "".join(
            "<span>%s</span>" % html.escape(x) for x in bl["v"])
    return ""
