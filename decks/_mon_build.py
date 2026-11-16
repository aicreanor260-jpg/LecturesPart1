# -*- coding: utf-8 -*-
"""Сборка деки «Мониторинг и управление» строго по pptx (тема «Черепашки», общие блоки — _pt_kit):

    python _mon_build.py        → monitoring-upravlenie.html
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _sw_lib as L  # noqa: E402
import _pt_kit as K  # noqa: E402
import _mon_theme  # noqa: E402


def build():
    import _mon_deck
    import _mon_final
    del L.SL[:]
    _mon_final.cover()
    _mon_deck.build()
    _mon_final.tail()
    K.build("monitoring-upravlenie.html", "Мониторинг и управление — лекция", "th-mon", _mon_theme.FONTS, _mon_theme.CSS,
            list(L.SL), extra_js=K.js("_mon_cli.js"), out_env="MON_OUT")


if __name__ == "__main__":
    build()
