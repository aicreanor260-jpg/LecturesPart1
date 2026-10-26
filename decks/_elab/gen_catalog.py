# -*- coding: utf-8 -*-
"""Генерирует _elab/catalog.js из sources/eltex/catalog/switches.json: в палитру попадают модели ветки ПО 10.x
(MES14xx/24xx/3400/37xx — тот же CLI, что у движка). Остальные ветки перечисляются как «ещё не эмулируются»."""
import json
import os

D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, "..", "..", "sources", "eltex", "catalog", "switches.json")
SKIP = ("OOB", "USB", "RS-232", "консол")


def short(p):
    t = p.get("type") or ""
    if "Combo" in t:
        k = "Combo"
    elif "SFP+" in t:
        k = "SFP/SFP+"
    elif "SFP" in t:
        k = "SFP"
    else:
        k = "RJ-45 " + ("2.5G" if "2500" in t else "1G" if "1000" in t else "100M")
    return k + (" PoE" if p.get("poe") else "")


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    models, other = {}, {}
    for m in data:
        fam = m.get("cli_family") or ""
        ports = [p for p in m["ports"] if not any(k in (p.get("type") or "") for k in SKIP)]
        if fam.startswith("ПО 10."):
            n = sum(p["count"] or 0 for p in ports)
            full = " + ".join("%d × %s" % (p["count"], p["type"]) for p in ports)
            note = " + ".join("%d × %s" % (p["count"], short(p)) for p in ports)
            models[m["model"]] = {"type": "mes", "ports": n, "group": m["group"], "note": note, "full": full, "url": m.get("url")}
        else:
            key = fam.split(" (")[0] or "ПО не указано"
            other.setdefault(key, []).append(m["model"])
    js = ("/* Сгенерировано gen_catalog.py из каталога eltex.ru — не править вручную. */\n"
          "(function (G) {\n  'use strict';\n  G.EL.CATALOG = %s;\n  G.EL.CATALOG_OTHER = %s;\n})(typeof window !== 'undefined' ? window : global);\n"
          % (json.dumps(models, ensure_ascii=False, indent=1), json.dumps(other, ensure_ascii=False)))
    with open(os.path.join(D, "catalog.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write(js)
    print(len(models), "моделей в палитре;", {k: len(v) for k, v in other.items()})


if __name__ == "__main__":
    main()
