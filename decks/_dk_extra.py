# -*- coding: utf-8 -*-
"""Титулы, цели, задачи, тесты и финалы дек-спутников (base / vlan)."""

import re

from _sw_lib import (slide, head, sc, grow, col, card, p, li, foot, tags, tag, table,
                     step, task, quiz)
from _dk_kit import conf


def cli(lines, title=""):
    """Команды шпаргалки: та же подсветка, что в слайдах с конфигурацией."""
    return conf([re.sub(r"<[^>]+>", "", l) for l in lines], title)


def _cover(big, lead, tg):
    slide("Титул", sc(
        '<div class="cover"><div class="big">%s</div><div class="lead">%s</div>%s'
        '<div class="lead" style="font-size:clamp(12px,.95vw,17px)">← → шаги · ↑ ↓ слайды · '
        'Esc — содержание · в сценах кнопки «Назад / Вперёд»</div></div>' % (big, lead, tg)), cover=True)


def _qslide(title, sub, qs):
    slide(title, sc(
        head(title.replace("Тест", "<em>Тест</em>"), sub),
        grow("g2", col(*qs[:2]), col(*qs[2:])),
        '<div class="foot" style="margin-top:8px"><i>✓</i><span>Результат: <span class="score">0 / 0</span></span></div>'
    ))


def _final(sub, nxt):
    slide("Финал", sc(
        head("<em>Спасибо</em> за внимание", sub),
        grow("g2",
             col(step(card("Что дальше", li(nxt), "cy"))),
             col(step(card("Контакты", tags(tag("VKontakte", "v"), tag("Telegram")) +
                           p("Вопросы по лекции и лабораторным — пишите."), "mg"))))
    ))


# ====================================================================== BASE
def base_head():
    _cover("Базовая<br><em>настройка</em><br>коммутатора",
           "Подключение через консоль, SSH и Web, имя устройства, баннеры, "
           "учётные записи и уровни привилегий на коммутаторах Eltex.",
           tags(tag("Раздел 2.2"), tag("Eltex", "v"), tag("CLI", "g"), tag("SSH", "y"), tag("AAA", "r")))
    slide("Цель главы", sc(
        head("Цель <em>главы</em>", "Что вы будете уметь после занятия."),
        grow("g2",
             col(step(card("Подключаться", p(
                 "Выбирать способ подключения — <b>консоль</b>, <b>SSH/Telnet</b> или <b>Web</b> — "
                 "и настраивать терминал: 115200 бод, 8N1, без управления потоком, VT100."), "cy", "1")),
                 step(card("Идентифицировать", p(
                     "Задавать <b>имя устройства</b> командой hostname и <b>баннеры</b> "
                     "banner login / banner exec."), "mg", "2"))),
             col(step(card("Защищать доступ", p(
                 "Ставить пароль на консоль, <b>exec-timeout</b>, включать SSH-сервер и генерировать ключи RSA."), "lm", "3")),
                 step(card("Разделять полномочия", p(
                     "Создавать и удалять <b>учётные записи</b> с уровнями privilege 1–15 и "
                     "временно повышать права командой <b>enable</b>."), "am", "4")))),
        step(foot("Пароли в примерах — только учебные. В действующих сетях используйте надёжные уникальные пароли.", "warn"))
    ))


def base_tail():
    slide("Шпаргалка команд", sc(
        head("Шпаргалка <em>команд</em>", "Всё, что нужно для базовой настройки, на одном слайде."),
        grow("g2",
             col(step(cli([
                 "<span class=\"p\">console#</span> configure",
                 "<span class=\"p\">(config)#</span> <span class=\"k\">hostname</span> SW1-Room502",
                 "<span class=\"p\">(config)#</span> <span class=\"k\">banner login</span> @ Unauthorized access prohibited! @",
                 "<span class=\"p\">(config)#</span> <span class=\"k\">banner exec</span> @ Welcome! @",
                 "<span class=\"p\">(config)#</span> <span class=\"k\">username</span> admin1 password admin1 privilege 15",
                 "<span class=\"p\">(config)#</span> <span class=\"k\">no username</span> admin1",
                 "<span class=\"p\">(config)#</span> <span class=\"k\">enable password level</span> 4 eltex4",
             ], "Имя · баннеры · пользователи"))),
             col(step(cli([
                 "<span class=\"p\">(config)#</span> <span class=\"k\">line console</span>",
                 "<span class=\"p\">(config-line)#</span> password consolepass",
                 "<span class=\"p\">(config-line)#</span> exec-timeout 5",
                 "<span class=\"p\">(config)#</span> <span class=\"k\">interface vlan</span> 20",
                 "<span class=\"p\">(config-if)#</span> ip address 10.10.1.28 /24",
                 "<span class=\"p\">(config)#</span> <span class=\"k\">ip default-gateway</span> 10.10.1.1",
                 "<span class=\"p\">(config)#</span> <span class=\"k\">ip ssh server</span>",
                 "<span class=\"p\">(config)#</span> <span class=\"k\">crypto key generate rsa</span>",
                 "<span class=\"p\">(config)#</span> <span class=\"k\">no ip http server</span>",
             ], "Консоль · SSH · Web")))),
    ))
    slide("Итоговые задачи", sc(
        head("Итоговые <em>задачи</em>", "Рассуждаем и вводим ответ."),
        grow("g2",
             col(task("bz1", "Вы создали пользователя admin1 с privilege 15. Будет ли теперь работать "
                             "заводская учётная запись admin / admin?",
                      "нет|не будет|no",
                      "Заводская запись admin перестаёт действовать после появления первой учётной записи "
                      "с уровнем привилегий 15. Ответ — <b>нет</b>.", "да / нет"),
                 task("bz2", "Какой адрес нужно ввести в браузере для первого входа в Web-интерфейс нового коммутатора Eltex?",
                      "192.168.1.239|http://192.168.1.239",
                      "Адрес <b>192.168.1.239</b> установлен на SVI VLAN 1, протокол HTTP.", "IP-адрес")),
             col(task("bz3", "Сколько минут бездействия задаёт команда exec-timeout 5?",
                      "5|пять",
                      "<b>5 минут</b>: после этого сессия сбрасывается, и пароль нужно ввести снова.", "минут"),
                 task("bz4", "Какой уровень привилегий нужен, чтобы войти в Web-интерфейс?",
                      "15|privilege 15",
                      "Подключение по Web-интерфейсу разрешено только пользователю с максимальным уровнем — "
                      "<b>privilege 15</b>.", "уровень")))
    ))
    _qslide("Тест · 1", "Выберите один вариант. Объяснение появится после ответа.", [
        quiz("Какая скорость терминала нужна для консольного подключения к Eltex?",
             ["9600", "19200", "57600", "115200"], 3,
             "115200 бод. Автоопределение есть не везде, скорость лучше выставить вручную."),
        quiz("Какой разъём консольного кабеля подключается к коммутатору?",
             ["RS-232", "RJ-45", "USB-C", "SFP"], 1,
             "Со стороны коммутатора — RJ-45, со стороны компьютера — RS-232 (или адаптер RS-232–USB)."),
        quiz("Какое имя по умолчанию у коммутаторов Eltex?",
             ["switch", "eltex", "console", "router"], 2,
             "Все коммутаторы Eltex по умолчанию имеют имя console."),
        quiz("Как задать имя устройства с пробелами?",
             ["через подчёркивания", "в кавычках", "нельзя", "через banner"], 1,
             "hostname \"SW1 Room502 Floor5\" — имя с пробелом указывается в кавычках."),
    ])
    _qslide("Тест · 2", "Продолжаем.", [
        quiz("Когда показывается banner exec?",
             ["до ввода логина", "после входа в режим пользователя",
              "при перезагрузке", "при ошибке пароля"], 1,
             "banner login — до ввода логина и пароля, banner exec — после попадания в режим пользователя."),
        quiz("Что означает атрибут encrypted в строке username?",
             ["пароль зашифрован SSH", "вместо пароля хранится его хеш",
              "пользователь заблокирован", "пароль временный"], 1,
             "В конфигурации хранится хеш пароля; encrypted говорит устройству, что строка — уже хеш."),
        quiz("Что делает команда enable без указания уровня?",
             ["понижает до уровня 1", "повышает до уровня 15",
              "перезагружает коммутатор", "сохраняет конфигурацию"], 1,
             "Повышает уровень сразу до 15 после ввода пароля enable."),
        quiz("Что нужно для подключения по SSH, кроме включения ip ssh server?",
             ["только пароль консоли", "VLAN управления, IP на её SVI и ключи RSA",
              "Web-интерфейс", "Telnet"], 1,
             "VLAN управления на портах, IP-адрес на SVI, шлюз по умолчанию, ключи RSA и параметры line ssh."),
    ])
    slide("Что запомнить", sc(
        head("Что <em>запомнить</em>", "Короткая выжимка лекции."),
        grow("g3",
             col(step(card("Подключение", li([
                 "Консоль: RJ-45 ↔ RS-232, <b>115200 8N1</b>, VT100.",
                 "SSH: VLAN управления + IP на SVI + ключи RSA.",
                 "Web: <b>192.168.1.239</b>, admin / admin, только privilege 15."]), "cy"))),
             col(step(card("Идентификация", li([
                 "<b>hostname</b> — до 128 символов, с пробелами в кавычках.",
                 "<b>banner login</b> — до логина, <b>banner exec</b> — после входа.",
                 "Разделитель текста баннера — символ @."], "mg"), "mg"))),
             col(step(card("Права", li([
                 "Уровни привилегий <b>1–15</b>.",
                 "admin / admin отключается после первого пользователя с privilege 15.",
                 "<b>enable</b> [уровень] — временное повышение прав."], "lm"), "lm")))),
    ))
    _final("Раздел 2.2 · Базовая настройка коммутатора", [
        "Виртуальные локальные сети VLAN и режимы портов.",
        "Удалённое администрирование и AAA.",
        "Сохранение и резервное копирование конфигурации."])


# ====================================================================== VLAN
def vlan_head():
    _cover("Виртуальные<br>локальные сети<br><em>VLAN</em>",
           "Широковещательные домены, тег IEEE 802.1Q, процесс тегирования, "
           "типы VLAN и режимы портов access, trunk, general и customer (Q-in-Q).",
           tags(tag("Раздел 2.2"), tag("802.1Q", "v"), tag("PVID", "g"), tag("Trunk", "y"), tag("Q-in-Q", "r")))
    slide("Цель главы", sc(
        head("Цель <em>главы</em>", "Четыре результата занятия."),
        grow("g2",
             col(step(card("Зачем VLAN", p(
                 "Понять, почему один большой широковещательный домен L2 перегружает сеть "
                 "и как VLAN делят его на независимые логические сегменты."), "cy", "1")),
                 step(card("Тег 802.1Q", p(
                     "Разобрать метку: <b>TPID 0x8100</b>, <b>PCP</b>, <b>DEI</b>, <b>VLAN ID</b> (12 бит) — "
                     "и где она вставляется в кадр."), "mg", "2"))),
             col(step(card("Тегирование", p(
                 "Проследить путь кадра: классификация на входе, фильтрация, "
                 "добавление и снятие тега, пересчёт FCS."), "lm", "3")),
                 step(card("Режимы портов", p(
                     "Настраивать <b>access</b>, <b>trunk</b> с native VLAN, <b>general</b> и "
                     "<b>customer</b> (Q-in-Q) на Eltex."), "am", "4")))),
    ))


def vlan_tail():
    # шпаргалка — только команды из pptx, в том же синтаксисе
    slide("Шпаргалка команд", sc(
        head("Шпаргалка <em>команд</em>", "Все команды лекции — как в слайдах."),
        grow("g2",
             col(step(cli([
                 "switch(config)# vlan 10", "switch(config-vlan)# name IT",
                 "switch(config)# no vlan 10", "switch# show vlan",
                 "switch(config)#interface gigabitethernet 1/0/1",
                 "switch(config-if)#switchport mode access",
                 "switch(config-if)#switchport access vlan 10",
                 "switch(config)#interface range gigabitethernet 1/0/1-4",
                 "switch(config-if)# no switchport access vlan",
                 "switch# show interfaces switchport gigabitethernet 1/0/1",
             ], "VLAN · access"))),
             col(step(cli([
                 "switch(config-if)# switchport mode trunk",
                 "switch(config-if)# switchport trunk allowed vlan add Num1,Num2,…,NumX",
                 "switch(config-if)# switchport trunk allowed vlan remove Num1,Num2,…,NumX",
                 "switch(config-if)# switchport trunk native vlan Num",
                 "switch(config-if)#switchport mode general",
                 "switch(config-if)#switchport general pvid 10",
                 "switch(config-if)#switchport general allowed vlan add 10 untagged",
                 "switch(config-if)#switchport general allowed vlan add 10,20 tagged",
                 "switch(config-if)# selective-qinq list ingress add_vlan 25",
                 "switch(config-if)# switchport general map macs-group 1 vlan 10",
             ], "Trunk · general · Q-in-Q · MAC-based")))),
    ))
    slide("Итоговые задачи", sc(
        head("Итоговые <em>задачи</em>", "По материалу лекции. Вводим ответ."),
        grow("g2",
             col(task("vz1", "На коммутаторе VLAN 10 (порты 1–8) и VLAN 20 (порты 9–16). "
                             "Сколько широковещательных доменов?",
                      "2|два",
                      "Все порты в VLAN с одним номером — один широковещательный домен. VLAN две — доменов <b>два</b>.", "число"),
                 task("vz2", "Какое шестнадцатеричное значение появляется в поле TPID при тегировании по 802.1Q?",
                      "0x8100|8100",
                      "TPID = <b>0x8100</b> (1000 0001 0000 0000).", "значение")),
             col(task("vz3", "Транк: разрешены VLAN 10 и 20, нативная VLAN 30. С тегом или без уйдёт кадр VLAN 30?",
                      "без|без тега|без метки",
                      "На выходе транкового порта идентификатор нативной VLAN удаляется — кадр уходит <b>без тега</b>.", "с / без"),
                 task("vz4", "Какой номер VLAN на Eltex нельзя создать или удалить, потому что это VLAN по умолчанию?",
                      "1|vlan 1",
                      "<b>VLAN 1</b> — Default VLAN; вместе с 4095 она зарезервирована.", "номер")))
    ))
    _qslide("Тест · 1", "Выберите один вариант.", [
        quiz("Сколько байт занимает метка 802.1Q?", ["2", "4", "6", "8"], 1,
             "32 бита = 4 байта: TPID (2) + TCI (2)."),
        quiz("Куда вставляется метка 802.1Q?",
             ["перед Destination MAC", "после Source MAC", "после EtherType", "перед FCS"], 1,
             "Метка вставляется между Source MAC и EtherType."),
        quiz("Какое значение у TPID?", ["0x0800", "0x86DD", "0x8100", "0x88A8"], 2,
             "TPID = 0x8100 — признак тегированного кадра 802.1Q."),
        quiz("Сколько бит занимает VLAN ID?", ["3", "8", "12", "16"], 2,
             "VLAN ID — 12 бит, значения от 1 до 4095; на Eltex 1 и 4095 зарезервированы."),
    ])
    _qslide("Тест · 2", "Режимы портов.", [
        quiz("Какие кадры передаёт порт доступа (access)?",
             ["только тегированные", "нетегированные одной VLAN",
              "любые", "только служебные"], 1,
             "Access обслуживает одну VLAN, кадры уходят к устройству без тега."),
        quiz("Что такое native VLAN на транке?",
             ["VLAN управления", "VLAN, кадры которой идут без тега",
              "VLAN по умолчанию для всех портов", "запрещённая VLAN"], 1,
             "Нетегированный кадр на входе транка относится к native VLAN."),
        quiz("Какой режим позволяет на одном порту и tagged, и untagged VLAN?",
             ["access", "trunk", "general", "customer"], 2,
             "General (гибридный) — тегирование задаётся отдельно для каждой VLAN, PVID для нетегированных."),
        quiz("Для чего режим customer?",
             ["подключение IP-телефона", "Q-in-Q: внешняя метка провайдера",
              "агрегация каналов", "зеркалирование"], 1,
             "customer — Q-in-Q интерфейс: к кадру клиента (C-VLAN) добавляется внешний SPVLAN провайдера."),
    ])
    slide("Что запомнить", sc(
        head("Что <em>запомнить</em>", "Короткая выжимка лекции."),
        grow("g3",
             col(step(card("VLAN", li([
                 "VLAN — логически выделенный <b>широковещательный домен L2</b>.",
                 "Между VLAN трафик идёт только через L3-устройство.",
                 "Broadcast копируется только в порты своей VLAN."]), "cy"))),
             col(step(card("Тег 802.1Q", li([
                 "4 байта между Source MAC и EtherType.",
                 "TPID 0x8100 · PCP 3 бита · DEI 1 бит · VID 12 бит.",
                 "После добавления или снятия тега <b>FCS пересчитывается</b>."], "mg"), "mg"))),
             col(step(card("Порты", li([
                 "<b>access</b> — одна VLAN без тега.",
                 "<b>trunk</b> — много VLAN с тегом + одна native.",
                 "<b>general</b> — tagged и untagged; <b>customer</b> — Q-in-Q."], "lm"), "lm")))),
        step(foot("Тег добавляется на входе и снимается на выходе — внутри коммутатора кадр всегда «знает» свою VLAN.", "ok"))
    ))
    _final("Раздел 2.2 · Виртуальные локальные сети VLAN", [
        "Протоколы STP / RSTP / MSTP — защита от петель L2.",
        "Маршрутизация между VLAN на L3-коммутаторе.",
        "Агрегация каналов LAG / LACP."])
