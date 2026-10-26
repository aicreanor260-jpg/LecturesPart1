# -*- coding: utf-8 -*-
"""Базовая настройка: 4 шага вокруг коммутатора — вёрстка на чистом фоне (эталон для остальных)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 262

CSS = """<style>
.bsx-card{position:absolute;background:rgba(255,255,255,.93);border:3px solid #2a0a2a;transform:skew(-3deg);
  box-shadow:9px 9px 0 rgba(255,46,147,.55)}
.bsx-rib{position:absolute;background:#ff2e93;color:#fff;font:italic 900 46px/1 Rubik,sans-serif;text-transform:uppercase;
  padding:12px 30px 14px;transform:skew(-8deg);box-shadow:6px 6px 0 #2a0a2a;letter-spacing:-.01em;white-space:nowrap}
.bsx-t{position:absolute;font:500 27px/1.3 "Golos Text",sans-serif;color:#1a0a1a}
.bsx-foot{position:absolute;left:300px;top:868px;width:1100px;height:56px;background:#fff;border:3px solid #2a0a2a;
  transform:skew(-6deg);box-shadow:6px 6px 0 rgba(255,46,147,.5);font:600 25px/50px "Golos Text",sans-serif;text-align:center;color:#2a0a2a}
.bsx-foot b{color:#ff2e93;font-weight:800}
.bsx-wire{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.bsx-wire path{fill:none;stroke:#3fe6ff;stroke-width:4;filter:drop-shadow(0 0 6px #3fe6ff);stroke-dasharray:10 8;animation:bsxd 1.2s linear infinite}
.bsx-wire circle{fill:#fff;filter:drop-shadow(0 0 8px #3fe6ff)}
@keyframes bsxd{to{stroke-dashoffset:-36}}
.bsx-sw{animation:bsxf 3.5s ease-in-out infinite}
@keyframes bsxf{50%{transform:translateY(-6px)}}
</style>"""

def card(x, y, w, h, n, title, text, rx, ico):
    return ('<div class="step">'
            '<div class="bsx-card" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
            '<div class="bsx-rib" style="left:%dpx;top:%dpx">%s. %s</div>'
            '<div class="bsx-t" style="left:%dpx;top:%dpx;width:380px">%s</div>%s</div>'
            % (x, y, w, h, x + 10, y - 22, n, title, rx, y + 82, text, ico))

HTML = CSS + bg("bgk_white") + "".join([
    '<div class="step">' + img("b_setup_sw.png", "left:300px;top:488px;width:1068px", "ab bsx-sw") + '</div>',
    card(60, 300, 670, 190, 1, "Подключение", "Настройте параметры подключения для дальнейшей работы.", 100,
         img("b_setup_term.png", "left:470px;top:342px;width:202px")),
    card(985, 300, 640, 190, 2, "Имя устройства", "Имя помогает идентифицировать коммутатор в сети.", 1048,
         img("b_setup_tag.png", "left:1378px;top:352px;width:234px")),
    card(60, 672, 700, 196, 3, "Баннер", "Предупреждение о&nbsp;неавторизованном входе и&nbsp;ответственности.", 102,
         img("b_setup_ban.png", "left:492px;top:688px;width:256px")),
    card(930, 672, 700, 196, 4, "Учётные записи", "Создавайте пользователей с&nbsp;разными полномочиями.", 1008,
         img("b_setup_users.png", "left:1392px;top:722px;width:226px")),
    '<div class="step"><svg class="bsx-wire" viewBox="0 0 1672 941">'
    '<path d="M700 345 C780 360 790 420 788 505"/><path d="M975 345 C900 360 900 420 900 505"/>'
    '<path d="M785 628 C780 690 770 720 745 735"/><path d="M895 628 C900 700 930 740 950 760"/>'
    '<circle cx="788" cy="505" r="7"/><circle cx="900" cy="505" r="7"/><circle cx="785" cy="628" r="7"/><circle cx="895" cy="628" r="7"/>'
    '</svg></div>',
    '<div class="step"><div class="bsx-foot"><b>IP-адрес</b> • <b>маска подсети</b> • <b>шлюз</b> — для удалённого администрирования</div></div>',
])
