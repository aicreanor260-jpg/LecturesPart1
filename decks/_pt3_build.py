# -*- coding: utf-8 -*-
"""Сборка дек STP, LACP и «Масштабируемость и избыточность сети» по pptx (автослайды _pt_auto + финал *_final.py):

    python _pt3_build.py stp|lacp|hier
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _sw_lib as L  # noqa: E402
import _pt_kit as K  # noqa: E402
import _pt_auto as A  # noqa: E402
import _pt_themes as TH  # noqa: E402

SRC = os.environ.get("PPTX_DIR", os.path.expanduser("~/ClaudeWork/pt/src_pptx"))
DECKS = {
    "stp": dict(pptx="1mKGPlsWl3wRhGjVqPwxQGj8-iBvZGGgX.pptx", out="stp-rstp-mstp.html", title="Протокол связующего дерева STP — лекция",
                fin="_stp_final", cli="_mes_cli.js"),
    "lacp": dict(pptx="1uK0mhMcwjzoX7l1ev4nhv_cDwDpYNZiU.pptx", out="agregaciya-lacp.html", title="Агрегация каналов LACP — лекция",
                 fin="_lacp_final", cli="_mes_cli.js"),
    "hier": dict(pptx="1zFvE-2j55WwqLPUz9U8Nr6c5YZL3cShB.pptx", out="ierarhiya-seti.html",
                 title="Масштабируемость и избыточность локальной сети — лекция", fin="_hier_final", cli=None),
}


def build(key):
    d = DECKS[key]
    adir = "_%s_assets" % key
    path = os.path.join(SRC, d["pptx"])
    if os.path.exists(path):
        A.assets(path, adir)
        slides = A.parse(path)
    else:                                   # чистая копия репозитория без pptx — берём сохранённый разбор
        import json
        slides = json.load(open(os.path.join(HERE, adir, "slides.json"), encoding="utf-8"))
    import json
    json.dump(slides, open(os.path.join(HERE, adir, "slides.json"), "w", encoding="utf-8"), ensure_ascii=False)
    fin = __import__(d["fin"])
    del L.SL[:]
    fin.cover()
    try:
        man = __import__("_%s_man" % key).M
    except ImportError:
        man = None
    A.render(slides, adir, getattr(fin, "TITLES", {}), man=man)
    fin.tail()
    js = K.js(d["cli"]) if d["cli"] else ""
    K.build(d["out"], d["title"], "th-" + key, TH.FONTS[key], TH.css(key, adir), list(L.SL), extra_js=js, out_env=key.upper() + "_OUT")


if __name__ == "__main__":
    for k in sys.argv[1:] or list(DECKS):
        build(k)
