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


HOMO = str.maketrans("acepoxyABCEHKMOPTX", "асерохуАВСЕНКМОРТХ")
WORD = re.compile(r"[\w\-]+", re.U)


def fix_homoglyphs(t):
    """«oтcyтствие» — в исходнике латинские буквы попали внутрь русских слов."""
    def one(m):
        w = m.group(0)
        lat = [c for c in w if "a" <= c.lower() <= "z"]
        if not lat or not re.search(r"[а-яё]", w, re.I):
            return w
        if all(c in HOMO for c in map(ord, lat)):
            return w.translate(HOMO)
        return w
    return WORD.sub(one, t)


def clean(text, slide_no=None):
    t = fix_homoglyphs(JUNK.sub(" ", text))
    for a, b in FIXES:
        t = t.replace(a, b)
    if slide_no is not None:
        # «... и т.д. 7 Во-вторых ...» — номер страницы посреди абзаца
        t = re.sub(r"(?<=[\.\;\s])%d(?=\s+[А-ЯA-Z])" % slide_no, " ", t)
    # в исходнике часто пропал пробел после точки: «память.candidate-config»
    t = re.sub(r"(?<=[а-яё]{3})\.(?=[А-ЯЁ][а-яё]|[a-z]{3,})", ". ", t)
    t = re.sub(r"(?<=\bт\.[депк])\.(?=[А-ЯЁA-Z])", ". ", t)
    t = re.sub(r"(?<=\d)\.(?=[А-ЯЁ])", ". ", t)
    t = re.sub(r"(?<=[а-яё]):(?=\d)", ": ", t)
    t = re.sub(r"(?<=[а-яё])\.(?=\d\.)", ". ", t)
    # «restore-configдля» — склейка латиницы с русским словом
    t = re.sub(r"(?<=[a-zA-Z])(?=[а-яё]{3,})", " ", t)
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
    # предложение начинается с заглавной, цифры, кавычки — либо с имени файла/команды
    parts = re.split(
        r"(?<=[\.\!\?])(?<!\s\d\.)\s+(?=[А-ЯA-Z«\d]|[a-z][a-z0-9]*-[a-z])"
        r"|(?<=:)\s+(?=\d\.\s*[А-ЯЁA-Z])", t)
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


# «Коммутатор (Switch) – это сетевое устройство ...» -> карточка термина
DEF_RE = re.compile(
    r"^(?P<ru>[А-ЯA-Z«][^–—\-\(\)]{2,70}?)"
    r"(?:\s*\((?P<lat>[^)]{2,46})\))?"
    r"\s*[–—]\s*(?:это|эта|этот)\s+(?P<body>.+)$", re.S)
DEF_DASH = re.compile(
    r"^(?P<ru>[А-ЯA-Z«][^–—\(\)]{2,60}?)"
    r"(?:\s*\((?P<lat>[^)]{2,46})\))?"
    r"\s*[–—]\s+(?P<body>[а-яa-z«].{40,})$", re.S)

# «running-config - текущая конфигурация ...» — определение технического объекта
DEF_CODE = re.compile(
    r"^(?P<ru>[a-zA-Z][\w\-]{2,28}(?:[ :][\w\-]{2,20}){0,2})"
    r"\s*[-–—]\s*(?P<body>.{30,})$", re.S)

CALLOUT = [
    ("example", re.compile(r"^(?:Например|В примере|Другой пример|Рассмотрим)\b", re.I)),
    ("warn", re.compile(r"^(?:Важно|Обратите внимание|Хочется отметить|Помните|Не закрывайте)\b", re.I)),
    ("sum", re.compile(r"^(?:Примечание|Таким образом|Именно поэтому)\b", re.I)),
]


def classify(sent):
    for label, rx in CALLOUT:
        if rx.match(sent):
            return label
    return None


def sentence_stream(sents, per):
    """Поток предложений -> абзацы, карточки терминов и врезки."""
    res, buf = [], []

    def flush():
        if buf:
            res.extend({"t": "p", "v": c} for c in group_sentences(buf, per))
            del buf[:]

    for s in sents:
        label = classify(s)
        if label:
            flush()
            res.append({"t": "note", "v": s, "k": label})
            continue
        m = DEF_RE.match(s) or (DEF_DASH.match(s) if len(s) > 90 else None)
        if m and len(m.group("ru")) < 72:
            flush()
            res.append({"t": "term", "ru": m.group("ru").strip(" «»"),
                        "lat": (m.group("lat") or "").strip(),
                        "v": m.group("body").strip()})
            continue
        m = DEF_CODE.match(s)
        if m:
            flush()
            res.append({"t": "term", "ru": m.group("ru").strip(),
                        "lat": "", "code": True, "v": m.group("body").strip()})
            continue
        buf.append(s)
    flush()
    return res


URL_ONLY = re.compile(r"^(?:[^h]{0,40}?)(https?://\S+)$")


def blocks(paragraph):
    """Абзац методички -> список блоков: p | lead | term | note | link | ul | ol | cli."""
    t = paragraph
    if is_cli(t) and len(t) < 160:
        return [{"t": "cli", "v": [t]}]

    m = URL_ONLY.match(t)
    if m and len(t) < 160:
        return [{"t": "link", "v": m.group(1).rstrip(".")}]

    # нумерованный список 1. 2. 3.
    if len(NUMBERED.findall(t)) >= 3:
        i = NUMBERED.search(t).start()
        head, body = t[:i].strip(), t[i:]
        items = [x.strip(" ;.") for x in NUMBERED.split(body)]
        items = [x for x in items if len(x) > 2 and not x.isdigit()]
        res = blocks(head) if head else []
        res.append({"t": "ol", "v": items})
        return res

    if BULLET.search(t):
        head, *rest = BULLET.split(t)
        res = blocks(head.strip()) if head.strip() else []
        items = [re.sub(r"^\d+[\.\)]\s*", "", x.strip(" ;.")) for x in rest if x.strip(" ;.")]
        if items:
            res.append({"t": "ul", "v": items})
        return res

    # перечисление через точку с запятой
    if t.count(";") >= 3:
        i = t.find(":")
        head, body = (t[: i + 1], t[i + 1:]) if 0 < i < 180 else ("", t)
        items = [x.strip(" ;") for x in body.split(";") if x.strip(" ;")]
        if len(items) >= 3:
            res = []
            if head.strip():
                res.append({"t": "p", "v": head.strip()})
            res.append({"t": "ul", "v": items})
            return res

    return sentence_stream(split_sentences(t), 2 if len(t) > 400 else 3)


CODE = re.compile(
    r"\b(esr(?:\([a-z\-]+\))?[#>]|console(?:\([a-z\-]+\))?[#>]|"
    r"running-config|candidate-config|startup-config|restore-config|default-config|factory-config|"
    r"show running-config|show candidate-config|commit|confirm|rollback|restore|enable|disable|"
    r"configure|exit|end|interface gigabitethernet|int gi|ip address|history size|show history|"
    r"traceroute|ping|reload|U-Boot|U-boot|POST)\b")

NUM = re.compile(
    r"\b(\d[\d\s]{0,6}(?:,\d+)?\s*"
    r"(?:[КМГ]?бит/с|[МГ]Гц|секунд[аыу]?|минут[аы]?|дБм|дБ|°C|[МГ][бБ]|RU\b|В\b|"
    r"порт(?:а|ов)?|шт\.?|штук|символ(?:а|ов)?|уровень|уровня|устройств|"
    r"точек доступа|пользовател(?:ь|я|ей)))")

LEAD_MIN = 60
LEAD_MAX = 230


def mark(s):
    """Команды -> <code>, количественные величины -> акцент."""
    s = html.escape(s)
    s = CODE.sub(lambda m: "<code>%s</code>" % m.group(0), s)
    s = NUM.sub(lambda m: '<b class="num">%s</b>' % m.group(0), s)
    s = re.sub(r"(https?://[^\s<]+)",
               lambda m: '<a href="%s" target="_blank" rel="noopener">%s</a>'
                         % (m.group(1), m.group(1)), s)
    return s


NOTE_LABEL = {"example": "ПРИМЕР", "warn": "ВАЖНО", "sum": "ВЫВОД"}


def render(bl, idx=None):
    t = bl["t"]
    if t == "p":
        return '<p class="step">%s</p>' % mark(bl["v"])
    if t == "lead":
        return '<p class="lead step">%s</p>' % mark(bl["v"])
    if t == "term":
        num = '<div class="tnum">%02d</div>' % idx if idx else ""
        body = bl["v"]
        body = body[0].upper() + body[1:] if body else body
        code = bl.get("code")
        name = html.escape(bl["ru"]) if code else html.escape(bl["ru"]).upper()
        lat = bl["lat"] or ("cli" if code else "")
        lat = '<div class="tlat">%s</div>' % html.escape(lat).upper() if lat else ""
        return ('<div class="term%s step">'
                '<div class="thead">%s<div><h4>%s</h4>%s</div></div>'
                '<p>%s</p></div>') % (
            " mono" if code else "", num, name, lat, mark(body))
    if t == "link":
        u = html.escape(bl["v"])
        return ('<a class="link step" href="%s" target="_blank" rel="noopener">'
                '<i>ИСТОЧНИК</i><span>%s</span></a>') % (u, u)
    if t == "note":
        return '<aside class="note %s step"><i>%s</i><p>%s</p></aside>' % (
            bl["k"], NOTE_LABEL[bl["k"]], mark(bl["v"]))
    if t == "ul":
        li = "".join("<li>%s</li>" % mark(x) for x in bl["v"])
        return '<ul class="step">%s</ul>' % li
    if t == "ol":
        li = "".join("<li>%s</li>" % mark(x) for x in bl["v"])
        return '<ol class="steps step">%s</ol>' % li
    if t == "cli":
        return '<div class="cli step">%s</div>' % "".join(
            "<span>%s</span>" % html.escape(x) for x in bl["v"])
    return ""


def render_all(bls):
    """Первый абзац слайда — лид; карточки терминов нумеруются 01, 02, 03."""
    out, term_no, lead_done = [], 0, False
    for bl in bls:
        if bl["t"] == "term":
            term_no += 1
            lead_done = True
            out.append(render(bl, term_no))
            continue
        if bl["t"] == "p" and not lead_done and LEAD_MIN <= len(bl["v"]) <= LEAD_MAX:
            lead_done = True
            out.append(render({"t": "lead", "v": bl["v"]}))
            continue
        if bl["t"] in ("term", "p"):
            lead_done = True
        out.append(render(bl))
    return "".join(out)
