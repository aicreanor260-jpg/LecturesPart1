# -*- coding: utf-8 -*-
"""Сборка деки «Глобальная сеть» строго по pptx на движке коммутации (тема «Скуби-Ду», общие блоки — _pt_kit):

    python _wan_build.py        → globalnaya-set-wan.html
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _sw_lib as L  # noqa: E402
import _pt_kit as K  # noqa: E402
import _wan_theme  # noqa: E402


def build():
    import _wan_deck
    import _wan_final
    del L.SL[:]
    _wan_final.cover()
    _wan_deck.build()
    _wan_final.tail()
    K.build("globalnaya-set-wan.html", "Глобальная сеть WAN — лекция", "th-wan", _wan_theme.FONTS,
            _wan_theme.css("_wan_assets") + __import__("_scoob").css(), list(L.SL), extra_js=__import__("_scoob").js(), out_env="WAN_OUT")


if __name__ == "__main__":
    build()
