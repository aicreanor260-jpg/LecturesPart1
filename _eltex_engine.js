/* Движок ледяной деки: шаги, навигация, содержание, прогон, тренажёр CLI */
(function () {
  'use strict';
  var slides = [].slice.call(document.querySelectorAll('.slide'));
  var cur = 0, step = 0, timer = null, speed = 1;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  var elCount = document.getElementById('count');
  var elName = document.getElementById('sname');
  var elProg = document.getElementById('prog');
  var toc = document.getElementById('toc');

  function steps(i) { return [].slice.call(slides[i].querySelectorAll('.step')); }

  function paint() {
    var st = steps(cur);
    st.forEach(function (e, k) { e.classList.toggle('vis', k < step); });
    elCount.textContent = (cur + 1) + ' / ' + slides.length +
      (st.length ? '  ·  ' + step + '/' + st.length : '');
    elName.textContent = slides[cur].dataset.label || '';
    elProg.style.width = ((cur + 1) / slides.length * 100) + '%';
  }

  function show(i, openAll) {
    stop();
    slides[cur].classList.remove('on');
    cur = Math.max(0, Math.min(slides.length - 1, i));
    slides[cur].classList.add('on');
    slides[cur].scrollTop = 0;
    var box = slides[cur].querySelector('.txt'); if (box) box.scrollTop = 0;
    step = openAll ? steps(cur).length : (reduce ? steps(cur).length : 0);
    paint();
    if (!reduce && !openAll) run();      // автозапуск шагов слайда
  }

  /* --- прогон слайда целиком --- */
  function run() {
    stop();
    var total = steps(cur).length;
    if (step >= total) return;
    timer = setInterval(function () {
      if (step >= total) { stop(); return; }
      step++; paint();
    }, 420 / speed);
  }
  function stop() { if (timer) { clearInterval(timer); timer = null; } }

  function next() {
    stop();
    if (step < steps(cur).length) { step++; paint(); }
    else if (cur < slides.length - 1) show(cur + 1);
  }
  function prev() {
    stop();
    if (step > 0) { step--; paint(); }
    else if (cur > 0) show(cur - 1, true);
  }

  /* --- содержание --- */
  function buildToc() {
    var g = document.getElementById('tocg');
    slides.forEach(function (s, i) {
      var b = document.createElement('button');
      b.className = 'tocit';
      b.innerHTML = '<i>' + (i + 1) + '</i>' + (s.dataset.label || '');
      b.onclick = function () { toc.classList.remove('on'); show(i); };
      g.appendChild(b);
    });
  }

  /* --- клавиатура --- */
  function inField(e) {
    var t = e.target;
    return t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable);
  }
  document.addEventListener('keydown', function (e) {
    if (inField(e)) return;
    var k = e.key;
    if (k === 'Escape') { toc.classList.toggle('on'); e.preventDefault(); return; }
    if (toc.classList.contains('on')) return;
    if (k === 'ArrowRight' || k === ' ') { if (k === ' ' && timer) { stop(); } else { next(); } e.preventDefault(); }
    else if (k === 'ArrowLeft') { prev(); e.preventDefault(); }
    else if (k === 'ArrowDown' || k === 'PageDown') { show(cur + 1); e.preventDefault(); }
    else if (k === 'ArrowUp' || k === 'PageUp') { show(cur - 1); e.preventDefault(); }
    else if (k === 'Home') { show(0); }
    else if (k === 'End') { show(slides.length - 1); }
    else if (k === 'r' || k === 'R' || k === 'к' || k === 'К') { step = 0; paint(); run(); }
  });

  /* --- колесо и свайп --- */
  var lock = 0;
  window.addEventListener('wheel', function (e) {
    if (toc.classList.contains('on')) return;
    var box = e.target.closest('.txt,.tasks,#term,.quiz');
    if (box) {
      var atTop = box.scrollTop <= 0, atEnd = box.scrollTop + box.clientHeight >= box.scrollHeight - 1;
      if ((e.deltaY > 0 && !atEnd) || (e.deltaY < 0 && !atTop)) return;
    }
    var now = Date.now(); if (now - lock < 420) return; lock = now;
    if (e.deltaY > 0) next(); else prev();
  }, { passive: true });

  var tx = 0, ty = 0;
  window.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; ty = e.touches[0].clientY; }, { passive: true });
  window.addEventListener('touchend', function (e) {
    var dx = e.changedTouches[0].clientX - tx, dy = e.changedTouches[0].clientY - ty;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy)) { dx < 0 ? next() : prev(); }
  }, { passive: true });

  document.getElementById('bprev').onclick = prev;
  document.getElementById('bnext').onclick = next;
  document.getElementById('btoc').onclick = function () { toc.classList.toggle('on'); };
  document.getElementById('bspeed').onclick = function () {
    speed = speed === 1 ? 2 : (speed === 2 ? 0.5 : 1);
    this.textContent = speed + '×';
    if (timer) run();
  };

  /* ---------------- тренажёр CLI ---------------- */
  var MODES = {
    user: { p: 'esr>', up: null },
    priv: { p: 'esr#', up: 'user' },
    conf: { p: 'esr(config)#', up: 'priv' },
    user_f: { p: 'esr(config-user)#', up: 'conf' },
    gre: { p: 'esr(config-gre)#', up: 'conf' },
    ssh: { p: 'esr(config-line-ssh)#', up: 'conf' },
    gi: { p: 'esr(config-if-gi)#', up: 'conf' }
  };
  var WHERE = {
    enable: 'user', disable: 'priv', configure: 'priv', config: 'priv',
    username: 'conf', 'tunnel gre': 'conf', 'line ssh': 'conf',
    'interface gigabitethernet': 'conf', commit: 'priv', confirm: 'priv',
    'show running-config': 'priv', ping: 'priv'
  };
  var HINT = { user: 'пользовательском', priv: 'привилегированном', conf: 'глобального конфигурирования' };
  var VOCAB = ['enable', 'disable', 'configure', 'exit', 'end', 'username', 'tunnel gre',
    'line ssh', 'interface gigabitethernet', 'commit', 'confirm', 'rollback', 'restore',
    'show running-config', 'show candidate-config', 'ping', 'help'];

  var term = document.getElementById('term');
  if (term) {
    var mode = 'user', hist = [], hp = -1, visited = {};
    var inp = document.getElementById('termin'), ps = document.getElementById('prompt');
    var done = { conf: false, user_f: false, back: false };

    function echo(s, cls) {
      var d = document.createElement('div');
      if (cls) d.className = cls;
      d.textContent = s;
      term.appendChild(d);
      term.scrollTop = term.scrollHeight;
    }
    function setMode(m) { mode = m; ps.textContent = MODES[m].p; visited[m] = true; checkTasks(); }
    function checkTasks() {
      if (visited.conf) done.conf = true;
      if (visited.user_f) done.user_f = true;
      if (done.user_f && mode === 'priv') done.back = true;
      ['conf', 'user_f', 'back'].forEach(function (k) {
        document.getElementById('t_' + k).classList.toggle('done', done[k]);
      });
    }
    function exec(raw) {
      var c = raw.trim().replace(/\s+/g, ' ');
      if (!c) return;
      echo(MODES[mode].p + ' ' + c);
      hist.push(c); hp = hist.length;
      var lc = c.toLowerCase();

      if (lc === 'help' || lc === '?') {
        echo('Доступно: ' + VOCAB.join(', '), 'ok'); return;
      }
      if (lc === 'end') { setMode(mode === 'user' ? 'user' : 'priv'); return; }
      if (lc === 'exit') {
        var up = MODES[mode].up;
        if (!up) { echo('Сеанс завершён (exit в пользовательском режиме).', 'ok'); return; }
        if (mode === 'priv') { echo('Ввод exit в привилегированном режиме закрывает сеанс.', 'ok'); }
        setMode(up); return;
      }
      var target = null, key = null;
      Object.keys(WHERE).forEach(function (k) {
        if (lc === k || lc.indexOf(k + ' ') === 0) { if (!key || k.length > key.length) key = k; }
      });
      if (!key) { echo('Unknown command «' + c + '»', 'err'); return; }
      target = WHERE[key];
      if (target !== mode) {
        echo('Команда «' + key + '» доступна в ' + (HINT[target] || target) + ' режиме.', 'err');
        return;
      }
      if (key === 'enable') { setMode('priv'); }
      else if (key === 'disable') { setMode('user'); }
      else if (key === 'configure' || key === 'config') { setMode('conf'); }
      else if (key === 'username') {
        if (lc === 'username') { echo('Incomplete command: нужно имя пользователя.', 'err'); return; }
        setMode('user_f'); echo('Пользователь создан, настройка в режиме функционала.', 'ok');
      }
      else if (key === 'tunnel gre') { setMode('gre'); }
      else if (key === 'line ssh') { setMode('ssh'); }
      else if (key === 'interface gigabitethernet') { setMode('gi'); }
      else if (key === 'commit') { echo('candidate-config применён, таймер 600 с запущен.', 'ok'); }
      else if (key === 'confirm') { echo('Изменения подтверждены.', 'ok'); }
      else if (key === 'ping') { echo('64 bytes: icmp_seq=1 time=0.4 ms', 'ok'); }
      else { echo('OK', 'ok'); }
    }
    inp.addEventListener('keydown', function (e) {
      e.stopPropagation();
      if (e.key === 'Enter') { exec(inp.value); inp.value = ''; e.preventDefault(); }
      else if (e.key === 'ArrowUp') { if (hp > 0) { hp--; inp.value = hist[hp]; } e.preventDefault(); }
      else if (e.key === 'ArrowDown') { if (hp < hist.length - 1) { hp++; inp.value = hist[hp]; } else { hp = hist.length; inp.value = ''; } e.preventDefault(); }
      else if (e.key === 'Tab') {
        var v = inp.value.trim().toLowerCase();
        var m = VOCAB.filter(function (x) { return v && x.indexOf(v) === 0; });
        if (m.length === 1) inp.value = m[0];
        else if (m.length > 1) echo(m.join('  '), 'ok');
        e.preventDefault();
      }
    });
    document.getElementById('termreset').onclick = function () {
      term.innerHTML = ''; visited = {}; done = { conf: false, user_f: false, back: false };
      setMode('user'); checkTasks();
      echo('Сессия сброшена. Введите help для списка команд.');
    };
    setMode('user');
    echo('ESR CLI (учебный эмулятор). Введите help для списка команд.');
  }

  /* ---------------- проверь себя ---------------- */
  [].forEach.call(document.querySelectorAll('.q'), function (q) {
    [].forEach.call(q.querySelectorAll('button'), function (b) {
      b.onclick = function () {
        [].forEach.call(q.querySelectorAll('button'), function (x) {
          x.classList.toggle('good', x.dataset.a === '1');
          if (x === b && b.dataset.a !== '1') x.classList.add('bad');
        });
      };
    });
  });

  buildToc();
  show(0);
})();
