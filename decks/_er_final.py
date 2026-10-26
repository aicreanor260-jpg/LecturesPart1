# -*- coding: utf-8 -*-
"""Титул и финальные блоки деки «Маршрутизаторы ESR»: шпаргалка → задачи → тренажёры → тренажёр CLI → тест → итоги → финал.
Все команды и ответы — строго по материалу pptx 2.3."""

from _sw_lib import slide, head, sc, grow, col, card, li, p, step, task, quiz, tags, tag
from _er_deck import conf


def cover():
    slide("Титул", sc(
        '<div class="cover"><div class="big">Маршрутиза&shy;торы<br><em>Eltex ESR</em></div>'
        '<div class="lead">Интерфейсы, базовая настройка, проверка соединения, AAA и учётные записи.</div>%s'
        '<div class="lead" style="font-size:clamp(12px,.95vw,17px)">← → шаги · ↑ ↓ слайды · Esc — содержание · '
        'в сценах кнопки «Назад / Вперёд»</div></div>'
        % tags(tag("Раздел 2.3"), tag("ESR", "v"), tag("ICMP", "g"), tag("AAA", "y"))), cover=True)


def _qslide(title, qs):
    slide(title, sc(head(title.replace("Тест", "<em>Тест</em>"), "Выберите один вариант. Объяснение появится после ответа."),
                    grow("g2", col(*qs[:2]), col(*qs[2:])),
                    '<div class="foot" style="margin-top:8px"><i>✓</i><span>Результат по всем вопросам: '
                    '<span class="score">0 / 0</span></span></div>'))


def _sim(label, title, sub, pool):
    slide(label, sc(head("Тренажёр <em>CLI</em>: " + title, sub), grow("g", col(
        '<div class="clisim" data-deck="esr" data-pool="%s">'
        '<div class="cs-side"><div class="cs-h">Задание</div><div class="cs-task"></div>'
        '<div class="cs-btns"><button data-cs="new">↻ Обновить задание</button><button data-cs="check">Проверить</button>'
        '<button data-cs="send" class="alt">Отправить ping</button><button data-cs="sol" class="sec">Решение</button></div>'
        '<div class="cs-res"></div><pre class="cli cs-sol" style="display:none"></pre></div>'
        '<div class="cs-term"><div class="cs-bar"><i></i><i></i><i></i><span>Console · Eltex ESR-200</span></div>'
        '<div class="cs-out"></div><label class="cs-in"><span class="cs-pr"></span>'
        '<input type="text" spellcheck="false" autocomplete="off" placeholder="введите команду и нажмите Enter"></label></div></div>'
        % ",".join(str(i) for i in pool)))))


def tail():
    slide("Шпаргалка команд", sc(head("Шпаргалка <em>команд</em>", "Команды лекции — в том же синтаксисе, что на слайдах."),
        grow("g2",
             col(step(conf(["esr-200(change-expiredpassword)# password <новый пароль>", "esr-200# configure",
                            "esr-200(config)# hostname R1", "esr-200(config)# exit", "esr-200# commit", "R1# confirm",
                            "esr-200(config)# interface gigabitethernet 1/0/1",
                            "esr-200(config-if-gi)# ip address 192.168.25.25/24", "esr-200(config-if-gi)# ip firewall disable",
                            "esr-200(config-if-gi)# speed auto", "esr-200(config)# interface loopback1",
                            "esr-200(config)# interface gigabitethernet 1/0/1.20",
                            "esr-200(config)# interface gigabitethernet 1/0/1.20.420"], "Пароль · имя · интерфейсы"))),
             col(step(conf(["esr-200(config)# ip ssh server", "esr-200# set date 17:23:55 09 October 2023",
                            "esr-200(config)# clock timezone gmt +7", "esr-200(config)# banner login <текст>",
                            "esr-200(config)# banner exec <текст>", "esr-200(config)# username user1",
                            "esr-200(config-user)# password eltex", "esr-200(config-user)# privilege 9",
                            "R1(config-user)# password encrypted <хэш функция>",
                            "esr(config)# aaa authentication attempts max-fail <N> <время>",
                            "esr(config)# aaa authentication login <ИМЯ СПИСКА> <СПОСОБ1> …",
                            "R1(config)# line console", "R1(config-line-console)# aaa disable"], "Сервисы · AAA · пользователи") +
                      conf(["esr-200# show interfaces status", "esr-200# show date", "R1# show user accounts",
                            "esr# show users blocked", "esr# clear users blocked", "R1# show aaa authentication"], "Проверка"))))))
    slide("Итоговые задачи", sc(head("Итоговые <em>задачи</em>", "Рассуждаем и вводим ответ."), grow("g2",
        col(task("er1", "Вы ввели hostname R1 в режиме (config)#, но приглашение всё ещё esr-200. Какую команду нужно выполнить "
                        "в привилегированном режиме, чтобы имя применилось?", "commit",
                 "Имя применяется командой <b>commit</b>, затем подтверждается командой confirm.", "команда"),
            task("er2", "PC1 (192.168.10.10) отправляет пакет PC3 (192.168.11.10). На какой адрес шлюза PC1 отправит пакет, "
                        "если gi 1/0/1 R1 имеет адрес .1 в сети 192.168.10.0/24?", "192.168.10.1",
                 "PC3 в другой сети, поэтому пакет идёт на шлюз по умолчанию — <b>192.168.10.1</b>.", "IP-адрес")),
        col(task("er3", "Какие UDP-порты использует RADIUS для аутентификации и учёта? (через пробел)", "1812 1813|1812,1813|1812 и 1813",
                 "<b>1812</b> — аутентификация, <b>1813</b> — учёт.", "порты"),
            task("er4", "Сколько неверных вводов пароля по умолчанию приводит к блокировке пользователя ESR?", "5|пять",
                 "<b>5 раз</b> — блокировка на 300 секунд.", "число")))))
    slide("Тренажёр: какое ICMP", sc(head("<em>Тренажёр</em>: тип и код ICMP", "По описанию — значения полей Тип и Код из таблицы pptx."),
        grow("g2",
             col(task("ic1", "Эхо-запрос (ping): Тип / Код?", "8 0|8/0|8,0", "Тип <b>8</b>, код <b>0</b>.", "тип код"),
                 task("ic2", "Эхо-ответ: Тип / Код?", "0 0|0/0|0,0", "Тип <b>0</b>, код <b>0</b>.", "тип код")),
             col(task("ic3", "Хост недоступен: Тип / Код?", "3 1|3/1|3,1", "Тип <b>3</b>, код <b>1</b>.", "тип код"),
                 task("ic4", "Переадресация: Тип / Код?", "5 0|5/0|5,0", "Тип <b>5</b>, код <b>0</b>.", "тип код")))))
    slide("Тренажёр: уровни привилегий", sc(head("<em>Тренажёр</em>: уровни привилегий",
                                                  "Какой минимальный уровень группы подходит пользователю?"), grow("g2",
        col(task("pr1", "Нужно создавать пользователей и загружать ПО. Какой уровень?", "15",
                 "Только <b>15</b> уровень разрешает всё без ограничений.", "уровень"),
            task("pr2", "Только мониторинг части функционала (15 команд), без настройки. Группа уровней?", "1-4|1 - 4|1–4",
                 "Уровни <b>1 - 4</b>.", "например 1-4")),
        col(task("pr3", "Просмотр оперативного состояния функционала безопасности, настройка запрещена. Группа?", "5-9|5 - 9|5–9",
                 "Уровни <b>5 - 9</b>.", "группа"),
            task("pr4", "До какого уровня рекомендуется понизить пользователя admin?", "1",
                 "Admin — сложный пароль и уровень <b>1</b>.", "уровень")))))
    _sim("Тренажёр CLI: базовая настройка", "базовая настройка", "Имя, первый вход, баннеры, часовой пояс — с commit и confirm.", [0, 1, 6, 7])
    _sim("Тренажёр CLI: интерфейсы", "интерфейсы", "Физический, loopback, sub и QinQ. «Отправить ping» проверит связность.", [2, 3, 4])
    _sim("Тренажёр CLI: пользователи и AAA", "пользователи и AAA", "Учётные записи, ssh, линии, блокировка.", [5, 8, 9])
    _qslide("Тест · 1", [
        quiz("На каком уровне модели OSI работает маршрутизатор?", ["1", "2", "3 (сетевом)", "7"], 2,
             "Маршрутизаторы работают на сетевом уровне."),
        quiz("Стандартные логин и пароль ESR?", ["admin / admin", "admin / password", "root / eltex", "techsupport / password"], 1,
             "Логин admin, пароль password."),
        quiz("Зачем на интерфейсе ESR выполняют ip firewall disable в этом курсе?",
             ["ускорить порт", "межсетевой экран включён на всех портах и блокирует трафик", "включить ssh", "сохранить конфигурацию"], 1,
             "Без настройки межсетевой экран блокирует весь трафик, маршрутизация невозможна."),
        quiz("Что означает 20 в interface gigabitethernet 1/0/1.20?", ["номер порта", "VLAN-тег", "MTU", "приоритет"], 1,
             "Числовой идентификатор VLAN-тега после точки."),
    ])
    _qslide("Тест · 2", [
        quiz("Сколько IP-адресов можно настроить на loopback?", ["1", "2", "до 8", "без ограничений"], 2, "До 8 IP-адресов."),
        quiz("Какой протокол удалённого управления рекомендуют?", ["telnet", "ssh", "http", "ftp"], 1,
             "ssh передаёт данные в зашифрованном виде."),
        quiz("Когда выводится banner exec?", ["перед авторизацией", "после авторизации", "при commit", "при перезагрузке"], 1,
             "banner login — перед авторизацией, banner exec — после."),
        quiz("Какое значение TTL отправитель ставит в первом пакете tracert?", ["0", "1", "64", "255"], 1,
             "Сначала TTL = 1, затем 2 и т. д."),
    ])
    _qslide("Тест · 3", [
        quiz("Что обозначают звёздочки * * * в traceroute?",
             ["узел назначения", "устройства с фильтрацией ICMP / без ответа", "лучший маршрут", "ошибка DNS"], 1,
             "Устройства с фильтрацией ICMP-запросов (пакеты без ответа или потерянные)."),
        quiz("В каком протоколе аутентификация и авторизация объединены, отдельной стадии авторизации нет?",
             ["TACACS+", "RADIUS", "LDAP", "ICMP"], 1,
             "RADIUS объединяет процессы аутентификации и авторизации."),
        quiz("По какому признаку NAS определяет домен пользователя?", ["по IP", "по строке после @ в имени", "по MAC", "по VLAN"], 1,
             "Домен — строка после разделителя @."),
        quiz("Режим aaa authentication mode по умолчанию?", ["break", "chain", "local", "radius"], 1, "chain — по умолчанию."),
    ])
    _qslide("Тест · 4", [
        quiz("Каким алгоритмом хранится пароль пользователя в конфигурации?", ["MD5", "SHA512", "открытым текстом", "DES"], 1,
             "Хэш-функция по алгоритму SHA512."),
        quiz("Что делает no username admin?", ["удаляет admin", "удаляет только пароль, ставит password", "блокирует admin", "ничего"], 1,
             "Удалить admin нельзя — сбрасывается пароль на password."),
        quiz("Какая команда переносит пароль как хэш на другое устройство?",
             ["password hash", "password encrypted", "secret", "crypto key"], 1, "password encrypted &lt;хэш функция&gt;."),
        quiz("Что делает aaa disable в line console?", ["включает ssh", "запрещает подключение через console",
                                                         "сбрасывает пароль", "включает учёт"], 1,
             "Подключение через console будет запрещено."),
    ])
    slide("Что запомнить", sc(head("Что <em>запомнить</em>", "Короткая выжимка лекции."), grow("g3",
        col(step(card("Настройка ESR", li([
            "Первый вход: admin / password → смена пароля (≥ 8 символов).",
            "Любая настройка: <b>commit</b> → <b>confirm</b>.",
            "gi1/0/n, loopback, sub .20, QinQ .20.420; <b>ip firewall disable</b>."]), "cy"))),
        col(step(card("Проверка", li([
            "show interfaces status, show ip route, show arp.",
            "ping — эхо-запрос / эхо-ответ ICMP.",
            "traceroute — TTL = 1, 2, 3 …, «* * *» — фильтрация ICMP."]), "mg"))),
        col(step(card("AAA", li([
            "Аутентификация, авторизация, учёт.",
            "Локально или RADIUS (UDP 1812/1813), TACACS, LDAP.",
            "Уровни 1–15; блокировка 5 попыток / 300 с."]), "lm"))))))
    slide("Финал", sc(head("<em>Спасибо</em> за внимание", "Раздел 2.3 · Маршрутизаторы Eltex ESR"), grow("g2",
        col(step(card("Что дальше", li(["Статическая и динамическая маршрутизация.", "Лабораторная работа по базовой настройке ESR."]), "cy"))),
        col(step(card("Контакты", tags(tag("VKontakte", "v"), tag("Telegram")) + p("Вопросы по лекции и лабораторным — пишите."), "mg"))))))
