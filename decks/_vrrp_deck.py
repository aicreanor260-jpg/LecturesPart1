"""VRRP: последовательность PPTX сохранена; краткая подача и полный текст источника."""
import json
import re
from pathlib import Path
from html import escape as e
import _sw_lib as L
import _pt_kit as K
import _vrrp_fig as F

HERE=Path(__file__).parent
SRC=json.loads((HERE/'_vrrp_assets/source-text.json').read_text(encoding='utf8'))
TX={}
MAP=[]

def notes(n):
    ps=SRC[n-1]['paragraphs']
    if len(ps)<2:return ''
    return '<details class="v-source"><summary>Полный текст исходного слайда</summary>'+''.join('<p>'+e(p)+'</p>' for p in ps[1:] if p.strip())+'</details>'

def box(title,*lines):
    return L.card(title,L.li(list(lines)),'cy')

def fig(svg):return '<div class="v-fig">'+svg+'</div>'

def emit(n,title,left='',right='',bottom='',green=False):
    main=L.grow('g2',L.col(left),L.col(right)) if right else L.grow('',L.col(left))
    L.slide(title,L.sc(L.head(title),main,bottom,notes(n) if n else ''))
    if green:L.SL[-1]=L.SL[-1].replace('class="slide"','class="slide v-green"',1)
    MAP.append({'slide':len(L.SL),'pptx':n,'title':title})

def terminal(n,title=None):
    item=TX.get(str(n),{})
    blocks=item.get('blocks',[])
    for k,b in enumerate(blocks):
        lines=b.get('lines',[])
        if not lines:continue
        # Построчный вывод оставлен на виду; длинные таблицы делятся на экраны.
        chunks=[];cur=[];size=0
        for ln in lines:
            if cur and (len(cur)>=14 or size+len(ln)>650):chunks.append(cur);cur=[];size=0
            cur.append(ln);size+=len(ln)
        if cur:chunks.append(cur)
        for j,part in enumerate(chunks):
            t=title or item.get('title','Настройка VRRP')
            if len(blocks)>1:t+=' · '+b.get('title','')
            if len(t)>85:t=item.get('title','VRRP')+' · '+str(k+1)
            if len(chunks)>1:t+=' · '+str(j+1)
            body='';run=[]
            def flush():
                nonlocal body,run
                if run:body+=K.term(run);run=[]
            for ln in part:
                if re.search('[А-Яа-яЁё]',ln) and not re.match(r'\w+\([^)]*\)#|\w+#',ln):
                    flush();body+='<div class="c"><p>'+e(ln)+'</p></div>'
                else:run.append(ln)
            flush()
            warn={25:'В колонке SW2 исходник трижды использует приглашение SW1 — сохранено дословно',28:'В исходнике у config-subif пропущен # — сохранено дословно'}
            emit(n,t,body,bottom=L.foot(warn.get(n,'Команды и значения — из исходного примера')))

def build():
    global TX
    p=HERE/'_vrrp_tx.json'
    if p.exists():TX=json.loads(p.read_text(encoding='utf8'))
    # PPTX 1
    L.slide('Избыточность на уровне L3 · VRRP','<div class="v-chapter">КОММУТАЦИЯ · 2.8</div><div class="v-cover"><div class="kicker">Резервирование шлюза по умолчанию</div><h1>VRRP</h1><h2>Избыточность на уровне L3</h2><p>Один виртуальный шлюз.<br>Два маршрутизатора, готовых его обслужить.</p></div>',cover=True)
    MAP.append({'slide':1,'pptx':1,'title':'VRRP'})
    # PPTX 2
    emit(2,'Цель главы',box('После лекции', 'Объяснить, зачем резервировать шлюз по умолчанию','Разобрать выбор Master, анонсы и переключение','Настроить VRRP и проверить его работу на ESR'),fig(F.topology()),green=True)
    # PPTX 3
    emit(3,'Зачем резервировать шлюз',box('Первый переход','Шлюз пересылает пакеты в сети, отличные от сети устройства','При отказе единственного шлюза связь с другими сетями пропадает','Резервирование сохраняет доступ к шлюзу'),fig(F.topology(mode='single')),L.foot('Сбой шлюза затрагивает всю локальную сеть'))
    # PPTX 4
    emit(4,'Один шлюз — одна точка отказа',box('Исходная сеть','R1: IP 10.10.1.1','MAC AA:BB:CC:11:33:22','PC-1…PC-4 используют R1 для выхода из своей сети'),fig(F.topology(mode='single')))
    emit(4,'Второй роутер с тем же IP',box('Простое дублирование адреса','В примере попытка назначить R2 адрес 10.10.1.1 приводит к конфликту','Проверка адреса через ARP обнаруживает другого владельца','Нужен механизм, который согласует активную роль'),fig(F.topology(mode='duplicate')),L.foot('Два физических устройства должны согласовать, кто обслуживает шлюз'))
    # PPTX 5
    emit(5,'Ручное переключение шлюза',box('Вариант 1','Дать R2 другой IP: 10.10.1.2','При отказе R1 вручную назначить R2 адрес 10.10.1.1'),box('Вариант 2','При отказе R1 поменять шлюз на всех компьютерах','Оба варианта требуют действий администратора'),L.foot('Для автоматического резервирования нужен протокол первого перехода'))
    emit(5,'Виртуальный маршрутизатор',box('VRRP','Virtual Router Redundancy Protocol','Физические маршрутизаторы совместно обслуживают виртуальный шлюз','При отказе активного устройства его роль принимает резервное'),fig(F.topology()),L.foot('В исходнике рассматривается VRRP для IPv4'))
    # PPTX 6
    emit(6,'Как ПК находит шлюз',box('ARP и адрес шлюза','PC-1 запрашивает MAC для IP 10.10.1.1','Активный маршрутизатор отвечает виртуальным MAC','ПК использует этот MAC в Destination MAC исходящих кадров'),fig(F.topology()))
    emit(6,'Общий IP и общий MAC',box('Группа VRRP','VRID объединяет маршрутизаторы одной группы','Виртуальный IP: 10.10.1.1','VRID: 100 → 0x64'),'<div class="v-formula"><div class="v-big">00:00:5E:00:01:XX</div><p>XX — номер VRID в шестнадцатеричном формате.</p><div class="v-big">100 → 64</div></div>',L.foot('В примере виртуальный MAC: 00:00:5E:00:01:64'))
    emit(6,'Переключение без смены шлюза',F.failover(),bottom=L.foot('Пройдите сцену кнопкой «Вперёд»; IP и MAC шлюза остаются прежними'))
    # PPTX 7
    emit(7,'Кто становится Master',box('Выбор активного устройства','Обычный приоритет: 1…254','Побеждает маршрутизатор с большим приоритетом','Владелец виртуального IP имеет приоритет 255'),box('Роли','Master обслуживает виртуальный шлюз','Backup готов заменить Master','В одной группе в нормальном режиме один Master'),green=True)
    emit(7,'Формат VRRP-пакета',fig(F.packet()),bottom=L.foot('Анонс содержит VRID, Priority, интервал и виртуальные IP-адреса'))
    emit(7,'Master сообщает о себе',box('VRRP Announcements','Master периодически отправляет анонсы','Backup узнаёт, что активный маршрутизатор доступен','Пока анонсы приходят, резервный не отвечает вместо Master'),fig(F.topology()))
    # PPTX 8
    emit(8,'Анонс VRRP: адреса и TTL',K.table(['Поле','Значение в исходнике'],[['IP назначения','224.0.0.18'],['MAC назначения · вариант 1','01:00:5E:00:00:12'],['MAC назначения · вариант 2','01:00:5E:00:00:18'],['MAC источника','00:00:5E:00:01:64'],['VRID / Priority','100 / 101'],['Интервал / TTL','1 секунда / 255']]),box('Проверка получателя','Пакет с TTL, отличным от 255, отбрасывается','Анонс используется в пределах локального сегмента','Два значения MAC перенесены без исправления'),L.foot('Расхождение исходника: …:12 и …:18. По RFC сопоставление 224.0.0.18 → …:12'))
    # PPTX 9
    emit(9,'Как анонс проходит через сеть',F.announcement(),bottom=L.foot('Коммутатор распространяет кадр; участник VRRP обрабатывает анонс'))
    emit(9,'Кто обрабатывает анонс',box('PC-1 и PC-4','Не участвуют в группе VRRP','Полученный служебный пакет не используется ими для работы шлюза'),box('SW2 и R2','SW2 получает кадр на Gi0/2','В примере отправляет его в Gi0/3 и Gi0/1','R2 принимает и обрабатывает VRRP-анонс'))
    # PPTX 10
    emit(10,'Что узнаёт R2 из анонса',box('Проверка группы','VRID = 100 совпадает с локальной группой','Анонс относится к тому же виртуальному маршрутизатору'),box('Проверка роли и таймера','Приоритет R1 выше → R2 остаётся Backup','AdverInt задаёт интервал анонсов','По интервалу и приоритету рассчитывается время ожидания'),L.foot('VRID → приоритет → интервал ожидания'),green=True)
    # PPTX 11
    terminal(11,'VRRP в Wireshark')
    # PPTX 12
    emit(12,'Три состояния VRRP',fig(F.states()),bottom=L.foot('Initialize → выбор роли → Master или Backup'))
    # PPTX 13
    emit(13,'Запуск: Initialize',box('Проверка настроек','Проверяются VRID, виртуальный IP и адрес интерфейса','Владелец виртуального IP становится Master','Остальные переходят в Backup'),fig(F.states()))
    emit(13,'Работа в состоянии Backup',box('Ожидание Master','Backup отслеживает объявления активного маршрутизатора','Допустимые объявления обновляют таймер ожидания','Когда Master Down Interval истекает, Backup становится Master'),F.failover())
    # PPTX 14
    emit(14,'Как Backup обрабатывает пакеты',K.table(['Пакет','Действие Backup'],[['ARP к виртуальному IP','Не отвечает вместо Master'],['Трафик на виртуальный MAC','Не маршрутизирует как Master'],['VRRP-анонс','Проверяет параметры группы и приоритет']]),box('Приоритет и вытеснение','Более высокий приоритет может привести к смене Master','Поведение зависит от Preempt','При выключенном Preempt работающий Master сохраняет роль'))
    emit(14,'Как Master обрабатывает пакеты',K.table(['Пакет','Действие Master'],[['ARP к виртуальному IP','Отвечает виртуальным MAC'],['Трафик на виртуальный MAC','Маршрутизирует'],['VRRP от более приоритетного узла','Переходит в Backup'],['VRRP при равных приоритетах','Сравнивает IP-адреса']]),box('Разрешение равенства','При одинаковом приоритете преимущество у большего IP','Если другой узел не имеет преимущества, Master сохраняет роль','Master продолжает отправлять объявления'))
    # PPTX 15
    terminal(15,'Переходы между состояниями')
    # PPTX 16
    emit(16,'Master Down Interval','<div class="v-formula"><div class="v-big">MDI = 3 × AdvertInt + ST</div><p><b>AdvertInt</b> — интервал объявлений Master.<br><b>ST</b> — Skew Time, добавка с учётом приоритета Backup.</p><div class="v-big">ST = <span class="fraction"><span>(256 − Pri) × AdvertInt</span><span>256</span></span></div></div>',bottom=L.foot('Backup использует свой приоритет Pri для расчёта времени ожидания'))
    emit(16,'Пример расчёта MDI',box('Pri = 100; AdvertInt = 1 с','ST = (256 − 100) / 256 = 0,609375 с','MDI = 3 × 1 + 0,609375','MDI ≈ 3,609 с'),box('Pri = 200; AdvertInt = 1 с','ST = (256 − 200) / 256 = 0,21875 с','MDI = 3 × 1 + 0,21875','MDI ≈ 3,219 с'),L.foot('Больший приоритет → меньший Skew Time → меньшее ожидание'))
    emit(16,'Тренажёр таймера','<div class="v-live" data-timer><label>Приоритет Backup: <strong data-priority>100</strong><input aria-label="Приоритет Backup" data-priority-input type="range" min="1" max="254" value="100"></label><label>Интервал анонса: <select aria-label="Интервал анонса" data-advert><option value="1">1 секунда</option><option value="2">2 секунды</option><option value="3">3 секунды</option></select></label><output data-mdi></output><p data-skew></p><p>Измените приоритет и сравните время перехода в Master.</p></div>',fig(F.states()))
    # PPTX 17
    emit(17,'Шкала Priority',K.table(['Значение','Назначение'],[['0','Master сообщает о прекращении участия'],['1…254','Настраиваемый приоритет'],['100','Значение по умолчанию'],['255','Владелец виртуального IP']]),box('Правило выбора','Чем больше Priority, тем выше шанс стать Master','При равенстве сравнивается IP','Значения 0 и 255 имеют специальный смысл'),green=True)
    # PPTX 18
    terminal(18,'Команды настройки VRRP')
    # PPTX 19
    emit(19,'Приоритетное вытеснение',box('Preempt = True','Backup с большим приоритетом может принять роль Master','Возвратившийся основной маршрутизатор снова получает активную роль','В исходном примере Preempt включён по умолчанию'),box('Preempt = False','Больший приоритет сам по себе не вытесняет работающий Master','При отказе Master резервный всё равно может принять роль','Отключение уменьшает число переключений при возврате узла'))
    emit(19,'Возвращение основного маршрутизатора',fig(F.preempt()),bottom=L.foot('Проверьте настройку вытеснения до теста отказоустойчивости'))
    emit(19,'Команды Preempt',K.conf(['ESR(config-if-gi)#vrrp preempt disable'],'Отключить вытеснение'),K.conf(['ESR(config-if-gi)#no vrrp preempt disable'],'Включить вытеснение'),L.foot('Команды выполняются в режиме настройки интерфейса'))
    # PPTX 20–21
    terminal(20,'Диагностика VRRP');terminal(21,'Подробная диагностика VRRP')
    # PPTX 22
    emit(22,'Пример 1: VLAN 10',fig(F.topology()),box('Параметры','Сеть: 10.10.1.0/24; шлюз: 10.10.1.1','R1: Gi1/0/1, 10.10.1.2, Priority 110','R2: Gi1/0/2, 10.10.1.3, Priority 100','VRID 100; PC-1 и PC-4 в VLAN 10'),L.foot('R1 — предпочтительный Master; R2 — Backup'))
    emit(22,'План настройки VLAN 10',box('Маршрутизаторы','Настроить R1 как предпочтительный Master','Настроить R2 как Backup'),box('Коммутаторы','Назначить VLAN 10 на портах к PC-1 и PC-4','Разрешить VLAN 10 между SW1 и SW2'),L.foot('Виртуальный шлюз должен быть доступен через оба маршрутизатора'))
    # PPTX 23–25
    terminal(23,'Пример 1: адреса и VRID');terminal(24,'Пример 1: приоритет и запуск');terminal(25,'Пример 1: коммутаторы')
    # PPTX 26
    emit(26,'Пример 2: два VLAN',fig(F.topology(mode='dual')),box('Разделение ролей','VLAN 10: 10.10.1.0/24, VIP 10.10.1.1, VRID 100','VLAN 20: 10.10.2.0/24, VIP 10.10.2.1, VRID 200','R1 — Master для VRID 100','R2 — Master для VRID 200'),L.foot('Две группы VRRP позволяют разделить активные роли'))
    emit(26,'План настройки двух VLAN',box('R1 и R2','Создать Gi1/0/1.10 и Gi1/0/1.20','Для VRID 100: R1 Master, R2 Backup','Для VRID 200: R2 Master, R1 Backup'),box('SW1 и SW2','PC-1 и PC-4 → VLAN 10','PC-2 и PC-3 → VLAN 20','Разрешить VLAN 10 и 20 на транковых каналах'))
    # PPTX 27–29
    terminal(27,'Пример 2: подинтерфейсы');terminal(28,'Пример 2: группы VRRP');terminal(29,'Пример 2: VLAN и trunk')
    (HERE/'_vrrp_assets/slide-map.json').write_text(json.dumps(MAP,ensure_ascii=False,indent=2),encoding='utf8')
