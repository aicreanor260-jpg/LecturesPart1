# -*- coding: utf-8 -*-
"""Темы дек-спутников: розовый комикс-город (base) и пиксельный платформер (vlan)."""


def common_css(bg, cover):
    return """
#bg{display:none}
#bgimg{position:fixed;inset:0;z-index:0;pointer-events:none;background:url(%s) center/cover no-repeat}
body:has(.slide.on.cover-slide) #bgimg{background-image:url(%s)}
#bgfx::after{display:none}
""" % (bg, cover)


BASE_CSS = r"""
:root{--fd:"Rubik","Arial Black",sans-serif}
body{background:#2a0a2a}
#bgfx{background:linear-gradient(180deg,rgba(40,6,38,.50),rgba(26,4,26,.62))!important}
body:has(.slide.on.cover-slide) #bgfx{background:linear-gradient(90deg,rgba(30,4,30,.05) 30%,rgba(30,4,30,.72))!important}
.cover{align-items:flex-end;text-align:right;padding-right:3vw}
.cover .meta,.cover .tags{justify-content:flex-end}
.head{padding-left:0}
.head::before{display:none}
h1.t{display:inline-block;font-family:var(--fd);font-style:italic;font-weight:900;letter-spacing:-.01em;
 background:#fff;color:#2a0a2a;padding:.12em .5em .16em;transform:skew(-8deg);
 box-shadow:7px 7px 0 #ff2e93;text-shadow:none;border:3px solid #2a0a2a}
h1.t em,h1.t em.v{color:#ff2e93;text-shadow:none}
p.sub{color:#ffe3f1;text-shadow:0 1px 2px #000;margin-top:12px}
.c,.q{border:2px solid #ff4fa3!important;border-radius:6px;box-shadow:6px 6px 0 rgba(20,0,20,.75)!important}
.c::before{display:none}
.ch h3{font-style:italic}
.pic{border:3px solid #fff;border-radius:6px;box-shadow:8px 8px 0 #ff2e93}
.cover .big{font-style:italic;font-weight:900;text-shadow:5px 5px 0 #ff2e93,0 0 30px rgba(0,0,0,.6)}
.cover .big em{color:#ffb3d6;text-shadow:5px 5px 0 #2a0a2a}
#hud{background:linear-gradient(0deg,rgba(30,4,30,.97),rgba(30,4,30,.7))}
#toc{background:rgba(30,4,30,.96)}
"""

VLAN_CSS = r"""
:root{--fd:"Press Start 2P","Golos Text",monospace}
h1.t{font-size:clamp(15px,1.7vw,30px)!important;line-height:1.3!important}
.ch h3{font-family:"Golos Text",sans-serif!important;font-weight:800}
.cover .big{font-size:clamp(26px,4.2vw,72px)!important;line-height:1.2!important}
body{background:#5ab8ff}
#bgfx{background:linear-gradient(180deg,rgba(10,20,60,.30),rgba(10,20,60,.45))!important}
body:has(.slide.on.cover-slide) #bgfx{background:rgba(10,20,60,.18)!important}
:root{--r:0px;--r2:0px}
.head{padding-left:0}
.head::before{display:none}
h1.t{display:inline-block;font-family:var(--fd);font-weight:700;text-transform:none;
 background:#c8501e;color:#fff;padding:.18em .6em .22em;border:4px solid #3a1606;
 box-shadow:inset 0 -5px 0 rgba(0,0,0,.25),inset 0 4px 0 rgba(255,255,255,.25),5px 5px 0 #000;text-shadow:3px 3px 0 #3a1606}
h1.t em,h1.t em.v{color:#ffe14a;text-shadow:3px 3px 0 #3a1606}
p.sub{display:inline-block;margin-top:10px;background:rgba(255,248,220,.95);color:#3a1606;padding:5px 12px;
 border:3px solid #3a1606;box-shadow:4px 4px 0 #000}
.c,.q{border:4px solid #fff!important;outline:3px solid #0a1440;border-radius:0;
 box-shadow:6px 6px 0 rgba(0,0,0,.55)!important}
.c::before{display:none}
.ch h3{font-family:var(--fd)}
.num,.tag,.foot,.foot i,.ir,.ir .ib,.tw,pre.cli,.scbar,.scbar button,.opts button,.inrow input,.inrow button,
#hud button,.tocit,.dots i{border-radius:0!important}
.pic{border:4px solid #fff;outline:3px solid #0a1440;border-radius:0;box-shadow:7px 7px 0 rgba(0,0,0,.5)}
.pic img{background:#5ab8ff}
.scbar button{box-shadow:3px 3px 0 #000}
.cover .big{font-family:var(--fd);text-transform:none;text-shadow:6px 6px 0 #3a1606}
.cover .big em{color:#ffe14a;text-shadow:6px 6px 0 #3a1606}
.cover{flex:0 1 auto;margin:auto;background:rgba(10,20,60,.82);border:4px solid #fff;outline:3px solid #0a1440;
 padding:34px 46px;box-shadow:8px 8px 0 rgba(0,0,0,.5)}
"""

FONT_LINK = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?%s&display=swap">')

THEMES = {
    "base": {
        "title": "Базовая настройка коммутатора — лекция",
        "out": "bazovye-nastrojki.html",
        "adir": "_bs_assets",
        "fonts": FONT_LINK % ("family=Rubik:ital,wght@0,600;0,800;1,800;1,900&"
                              "family=Golos+Text:wght@400;600;700;800&family=JetBrains+Mono:wght@400;700"),
        "range": ("Базовая настройка", "Шпаргалка команд"),
        # синие/голубые → розовые, фиолетовые → голубой второй акцент
        "hues": [(170, 262, 328, 1.0), (263, 300, 192, 1.0)],
        "ovr": {"base_setup": "b_setup", "base_setup2": "b_connect", "base_console": "b_console",
                "web_login": "b_web_login", "sec_roles": "b_roles", "sec_users": "b_users"},
        "extra": {
            "Вход в Web-интерфейс": [("Web: после входа", "Web-интерфейс: <em>после входа</em>", "b_web_save")],
            "Web-интерфейс Eltex": [("Web в работающей сети", "Web в <em>работающей сети</em>", "b_web_work")],
        },
        "css": BASE_CSS,
    },
    "vlan": {
        "title": "Виртуальные локальные сети VLAN — лекция",
        "out": "vlan.html",
        "adir": "_vl_assets",
        "fonts": FONT_LINK % ("family=Press+Start+2P&family=Pixelify+Sans:wght@500;600;700&"
                              "family=Golos+Text:wght@400;600;700;800&family=JetBrains+Mono:wght@400;700"),
        "range": ("VLAN: принципы работы", "Базовая настройка"),
        # голубой акцент → золото монет, фиолетовый → кирпично-красный; тёмно-синие панели остаются
        "hues": [(180, 205, 46, 1.0), (265, 300, 12, 1.0)],
        "ovr": {"vlan_intro": "v_intro", "vlan_tag8021q": "v_tag8021q", "vlan_id": "v_tagstruct",
                "tagging1": "v_tagproc", "tagging2": "v_fcs", "vlan_pros": "v_pros",
                "vlan_types": "v_types", "port_modes": "v_modes"},
        "extra": {
            "Деление на сегменты": [("ARP-запрос: один домен", "Широковещательный <em>ARP-запрос</em>", "v_arp")],
            "ARP с VLAN": [("VLAN: раздельные домены", "VLAN — <em>раздельные домены</em>", "v_domains"),
                           ("Меньше домен", "Меньше домен — <em>меньше лишнего трафика</em>", "v_smaller")],
            "Тег: что на выходе": [("Этап 1: приём кадра", "Этап 1. <em>Приём кадра</em> на порт", "v_stage1"),
                                   ("Broadcast в VLAN 10", "Broadcast — <em>только в VLAN 10</em>", "v_bcast10"),
                                   ("Растегирование", "Растегирование — <em>untagging</em>", "v_untag")],
            "Сцена: работа порта доступа": [("Порты доступа: схема", "Порты доступа — <em>трафик без тегов</em>", "v_access"),
                                            ("Порты доступа: ПК1 → ПК2", "Порты доступа: <em>кадр от ПК1 к ПК2</em>", "v_access_pc")],
            "Сцена: магистральный порт": [("Trunk: несколько VLAN", "Магистральный порт — <em>несколько VLAN</em>", "v_trunk1"),
                                          ("Trunk: VLAN и MAC", "Магистральные порты: <em>VLAN и MAC</em>", "v_trunk_mac")],
            "Сцена: native VLAN": [("Native VLAN на транке", "Native VLAN <em>на транковом порту</em>", "v_native_trunk"),
                                   ("Native VLAN 10", "Native VLAN 10 — <em>трафик без тегов</em>", "v_native10")],
            "Сцена: general и IP-телефон": [("General: схема", "Интерфейс с полной <em>поддержкой 802.1Q</em>", "v_general1"),
                                            ("General: два коммутатора", "General: <em>обмен через SW1 и SW2</em>", "v_general2"),
                                            ("Приём кадра на SW1", "Приём <em>нетегированного кадра</em> на SW1", "v_sw1rx"),
                                            ("IP-телефон и ПК", "Нетегированный трафик <em>на транке</em>", "v_untag_trunk")],
            "Сцена: Q-in-Q": [("Q-in-Q: VLAN клиента", "Q-in-Q — <em>VLAN клиента</em> у провайдера", "v_qinq1"),
                              ("Q-in-Q: двойная метка", "Q-in-Q — <em>двойная маркировка</em>", "v_qinq2")],
            "MAC-VLAN: схема": [("MAC-VLAN: правила", "Назначение VLAN <em>по MAC-адресам</em>", "v_macvlan")],
        },
        "css": VLAN_CSS,
    },
}

# вёрстка инфографик: фон-картинка сама задаёт подложку, без неоновой рамки и масок
REP_CSS = """
.dkrep .repc{background:none!important;border-radius:0!important;box-shadow:0 8px 30px rgba(0,0,0,.35)!important;color:#1a0a1a}
.dkrep .repc img{-webkit-mask:none!important;mask:none!important}
"""

SCENE_CSS = {
 "vlan": """
.scene .figwrap{background:linear-gradient(180deg,#1d3a8f,#132a6b);border:4px solid #fff;outline:3px solid #0a1440;
 box-shadow:6px 6px 0 rgba(0,0,0,.5);padding:10px}
svg.dkfig rect{rx:0!important;ry:0!important}
svg.dkfig rect[fill^="url(#gsw)"]{fill:#3b4a7a;stroke:#fff;stroke-width:4}
svg.dkfig text{font-family:"Golos Text",sans-serif}
.scbar{border:4px solid #fff!important;outline:3px solid #0a1440;background:#0f2160!important}
""",
 "base": """
.scene .figwrap{background:linear-gradient(160deg,rgba(60,10,56,.94),rgba(34,6,32,.96));border:3px solid #ff4fa3;
 border-radius:6px;box-shadow:8px 8px 0 rgba(20,0,20,.7);padding:10px}
svg.dkfig rect[fill^="url(#gsw)"]{fill:#55586a;stroke:#1a0a1a;stroke-width:3.5}
.scbar{border:2px solid #ff4fa3!important;border-radius:6px}
""",
}
