# -*- coding: utf-8 -*-
"""Титул и финал деки MPLS 2.9: шпаргалка → задачи → тренажёры → живой тренажёр LSP → тест → итоги → финал.
Все ответы — строго по материалу pptx «2.9. MPLS». Команд CLI в pptx нет, поэтому живой тренажёр — таблицы
продвижения LSR со случайными заданиями (метки, Push/Swap/Pop, PHP, обход FRR) и отправкой пакета по LSP."""

from _sw_lib import slide, head, sc, grow, col, card, li, p, foot, step, task, quiz, tags, tag
from _mp_lib import tbl


def head_():
    slide("Титул", sc(
        '<div class="cover"><div class="big">MPLS</div>'
        '<div class="lead" style="font-size:clamp(18px,1.8vw,34px);font-weight:800">Технологии внутри оператора связи</div>'
        '<div class="lead">Раздел 2.9 · метки, LSP, LDP, RSVP-TE, LSP Ping, BFD, MPLS TE, быстрая защита, сегментная маршрутизация</div>'
        + tags(tag("2.9"), tag("LSP", "v"), tag("LDP", "g"), tag("RSVP-TE", "y"), tag("SR")) +
        '<div class="lead" style="font-size:clamp(12px,.95vw,17px)">← → шаги · ↑ ↓ слайды · Esc — содержание · '
        'в сценах кнопки «Назад / Вперёд»</div></div>'), cover=True)


head = head_  # noqa: F811  (имя, которое вызывает _mp_build)
from _sw_lib import head as H  # noqa: E402


def _qslide(title, qs):
    slide(title, sc(H(title.replace("Тест", "<em>Тест</em>"), "Выберите ответ — проверка сразу."),
                    grow("g2", col(*qs[:2]), col(*qs[2:])),
                    '<div class="foot" style="margin-top:8px"><i>✓</i><span>Результат по всем вопросам: '
                    '<span class="score">0 / 0</span></span></div>'))


def _tasks(title, items):
    slide(title, sc(H(title.replace("задачи", "<em>задачи</em>").replace("Тренажёр", "<em>Тренажёр</em>"),
                      "Введите ответ и нажмите «Проверить»."), grow("g2", col(*items[:2]), col(*items[2:]))))


def tail():
    # ---------------------------------------------------------------- шпаргалка
    slide("Шпаргалка", sc(H("Шпаргалка <em>MPLS</em>", "Термины, операции и числа лекции."), grow("g3",
        col(step(card("Роли и пути", li([
            "<b>LER</b> — пограничный: Ingress (FEC + Push), Egress",
            "<b>LSR</b> — коммутация по верхней метке, обычно Swap",
            "<b>CE / PE / P</b> — клиент / граница оператора / ядро",
            "<b>LSP</b> — однонаправленный путь коммутации по меткам",
            "<b>FEC</b> — пакеты, пересылаемые одинаково; <b>FTN</b> — FEC → next hop",
            "<b>PHP</b> — метку снимает предпоследний хоп"]), "cy")),
            step(card("Метка", li([
                "4 байта: <b>Label 20 бит · TC 3 · S 1 · TTL 8</b>",
                "Label 0…1 048 575; S = 1 — дно стека",
                "<b>0–15</b> служебные (0 IPv4 Explicit NULL, 3 Implicit NULL…)",
                "<b>16–1048575</b> — LDP и MP-BGP",
                "Стек — <b>LIFO</b>; <b>Push / Swap / Pop</b>"]), "am"))),
        col(step(card("LDP", li([
            "Hello → <b>224.0.0.2</b> (UDP), сеанс <b>TCP 646</b>",
            "Метку выбирает сосед <b>ниже по потоку</b>",
            "Label Request (FEC) → Label Mapping",
            "Управление: <b>упорядоченное / независимое</b>",
            "Метод: <b>по запросу / без запроса</b> → 4 режима"]), "lm")),
            step(card("RSVP и RSVP-TE", li([
                "<b>PATH</b> — источник → получатели, «состояние пути»",
                "<b>RESV</b> — обратно, резервирование; сливаются в точке ветвления",
                "Мягкое состояние: обновления Path/Resv, тайм-аут",
                "Объекты Path: <b>SESSION, SENDER_TSPEC, ERO, LABEL_REQUEST</b>",
                "<b>CSPF</b> + TED (OSPF-TE / IS-IS-TE)"]), "mg"))),
        col(step(card("Мониторинг и TE", li([
            "<b>LSP Ping</b>: Echo Request, DA 127.0.0.1, поле FEC; ответ по IP",
            "Трассировка — TTL в заголовке MPLS",
            "<b>BFD</b> — Hello в обе стороны, без локализации",
            "Туннели: <b>строгий / свободный</b>; критерий <b>min(max K)</b>",
            "K = суммарная скорость потоков / пропускная способность"]), "cy")),
            step(card("Защита и SR", li([
                "Восстановление начальным узлом; <b>защита линии / узла</b> (≤ 50 мс); <b>защита пути</b>",
                "FRR: Swap на метку основного пути + Push метки обхода",
                "<b>SID</b>: узла 1600X, смежности 160XX",
                "SR-MPLS / SRv6; верхний SID свой — удалить, иначе ECMP",
                "<b>PCEP</b>, <b>NETCONF</b> — контроллер"]), "lm"))))))
    # ---------------------------------------------------------------- задачи
    _tasks("Итоговые задачи · 1", [
        task("mp1", "LSP1: LER1 добавляет 256, LSR1 меняет на 272, LSR2 — на 132, LSR3 — предпоследний. "
                    "Какую операцию выполняет LSR3?", "Pop",
             "LSR3 — предпоследний хоп: выполняет <b>Pop</b> (PHP), LER2 продвигает пакет по IP-адресу.", "операция"),
        task("mp2", "LER2 получил стек [315 | IP]. По таблице: заменить 315 на 317, затем добавить сверху 188. "
                    "Какая метка окажется на вершине стека?", "188",
             "Swap 315 → 317, затем Push 188: стек [188 | 317 | IP], на вершине <b>188</b>.", "метка"),
        task("mp3", "Сколько бит занимает поле Label в MPLS-заголовке?", "20",
             "Label — <b>20 бит</b> (0…1 048 575); TC 3, S 1, TTL 8 — всего 32 бита.", "бит"),
        task("mp4", "По какому порту TCP устанавливается сеанс LDP?", "646",
             "Hello рассылаются на 224.0.0.2 (UDP), сеанс — <b>TCP 646</b>.", "порт")])
    _tasks("Итоговые задачи · 2", [
        task("mp5", "RSVP-TE: на участке было доступно 150 Мбит/с, LSP резервирует 100 Мбит/с. Сколько Мбит/с останется "
                    "для других туннелей?", "50", "150 − 100 = <b>50 Мбит/с</b> в направлении LER1 → LER2.", "Мбит/с"),
        task("mp6", "Потоки 40 и 30 Мбит/с на верхнем пути с каналами 155 Мбит/с. Чему равен K в процентах (округлить до целого)?",
             "45", "K = (40 + 30) / 155 ≈ 0,45 = <b>45%</b>.", "%"),
        task("mp7", "Какой IP-адрес назначения ставится в пакет с Echo Request протокола LSP Ping?", "127.0.0.1",
             "<b>127.0.0.1</b> — адрес обратной петли: при сбое узел передаёт запрос своему стеку TCP/IP.", "адрес"),
        task("mp8", "FRR: основной путь LSP1 — метки 15, 17, 21; обход — 7 и 8. С какой меткой кадр приходит на LSR7 "
                    "по обходному пути?", "17",
             "LSR2 меняет 15 на 17 и проталкивает 7; LSR3 снимает 7 — на LSR7 приходит метка <b>17</b>.", "метка")])
    # ---------------------------------------------------------------- тренажёры (выбор операции)
    _tasks("Тренажёр: что делает узел", [
        quiz("Входной LER получил IP-пакет, FEC определён.", ["Push", "Swap", "Pop", "IP-пересылка"], 0,
             "Входной LER определяет FEC и добавляет метку — <b>Push</b>."),
        quiz("Транзитный LSR получил пакет с меткой 245 на S0; в таблице: S1, 256.", ["Push 256", "Swap 256", "Pop", "Отбросить"], 1,
             "Число в поле «Действие» — замена метки: <b>Swap</b> 245 → 256, выход S1."),
        quiz("SR: верхний SID в списке идентифицирует локальный узел.", ["Переслать по ECMP", "Удалить SID и продолжить",
                                                                         "Добавить SID", "Отбросить пакет"], 1,
             "Свой SID — <b>удалить</b> и выполнять следующие процедуры."),
        quiz("SR: верхний SID 16005, пакет на R2.", ["Удалить SID", "Переслать к следующему узлу в режиме ECMP",
                                                     "Вернуть отправителю", "Push 16002"], 1,
             "SID не свой — пересылка следующему узлу <b>в режиме ECMP</b>.")])
    # ---------------------------------------------------------------- живой тренажёр LSP
    slide("Живой тренажёр LSP", sc(H("Живой тренажёр <em>LSP</em>",
                                     "Случайная сеть: заполните таблицы продвижения и отправьте пакет по пути."),
                                   '<div class="mplab" data-mplab></div>'))
    # ---------------------------------------------------------------- тест
    _qslide("Тест · 1", [
        quiz("MPLS-метка значима…", ["Глобально во всей сети", "Только локально", "Только на LER", "Только в домене SR"], 1,
             "Метка — короткий идентификатор фиксированной длины, <b>значимый только локально</b>."),
        quiz("Где располагается MPLS-заголовок?", ["После IP-заголовка", "Между заголовками канального и сетевого уровней",
                                                   "В конце кадра", "Внутри TCP"], 1, "Между L2 и L3 — <b>4-байтовый</b> заголовок."),
        quiz("Что означает S = 1?", ["Метка служебная", "Метка на дне стека", "TTL исчерпан", "Нужен PHP"], 1,
             "Поле S = 1 — метка находится <b>в нижней части стека</b>."),
        quiz("Метка 3 (Implicit NULL) указывает…", ["Удалить метку, дальше IPv6", "Предпоследнему LSR удалить метку",
                                                    "Пакет для OAM", "Зарезервировано"], 1,
             "Implicit NULL — <b>предпоследнему LSR удалить метку</b> перед отправкой на Egress-LER.")])
    _qslide("Тест · 2", [
        quiz("Кто выбирает значение метки для нового пути в LDP?", ["Сосед выше по потоку", "Сосед ниже по потоку",
                                                                   "Входной LER всегда", "Администратор"], 1,
             "Метку выбирает <b>устройство ниже по потоку</b> — оно будет её принимать."),
        quiz("Упорядоченный режим LDP — это когда LSR…", ["передаёт метку, не дожидаясь соседа", "ждёт метку от соседа ниже "
                                                          "по потоку и только потом передаёт свою", "рассылает метки всем",
                                                          "не использует TCP"], 1,
             "LSR2 ждал метку от LSR3 и уже потом передал метку LSR1."),
        quiz("В каком направлении идёт RESV?", ["От источника к получателю", "От получателя к источнику по состоянию пути",
                                                "Широковещательно", "Только между LER"], 1,
             "RESV идёт <b>в обратном направлении</b> по сохранённому состоянию Path."),
        quiz("Резервирование RSVP называется мягким, потому что…", ["его можно изменить", "оно отменяется по тайм-ауту без "
                                                                   "подтверждений", "оно не гарантирует QoS",
                                                                   "оно только на LER"], 1,
             "Без периодических подтверждений состояние <b>удаляется по истечении срока жизни</b>.")])
    _qslide("Тест · 3", [
        quiz("Почему Echo Reply в LSP Ping идёт как обычный UDP/IP?", ["Так быстрее", "LSP однонаправленные — обратного "
                                                                     "пути может не быть", "Чтобы проверить FEC",
                                                                     "Так требует BFD"], 1,
             "Пути LSP <b>однонаправленные</b>, обратного LSP от LSR8 к LSR1 может не существовать."),
        quiz("Чего не умеет BFD по сравнению с LSP Ping?", ["Обнаруживать отказ", "Локализовать отказавший элемент",
                                                            "Работать в обе стороны", "Использовать UDP"], 1,
             "BFD показывает только, работоспособен путь или нет."),
        quiz("Строгий TE-туннель задаёт…", ["Только начало и конец", "Все промежуточные узлы", "Только полосу",
                                            "Только метки"], 1, "Строгий туннель определяет <b>все промежуточные узлы</b>."),
        quiz("Время переключения при защите линии обычно…", ["десятки секунд", "не более 50 мс", "несколько минут",
                                                              "1 секунда"], 1,
             "Быстрая перемаршрутизация — <b>не более 50 мс</b>, как в SDH.")])
    _qslide("Тест · 4", [
        quiz("Вариант 2 примера min(max K) лучше, потому что…", ["использует меньше путей", "самый загруженный канал занят на "
                                                                "50%, а не на 58%", "все потоки на верхнем пути",
                                                                "K ≥ 65%"], 1, "Минимизируется загрузка самого загруженного ресурса."),
        quiz("SID смежного канала R3–R5 в примере:", ["16003", "16005", "16035", "16023"], 2,
             "SID смежных каналов — 160XX: <b>16035</b>."),
        quiz("SR с метками MPLS называют…", ["SRv6", "SR-MPLS", "MPLS TE", "LDP"], 1, "<b>SR-MPLS</b>; с IPv6 — SRv6."),
        quiz("PCEP — это…", ["протокол конфигурации сети", "протокол взаимодействия элементов расчёта пути",
                             "протокол распределения меток", "протокол мониторинга"], 1,
             "PCEP — взаимодействие элементов расчёта пути; NETCONF — конфигурация сети.")])
    # ---------------------------------------------------------------- итоги и финал
    slide("Что запомнить", sc(H("Что <em>запомнить</em>", "Главное из лекции."), grow("g2",
        col(step(card("Продвижение", li([
            "MPLS объединяет виртуальные каналы с IP: путь LSP строится заранее, пересылка — по метке.",
            "LER: FEC и Push; LSR: Swap; предпоследний хоп снимает метку (PHP).",
            "Стек меток — LIFO: многоуровневые пути и быстрая защита."]), "cy")),
            step(card("Сигнализация", li([
                "LDP строит LSP по маршрутам IGP; метку выбирает сосед ниже по потоку.",
                "RSVP-TE: Path → Resv, метки и резервирование вдоль выбранного пути."]), "am"))),
        col(step(card("Эксплуатация", li([
            "LSP Ping и трассировка по TTL MPLS; BFD — лёгкий постоянный контроль.",
            "MPLS TE: строгие и свободные туннели, критерий min(max K).",
            "Защита: восстановление, защита линии и узла (≤ 50 мс), защита пути."]), "lm")),
            step(card("Сегментная маршрутизация", li([
                "Путь — список SID в пакете; IGP/BGP распределяют метки.",
                "С контроллером — предпочтительный режим, пути под услуги."]), "mg"))))))
    slide("Финал", sc(H("<em>Спасибо</em> за внимание", "Вопросы по лекции и лабораторным — пишите."), grow("g2",
        col(step(card("Что дальше", li(["Повторить шпаргалку и решить задачи", "Пройти живой тренажёр LSP",
                                        "Набрать в тесте 16 / 16"]), "cy"))),
        col(step(card("Контакты", tags(tag("VKontakte", "v"), tag("Telegram")) + p("Пишите в VK или Telegram."), "mg"))))))


CSS = r"""
.mplab{display:grid;grid-template-columns:1.25fr 1fr;gap:14px;align-items:start}
.mplab .c{overflow:auto}
.mplab .bar{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}
.mplab button{font:800 clamp(13px,1vw,18px)/1 "Golos Text",sans-serif;padding:9px 14px;border-radius:10px;border:0;
 background:#1f63c6;color:#fff;cursor:pointer;box-shadow:0 4px 0 #123a7a}
.mplab button.o{background:#e8742c;box-shadow:0 4px 0 #8a3e10}.mplab button.g{background:#2f9e5b;box-shadow:0 4px 0 #1b5e36}
.mplab button:active{transform:translateY(3px);box-shadow:none}
.mplab .task{font:600 clamp(14px,1.15vw,22px)/1.45 "Golos Text",sans-serif;color:var(--ink)}
.mplab table{width:100%;border-collapse:collapse;font:600 clamp(13px,1vw,19px)/1.3 "Golos Text",sans-serif;color:var(--ink)}
.mplab th{background:#1f63c6;color:#fff;padding:6px 8px;text-align:left}
.mplab td{border-top:1px solid #c9d8ef;padding:5px 8px}
.mplab input{width:100%;font:700 clamp(13px,1vw,19px)/1 "JetBrains Mono",monospace;padding:6px 8px;border:2px solid #1f63c6;
 border-radius:8px;background:#fff;color:var(--ink)}
.mplab td.ok input{border-color:#2f9e5b;background:#e3f7ea}.mplab td.no input{border-color:#d9363e;background:#ffe0e0}
.mplab .log{font:600 clamp(13px,1vw,19px)/1.5 "JetBrains Mono",monospace;background:#0d1b33;color:#e8f1ff;border-radius:10px;
 padding:10px 12px;min-height:90px;white-space:pre-wrap}
.mplab .log .ok{color:#7dff9a}.mplab .log .no{color:#ff8a8a}
.mplab svg{width:100%;height:auto}
"""

JS = r"""
(function(){
  'use strict';
  function rnd(a,b){return a+Math.floor(Math.random()*(b-a+1));}
  function pick(a){return a[rnd(0,a.length-1)];}
  function labels(n){var s={},out=[];while(out.length<n){var v=rnd(16,999);if(!s[v]){s[v]=1;out.push(v);}}return out;}
  var KINDS=['ldp','rsvp','stack','frr'];
  function gen(){
    var kind=pick(KINDS), t={kind:kind};
    if(kind==='ldp'||kind==='rsvp'){
      var n=rnd(3,4), L=labels(n), php=(kind==='ldp')?Math.random()<.6:false;
      var nodes=['LER1'];for(var i=1;i<=n-1;i++)nodes.push('LSR'+i);nodes.push('LER2');
      t.nodes=nodes;t.adv=L;t.php=php;
      t.sol=nodes.map(function(nm,i){
        if(i===0)return 'push '+L[0];
        if(i===nodes.length-1)return php?'ip':'pop';
        if(i===nodes.length-2&&php)return 'pop';
        return 'swap '+L[i];
      });
      t.inl=nodes.map(function(nm,i){return i===0?'IP':(php&&i===nodes.length-1?'IP':L[i-1]);});
      var net=pick(['132.100.0.0','105.0.0.0','194.15.17.0','201.25.10.0']);
      t.text=(kind==='ldp'?'<b>LDP</b>, упорядоченный режим. Сеть назначения <b>'+net+'</b>. Каждый узел сообщил соседу выше по потоку свою метку: '
        :'<b>RSVP-TE</b>: Resv прошёл LER2 → … → LER1, каждый узел сообщил предыдущему свою метку: ')+
        nodes.slice(1).map(function(nm,i){return nm+' → <b>'+((php&&i===n-1)?'3 (Implicit NULL)':L[i])+'</b>';}).join(', ')+'. '+
        (php?'Используется <b>PHP</b> (метку снимает предпоследний хоп).':'Транспортная метка снимается непосредственно на <b>LER2</b>.')+
        ' Заполните действие каждого узла: <code>push N</code>, <code>swap N</code>, <code>pop</code> или <code>ip</code>.';
    } else if(kind==='stack'){
      var L2=labels(5);
      t.nodes=['LER1','LSR1','LSR2','LSR3','LER2'];
      t.sol=['push '+L2[4]+'; push '+L2[0],'swap '+L2[1],'swap '+L2[2],'pop','swap '+L2[3]+'; push '+L2[0]];
      t.inl=['IP',L2[0],L2[1],L2[2],L2[4]];t.end=[L2[0],L2[3]];
      t.text='Двухуровневый путь. Внутренняя метка LSP3 на входе — <b>'+L2[4]+'</b>, внешняя LSP1 — <b>'+L2[0]+
        '</b>; LSR1 и LSR2 меняют внешнюю на <b>'+L2[1]+'</b> и <b>'+L2[2]+'</b>; LSR3 — предпоследний для LSP1 (PHP). '+
        'LER2 меняет '+L2[4]+' на <b>'+L2[3]+'</b> и добавляет сверху метку LSP2 <b>'+L2[0]+'</b>. '+
        'Несколько операций — через «;», например <code>swap 317; push 188</code>.';
    } else {
      var a=labels(5);
      t.nodes=['LSR1','LSR2','LSR3','LSR7','LSR8'];
      t.sol=['push '+a[0],'swap '+a[1]+'; push '+a[3],'pop','swap '+a[2],'pop'];
      t.inl=['IP',a[0],a[3],a[1],a[2]];
      t.text='<b>Быстрая защита линии LSR2–LSR7.</b> Основной LSP1: метки <b>'+a[0]+'</b> (LSR1→LSR2), <b>'+a[1]+
        '</b> (LSR2→LSR7), <b>'+a[2]+'</b> (LSR7→LSR8). Обходной B-LSP1 через LSR3: первый участок — метка <b>'+a[3]+
        '</b>. Линия LSR2–LSR7 отказала. LSR3 — предпоследний на обходном пути. LSR8 — конец LSP1, снимает метку. Заполните действия.';
    }
    return t;
  }
  function norm(s){return String(s||'').toLowerCase().replace(/\s*;\s*/g,'; ').replace(/\s+/g,' ').trim();}
  function apply(stack,act){
    var ops=norm(act).split('; ');
    for(var i=0;i<ops.length;i++){
      var m=ops[i].match(/^(push|swap)\s+(\d+)$/);
      if(m){ if(m[1]==='push')stack.unshift(+m[2]); else { if(!stack.length)return null; stack[0]=+m[2]; } continue; }
      if(ops[i]==='pop'){ if(!stack.length)return null; stack.shift(); continue; }
      if(ops[i]==='ip'){ if(stack.length)return null; continue; }
      return null;
    }
    return stack;
  }
  function svgOf(t){
    var n=t.nodes.length,w=1000,out=['<svg viewBox="0 0 1000 150">'];
    for(var i=0;i<n-1;i++){var x1=80+i*(840/(n-1)),x2=80+(i+1)*(840/(n-1));
      out.push('<line x1="'+x1+'" y1="70" x2="'+x2+'" y2="70" style="stroke:#5d7396;stroke-width:5"/>');}
    for(i=0;i<n;i++){var x=80+i*(840/(n-1));
      out.push('<ellipse cx="'+x+'" cy="62" rx="30" ry="13" style="fill:#8fc3ff;stroke:#0d2f66;stroke-width:2"/>'+
        '<path d="M'+(x-30)+' 62 v16 a30 13 0 0 0 60 0 v-16" style="fill:#1f63c6;stroke:#0d2f66;stroke-width:2"/>'+
        '<ellipse cx="'+x+'" cy="62" rx="30" ry="13" style="fill:#8fc3ff;stroke:#0d2f66;stroke-width:2"/>'+
        '<text x="'+x+'" y="122" text-anchor="middle" font-size="20" font-weight="900" style="fill:#1d2a44">'+t.nodes[i]+'</text>'+
        '<g class="pk" data-i="'+i+'"></g>');}
    out.push('</svg>');return out.join('');
  }
  function render(box){
    var t=gen();box._t=t;
    var rows=t.nodes.map(function(nm,i){return '<tr><td><b>'+nm+'</b></td><td>'+(i===0?'IP / FEC':t.inl[i])+
      '</td><td><input data-i="'+i+'" spellcheck="false" placeholder="действие"></td></tr>';}).join('');
    box.innerHTML='<div class="c"><div class="task">'+t.text+'</div><div class="fig">'+svgOf(t)+'</div>'+
      '<div class="bar"><button data-a="new" class="o">↻ Обновить задание</button><button data-a="chk">Проверить</button>'+
      '<button data-a="send" class="g">▶ Отправить пакет</button><button data-a="sol" class="o">Решение</button></div></div>'+
      '<div class="c"><table><thead><tr><th>Узел</th><th>Входная метка</th><th>Действие</th></tr></thead><tbody>'+rows+
      '</tbody></table><div class="log" data-log>Задание готово. Введите действия и отправьте пакет.</div></div>';
  }
  function check(box){
    var t=box._t,ok=0,lines=[];
    box.querySelectorAll('input[data-i]').forEach(function(inp){
      var i=+inp.dataset.i,good=norm(inp.value)===norm(t.sol[i]);
      inp.parentNode.className=good?'ok':'no';if(good)ok++;
      lines.push('<span class="'+(good?'ok':'no')+'">'+(good?'✓ ':'✗ ')+t.nodes[i]+': '+(inp.value||'(пусто)')+'</span>');
    });
    var all=ok===t.nodes.length;
    box.querySelector('[data-log]').innerHTML=lines.join('\n')+'\n'+(all?'<span class="ok">Задание выполнено ✓</span>':
      '<span class="no">Верно '+ok+' из '+t.nodes.length+'</span>');
  }
  function send(box){
    var t=box._t,st=[],log=['IP-пакет приходит на '+t.nodes[0]];
    var inps=box.querySelectorAll('input[data-i]');
    for(var i=0;i<t.nodes.length;i++){
      var act=inps[i].value,want=(i===0)?null:t.inl[i];
      var top=st.length?st[0]:'IP';
      if(i>0&&String(top)!==String(want)){
        log.push('<span class="no">✗ '+t.nodes[i]+' получил '+(st.length?'метку '+top:'IP-пакет')+', а ждёт '+(want==='IP'?'IP-пакет':'метку '+want)+' — кадр отброшен</span>');
        break;
      }
      var r=apply(st,act);
      if(r===null){log.push('<span class="no">✗ '+t.nodes[i]+': действие «'+(act||'')+'» невозможно</span>');break;}
      st=r;
      log.push(t.nodes[i]+': '+(act||'')+' → стек ['+(st.length?st.join(' | ')+' | ':'')+'IP]');
      if(i===t.nodes.length-1){var end=(t.end||[]).join('|');
        if(st.join('|')!==end)log.push('<span class="no">✗ на выходе стек ['+st.concat(['IP']).join(' | ')+'], а нужен ['+(t.end||[]).concat(['IP']).join(' | ')+']</span>');
        else log.push(st.length?'<span class="ok">✓ Кадр уходит в домен 2 по LSP2 со стеком ['+st.join(' | ')+' | IP]</span>':'<span class="ok">✓ Пакет дошёл: на выходе обычный IP-пакет</span>');}
    }
    box.querySelector('[data-log]').innerHTML=log.join('\n');
  }
  function init(){
    document.querySelectorAll('[data-mplab]').forEach(render);
    document.addEventListener('click',function(e){
      var b=e.target.closest('.mplab button');if(!b)return;
      var box=b.closest('[data-mplab]'),a=b.dataset.a;
      if(a==='new')render(box);
      else if(a==='chk')check(box);
      else if(a==='send')send(box);
      else if(a==='sol'){box.querySelectorAll('input[data-i]').forEach(function(inp){inp.value=box._t.sol[+inp.dataset.i];});
        box.querySelector('[data-log]').textContent='Решение подставлено. Нажмите «Отправить пакет» или «Проверить».';}
    });
    document.addEventListener('keydown',function(e){if(e.target.closest&&e.target.closest('.mplab'))e.stopPropagation();},true);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
  window.MPLAB={gen:gen,apply:apply,norm:norm};
})();
"""
