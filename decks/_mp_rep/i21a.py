# -*- coding: utf-8 -*-
"""pptx: многоуровневый путь LSP внутри LSP — вёрстка поверх чистого фона bgk_14."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 158

CSS = """<style>
.i21-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i21-h{position:absolute;font:900 30px/1 "Rubik",sans-serif;color:#13306e}
.i21-t{position:absolute;font:500 20px/1.35 "Golos Text",sans-serif;color:#1d2a44}
.i21-t b{font-weight:800;color:#13306e}
.i21-n{position:absolute;font:900 24px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:140px}
.i21-cl{position:absolute;border-radius:60px;filter:blur(2px)}
.i21-ar{position:absolute;height:3px}
.i21-ar::after{content:"";position:absolute;right:-2px;top:-6px;border:7px solid transparent;border-left:11px solid currentColor;border-right:0}
.i21-num{display:inline-block;width:26px;height:26px;border-radius:50%;background:#f2694a;color:#fff;font:800 17px/26px "Golos Text";
 text-align:center;margin-right:12px}
.i21-li{position:absolute;font:500 19px/1.25 "Golos Text",sans-serif;color:#1d2a44;display:flex}
.i21-st{position:absolute;display:flex;border:3px solid #1d3f8a;border-radius:4px;overflow:hidden;height:56px;
 font:700 18px/1.1 "Golos Text",sans-serif;color:#13306e;text-align:center}
.i21-st div{display:flex;align-items:center;justify-content:center}
.i21-y{position:absolute;background:#fde27a;border-radius:14px}
.i21-fly{animation:i21f 3s ease-in-out infinite}
@keyframes i21f{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
</style>"""


def ar(x, y, w, col):
    return '<div class="i21-ar" style="left:%dpx;top:%dpx;width:%dpx;background:%s;color:%s"></div>' % (x, y, w, col, col)


def li(n, y, text):
    return '<div class="i21-li" style="left:448px;top:%dpx;width:600px;font-size:18.5px"><span class="i21-num">%d</span><span>%s</span></div>' % (y, n, text)


GREEN, BLUE = "#1e8a6a", "#1f63c6"

HTML = CSS + bg("bgk_14") + "".join([
    '<div class="step">',
    '<div class="i21-p" style="left:280px;top:170px;width:1350px;height:112px;border-radius:18px"></div>',
    '<div class="i21-t" style="left:306px;top:178px;width:1300px"><b>Многоуровневый путь MPLS</b> — это передача пакета по вложенным путям: '
    'один LSP проходит внутри другого LSP.<br>Для этого поверх уже имеющейся метки добавляют ещё одну.</div>',
    '<div class="i21-t" style="left:306px;top:240px;width:1300px">Так можно связать MPLS-домены, в том числе принадлежащие разным поставщикам услуг.</div>',
    '</div>',
    # ---- LSP3
    '<div class="step">',
    '<div class="i21-p" style="left:280px;top:296px;width:1350px;height:302px"></div>',
    '<div class="i21-h" style="left:306px;top:312px">LSP3: логический путь между пограничными узлами</div>',
    '<div class="i21-cl" style="left:390px;top:398px;width:470px;height:122px;background:#bfeee0"></div>',
    '<div class="i21-cl" style="left:1060px;top:390px;width:500px;height:128px;background:#cfe6fb"></div>',
    '<div style="position:absolute;left:374px;top:362px;width:1174px;height:60px;border-left:3px solid #e2564a;border-right:3px solid #e2564a"></div>',
    '<div style="position:absolute;left:378px;top:375px;width:1166px;height:3px;background:#e2564a"></div>',
    '<div class="i21-h" style="left:902px;top:358px;width:116px;background:#fdf8ea;text-align:center;color:#e2564a;font-size:30px">LSP3</div>',
    '<div class="i21-t" style="left:500px;top:408px;width:280px;font-weight:800;color:#1e8a6a;text-align:center">LSP1 — MPLS-домен 1</div>',
    '<div class="i21-t" style="left:1170px;top:408px;width:280px;font-weight:800;color:#1f63c6;text-align:center">LSP2 — MPLS-домен 2</div>',
    img("i21a_rt.png", "left:322px;top:438px;width:112px"),
    img("i21a_rt.png", "left:806px;top:438px;width:104px"),
    img("i21a_rt.png", "left:1006px;top:438px;width:112px"),
    img("i21a_rt2.png", "left:1490px;top:436px;width:110px"),
    "".join(img("i21a_rg.png", "left:%dpx;top:448px;width:66px" % x) for x in (486, 596, 706)),
    "".join(img("i21a_rb.png", "left:%dpx;top:446px;width:68px" % x) for x in (1182, 1266, 1380)),
    ar(436, 473, 44, GREEN), ar(554, 473, 36, GREEN), ar(664, 473, 36, GREEN), ar(774, 473, 28, GREEN),
    '<div style="position:absolute;left:912px;top:472px;width:92px;height:3px;background:#13306e"></div>',
    ar(1140, 473, 38, BLUE), ar(1252, 473, 12, BLUE), ar(1334, 473, 42, BLUE), ar(1450, 473, 36, BLUE),
    '<div class="i21-n" style="left:305px;top:518px">LER1</div><div class="i21-n" style="left:788px;top:518px">LER2</div>',
    '<div class="i21-n" style="left:986px;top:518px">LER3</div><div class="i21-n" style="left:1474px;top:518px">LER4</div>',
    '<div class="i21-t" style="left:300px;top:558px;width:1320px;text-align:center;font-weight:600">'
    'На уровне LSP3 внутренние LSR доменов скрыты: логические хопы  — LER1 → LER2 → LER3 → LER4.</div>',
    '</div>',
    # ---- стек
    '<div class="step">',
    '<div class="i21-p" style="left:428px;top:612px;width:618px;height:300px"></div>',
    '<div class="i21-h" style="left:446px;top:622px;font-size:27px">Как работает стек</div>',
    li(1, 660, "Входной LER назначает метку LSP3."),
    li(2, 688, "Для пересечения домена поверх неё добавляется<br>транспортная метка локального LSP."),
    li(3, 739, "Внутренние LSR обрабатывают только верхнюю метку."),
    li(4, 767, "После снятия транспортной метки снова доступна метка LSP3."),
    '<div class="i21-st i21-fly" style="left:472px;top:808px;width:526px">'
    '<div style="width:182px;background:#9fe3cc">Транспортная<br>метка</div>'
    '<div style="width:186px;background:#f2694a">Метка LSP3</div>'
    '<div style="flex:1;background:#fff">IP-пакет</div></div>',
    '<div class="i21-t" style="left:490px;top:870px;width:150px;text-align:center;font-weight:700">S = 0</div>',
    '<div class="i21-t" style="left:672px;top:870px;width:150px;text-align:center;font-weight:700">S = 1</div>',
    '</div>',
    # ---- два уровня
    '<div class="step">',
    '<div class="i21-p" style="left:1060px;top:612px;width:570px;height:300px"></div>',
    '<div class="i21-h" style="left:1084px;top:622px;font-size:27px">Два уровня пути</div>',
    '<div class="i21-t" style="left:1084px;top:660px;width:540px;line-height:1.28">LSP3 задаёт последовательность пограничных узлов. '
    'LSP1 и LSP2 обеспечивают передачу внутри отдельных доменов.</div>',
    '<div class="i21-t" style="left:1084px;top:740px;width:540px;line-height:1.28">Аналогия с BGP — разделение междоменного пути '
    'и внутренней топологии. Это концептуальное сходство, а не тождество механизмов.</div>',
    '<div class="i21-y" style="left:1084px;top:826px;width:524px;height:72px"></div>',
    img("i21a_bulb.png", "left:1098px;top:834px;width:62px"),
    '<div class="i21-t" style="left:1172px;top:836px;width:430px;font:800 22px/1.3 Golos Text,sans-serif;color:#13306e">'
    'Продвижение всегда выполняется<br>по текущей верхней метке стека.</div>',
    '</div>',
])
