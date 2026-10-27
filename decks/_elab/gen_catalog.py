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
            elif k in ONT:
                models[k] = {"type": "mes", "kind": "ont", "ports": 2, "portList": ["PON", "LAN"], "group": "ONT (абонентские терминалы)", "pon": ONT[k], "swv": sv,
                             "sw": "ПО " + sv, "note": (m.get("summary") or "") + " · мост, настраивается с OLT (OMCI)", "full": (m.get("summary") or "") + " · ПО " + sv, "url": m.get("url")}
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
