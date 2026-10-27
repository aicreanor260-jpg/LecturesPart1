# -*- coding: utf-8 -*-
"""pptx: протокол LDP — LSR3 объявляет метку для сети назначения (Label Mapping) — вёрстка поверх чистого фона bgk_13."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 162

CSS = """<style>
.i29-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i29-h{position:absolute;font:800 27px/1 "Rubik",sans-serif;color:#13306e}
.i29-t{position:absolute;font:500 21px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i29-t b{font-weight:800;color:#1f4fae}
.i29-n{position:absolute;font:800 28px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:140px}
.i29-ar{position:absolute;height:3px}
.i29-ar::after{content:"";position:absolute;top:-7px;border:8px solid transparent}
.i29-r::after{right:-2px;border-left:12px solid currentColor;border-right:0}
.i29-l::after{left:-2px;border-right:12px solid currentColor;border-left:0}
.i29-tb{position:absolute;border-collapse:collapse;font:500 20px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;background:#fdf8ea}
.i29-tb td{height:38px;border:2px solid #1d3f8a}
.i29-go{animation:i29g 3s ease-in-out infinite}
@keyframes i29g{0%,100%{transform:translateX(0)}50%{transform:translateX(10px)}}
.i29-back{animation:i29b 3s ease-in-out infinite}
@keyframes i29b{0%,100%{transform:translateX(0)}50%{transform:translateX(-10px)}}
</style>"""


def ar(x, y, w, col, d="r"):
    return '<div class="i29-ar i29-%s" style="left:%dpx;top:%dpx;width:%dpx;background:%s;color:%s"></div>' % (d, x, y, w, col, col)


HTML = CSS + bg("bgk_13") + "".join([
    '<div class="step">',
    '<div class="i29-p" style="left:210px;top:172px;width:1076px;height:94px"></div>',
    '<div class="i29-t" style="left:244px;top:184px;width:1030px;font-size:25px;line-height:1.35">В нашем примере <b>LSR3</b> — выходной узел '
    'MPLS-сети для пути к сети <b style="color:#13306e">132.100.0.0</b>.<br>Он выделяет метку <b>231</b> и сообщает её <b>LSR2</b> '
    'в сообщении Label Mapping.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i29-p" style="left:208px;top:284px;width:1244px;height:302px"></div>',
    '<div style="position:absolute;left:310px;top:306px;width:736px;height:240px;background:#c6ebe4;border-radius:28px"></div>',
    '<div style="position:absolute;left:404px;top:322px;width:536px;height:26px;border:2px solid #13306e;border-bottom:0"></div>',
    '<div class="i29-t" style="left:536px;top:304px;width:290px;text-align:center;background:#c6ebe4;font:800 23px/32px Golos Text,sans-serif;color:#13306e">'
    'MPLS-сеть оператора</div>',
    img("i29a_rt.png", "left:328px;top:366px;width:134px"),
    img("i29a_rt.png", "left:876px;top:366px;width:134px"),
    '<div class="i29-n" style="left:326px;top:470px">LSR2</div><div class="i29-n" style="left:874px;top:466px">LSR3</div>',
    '<div class="i29-back" style="position:absolute;left:528px;top:346px;width:282px;height:38px">'
    '<div style="position:absolute;left:0;top:0;width:276px;height:34px;background:#f6866b;border:2px solid #b8342a;border-radius:4px;'
    'font:600 20px/34px Golos Text,sans-serif;color:#1d1d1d;text-align:center">Label Mapping: FEC → 231</div></div>',
    ar(484, 395, 376, "#e2564a", "l"),
    ar(480, 440, 104, "#1d3f8a"),
    '<div class="i29-go" style="position:absolute;left:594px;top:420px;display:flex;height:40px;border:2.5px solid #1d3f8a;border-radius:3px;'
    'overflow:hidden;font:700 22px/38px Golos Text,sans-serif;color:#13306e"><span style="background:#f2694a;padding:0 20px">231</span>'
    '<span style="background:#fff;padding:0 26px;border-left:2px solid #1d3f8a">IP</span></div>',
    ar(748, 440, 82, "#1d3f8a"),
    '<div class="i29-t" style="left:840px;top:404px;font-size:20px;font-weight:600;color:#13306e">S0</div>',
    '<div style="position:absolute;left:868px;top:410px;width:12px;height:12px;border-radius:50%;background:#fff;border:2px solid #13306e"></div>',
    '<div class="i29-t" style="left:540px;top:470px;width:260px;text-align:center;font-size:20px">Данные с меткой 231</div>',
    '<div style="position:absolute;left:864px;top:496px;width:160px;height:48px;background:#bfe9e4;border-radius:8px;'
    'font:500 18px/1.2 Golos Text,sans-serif;color:#13306e;text-align:center;padding-top:2px">Egress для<br>данного FEC</div>',
    '<div style="position:absolute;left:1046px;top:346px;width:0;height:200px;border-left:2px dotted #13306e"></div>',
    '<div class="i29-t" style="left:1070px;top:370px;font-size:19px;font-weight:600;color:#13306e">IP без метки</div>',
    ar(1018, 418, 168, "#1d3f8a"),
    '<div style="position:absolute;left:1194px;top:340px;width:240px;height:150px;background:#dff1fd;border:3px solid #2a7fd4;border-radius:76px;'
    'font:800 24px/1.25 Golos Text,sans-serif;color:#13306e;text-align:center;padding-top:36px;box-sizing:border-box">Внешняя<br>IP-сеть<br>132.100.0.0</div>',
    '<div class="i29-t" style="left:208px;top:556px;width:1244px;text-align:center;font-size:17px;color:#13306e">'
    '231 — условное значение обычной метки в этом учебном примере.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i29-p" style="left:358px;top:602px;width:594px;height:296px"></div>',
    '<div class="i29-h" style="left:382px;top:618px">Как LSR3 определяет роль Egress?</div>',
    '<div class="i29-t" style="left:382px;top:658px;width:556px;font-size:20.5px;line-height:1.28">По маршруту к FEC и конфигурации MPLS: '
    'следующий хоп находится вне сети коммутации по меткам либо LSR3 завершает LSP для этого FEC.</div>',
    '<div style="position:absolute;left:374px;top:752px;width:562px;height:132px;background:#cdeedd;border-radius:14px"></div>',
    img("i29a_lock.png", "left:382px;top:770px;width:74px"),
    '<div class="i29-h" style="left:474px;top:764px;font-size:25px">Аутентификация — защита сеанса</div>',
    '<div class="i29-t" style="left:474px;top:800px;width:456px;font-size:17.5px;line-height:1.3">LDP использует TCP-сеансы. Аутентификацию '
    'можно настроить для защиты обмена;<br>сама по себе она не определяет границу оператора.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i29-p" style="left:970px;top:602px;width:640px;height:296px"></div>',
    '<div class="i29-h" style="left:990px;top:618px">Сообщение Label Mapping</div>',
    '<table class="i29-tb" style="left:992px;top:656px;width:598px"><tr><td>Отображение метки (0x0400)</td><td>Длина сообщения</td></tr>'
    '<tr><td colspan="2">Идентификатор сообщения</td></tr><tr><td colspan="2">FEC TLV — сеть 132.100.0.0</td></tr>'
    '<tr><td colspan="2">Generic Label TLV — метка 231</td></tr></table>',
    '<div style="position:absolute;left:990px;top:826px;width:600px;height:60px;background:#fde27a;border-radius:12px"></div>',
    img("i29a_bulb.png", "left:1010px;top:832px;width:42px"),
    '<div class="i29-t" style="left:1066px;top:832px;width:520px;font-size:18px;line-height:1.3;color:#13306e">При использовании PHP выходной узел '
    'может объявить Implicit NULL (3), чтобы сосед снял метку заранее.</div>',
    '<div class="i29-t" style="left:1556px;top:908px;font-size:16px;font-weight:700;color:#fff">RFC 5036</div>',
    '</div>',
])
