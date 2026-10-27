# -*- coding: utf-8 -*-
"""Генерирует _elab/catalog.js из sources/eltex/catalog/switches.json: все коммутаторы MES из каталога eltex.ru.
Порты именуются по типу, как в CLI соответствующей ветки ПО: fa/gi/tw/te/fo/hu + 1/0/N (ветки 10.x, 6.x, 4.x),
у MES5448/MES7048 (ПО 8.x, FASTPATH) — просто 1/0/N подряд. Диалект CLI: '10', '6' (6.x и 4.x — общий синтаксис), '8'."""
import json
import os

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
    js = ("/* Сгенерировано gen_catalog.py из каталога eltex.ru — не править вручную. */\n"
          "(function (G) {\n  'use strict';\n  G.EL.CATALOG = %s;\n  G.EL.CATALOG_OTHER = {};\n})(typeof window !== 'undefined' ? window : global);\n"
          % json.dumps(models, ensure_ascii=False, separators=(",", ":")))
    with open(os.path.join(D, "catalog.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write(js)
    by = {}
    for v in models.values():
        by[v["dialect"]] = by.get(v["dialect"], 0) + 1
    print(len(models), "моделей;", by)


if __name__ == "__main__":
    main()
