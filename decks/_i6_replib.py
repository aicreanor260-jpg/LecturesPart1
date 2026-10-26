# -*- coding: utf-8 -*-
"""Вёрстки инфографик деки 2.6 (_dk_rep/n6_*.py): чистые фоны из _i6_assets (генерирует _i6_mkbg.py), вырезки — _dk_replib.img."""
import base64
import os

from _dk_replib import img  # noqa: F401

HERE = os.path.dirname(os.path.abspath(__file__))


def bg(name):
    """Чистый фон на весь холст 1672×941: bg('bgk_space') | bg('bgk_globe') | bg('bgk_net')."""
    with open(os.path.join(HERE, "_i6_assets", name + ".webp"), "rb") as fh:
        uri = "data:image/webp;base64," + base64.b64encode(fh.read()).decode()
    return '<img class="ab dkbg" src="%s" style="left:0;top:0;width:1672px;height:941px" alt="">' % uri
