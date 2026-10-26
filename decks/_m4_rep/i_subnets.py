import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _m4_replib import bg, img
from _kr import css, defs, cloud_at
W, H, TOP = 1672, 941, 0  # заголовок слева налезает на схему по вертикали — срез не нужен, фон под ним чистый
P = "m4x-sub"
CSS = css(P)

def rt(cx, cy):
    return img("sub_router.png", "left:%dpx;top:%dpx;width:136px;height:80px" % (cx - 68, cy - 40))

ROUTERS = [(880, 237), (1180, 237), (662, 417), (880, 417), (1180, 417), (1514, 417), (662, 597), (880, 597), (1180, 597), (1514, 597)]
DASH = ["M942 240H1118", "M880 290V382", "M880 452V560", "M662 452V560", "M720 417H820", "M942 417H1118",
        "M938 252L1124 398", "M1242 417H1456", "M1242 440L1458 584", "M1128 468L936 572",
        "M780 609H820", "M942 609H1118", "M1242 609H1456", "M1514 310V380", "M1514 452V560"]
dash = "".join('<path d="%s"/>' % d for d in DASH)
svg_dash = ('<svg class="%s-sv" viewBox="0 0 1672 941">%s<g fill="none" stroke="#f0c75e" stroke-width="1.8" stroke-dasharray="9 7" opacity=".8">%s</g></svg>'
            % (P, defs(P), dash))
svg_solid = ('<svg class="%s-sv" viewBox="0 0 1672 941"><g fill="none" stroke="#f6d36a" stroke-width="4.5" filter="url(#%s-gl)" stroke-linejoin="round">'
             '<path d="M1242 240H1384" marker-end="url(#%s-ah)"/><path d="M1180 384V288" marker-end="url(#%s-ah)"/>'
             '<path d="M722 595H786" marker-end="url(#%s-ah)"/><path d="M796 583L1114 425" marker-end="url(#%s-ah)"/>'
             '<path d="M378 611H598" marker-start="url(#%s-ah)" marker-end="url(#%s-ah)"/></g></svg>' % ((P,) * 8))
HTML = CSS + bg() + "".join([
    '<div class="step"><div class="%s-pn" style="left:47px;top:275px;width:490px;height:253px"></div>'
    '<div class="%s-t" style="left:85px;top:292px;width:440px;font-size:25.5px;line-height:31px">Каждый IP-адрес принадлежит определённой подсети. Чтобы обеспечить связь между разными подсетями, маршрутизаторы передают IP-пакеты от одной сети к другой, последовательно выбирая путь до получателя.</div></div>' % (P, P),
    '<div class="step">' + svg_dash + "".join(rt(*r) for r in ROUTERS) + '</div>',
    '<div class="step">' + cloud_at(P, 239, 612, 252, "Сеть N", 32) + cloud_at(P, 1514, 240, 232, "Сеть M", 32) + '</div>',
    '<div class="step">' + svg_solid +
    img("sub_cube.png", "left:497px;top:561px;width:52px;height:44px") +
    '<div class="%s-t" style="left:558px;top:505px;font-size:16px">IP-пакет</div>' % P +
    '<svg class="%s-sv" viewBox="0 0 1672 941"><path d="M580 528L562 562L548 572" fill="none" stroke="#f0c75e" stroke-width="1.2"/><circle cx="579" cy="530" r="3" fill="#f0c75e"/></svg></div>' % P,
])
