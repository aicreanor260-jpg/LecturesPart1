# -*- coding: utf-8 -*-
"""Генерирует _elab/catalog.js из sources/eltex/catalog/switches.json: все коммутаторы MES из каталога eltex.ru.
Порты именуются по типу, как в CLI соответствующей ветки ПО: fa/gi/tw/te/fo/hu + 1/0/N (ветки 10.x, 6.x, 4.x),
у MES5448/MES7048 (ПО 8.x, FASTPATH) — просто 1/0/N подряд. Диалект CLI: '10', '6' (6.x и 4.x — общий синтаксис), '8'."""
import json
import os
import re

D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, "..", "..", "sources", "eltex", "catalog", "switches.json")
SKIP = ("OOB", "USB", "RS-232", "консол")


def pfx(t):
    t = t or ""
    if "QSFP28" in t or "100G" in t:
        return "hu"
    if "QSFP" in t or "40G" in t:
        return "fo"
    if "SFP+" in t or "10GBASE" in t or "SFP28" in t or "25G" in t:
        return "te"
    if "2500" in t or "2.5G" in t:
        return "tw"
    if "10/100BASE-TX" in t and "1000" not in t:
        return "fa"
    return "gi"


def short(p):
    t = p.get("type") or ""
    k = {"hu": "100G", "fo": "40G", "te": "SFP+ 10G", "tw": "RJ-45 2.5G", "fa": "RJ-45 100M"}.get(pfx(t))
    if not k:
        k = "Combo" if "Combo" in t else ("SFP" if "SFP" in t else "RJ-45 1G")
    return k + (" PoE" if p.get("poe") else "")


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    models = {}
    for m in data:
        fam = m.get("cli_family") or ""
        dl = "10" if fam.startswith("ПО 10.") else "8" if fam.startswith("ПО 8.") else "6"
        ports = [p for p in m["ports"] if p.get("count") and not any(k in (p.get("type") or "") for k in SKIP)]
        names, cnt = [], {}
        for p in ports:
            for _ in range(p["count"]):
                if dl == "8":
                    names.append("1/0/%d" % (len(names) + 1))
                else:
                    k = pfx(p["type"])
                    cnt[k] = cnt.get(k, 0) + 1
                    names.append("%s1/0/%d" % (k, cnt[k]))
        if not names or len(names) > 64:
            continue
        models[m["model"]] = {"type": "mes", "ports": len(names), "portList": names, "group": m["group"], "dialect": dl,
                              "sw": fam.split(" (")[0] or "ПО не указано",
                              "note": " + ".join("%d × %s" % (p["count"], short(p)) for p in ports),
                              "full": " + ".join("%d × %s" % (p["count"], p["type"]) for p in ports) + " · " + (fam.split(" (")[0] or "ПО ?"),
                              "url": m.get("url")}
    # маршрутизаторы ESR (routers.json): порты по скорости — gi 1G, te 10G, twe 25G, fo 40G, hu 100G, нумерация в типе с 1
    rsrc = os.path.join(os.path.dirname(SRC), "routers.json")
    nr = 0
    if os.path.exists(rsrc):
        RP = {"1G": "gi", "10G": "te", "25G": "twe", "40G": "fo", "100G": "hu"}
        for m in json.load(open(rsrc, encoding="utf-8")):
            ports = [p for p in (m.get("ports") or []) if p.get("count") and RP.get(p.get("speed"))]
            if not ports or m["model"] == "vESR":
                continue
            names, cnt = [], {}
            for p in ports:
                k = RP[p["speed"]]
                for _ in range(p["count"]):
                    cnt[k] = cnt.get(k, 0) + 1
                    names.append("%s1/0/%d" % (k, cnt[k]))
            st = m.get("status")
            models[m["model"]] = {"type": "esr", "ports": len(names), "portList": names, "group": "Маршрутизаторы ESR", "host": "esr",
                                  "sw": "ПО ESR",
                                  "note": (m.get("summary") or " + ".join("%d×%s" % (p["count"], p["speed"]) for p in ports)) + (" · " + st.lower() if st else ""),
                                  "full": " + ".join("%d × %s" % (p["count"], p["type"]) for p in ports) + ((" · " + m["note"]) if m.get("note") else ""),
                                  "url": m.get("url")}
            nr += 1
    # консольные серверы SCS (console-servers.json): Ethernet по скорости, консольные порты aux1/0/1…N — из «other» (32 × Serial RS-232)
    csrc = os.path.join(os.path.dirname(SRC), "console-servers.json")
    if os.path.exists(csrc):
        RP = {"1G": "gi", "10G": "te"}
        for m in json.load(open(csrc, encoding="utf-8")):
            names, cnt = [], {}
            for p in m.get("ports") or []:
                k = RP.get(p.get("speed"))
                for _ in range(p.get("count") or 0):
                    if k:
                        cnt[k] = cnt.get(k, 0) + 1
                        names.append("%s1/0/%d" % (k, cnt[k]))
            na = re.search(r"(\d+)\s*×\s*Serial RS-232", m.get("other") or "")
            if not names or not na:
                continue
            models[m["model"]] = {"type": "esr", "kind": "scs", "ports": len(names), "portList": names, "aux": int(na.group(1)),
                                  "group": "Консольные серверы SCS", "host": "scs-32", "sw": "ПО SCS " + (m.get("sw_version") or "?"),
                                  "note": "%s × RS-232 (aux) + %s" % (na.group(1), " + ".join("%d×%s" % (p["count"], p["speed"]) for p in m["ports"])),
                                  "full": " + ".join("%d × %s" % (p["count"], p["type"]) for p in m["ports"]) + " + " + na.group(1) + " × RS-232 (RJ-45) · ПО " + (m.get("sw_version") or "?"),
                                  "url": m.get("url")}
    # контроллеры WLC и точки доступа (wifi.json; порты WLC — РЭ WLC 1.39.2 §6.1.1, у ТД одно условное имя порта LAN)
    wsrc = os.path.join(os.path.dirname(SRC), "wifi.json")
    WLCP = {"WLC-15": ["gi1/0/%d" % i for i in range(1, 7)], "WLC-30": ["gi1/0/1", "gi1/0/2", "gi1/0/3", "gi1/0/4", "te1/0/1", "te1/0/2"],
            "WLC-3200": ["twe1/0/%d" % i for i in range(1, 13)], "WLC-3250": ["gi1/0/%d" % i for i in range(1, 9)] + ["twe1/0/%d" % i for i in range(1, 5)],
            "WLC-3350": ["gi1/0/%d" % i for i in range(1, 9)] + ["twe1/0/%d" % i for i in range(1, 5)]}
    APS = ["WEP-3ax", "WEP-30L", "WEP-30L-Z", "WEP-3L", "WEP-50L", "WEP-500K", "WEP-550K", "WOP-20L", "WOP-2L", "WOP-2ac", "WOP-30L", "WOP-30LS", "WOP-30LI", "WOP-3L-EX"]
    if os.path.exists(wsrc):
        for m in json.load(open(wsrc, encoding="utf-8")):
            k, sv = m["model"], m.get("sw_version") or "?"
            if k in WLCP:
                models[k] = {"type": "esr", "kind": "wlc", "ports": len(WLCP[k]), "portList": WLCP[k], "group": "Контроллеры Wi-Fi", "host": "wlc",
                             "sw": "ПО WLC " + sv, "note": m.get("summary") or "", "full": (m.get("summary") or "") + " · ПО " + sv, "url": m.get("url")}
            elif k in APS:
                models[k] = {"type": "deb", "kind": "ap", "ports": 1, "portList": ["LAN"], "group": "Точки доступа Wi-Fi", "swv": sv, "sw": "ПО " + sv,
                             "note": (m.get("summary") or "") + " · порт LAN (имя условное)", "full": (m.get("summary") or "") + " · ПО " + sv, "url": m.get("url")}
    # OLT LTP-N/LTX и ONT-мосты (pon.json; порты — как в CLI ПО 1.12.0: front-port N, pon-port N, port-oob — UM табл. 35–37)
    psrc = os.path.join(os.path.dirname(SRC), "pon.json")
    OLT = {"LTP-4N": (4, 4, "gpon", "4 × SFP+ 10G"), "LTP-8N": (4, 8, "gpon", "4 × SFP+ 10G"), "LTP-16N": (8, 16, "gpon", "8 × SFP+ 10G"),
           "LTX-8": (4, 8, "xgs", "4 × QSFP28 100G"), "LTX-16": (4, 16, "xgs", "4 × QSFP28 100G"),
           "LTX-8 rev.B": (4, 8, "xgs", "2 × QSFP28 100G + 2 × SFP28 25G"), "LTX-16 rev.B": (4, 16, "xgs", "2 × QSFP28 100G + 2 × SFP28 25G"),
           "LTX-8C": (4, 16, "combo", "2 × QSFP28 100G + 2 × SFP28 25G"), "LTX-16C": (4, 32, "combo", "2 × QSFP28 100G + 2 × SFP28 25G")}
    ONT = {"NTU-1L": "gpon", "NTU-1LC": "gpon", "NTU-1D": "gpon", "NTX-1": "xgs", "NTX-1F": "xgs"}
    if os.path.exists(psrc):
        for m in json.load(open(psrc, encoding="utf-8")):
            k, sv = m["model"], m.get("sw_version") or "?"
            if k in OLT:
                fr, pn, kind, fnote = OLT[k]
                names = ["front-port %d" % i for i in range(1, fr + 1)] + ["pon-port %d" % i for i in range(1, pn + 1)] + ["port-oob"]
                models[k] = {"type": "mes", "kind": "olt", "ports": len(names), "portList": names, "group": "OLT GPON / XGS-PON", "host": k, "pon": kind,
                             "sw": "ПО " + sv, "note": "%s + %d × PON + OOB" % (fnote, pn), "full": (m.get("summary") or "") + " · ПО " + sv, "url": m.get("url")}
            elif k.startswith("LTP-4X") or k.startswith("LTP-8X"):   # LTP-X, ПО 3.52: порты как в CLI коммутатора, нумерация с нуля; OOB нет
                fr = 8 if k.startswith("LTP-8X") else 4
                names = ["front-port %d" % i for i in range(fr)] + ["10G-front-port 0", "10G-front-port 1"] + ["gpon-port %d" % i for i in range(fr)]
                models[k] = {"type": "mes", "kind": "olt", "oltDialect": "ltp-x", "ports": len(names), "portList": names, "group": "OLT GPON / XGS-PON",
                             "host": "LTP-8X" if fr == 8 else "LTP-4X", "pon": "gpon", "sw": "ПО " + sv,
                             "note": "%d × GPON, встроенный коммутатор · ПО 3.52" % fr, "full": (m.get("summary") or "") + " · ПО " + sv, "url": m.get("url")}
            elif k in ("MA5160", "MA5020"):   # шасси MA5000: FC1 + одна LC16G (в слоте 4 у MA5160, в слоте 1 у MA5020) — допущение эмулятора
                nf, sl = (10, 4) if k == "MA5160" else (4, 1)
                names = ["front-port 1/%d" % i for i in range(1, nf + 1)] + ["pon-port %d/%d" % (sl, i) for i in range(1, 17)] + ["port-oob"]
                models[k] = {"type": "mes", "kind": "olt", "oltDialect": "ma5000", "slots": 16 if k == "MA5160" else 2, "ports": len(names), "portList": names,
                             "group": "OLT GPON / XGS-PON", "host": k, "pon": "gpon", "sw": "ПО " + sv,
                             "note": "шасси MA5000: FC + LC16G (16 × GPON) · commit + confirm", "full": (m.get("summary") or "") + " · ПО " + sv, "url": m.get("url")}
            elif k in ("LTE-8X", "LTE-2X"):   # OLT Turbo GEPON (РЭ и Quick guide 3.16.7): front-port 0–7 / 0–3, pon-port 0–7 / 0–1 — нумерация с нуля, как в CLI
                fr, pn = (8, 8) if k == "LTE-8X" else (4, 2)
                names = ["front-port %d" % i for i in range(fr)] + ["pon-port %d" % i for i in range(pn)]
                models[k] = {"type": "mes", "kind": "lte", "ports": len(names), "portList": names, "group": "OLT GPON / XGS-PON", "host": k, "pon": "epon", "sw": "ПО " + sv,
                             "note": "OLT Turbo GEPON: %d × EPON, встроенный коммутатор, ONT по MAC и профили правил" % pn, "full": (m.get("summary") or "") + " · ПО " + sv, "url": m.get("url")}
            elif k == "NTE-2 (B+)":   # абонентский EPON-терминал для LTE: PON и LAN (имя условное), настраивается с OLT
                models[k] = {"type": "mes", "kind": "eont", "ports": 2, "portList": ["PON", "LAN"], "group": "ONT (абонентские терминалы)", "pon": "epon", "swv": sv, "sw": "ПО " + sv,
                             "note": (m.get("summary") or "") + " · EPON, настраивается с OLT LTE по MAC", "full": (m.get("summary") or "") + " · ПО " + sv, "url": m.get("url")}
            elif k == "MA4000-PX":   # крейт MA4000-PX (CLI 3.38.1): PP4X-1 и PP4X-2 (front-port 1/0–1/5, 2/0–2/5) + PLC8 в слотах 0 и 1 (gpon-port S/0–7) — допущение эмулятора
                names = ["front-port %d/%d" % (u, i) for u in (1, 2) for i in range(6)] + ["gpon-port %d/%d" % (sl, i) for sl in (0, 1) for i in range(8)]
                models[k] = {"type": "mes", "kind": "olt", "oltDialect": "ma4000", "slots": 16, "ports": len(names), "portList": names,
                             "group": "OLT GPON / XGS-PON", "host": "ma4000", "pon": "gpon", "sw": "ПО " + sv,
                             "note": "крейт MA4000: 2 × PP4X + 2 × PLC8 (16 × GPON) · slot N type plc8 · commit + confirm", "full": (m.get("summary") or "") + " · ПО " + sv, "url": m.get("url")}
            elif k in ONT:
                models[k] = {"type": "mes", "kind": "ont", "ports": 2, "portList": ["PON", "LAN"], "group": "ONT (абонентские терминалы)", "pon": ONT[k], "swv": sv,
                             "sw": "ПО " + sv, "note": (m.get("summary") or "") + " · мост, настраивается с OLT (OMCI)", "full": (m.get("summary") or "") + " · ПО " + sv, "url": m.get("url")}
    # VoIP: TAU-72.IP (РЭ 2.23.8) и SMG-1016M (РЭ 3.411.0) из voip.json — один сценарий: телефоны на FXS, регистрация на SMG, вызов; аналоговый телефон — условная модель
    vsrc = os.path.join(os.path.dirname(SRC), "voip.json")
    if os.path.exists(vsrc):
        for m in json.load(open(vsrc, encoding="utf-8")):
            k, sv = m["model"], m.get("sw_version") or "?"
            if k == "TAU-72.IP":
                names = ["eth0"] + ["fxs %d" % i for i in range(1, 9)]
                models[k] = {"type": "vpc", "kind": "tau", "ports": len(names), "portList": names, "group": "VoIP-шлюзы", "host": "tau-72", "sw": "ПО " + sv,
                             "note": "абонентский шлюз: eth0 + FXS 1–8 (у TAU-72 их 72) · admin / rootpasswd · commit + confirm", "full": (m.get("summary") or "") + " · ПО " + sv, "url": m.get("url")}
            elif k == "SMG-1016M":
                models[k] = {"type": "vpc", "kind": "smg", "ports": 1, "portList": ["eth0"], "group": "VoIP-шлюзы", "sw": "ПО " + sv,
                             "note": "цифровой шлюз с SIP-регистратором (sip users) · admin / rootpasswd", "full": (m.get("summary") or "") + " · ПО " + sv, "url": m.get("url")}
    # абонентский роутер RG-35-WZ (cpe.json, РЭ 2.3.0): WAN = gi1/0/1, LAN 1–4 = gi1/0/2–5 — имена ESR (допущение), настройка через веб-интерфейс
    csrc = os.path.join(os.path.dirname(SRC), "cpe.json")
    if os.path.exists(csrc):
        for m in json.load(open(csrc, encoding="utf-8")):
            if m["model"] == "RG-35-WZ":
                sv = m.get("sw_version") or "?"
                models["RG-35-WZ"] = {"type": "esr", "kind": "cpe", "ports": 5, "portList": ["gi1/0/%d" % i for i in range(1, 6)], "group": "Абонентские роутеры", "host": "RG-35-WZ", "sw": "ПО " + sv,
                                      "note": "WAN gi1/0/1, LAN 1–4 gi1/0/2–5 · настройка через веб-интерфейс · 192.168.1.1, admin / password", "full": (m.get("summary") or "") + " · ПО " + sv, "url": m.get("url")}
    models["Телефон"] = {"type": "vpc", "kind": "phone", "ports": 1, "portList": ["Line"], "group": "VoIP-шлюзы", "sw": "—",
                        "note": "аналоговый телефон (условная модель): dial НОМЕР, hangup", "full": "Аналоговый телефон к порту FXS шлюза TAU"}
    # маршрутизаторы ME (me.json): порты 0/0/N по скорости (10G te, 25G twe — допущение для ME2001, 100G hu), MGMT 0/fmc0/1; шасси без портов — пропуск
    msrc = os.path.join(os.path.dirname(SRC), "me.json")
    if os.path.exists(msrc):
        MP = {"10G": "te", "25G": "twe", "100G": "hu"}
        for m in json.load(open(msrc, encoding="utf-8")):
            names, cnt = [], {}
            for p in m.get("ports") or []:
                k = MP.get(p.get("speed"))
                for _ in range(p.get("count") or 0):
                    if k:
                        cnt[k] = cnt.get(k, 0) + 1
                        names.append("%s0/0/%d" % (k, cnt[k]))
            if not names:
                continue
            sv = m.get("sw_version") or "?"
            models[m["model"]] = {"type": "esr", "kind": "me", "ports": len(names) + 1, "portList": names + ["mgmt0/fmc0/1"], "group": "Маршрутизаторы ME", "host": "EOS",
                                  "promptModel": m["model"].split(" ")[0], "sw": "ПО ME " + sv, "note": m.get("summary") or "", "full": (m.get("summary") or "") + " · ПО " + sv, "url": m.get("url")}
    # межсетевые экраны ESR ФСТЭК (esr-fstec.json, ПО 1.5.10): порты как у ESR; у ESR-30 по РЭ 1.5.10 §5.1 ещё te1/0/1–2 (в каталоге их нет)
    fsrc = os.path.join(os.path.dirname(SRC), "esr-fstec.json")
    if os.path.exists(fsrc):
        RP = {"1G": "gi", "10G": "te", "25G": "twe", "40G": "fo", "100G": "hu"}
        for m in json.load(open(fsrc, encoding="utf-8")):
            names, cnt = [], {}
            for p in m.get("ports") or []:
                k = RP.get(p.get("speed"))
                for _ in range(p.get("count") or 0):
                    if k:
                        cnt[k] = cnt.get(k, 0) + 1
                        names.append("%s1/0/%d" % (k, cnt[k]))
            if m["model"] == "ESR-30 FSTEC" and "te1/0/1" not in names:
                names += ["te1/0/1", "te1/0/2"]
            if not names:
                continue
            models[m["model"]] = {"type": "esr", "kind": "fstec", "ports": len(names), "portList": names, "group": "Межсетевые экраны ESR ФСТЭК", "host": "esr",
                                  "sw": "ПО 1.5.10 (FSTEC)", "note": (m.get("summary") or "") + " · ПО 1.5.10 ФСТЭК", "full": (m.get("summary") or "") + " · ПО 1.5.10", "url": m.get("url")}
    # заводские учётные записи (поле login каталога) и типы портов по группам (pt: [[кол-во, тип], …]) — для «Свойств» в «Тесте»
    import glob
    for f in glob.glob(os.path.join(os.path.dirname(SRC), "*.json")):
        try:
            items = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for m in items if isinstance(items, list) else []:
            if not isinstance(m, dict) or m.get("model") not in models:
                continue
            x = models[m["model"]]
            if m.get("login"):
                x["login"] = [{"u": l.get("user", ""), "p": l.get("password", ""), "a": l.get("access", "")} for l in m["login"] if isinstance(l, dict)]
            pt = [[p["count"], p.get("type") or ""] for p in (m.get("ports") or []) if isinstance(p, dict) and p.get("count") and not any(k in (p.get("type") or "") for k in SKIP)]
            if pt and sum(c for c, _ in pt) == x.get("ports"):
                x["pt"] = pt
    js = ("/* Сгенерировано gen_catalog.py из каталога eltex.ru — не править вручную. */\n"
          "(function (G) {\n  'use strict';\n  G.EL.CATALOG = %s;\n  G.EL.CATALOG_OTHER = {};\n})(typeof window !== 'undefined' ? window : global);\n"
          % json.dumps(models, ensure_ascii=False, separators=(",", ":")))
    with open(os.path.join(D, "catalog.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write(js)
    by = {}
    for v in models.values():
        k = v.get("dialect", "esr")
        by[k] = by.get(k, 0) + 1
    print(len(models), "моделей;", by, "· из них ESR:", nr)


if __name__ == "__main__":
    main()
