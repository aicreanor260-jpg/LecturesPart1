# -*- coding: utf-8 -*-
"""2.6: NAT — вариант без классов A/B/C и с «Адрес от провайдера» (вёрстка общая с n6_nat)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n6_nat import build, W, H, TOP  # noqa: F401

HTML = build(True)
