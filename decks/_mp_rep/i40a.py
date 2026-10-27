# -*- coding: utf-8 -*-
"""pptx: RSVP-TE шаги 6–8 (передача, учёт полосы, поддержание LSP) — вёрстка поверх bgk_12."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 126

CSS = """<style>
.i40-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i40-h{position:absolute;font:900 34px/1 "Rubik",sans-serif;color:#13306e}
.i40-t{position:absolute;font:500 21px/1.22 "Golos Text",sans-serif;color:#1d2a44}
.i40-c{text-align:center}
.i40-ar{position:absolute;height:3px;background:#1b7a6a}
.i40-ar::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:12px solid #1b7a6a;border-right:0}
.i40-pk{position:absolute;display:flex;height:42px;border:2px solid #1d3f8a;border-radius:3px;overflow:hidden;font:500 21px/38px "Golos Text",sans-serif}
.i40-pk b{background:#f2694a;color:#1d1d1d;padding:0 10px;font-weight:500}.i40-pk i{background:#fff;color:#1d3f8a;padding:0 16px;font-style:normal}
.i40-n{position:absolute;font:900 23px/1 "Golos Text",sans-serif;color:#13306e;text-align:center}
.i40-op{position:absolute;background:#f5d24a;border-radius:6px;font:700 20px/36px "Golos Text",sans-serif;color:#1d2a44;text-align:center}
.i40-big{position:absolute;border-radius:8px;font:900 40px/58px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i40-ic{position:absolute;width:56px}
.i40-fly{animation:i40f 3s ease-in-out infinite}
@keyframes i40f{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
</style>"""


def ar(x, y, w):
    return '<div class="i40-ar" style="left:%dpx;top:%dpx;width:%dpx"></div>' % (x, y, w)


def pk(x, y, lab):
    return '<div class="i40-pk i40-fly" style="left:%dpx;top:%dpx"><b>%s</b><i>IP</i></div>' % (x, y, lab)


def rt(x, name, op, w):
    return img("i45a_rt.png", "left:%dpx;top:262px;width:100px" % x) + \
        '<div class="i40-n" style="left:%dpx;top:346px;width:100px">%s</div>' % (x, name) + \
        '<div class="i40-op" style="left:%dpx;top:372px;width:%dpx">%s</div>' % (x + 50 - w // 2, w, op)


def ipdoc(x):
    return img("i40a_ip.png", "left:%dpx;top:276px;width:94px" % x) + \
        '<div class="i40-t i40-c" style="left:%dpx;top:338px;width:130px;font-size:19px">IP-пакет<br>(без метки)</div>' % (x - 18)


def mt(y, ic, strong, rest):
    return img(ic, "left:940px;top:%dpx;width:58px" % y) + \
        '<div class="i40-t" style="left:1022px;top:%dpx;width:420px;font-size:18px"><b style="font-size:20px">%s</b> — %s</div>' % (y + 14, strong, rest)


HTML = CSS + bg("bgk_12") + "".join([
    '<div class="step">',
    '<div class="i40-p" style="left:180px;top:132px;width:1312px;height:358px"></div>',
    '<div class="i40-h" style="left:208px;top:146px">6. Передача пользовательских данных</div>',
    '<div class="i40-t i40-c" style="left:296px;top:196px;width:1086px;height:52px;background:#c4e8e0;border-radius:12px;'
    'font:900 29px/52px Golos Text,sans-serif;color:#13306e">На входном LER1 трафик должен быть направлен в туннель</div>',
    ipdoc(212), ar(312, 302, 36),
    rt(358, "LER1", "Push 100", 132), ar(462, 302, 22), pk(496, 280, 100), ar(614, 302, 22),
    rt(645, "LSR1", "Swap 100 → 200", 178), ar(748, 302, 22), pk(782, 280, 200), ar(902, 302, 22),
    rt(932, "LSR2", "Swap 200 → 300", 178), ar(1036, 302, 22), pk(1068, 280, 300), ar(1188, 302, 22),
    rt(1218, "LER2", "Pop 300", 128), ar(1322, 302, 36), ipdoc(1368),
    '<div class="i40-t" style="left:254px;top:420px;width:1170px;height:60px;background:#c4e8e0;border-radius:12px;'
    'padding:4px 0 0 250px;box-sizing:border-box;font-size:20px">•&nbsp;&nbsp; Показана одна транспортная метка; она снимается на LER2.<br>'
    '•&nbsp;&nbsp; Создание LSP само по себе не направляет в него все пакеты.</div>',
    '</div>',
    # ---- 7
    '<div class="step">',
    '<div class="i40-p" style="left:300px;top:504px;width:590px;height:410px"></div>',
    '<div class="i40-h" style="left:320px;top:518px;font-size:27px">7. Учёт зарезервированной полосы</div>',
    '<div class="i40-big" style="left:360px;top:566px;width:112px;background:#a9dccb">150</div>',
    '<div class="i40-t" style="left:480px;top:568px;font:900 40px/58px Golos Text;color:#13306e">–</div>',
    '<div class="i40-big" style="left:516px;top:566px;width:112px;background:#f68e74">100</div>',
    '<div class="i40-t" style="left:636px;top:568px;font:900 40px/58px Golos Text;color:#13306e">=</div>',
    '<div class="i40-big" style="left:672px;top:566px;width:84px;background:#f5d24a">50</div>',
    '<div class="i40-t" style="left:764px;top:578px;font:900 26px/1 Golos Text;color:#13306e">Мбит/с</div>',
    '<div class="i40-t i40-c" style="left:340px;top:628px;width:150px;font-size:19px">доступно до</div>',
    '<div class="i40-t i40-c" style="left:497px;top:628px;width:150px;font-size:19px">резерв LSP</div>',
    '<div class="i40-t i40-c" style="left:640px;top:628px;width:150px;font-size:19px">остаётся<br>для TE</div>',
    '<div class="i40-t" style="left:338px;top:684px;width:520px">На каждом выбранном участке, в направлении LER1 → LER2. '
    'Остаток учитывается при создании других туннелей.</div>',
    '<div class="i40-t" style="left:322px;top:768px;width:548px;height:68px;background:#f9b5a6;border-radius:14px;padding:8px 0 0 78px;'
    'box-sizing:border-box;font-weight:700;color:#5a1010">Резервирование RSVP-TE само по себе<br>не ограничивает скорость.</div>',
    '<div class="i40-t i40-c" style="left:340px;top:780px;width:44px;height:44px;border-radius:50%;background:#e2342b;color:#fff;'
    'font:900 28px/44px Golos Text">!</div>',
    '<div class="i40-t" style="left:338px;top:846px;width:520px">Для требуемого QoS настраивают очереди<br>и планирование трафика.</div>',
    '</div>',
    # ---- 8
    '<div class="step">',
    '<div class="i40-p" style="left:904px;top:504px;width:540px;height:410px"></div>',
    '<div class="i40-h" style="left:926px;top:518px;font-size:25px">8. Поддержание и завершение LSP</div>',
    mt(554, "i40a_ic1.png", "Path и Resv", "обновляют состояние."),
    mt(610, "i40a_ic2.png", "Нет обновлений", "удаление по тайм-ауту."),
    mt(667, "i40a_ic3.png", "PathErr и ResvErr", "сообщения об ошибках."),
    mt(722, "i40a_ic4.png", "PathTear и ResvTear", "явное удаление состояния."),
    '<div class="i40-t" style="left:920px;top:798px;width:512px;height:108px;background:#c4e8e0;border-radius:14px;padding:6px 8px 0 100px;'
    'box-sizing:border-box;font-size:16px;line-height:1.3"><b style="font-size:19px">При отказе возможен новый путь.</b><br>'
    'Заранее настроенный Fast Reroute позволяет ближайшему к отказу узлу переключить трафик на подготовленный защитный участок.</div>',
    img("i40a_ic5.png", "left:936px;top:814px;width:72px"),
    '</div>',
])
