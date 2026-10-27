# -*- coding: utf-8 -*-
"""pptx: RSVP-TE шаги 4–5 (Path / Resv) — вёрстка поверх bgk_29."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 92

CSS = """<style>
.i39-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i39-h{position:absolute;font:900 33px/1 "Rubik",sans-serif;color:#13306e}
.i39-num{position:absolute;width:58px;height:58px;border-radius:50%;background:#1b6f86;color:#fff;font:900 36px/58px "Rubik",sans-serif;text-align:center}
.i39-t{position:absolute;font:500 20px/1.25 "Golos Text",sans-serif;color:#1d2a44}
.i39-nd{position:absolute;background:#d6ebfb;border:2px solid #6aa6e0;border-radius:6px;font:700 20px/1.1 "Golos Text",sans-serif;color:#13306e;
 text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center}
.i39-nd small{font-weight:500;font-size:18px}
.i39-ar{position:absolute;height:3px;background:#24577a}
.i39-ar::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:12px solid #24577a;border-right:0}
.i39-rr{position:absolute;height:3px;background:#f2694a}
.i39-rr::before{content:"";position:absolute;left:-2px;top:-7px;border:8px solid transparent;border-right:12px solid #f2694a;border-left:0}
.i39-lb{position:absolute;font:700 20px/1 "Golos Text",sans-serif;color:#13306e;text-align:center}
.i39-g{position:absolute;background:#d9f1dc;border:2px solid #5fb873;border-radius:5px;font:500 18px/1.2 "Golos Text",sans-serif;color:#1d2a44;padding:4px 12px}
.i39-op{position:absolute;background:#bfe6c8;border:2px solid #5fb873;border-radius:8px;font:700 20px/34px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i39-vl{position:absolute;width:2px;background:#1d3f8a}
.i39-fly{animation:i39f 3s ease-in-out infinite}
@keyframes i39f{0%,100%{transform:translateX(0)}50%{transform:translateX(-10px)}}
</style>"""


def nd(x, y, w, name, sub=""):
    s = "<br><small>%s</small>" % sub if sub else ""
    return '<div class="i39-nd" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">%s%s</div>' % (x, y, w, 52 if sub else 46, name, s)


def rt(x, y, w=92):
    return img("i45a_rt.png", "left:%dpx;top:%dpx;width:%dpx" % (x, y, w))


def ar(x, y, w):
    return '<div class="i39-ar" style="left:%dpx;top:%dpx;width:%dpx"></div>' % (x, y, w)


def lb(x, y, w, t, color="#13306e"):
    return '<div class="i39-lb" style="left:%dpx;top:%dpx;width:%dpx;color:%s">%s</div>' % (x, y, w, color, t)


HTML = CSS + bg("bgk_29") + "".join([
    # ---- шаг 4
    '<div class="step">',
    '<div class="i39-p" style="left:136px;top:100px;width:1400px;height:214px"></div>',
    '<div class="i39-num" style="left:160px;top:110px">4</div>',
    '<div class="i39-h" style="left:246px;top:116px">Транзитные LSR обрабатывают Path</div>',
    nd(212, 168, 132, "LER1", "(входной)"), nd(474, 176, 116, "LSR1"), nd(724, 176, 108, "LSR2"), nd(930, 168, 134, "LER2", "(выходной)"),
    rt(230, 230), rt(486, 230), rt(735, 230), rt(960, 230),
    ar(324, 265, 158), lb(350, 235, 110, "Path"), ar(580, 265, 152), lb(600, 235, 110, "Path"), ar(830, 265, 126), lb(840, 235, 110, "Path"),
    '<div class="i39-t" style="left:1102px;top:140px;width:410px">LSR1 и LSR2 сохраняют состояние пути и предыдущий RSVP-узел. '
    'Это позволяет вернуть Resv через те же устройства в обратном порядке.</div>',
    '<div class="i39-t" style="left:1098px;top:244px;width:400px;height:56px;padding:4px 12px;background:#f9b5a6;border-radius:8px;'
    'font-weight:700;font-size:18px;color:#a3201a">Получение Path ещё не означает успешного сквозного резервирования.</div>',
    '</div>',
    # ---- шаг 5
    '<div class="step">',
    '<div class="i39-p" style="left:136px;top:326px;width:1400px;height:332px"></div>',
    '<div class="i39-num" style="left:160px;top:338px">5</div>',
    '<div class="i39-h" style="left:246px;top:340px">Resv: резервирование и распределение меток</div>',
    nd(284, 382, 126, "LER1", "(входной)"), nd(552, 384, 124, "LSR1"), nd(822, 384, 112, "LSR2"), nd(1078, 382, 130, "LER2", "(выходной)"),
    '<div class="i39-vl" style="left:346px;top:436px;height:212px"></div><div class="i39-vl" style="left:613px;top:432px;height:216px"></div>',
    '<div class="i39-vl" style="left:878px;top:432px;height:216px"></div><div class="i39-vl" style="left:1143px;top:436px;height:212px"></div>',
    '<div class="i39-vl" style="left:1256px;top:386px;height:250px;background:#4a6a8a"></div>',
    '<div class="i39-vl" style="left:240px;top:442px;height:146px;background:#24577a"></div>',
    '<div class="i39-t" style="left:232px;top:584px;font:900 22px/1 Golos Text;color:#24577a;transform:translateX(-50%)">↓</div>',
    lb(170, 518, 74, "Время").replace("700 20px", "500 18px"),
    '<div class="i39-t" style="left:1284px;top:400px;width:236px;height:204px;padding:18px 24px;box-sizing:border-box;background:#d4ecf6;'
    'border-radius:14px;font-size:21px">LER2 начинает обратный обмен. При обработке Resv согласуется резервирование ресурсов.</div>',
    '</div>',
    '<div class="step"><div class="i39-fly">',
    '<div class="i39-rr" style="left:884px;top:462px;width:258px"></div>', lb(930, 441, 200, "Resv • метка 300").replace("20px", "18px"),
    '<div class="i39-g" style="left:830px;top:472px">Подготовить Swap 200 → 300</div>',
    '<div class="i39-rr" style="left:620px;top:526px;width:258px"></div>', lb(660, 504, 200, "Resv • метка 200").replace("20px", "18px"),
    '<div class="i39-g" style="left:584px;top:536px">Подготовить Swap 100 → 200</div>',
    '<div class="i39-rr" style="left:352px;top:587px;width:261px"></div>', lb(390, 565, 200, "Resv • метка 100").replace("20px", "18px"),
    '<div class="i39-g" style="left:296px;top:597px">Использовать Push 100<br>для отправки в LSP</div>',
    '</div></div>',
    # ---- передача данных
    '<div class="step">',
    '<div class="i39-p" style="left:236px;top:676px;width:1200px;height:182px;background:#dff3e7;border-color:#5fb873"></div>',
    '<div class="i39-num" style="left:258px;top:688px;background:#13633f;font-size:32px">✓</div>',
    '<div class="i39-h" style="left:330px;top:690px;font-size:28px">После успешного Resv: передача данных</div>',
    nd(382, 728, 122, "LER1"), nd(642, 728, 122, "LSR1"), nd(908, 728, 122, "LSR2"), nd(1174, 728, 124, "LER2"),
    rt(400, 760, 86), rt(660, 760, 86), rt(926, 760, 86), rt(1192, 760, 86),
    ar(494, 786, 130), ar(760, 786, 136), ar(1026, 786, 142),
    '<div class="i39-op" style="left:368px;top:814px;width:148px">Push 100</div>',
    '<div class="i39-op" style="left:608px;top:814px;width:192px">Swap 100 → 200</div>',
    '<div class="i39-op" style="left:874px;top:814px;width:190px">Swap 200 → 300</div>',
    '<div class="i39-op" style="left:1160px;top:814px;width:148px">Pop 300</div>',
    '</div>',
    '<div class="step">',
    '<div class="i39-p" style="left:282px;top:858px;width:1106px;height:62px;border-radius:14px;border-width:2px"></div>',
    '<div class="i39-num" style="left:298px;top:868px;width:40px;height:40px;font:900 26px/40px Georgia;background:#1f63c6">i</div>',
    '<div class="i39-t" style="left:356px;top:866px;width:560px;font-size:18px"><b>Метки локальны:</b> принимающий узел сообщает предыдущему, '
    'с какой меткой присылать пакеты.</div>',
    '<div class="i39-vl" style="left:930px;top:866px;height:46px"></div>',
    '<div class="i39-num" style="left:952px;top:868px;width:40px;height:40px;font:900 26px/40px Georgia;background:#1f63c6">i</div>',
    '<div class="i39-t" style="left:1010px;top:866px;width:370px;font-size:18px">В этом примере транспортная метка снимается на LER2.</div>',
    '</div>',
])
