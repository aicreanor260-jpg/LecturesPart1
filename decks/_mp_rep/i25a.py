# -*- coding: utf-8 -*-
"""pptx: протокол LDP — один LSP для двух сетей, FTN на LSR1 — вёрстка поверх чистого фона bgk_26.
Плашка вывода стоит справа от заголовка оригинала, поэтому TOP маленький (заголовок оригинала не воспроизводится)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 12

CSS = """<style>
.i25-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i25-pb{position:absolute;background:#ddf1fb;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i25-h{position:absolute;font:900 31px/1 "Rubik",sans-serif;color:#13306e;text-transform:uppercase}
.i25-t{position:absolute;font:500 21px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i25-n{position:absolute;font:800 21px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:120px}
.i25-cl{position:absolute;background:#fff;border:3px solid #1d3f8a;border-radius:50px;display:flex;align-items:center;justify-content:center;
 font:700 21px/1 "Golos Text",sans-serif;color:#13306e;box-shadow:inset 0 -4px 0 rgba(29,63,138,.08)}
.i25-ln{position:absolute;height:3px;transform-origin:0 50%}
.i25-ln::after{content:"";position:absolute;right:-2px;top:-6px;border:7px solid transparent;border-left:11px solid currentColor;border-right:0}
.i25-tb{position:absolute;border-collapse:collapse;font:500 21px/1 "Golos Text",sans-serif;color:#1d2a44;background:#fff}
.i25-tb th{background:#c6ebe4;font-weight:700;height:46px;border:2px solid #1d3f8a}
.i25-tb td{height:44px;border:2px solid #1d3f8a}
.i25-fly{animation:i25f 3s ease-in-out infinite}
@keyframes i25f{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
</style>"""


def ln(x, y, w, col, ang=0):
    return '<div class="i25-ln" style="left:%dpx;top:%dpx;width:%dpx;background:%s;color:%s;transform:rotate(%ddeg)"></div>' % (
        x, y, w, col, col, ang)


def rt(x, y, name):
    return img("i25a_rt.png", "left:%dpx;top:%dpx;width:104px" % (x, y)) + \
        '<div class="i25-n" style="left:%dpx;top:%dpx">%s</div>' % (x - 8, y + 80, name)


DK, GR, TL = "#1d3f8a", "#8a8a8a", "#1e6f6a"

HTML = CSS + bg("bgk_26") + "".join([
    '<div class="step">',
    '<div class="i25-p" style="left:858px;top:20px;width:572px;height:138px"></div>',
    '<div class="i25-t" style="left:890px;top:34px;width:520px;font:800 25px/1.2 Golos Text,sans-serif;color:#13306e">'
    'LDP автоматически формирует LSP<br>на основе IP-маршрутизации.</div>',
    '<div class="i25-t" style="left:890px;top:96px;width:520px">В обычном режиме следующий хоп<br>определяется маршрутами IGP.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i25-pb" style="left:46px;top:172px;width:782px;height:104px"></div>',
    img("i25a_lay.png", "left:68px;top:178px;width:96px"),
    '<div class="i25-h" style="left:184px;top:194px;font-size:34px">MPLS IGP</div>',
    '<div class="i25-t" style="left:186px;top:232px;font-size:22px">LSP следует пути, выбранному IGP.</div>',
    '<div class="i25-pb" style="left:844px;top:172px;width:782px;height:104px"></div>',
    img("i25a_gear.png", "left:868px;top:178px;width:96px"),
    '<div class="i25-h" style="left:984px;top:194px;font-size:34px">MPLS TE</div>',
    '<div class="i25-t" style="left:986px;top:232px;font-size:22px">Путь может выбираться с учётом ресурсов и ограничений.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i25-p" style="left:46px;top:292px;width:1122px;height:356px"></div>',
    '<div class="i25-h" style="left:66px;top:308px">Пример: один LSP для двух сетей</div>',
    '<div style="position:absolute;left:346px;top:470px;width:530px;height:56px;background:#c6ebe4;border-radius:8px"></div>',
    img("i25a_ip.png", "left:76px;top:450px;width:116px"),
    '<div class="i25-t" style="left:56px;top:516px;width:156px;text-align:center;font-size:20px;line-height:1.2">IP-пакеты<br>(без метки)</div>',
    ln(198, 489, 64, DK),
    rt(270, 455, "LSR1"), rt(536, 352, "LSR2"), rt(564, 455, "LSR4"), rt(774, 455, "LSR5"),
    ln(330, 452, 205, GR, -19), ln(636, 386, 132, GR),
    ln(380, 489, 30, DK),
    '<div class="i25-fly" style="position:absolute;left:422px;top:470px;width:56px;height:36px;background:#f2694a;border:2px solid #1d3f8a;'
    'border-radius:3px;font:700 21px/34px Golos Text,sans-serif;color:#13306e;text-align:center">231</div>',
    '<div class="i25-t" style="left:452px;top:520px;font:800 19px/1 Golos Text;color:#1e8a6a">LSP1</div>',
    ln(486, 489, 70, DK), ln(674, 489, 92, DK),
    ln(884, 482, 82, TL, -14), ln(884, 498, 86, TL, 18),
    '<div class="i25-cl" style="left:780px;top:356px;width:178px;height:62px">132.100.0.0</div>',
    '<div class="i25-cl" style="left:976px;top:432px;width:170px;height:62px">105.0.0.0</div>',
    '<div class="i25-cl" style="left:972px;top:518px;width:182px;height:62px">192.201.103.0</div>',
    '<div style="position:absolute;left:64px;top:600px;width:1086px;height:36px;background:#c6ebe4;border-radius:8px;'
    'font:500 21px/36px Golos Text,sans-serif;color:#1d2a44;text-align:center">'
    'Для сетей 105.0.0.0 и 192.201.103.0 следующий хоп — <b style="font-weight:800;color:#13306e">LSR4.</b></div>',
    '</div>',
    '<div class="step">',
    '<div class="i25-p" style="left:1182px;top:292px;width:442px;height:264px"></div>',
    '<div class="i25-h" style="left:1202px;top:310px">Маршруты на LSR1</div>',
    '<table class="i25-tb" style="left:1198px;top:356px;width:412px"><tr><th>Сеть</th><th>Следующий хоп</th></tr>'
    '<tr><td style="padding-left:24px">132.100.0.0</td><td style="padding-left:20px">LSR2</td></tr>'
    '<tr><td style="padding-left:24px">105.0.0.0</td><td style="padding-left:20px">LSR4</td></tr>'
    '<tr><td style="padding-left:24px">192.201.103.0</td><td style="padding-left:20px">LSR4</td></tr></table>',
    '</div>',
    '<div class="step">',
    '<div class="i25-p" style="left:46px;top:660px;width:866px;height:180px"></div>',
    '<div class="i25-h" style="left:84px;top:672px;font-size:28px">Фрагмент FTN на LSR1</div>',
    '<table class="i25-tb" style="left:82px;top:710px;width:808px;text-align:center"><tr><th>Сети назначения / FEC</th><th>Путь</th>'
    '<th>Выходная метка</th></tr><tr><td>105.0.0.0; 192.201.103.0</td><td style="font-weight:700">LSP1</td>'
    '<td style="background:#f6a08c;font-weight:700">231</td></tr></table>',
    '<div class="i25-t" style="left:84px;top:804px">Обе сети в данном примере направляются в LSP1.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i25-p" style="left:46px;top:854px;width:1276px;height:68px;border-radius:14px"></div>',
    img("i25a_s1.png", "left:76px;top:860px;width:58px"),
    '<div class="i25-t" style="left:152px;top:876px;font-size:19px"><b style="font-weight:800;color:#13306e">IGP</b> выбирает маршрут</div>',
    '<div class="i25-t" style="left:394px;top:868px;font:900 30px/1 Golos Text;color:#13306e">→</div>',
    img("i25a_s2.png", "left:458px;top:858px;width:60px"),
    '<div class="i25-t" style="left:536px;top:876px;font-size:19px"><b style="font-weight:800;color:#13306e">LDP</b> распространяет метки</div>',
    '<div class="i25-t" style="left:808px;top:868px;font:900 30px/1 Golos Text;color:#13306e">→</div>',
    img("i25a_s3.png", "left:868px;top:858px;width:60px"),
    '<div class="i25-t" style="left:946px;top:876px;font-size:19px"><b style="font-weight:800;color:#13306e">LSR</b> формирует записи продвижения.</div>',
    '</div>',
])
