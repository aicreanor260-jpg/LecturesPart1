# -*- coding: utf-8 -*-
"""Web-интерфейс после входа: окно конфигурации и кнопка Save — вёрстка на фоне «за ноутбуком»."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 150

CSS = """<style>
.bws-c{position:absolute;background:#fff;border:4px solid #ff2e93;box-shadow:7px 7px 0 #2a0a2a;
  font:italic 800 28px/1.15 Rubik,sans-serif;color:#1a0a1a;transform:rotate(-4deg);padding:18px 24px;box-sizing:border-box}
.bws-svg{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.bws-svg path{fill:none;stroke:#ff2e93;stroke-width:12;stroke-linecap:round}
.bws-save{position:absolute;left:1478px;top:232px;width:132px;height:66px;border:4px solid #ff2e93;border-radius:12px;
  box-shadow:0 0 22px #ff2e93;animation:bwsp 1.1s ease-in-out infinite}
@keyframes bwsp{50%{box-shadow:0 0 4px #ff2e93;opacity:.55}}
</style>"""

HTML = CSS + bg("bgk_laptop") + "".join([
    '<div class="step">' + img("b_web_save_br.png", "left:800px;top:150px;width:840px") + '</div>',
    '<div class="step"><div class="bws-c" style="left:62px;top:258px;width:268px;height:176px">После входа доступна конфигурация устройства</div></div>',
    '<div class="step">' + img("b_web_save_sw.png", "left:1075px;top:712px;width:597px") + '</div>',
    '<div class="step"><div class="bws-save"></div>'
    '<svg class="bws-svg" viewBox="0 0 1672 941"><path d="M1410 410 L1515 305"/><path d="M1478 308 L1520 300 L1512 342"/></svg>'
    '<div class="bws-c" style="left:1334px;top:400px;width:318px;height:200px;transform:rotate(-6deg)">После изменений нажмите Save в верхнем правом углу окна</div></div>',
])
