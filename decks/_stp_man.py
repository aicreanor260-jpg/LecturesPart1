# -*- coding: utf-8 -*-
"""STP: ручные слайды (инфографики автора — вёрсткой)."""
from _stp_pix import PX

M = dict(PX)
from _stp_pix2 import PX2  # noqa: E402

M.update({n: [f()] for n, f in PX2.items()})
