# -*- coding: utf-8 -*-
"""Тренажёр-консоль: живой CLI коммутатора со сменой режимов, случайными заданиями и проверкой (движок — _dk_cli.js)."""
import os

from _sw_lib import slide, head, sc, grow, col

JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_dk_cli.js"), encoding="utf-8").read()


def sim(deck, pool):
    """deck — 'base' | 'vlan'; pool — номера шаблонов заданий из TASKS[deck]."""
    return (
        '<div class="clisim" data-deck="%s" data-pool="%s">'
        '<div class="cs-side"><div class="cs-h">Задание</div><div class="cs-task"></div>'
        '<div class="cs-btns"><button data-cs="new">↻ Обновить задание</button><button data-cs="check">Проверить</button>'
        '<button data-cs="send" class="alt">Отправить кадр</button><button data-cs="sol" class="sec">Решение</button></div>'
        '<div class="cs-res"></div><pre class="cli cs-sol" style="display:none"></pre></div>'
        '<div class="cs-term"><div class="cs-bar"><i></i><i></i><i></i><span>Console · Eltex MES</span></div>'
        '<div class="cs-out"></div><label class="cs-in"><span class="cs-pr"></span>'
        '<input type="text" spellcheck="false" autocomplete="off" placeholder="введите команду и нажмите Enter"></label></div></div>'
    ) % (deck, ",".join(str(i) for i in pool))


def sim_slide(label, title, sub, deck, pool):
    slide(label, sc(head(title, sub), grow("g", col(sim(deck, pool)))))


CSS = r"""
.clisim{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:16px;flex:1 1 auto;min-height:0}
.cs-side{display:flex;flex-direction:column;gap:10px;background:var(--panel);border:4px solid #fff;outline:3px solid #0a1440;padding:14px 16px;
 box-shadow:6px 6px 0 rgba(0,0,0,.5);overflow:auto}
.th-base .cs-side{border:2px solid #ff4fa3;outline:0;border-radius:6px}
.cs-h{font:800 clamp(14px,1.2vw,23px)/1 var(--f);color:var(--cy);text-transform:uppercase;letter-spacing:.04em}
.cs-task{font:600 clamp(14px,1.25vw,24px)/1.45 var(--f);color:var(--ink)}
.cs-task b{color:var(--cy2)}
.cs-btns{display:flex;flex-wrap:wrap;gap:8px}
.cs-btns button{font:800 clamp(12px,.95vw,17px)/1 var(--f);padding:10px 14px;border:3px solid #0a1440;cursor:pointer;
 background:var(--cy);color:#10183a;box-shadow:3px 3px 0 rgba(0,0,0,.5)}
.cs-btns button.alt{background:#7dff9a}.cs-btns button.sec{background:rgba(255,255,255,.15);color:var(--ink);border-color:var(--cy)}
.th-base .cs-btns button{border-radius:5px;border-color:#2a0a2a}
.cs-res{font:600 clamp(13px,1.05vw,20px)/1.5 var(--f)}
.cs-res .ok{color:#7dff9a}.cs-res .no{color:#ff8a8a}.cs-res .exp{color:#ffd23a}
.cs-sum{margin-top:6px;font-weight:900}
.cs-send>div{padding:6px 0;border-bottom:1px dashed rgba(255,255,255,.2)}
.cs-send .env{display:inline-block;animation:csfly 1s ease-out both}
@keyframes csfly{from{transform:translateX(-40px);opacity:0}to{transform:none;opacity:1}}
.cs-term{display:flex;flex-direction:column;min-height:0;background:#05060a;border:4px solid #fff;outline:3px solid #0a1440;
 box-shadow:6px 6px 0 rgba(0,0,0,.5)}
.th-base .cs-term{border:2px solid #ff4fa3;outline:0;border-radius:6px}
.cs-bar{display:flex;align-items:center;gap:6px;padding:6px 10px;background:#1b2240;color:#cfd8ff;font:700 13px/1 var(--m)}
.cs-bar i{width:11px;height:11px;border-radius:50%;background:#ff5f57}.cs-bar i+i{background:#febc2e}.cs-bar i+i+i{background:#28c840}
.cs-bar span{margin-left:8px}
.cs-out{flex:1 1 auto;min-height:220px;overflow:auto;padding:10px 12px;font:500 clamp(13px,1.05vw,20px)/1.45 var(--m);color:#e8e8e8;white-space:pre-wrap}
.cs-out .cs-cmd{color:#fff}.cs-out .cs-err{color:#ff8a8a}.cs-out .cs-sys{color:#7a86b8}
.cs-in{display:flex;align-items:center;gap:0;padding:8px 12px;border-top:2px solid #1b2240;font:700 clamp(13px,1.05vw,20px)/1 var(--m)}
.cs-pr{color:#7dff9a;white-space:pre}
.cs-in input{flex:1;min-width:0;background:transparent;border:0;outline:0;color:#fff;font:inherit;caret-color:#7dff9a}
"""
