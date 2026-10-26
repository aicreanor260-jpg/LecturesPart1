# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

"""Ролевое управление коммутатором: 3 роли + шкала 15 уровней — вёрстка на фоне крыши."""
W, H, TOP = 1672, 941, 310

CSS = """<style>
.brl-card{position:absolute;background:rgba(255,255,255,.93);border:3px solid #2a0a2a;transform:skew(-2deg);box-shadow:9px 9px 0 rgba(255,46,147,.55)}
.brl-rib{position:absolute;background:#ff2e93;color:#fff;font:italic 900 32px/1.05 Rubik,sans-serif;text-transform:uppercase;text-align:center;white-space:nowrap;
  padding:10px 16px;transform:skew(-6deg);box-shadow:5px 5px 0 #2a0a2a}
.brl-t{position:absolute;font:500 26px/1.25 "Golos Text",sans-serif;color:#1a0a1a;text-align:center}
.brl-lab{position:absolute;left:600px;top:664px;width:480px;height:50px;background:#fff;border:3px solid #2a0a2a;transform:skew(-8deg);
  font:italic 800 30px/44px Rubik,sans-serif;text-align:center;color:#1a0a1a;box-shadow:5px 5px 0 #ff2e93}
.brl-bar{position:absolute;left:180px;top:708px;width:1310px;height:50px;display:flex;border:3px solid #2a0a2a;background:#fff}
.brl-bar i{flex:1;border-right:2px solid #fff;animation:brlf 2.4s ease-in-out infinite}
@keyframes brlf{50%{filter:brightness(1.18)}}
.brl-n{position:absolute;width:62px;height:62px;border-radius:50%;background:#fff;border:4px solid #2a0a2a;font:900 34px/56px Rubik,sans-serif;text-align:center}
.brl-cap{position:absolute;background:rgba(255,255,255,.95);border:3px solid #2a0a2a;font:500 21px/1.2 "Golos Text",sans-serif;text-align:center;padding:8px 12px;box-shadow:5px 5px 0 rgba(255,46,147,.5)}
.brl-foot{position:absolute;left:105px;top:842px;width:1480px;height:84px;background:rgba(255,255,255,.95);border:3px solid #2a0a2a;box-shadow:6px 6px 0 rgba(255,46,147,.5)}
.brl-foot ul{position:absolute;left:220px;top:8px;margin:0;padding:0;list-style:none;font:500 22px/34px "Golos Text",sans-serif;color:#1a0a1a}
.brl-foot li:before{content:"●";color:#ff2e93;margin-right:14px}
</style>"""

def card(x, w, ico, rib, text, rw):
    return ('<div class="step"><div class="brl-card" style="left:%dpx;top:330px;width:%dpx;height:322px"></div>%s'
            '<div class="brl-rib" style="left:%dpx;top:478px;width:%dpx">%s</div>'
            '<div class="brl-t" style="left:%dpx;top:556px;width:%dpx">%s</div></div>'
            % (x, w, ico, x + (w - rw) // 2, rw, rib, x + 10, w - 20, text))

cells = "".join('<i style="background:hsl(%d,85%%,%d%%)"></i>' % (280 + k * 4, 84 - k * 2) for k in range(15))

HTML = CSS + bg("bgk_roof") + "".join([
    card(165, 430, img("b_roles_user.png", "left:295px;top:352px;width:170px"), "Пользователь",
         "Просмотр IP-адреса<br>и проверка связности<br>через ping", 340),
    card(612, 450, img("b_roles_l1.png", "left:745px;top:350px;width:180px"), "<span style='font-size:23px'>Младший администратор /<br>техподдержка L1</span>",
         "<div style='margin-top:18px'>Просмотр конфигурации<br>интерфейсов без изменений</div>", 420),
    card(1080, 440, img("b_roles_su.png", "left:1210px;top:345px;width:180px"), "Суперадмин",
         "Просмотр и изменение<br>конфигурации всех<br>элементов", 300),
    '<div class="step"><div class="brl-lab">15 уровней привилегий</div>'
    '<div class="brl-bar">' + cells + '</div>'
    '<div class="brl-n" style="left:150px;top:700px">1</div>'
    '<div class="brl-n" style="left:1455px;top:700px;background:#ff2e93;color:#fff">15</div></div>',
    '<div class="step"><div class="brl-cap" style="left:130px;top:766px;width:270px">Privilege 1 —<br>ограниченный доступ</div>'
    '<div class="brl-cap" style="left:1180px;top:766px;width:410px">Privilege 15 — просмотр<br>и изменение всей конфигурации</div></div>',
    '<div class="step"><div class="brl-foot">' + img("b_roles_lock.png", "left:105px;top:4px;width:80px") +
    '<ul><li>Роли и права определяет политика безопасности организации</li>'
    '<li>Используйте надёжные уникальные пароли; учебные пароли не подходят для действующих сетей</li></ul></div></div>',
])
