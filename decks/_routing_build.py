# -*- coding: utf-8 -*-
# Сборщик деки «Маршрутизация и типы маршрутизации»: python decks/_routing_build.py -> decks/routing.html
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import _rt_lib as L
L.CSS += (pathlib.Path(__file__).parent / "_rt_extra.css").read_text(encoding="utf-8")
import _rt_s1  # noqa: F401
for mod in ("_rt_s2", "_rt_s3", "_rt_s4"):
    try:
        __import__(mod)
    except ModuleNotFoundError as e:
        if e.name != mod: raise
extra = ""
xf = pathlib.Path(__file__).parent / "_rt_extra.js"
if xf.exists(): extra = xf.read_text(encoding="utf-8")
L.render(pathlib.Path(__file__).parent / "routing.html", "Маршрутизация и типы маршрутизации", extra)
