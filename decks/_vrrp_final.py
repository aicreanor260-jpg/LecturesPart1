"""Практика VRRP на фактах исходной презентации."""
import _sw_lib as L
import _pt_kit as K
from _vrrp_deck import emit,box,fig
import _vrrp_fig as F

def lab(kind):
    return '''<div class="v-lab v-cli" data-lab="%s"><div class="c"><div class="qt">Задание</div><div data-cli-task class="v-result"></div><div class="v-buttons"><button data-cli-action="new">Новое задание</button><button data-cli-action="check">Проверить</button><button data-cli-action="solution">Решение</button><button data-cli-action="send">Отправить пакет</button><button data-cli-action="reconnect">Подключиться заново</button></div><div data-cli-result class="v-result" aria-live="polite"></div><pre data-cli-solution class="v-solution" hidden></pre><p style="margin-top:16px;font-size:16px">Учебная модель ESR. Команды не отправляются на реальное оборудование.</p></div><div class="v-terminal"><header>ELTEX ESR · VRRP LAB</header><div data-cli-out class="v-output" role="log" aria-live="polite"></div><label class="v-input"><span data-cli-prompt></span><input data-cli-input aria-label="Команда ESR" spellcheck="false" autocomplete="off" placeholder="Введите команду"></label></div></div>'''%kind

def build():
    emit(0,'Шпаргалка: настройка VRRP',K.conf(['ESR#configure','ESR(config)#interface gigabitethernet 1/0/1','ESR(config-if-gi)#ip address 10.10.1.2/24','ESR(config-if-gi)#ip firewall disable','ESR(config-if-gi)#vrrp id 100','ESR(config-if-gi)#vrrp ip 10.10.1.1','ESR(config-if-gi)#vrrp priority 110','ESR(config-if-gi)#vrrp','ESR(config-if-gi)#do commit','ESR(config-if-gi)#do confirm']),bottom=L.foot('Пример R1: VLAN 10, VRID 100, приоритет 110'))
    emit(0,'Шпаргалка: проверка',K.conf(['ESR#show vrrp','ESR#show vrrp 100','ESR#show running-config interfaces gigabitethernet 1/0/1']),box('Проверить','VRID и виртуальный IP совпадают у участников группы','Роли соответствуют приоритетам и Preempt','При отказе Master резервный принимает обслуживание шлюза'))
    emit(0,'Задачи: MAC и таймер',L.task('vrrp-mac','VRID = 100. Какой последний октет виртуального MAC?','64|0x64','100 в десятичной записи = 64 в шестнадцатеричной.'),L.task('vrrp-mdi','Pri = 100, AdvertInt = 1 с. MDI с точностью до 0,001 с?','3,609|3.609|3,609 с|3.609 с','ST = 156 / 256 = 0,609375 с. MDI = 3 + ST ≈ 3,609 с.'))
    emit(0,'Задачи: выбор Master',L.task('vrrp-role','R1: Priority 110. R2: Priority 100. Кто предпочтительный Master?','R1|Р1','Приоритет R1 больше: 110 > 100.'),L.task('vrrp-vlan','В примере двух VLAN кто Master для VRID 200?','R2|Р2','Для VLAN 20 (VRID 200) активная роль назначена R2.'))
    emit(0,'Тренажёр: роли и пакеты',K.sorter('vrrp-roles',['Master','Backup'],[('Отвечает на ARP для виртуального IP',0),('Маршрутизирует трафик на виртуальный MAC',0),('Рассылает анонсы VRRP',0),('Следит за Master Down Interval',1),('Готов принять роль после отказа Master',1),('Не отвечает на ARP вместо действующего Master',1)],'Выберите действие, затем нажмите на соответствующую роль.'))
    emit(0,'CLI: виртуальный шлюз',lab('single'))
    emit(0,'CLI: два виртуальных шлюза',lab('dual'))
    questions=[
      ('Для чего VRRP нужен оконечному устройству?',['Для резервирования шлюза по умолчанию','Для выбора DNS','Для назначения VLAN'],0,'VRRP повышает доступность первого перехода.'),
      ('Кто отвечает на ARP для виртуального IP?',['Любой Backup','Действующий Master','Оба маршрутизатора одновременно'],1,'Master обслуживает виртуальный адрес.'),
      ('Какой VRID соответствует MAC …:64?',['64','100','200'],1,'0x64 = 100.'),
      ('Обычный настраиваемый диапазон Priority?',['0…255','1…254','100…200'],1,'0 и 255 имеют специальный смысл.'),
      ('IP назначения анонса VRRP для IPv4?',['224.0.0.18','255.255.255.255','10.10.1.1'],0,'Групповой адрес анонсов — 224.0.0.18.'),
      ('Какое значение TTL ожидается в анонсе?',['1','64','255'],2,'Пакет с другим TTL отбрасывается.'),
      ('Что означает Priority 255?',['Владелец виртуального IP','Выключенный интерфейс','Резервный узел по умолчанию'],0,'Владелец виртуального IP имеет приоритет 255.'),
      ('Из чего складывается MDI?',['3 × AdvertInt + ST','AdvertInt / Priority','Priority × ST'],0,'Три интервала анонса плюс Skew Time.'),
      ('Что меняет отключение Preempt?',['Backup не заменит отказавший Master','Больший приоритет не вытеснит работающий Master','VRRP перестаёт отправлять анонсы'],1,'При отказе Master переключение по таймеру сохраняется.'),
      ('Команда просмотра всех процессов VRRP?',['show vlan','show vrrp','vrrp show all'],1,'show vrrp выводит состояние виртуальных маршрутизаторов.'),
      ('Какая команда включает VRRP на интерфейсе?',['vrrp','vrrp start','ip vrrp enable'],0,'В исходном синтаксисе ESR используется команда vrrp.'),
      ('Что нужно разрешить на trunk в примере двух VLAN?',['Только VLAN 10','Только VLAN 20','VLAN 10 и 20'],2,'По транку должны проходить обе сети.')]
    for i in range(0,len(questions),4):
        qs=[L.quiz(*q) for q in questions[i:i+4]]
        emit(0,'Тест · '+str(i//4+1),L.g('g2',L.col(*qs[:2]),L.col(*qs[2:])),bottom='<div class="v-meta">Результат: <span class="score">0 / 12</span></div>')
    emit(0,'Что запомнить',box('Виртуальный шлюз','VRID связывает участников одной группы','IP и MAC шлюза сохраняются при смене Master','Master обслуживает трафик; Backup следит за анонсами'),box('Настройка и проверка','Priority определяет предпочтительную активную роль','MDI задаёт ожидание отказавшего Master','Preempt управляет вытеснением работающего Master','show vrrp показывает состояние'),green=True)
    emit(0,'Материалы и уточнения',box('Основа лекции','Презентация «2.8. Избыточность на уровне L3. VRRP»','Схемы повторяют адреса и порты исходных примеров','Команды ESR/MES и диагностические выводы перенесены со скриншотов'),'<div class="c"><div class="ch"><h3>Технические уточнения</h3></div><p>В исходном тексте слайда 8 указан MAC …:18. Для 224.0.0.18 сопоставление multicast MAC — <b>01:00:5E:00:00:12</b>.</p><p>TTL 255 позволяет проверить локальное происхождение анонса; это не криптографическое подтверждение отправителя.</p><p>Таймер Backup обновляется допустимыми анонсами. Вытеснение учитывает истечение таймера, а не мгновенную смену по одному пакету.</p><p><a href="https://www.rfc-editor.org/rfc/rfc3768.html" target="_blank" rel="noopener">RFC 3768 · VRRPv2</a></p></div>')
    L.slide('Финал · Вопросы','<div class="v-cover"><div class="kicker">Коммутация · 2.8</div><h1>Вопросы?</h1><h2>Объясните переключение шлюза по шагам</h2><p>Кто Master? Кто Backup?<br>Какой адрес видит ПК?<br>Что произойдёт после отказа и возврата R1?</p><p><a href="index.html" style="color:#f5d48c">Каталог лекций</a></p></div>',cover=True)
