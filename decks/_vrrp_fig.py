# -*- coding: utf-8 -*-
"""VRRP: редактируемые SVG и сцены по топологиям исходной PPTX."""
from html import escape
from _sw_lib import scene as _scene

INK='#142c28'; PAPER='#f4e9cb'; GOLD='#d5b66c'; GREEN='#1d5146'; RED='#ae3b30'
_seq=0

def txt(x,y,text,size=20,color=INK,weight=700,anchor='middle'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" style="fill:{color};font-family:Segoe UI,Arial,sans-serif">{escape(str(text))}</text>'

def box(x,y,w,h,fill=PAPER,stroke=INK,r=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'

def path(d,color=INK,width=4,extra=''):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'

def _svg(body,label,height=560):
    return f'<svg class="fig vrrpfig" viewBox="0 0 1000 {height}" role="img" aria-label="{escape(label)}" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="3" width="994" height="{height-6}" rx="12" fill="{PAPER}" stroke="{GOLD}" stroke-width="5"/>{body}</svg>'

def router(x,y,label,fill=GREEN):
    b=f'<g>{box(x-64,y-38,128,76,fill,GOLD,22)}'
    b+=path(f'M{x-36} {y-9}h26m-8 -8 8 8 -8 8 M{x+36} {y+9}h-26m8 -8 -8 8 8 8',PAPER,4)
    b+=txt(x,y+31,label,20,PAPER)+f'<rect x="{x-7}" y="{y+34}" width="14" height="10" fill="{GOLD}" stroke="{INK}" stroke-width="2"/></g>'
    return b

def switch(x,y,name):
    b=box(x-85,y-30,170,60,GREEN,GOLD)+txt(x,y-6,name,21,PAPER)
    for px in [x-45,x,x+45]:b+=box(px-8,y+10,16,14,GOLD,INK,1)
    b+=box(x-7,y-34,14,10,GOLD,INK,1)
    return b

def pc(x,y,name,ip,vlan=None):
    b=box(x-41,y-28,82,52,GREEN,INK,4)+path(f'M{x} {y+25}v10m-24 0h48',INK,4)
    b+=txt(x,y+5,name,19,PAPER)+txt(x,y+59,ip,17)
    if vlan:b+=txt(x,y+82,f'VLAN {vlan}',17,GREEN)
    return b

def _top(mode='normal',roles=True,priority=110,edge_only=False):
    dual=mode=='dual';single=mode=='single';fail=mode=='fail';duplicate=mode=='duplicate'
    # Ports: routers bottom connector, switch top Gi0/1, right/left Gi0/2,
    # bottom access Gi0/3 and Gi0/5. Every cable terminates on these connectors.
    b=path('M270 179V286 M355 320H645',INK,5)
    if not single:b+=path('M730 179V286',INK,5)
    if dual:
        b+=path('M278 179V286 M355 328H645 M738 179V286',RED,4)
    b+=path('M225 334V443H130 M775 334V443H870',INK,4)
    if not edge_only:b+=path('M315 334V443H380 M685 334V443H620',INK,4)
    if dual:b+=path('M315 334V443H380 M685 334V443H620',RED,4)
    if not single and not duplicate:
        b+=f'<ellipse cx="500" cy="120" rx="402" ry="98" fill="none" stroke="{GOLD}" stroke-width="3" stroke-dasharray="8 6"/>'
    b+=router(270,135,'R1',RED if fail else GREEN)
    if not single:b+=router(730,135,'R2')
    b+=switch(270,320,'SW1')+switch(730,320,'SW2')
    for x,name,ip,v in [(130,'PC-1','10.10.1.20',10),(380,'PC-2','10.10.1.30',20),(620,'PC-3','10.10.1.40',20),(870,'PC-4','10.10.1.50',10)]:
        if edge_only and name in ('PC-2','PC-3'):continue
        b+=pc(x,460,name,ip.replace('10.10.1.','10.10.2.') if dual and v==20 else ip,v if dual else None)
    b+=txt(279,270,'Gi0/1',17,INK,700,'start')+txt(721,270,'Gi0/1',17,INK,700,'end')
    b+=txt(382,307,'Gi0/2',17)+txt(618,307,'Gi0/2',17)
    b+=txt(216,369,'Gi0/3',17,INK,700,'end')+txt(784,369,'Gi0/3',17,INK,700,'start')
    if not edge_only:b+=txt(322,369,'Gi0/5',17,INK,700,'start')+txt(677,369,'Gi0/5',17,INK,700,'end')
    if dual:
        b+=txt(270,47,'Master 100 · Backup 200',19)+txt(730,47,'Backup 100 · Master 200',19)
        b+=txt(500,89,'VRID 100 · 10.10.1.1',19)+txt(500,118,'VRID 200 · 10.10.2.1',19)
        b+=txt(270,218,'Gi1/0/1.10 · 10.10.1.2',17)+txt(270,241,'Gi1/0/1.20 · 10.10.2.3',17)
        b+=txt(730,218,'Gi1/0/1.10 · 10.10.1.3',17)+txt(730,241,'Gi1/0/1.20 · 10.10.2.2',17)
    elif single:
        b+=txt(270,71,'Шлюз по умолчанию',22)+txt(500,106,'10.10.1.1',23)+txt(500,137,'AA:BB:CC:11:33:22',18)
    elif duplicate:
        b+=txt(270,66,'R1 доступен',22)+txt(730,66,'R2 доступен',22)
        b+=txt(500,110,'Одинаковый IP',23,RED)+txt(500,146,'10.10.1.1',25,RED)
        b+=txt(270,218,'Gi1/0/1 · 10.10.1.1',18)+txt(730,218,'Gi1/0/2 · 10.10.1.1',18)
        b+=txt(500,263,'Конфликт адресов — это не резервирование',20,RED)
    else:
        if roles:b+=txt(270,66,'Отказ' if fail else f'Master · Priority {priority}',21,RED if fail else GREEN)+txt(730,66,'Master · Priority 100' if fail else 'Backup · Priority 100',21)
        b+=txt(500,97,'VRID 100',20)+txt(500,129,'10.10.1.1',25)+txt(500,159,'00:00:5E:00:01:64',18)
        b+=txt(270,220,'Gi1/0/1 · 10.10.1.2',18)+txt(730,220,'Gi1/0/2 · 10.10.1.3',18)
        if fail:b+=path('M235 105L305 165M305 105L235 165',PAPER,7)
    return b

def topology(mode='normal',scene=False):
    if mode not in ('normal','single','fail','dual','duplicate'):raise ValueError(mode)
    if scene:return failover() if mode=='fail' else announcement()
    return _svg(_top(mode),'Топология VRRP: '+mode)

def _phase(i,body):
    return f'<g data-ph="{i}" data-ph-only="{i}">{body}</g>'

def _pulse(d,color=RED):
    # A moving packet makes the direction visible without a raster asset.
    return path(d,color,8,extra='stroke-dasharray="12 8"')+f'<circle r="9" fill="{color}" stroke="{PAPER}" stroke-width="3"><animateMotion dur="2s" repeatCount="indefinite" path="{d}"/></circle>'

def _callout(text,color=GREEN):
    return box(352,370,296,54,color,GOLD)+txt(500,404,text,21,PAPER)

def announcement(scene=True):
    b=_top('normal',priority=101,edge_only=True)
    def rejected(x):
        return box(x-29,386,58,38,PAPER,RED,3)+path(f'M{x-24} 391L{x} 410L{x+24} 391',RED,2)+path(f'M{x-29} 382L{x+29} 428 M{x+29} 382L{x-29} 428',RED,5)
    b+=_phase(0,_callout('R1 отправляет анонс'))
    b+=_phase(1,_pulse('M270 180V286')+_callout('R1 → SW1'))
    b+=_phase(2,_pulse('M355 320H645')+_pulse('M225 334V443H130')+_callout('SW1 → SW2 и PC-1'))
    b+=_phase(3,rejected(130)+_callout('PC-1 отбрасывает анонс',RED))
    b+=_phase(4,_pulse('M730 286V180')+_pulse('M775 334V443H870')+_callout('SW2 → R2 и PC-4'))
    b+=_phase(5,rejected(870)+_callout('PC-4 отбрасывает анонс',RED))
    b+=_phase(6,rejected(130)+rejected(870)+_callout('R2 остаётся Backup'))
    svg=_svg(b,'Путь VRRP-анонса через SW1 и SW2')
    return _scene(svg,['Master R1 формирует анонс VRID 100, Priority 101.','Через Gi0/1 анонс поступает на SW1.','SW1 передаёт анонс через Gi0/2 на SW2 и через Gi0/3 на PC-1.','PC-1 не участвует в VRRP и отбрасывает анонс.','SW2 передаёт анонс через Gi0/1 к R2 и через Gi0/3 к PC-4.','PC-4 также не участвует в VRRP и отбрасывает анонс.','R2 проверяет VRID 100 и Priority 101; таймер обновляется, роль Backup сохраняется.']) if scene else svg

def failover():
    b=_top('normal',roles=False)
    b+=_phase(0,txt(270,66,'Master',23)+txt(730,66,'Backup',23)+_pulse('M130 432H225V334 M270 286V180',GREEN)+_callout('Пакеты идут через R1'))
    b+=_phase(1,path('M235 105L305 165M305 105L235 165',RED,8)+txt(270,66,'R1 недоступен',23,RED)+txt(730,66,'Backup',23)+_callout('Анонсы прекратились',RED))
    b+=_phase(2,path('M235 105L305 165M305 105L235 165',RED,8)+txt(730,66,'Backup ждёт MDI',23)+_callout('Истекает таймер MDI'))
    b+=_phase(3,path('M235 105L305 165M305 105L235 165',RED,8)+txt(730,66,'Новый Master',23)+_callout('VIP и MAC те же'))
    b+=_phase(4,path('M235 105L305 165M305 105L235 165',RED,8)+txt(730,66,'Master',23)+_pulse('M130 432H225V334 M355 320H645 M730 286V180',GREEN)+_callout('Пакеты идут через R2'))
    return _scene(_svg(b,'Переключение шлюза VRRP при отказе R1'),['R1 обслуживает виртуальный шлюз 10.10.1.1.','R1 выходит из строя. Анонсы больше не приходят.','Backup R2 ожидает истечения Master Down Interval.','R2 принимает роль Master: виртуальные IP и MAC сохраняются.','Трафик проходит через SW1, SW2 и R2; шлюз на ПК менять не требуется.'])

def packet():
    b=txt(500,45,'VRRPv2 · Advertisement',27)
    fields=[('Version',4),('Type',4),('Virtual Router ID',8),('Priority',8),('Count IP Addr',8)]
    x=40
    for name,bits in fields:
        w=920*bits/32;b+=box(x,85,w,92,GREEN,GOLD,0)+txt(x+w/2,120,name,17,PAPER)+txt(x+w/2,151,str(bits)+' бит',18,GOLD);x+=w
    fields=[('Auth Type',8),('Adver Int',8),('Checksum',16)];x=40
    for name,bits in fields:
        w=920*bits/32;b+=box(x,177,w,74,PAPER,INK,0)+txt(x+w/2,207,name,20)+txt(x+w/2,235,str(bits)+' бит',17);x+=w
    b+=box(40,251,920,74,PAPER,INK,0)+txt(500,281,'IP Address (1) … IP Address (n)',23)+txt(500,309,'Список виртуальных IPv4-адресов',18)
    b+=box(40,325,920,70,PAPER,INK,0)+txt(500,367,'Authentication Data · 64 бита',22)
    b+=txt(500,435,'Пример: VRID 100 · Priority 101 · Adver Int 1 с',23)
    b+=txt(500,475,'IPv4: 224.0.0.18 · MAC: 01:00:5E:00:00:12',22)
    b+=txt(500,512,'TTL = 255 · виртуальный MAC источника 00:00:5E:00:01:64',19)
    return _svg(b,'Формат пакета VRRP версии 2')

def states():
    b=box(320,35,360,95,GREEN,GOLD)+txt(500,76,'Initialize / Fault',27,PAPER)+txt(500,107,'Начальное состояние',19,PAPER)
    b+=box(55,345,350,110,GREEN,GOLD)+txt(230,391,'Master',30,PAPER)+txt(230,427,'Обслуживает виртуальный IP',20,PAPER)
    b+=box(595,345,350,110,PAPER,GOLD)+txt(770,391,'Backup',30)+txt(770,427,'Ждёт объявления Master',20)
    b+=path('M400 130V220H230V345 M220 330L230 345L240 330',GREEN,5)+txt(240,184,'Владелец VIP',21)+txt(240,210,'Priority 255',20)
    b+=path('M600 130V220H770V345 M760 330L770 345L780 330',INK,5)+txt(775,192,'Не владелец VIP',21)
    b+=path('M595 370H405 M420 360L405 370L420 380',GREEN,5)+txt(500,337,'Истёк MDI',21)
    b+=path('M405 440H595 M580 430L595 440L580 450',RED,5)+txt(500,479,'Пришёл более сильный Master',20,RED)
    b+=path('M90 345V80H320 M305 70L320 80L305 90',INK,3)+path('M910 345V80H680 M695 70L680 80L695 90',INK,3)
    b+=txt(125,275,'Отключение',18,INK,700,'start')+txt(875,275,'Отключение',18,INK,700,'end')
    b+=txt(500,529,'При равном приоритете преимущество у большего IP-адреса',21)
    return _svg(b,'Переходы между состояниями Initialize, Master и Backup')

def preempt():
    b=txt(500,45,'Возвращение R1: Priority 150 > 100',27)
    for x,title,color in [(35,'Preempt = True',GREEN),(525,'Preempt = False',RED)]:
        b+=box(x,78,440,420,PAPER,GOLD)+box(x,78,440,58,color,GOLD)+txt(x+220,116,title,26,PAPER)
        b+=router(x+110,205,'R1')+router(x+330,205,'R2')
        b+=txt(x+110,268,'Priority 150',20)+txt(x+330,268,'Priority 100',20)
        b+=txt(x+220,318,'R2 уже работает как Master',21)
    b+=path('M360 358H160 M175 348L160 358L175 368',GREEN,6)+txt(255,407,'R1 возвращает роль Master',23,GREEN)+txt(255,451,'Вытеснение разрешено',21)
    b+=txt(745,378,'R2 остаётся Master',24,RED)+txt(745,423,'R1 ждёт отказа R2',23)+txt(745,460,'Вытеснение запрещено',21)
    b+=txt(500,538,'По умолчанию приоритетное вытеснение включено',22)
    return _svg(b,'Сравнение VRRP с включённым и отключённым вытеснением')
