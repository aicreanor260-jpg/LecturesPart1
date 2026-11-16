# -*- coding: utf-8 -*-
"""Сборка деки «WAN на основе Ethernet. Технологии подключения абонентов» строго по pptx (тема «Скуби-Ду», общие блоки — _pt_kit):

    python _wan2_build.py        → wan-ethernet.html
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _sw_lib as L  # noqa: E402
import _pt_kit as K  # noqa: E402
import _wan_theme  # noqa: E402


def build():
    import _wan2_deck
    import _wan2_final
    del L.SL[:]
    _wan2_final.cover()
    _wan2_deck.build()
    _wan2_final.tail()
    K.build("wan-ethernet.html", "WAN на основе Ethernet — лекция", "th-wan", _wan_theme.FONTS,
            _wan_theme.css("_wan_assets"), list(L.SL), extra_js=K.js("_gre_cli.js"), out_env="WAN2_OUT")


if __name__ == "__main__":
    build()
