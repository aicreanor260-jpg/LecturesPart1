/* Вкладка «Анализ на Python» окна «Результаты» (режим «Тест»): Python в браузере (Pyodide, WebAssembly) с pandas и matplotlib.
   Pyodide не встроен в страницу: загружается по кнопке из интернета — pyodide.js с cdn.jsdelivr.net/npm/pyodide@0.26.4,
   пакеты из полной сборки той же версии (cdn.jsdelivr.net/pyodide/v0.26.4/full/ — в npm-пакете только ядро). Без интернета — «нужен интернет».
   Данные текущей симуляции уже загружены: vec (векторы), sca (скаляры), hist (гистограммы) — те же функции read_vec / read_sca, что в тетрадке;
   образцы — ячейки тетрадки; графики matplotlib выводятся картинками, print — текстом. */
(function () {
  'use strict';
  var EL = window.EL, U = window.ELUI, esc = U.esc;
  var VER = '0.26.4', JS = 'https://cdn.jsdelivr.net/npm/pyodide@' + VER + '/pyodide.js', IDX = 'https://cdn.jsdelivr.net/pyodide/v' + VER + '/full/';
  var py = null, loading = null, code = null;
  // образцы — кодовые ячейки тетрадки с графиками (заголовок — из markdown перед ними)
  function samples() { var C = EL.SIM_CELLS || [], out = [], title = 'Загрузка данных и таблица скаляров';
    C.forEach(function (c) { if (c.md) { var h = c.lines.filter(function (l) { return /^##/.test(l); })[0]; if (h) title = h.replace(/^#+\s*/, ''); return; }
      var t = c.lines.join('\n'); if (/plt\.|groupby|print\(/.test(t) && !/def read_vec|glob\.glob\('\*\.vec'\)/.test(t)) out.push({ t: title, code: t }); });
    out.push({ t: 'Своя таблица: средняя задержка по потокам', code: "d = vec[vec['name'].isin(['rtt:vector', 'endToEndDelay:vector'])]\nprint(d.assign(ms=d['value'] * 1000).groupby('module')['ms'].describe().round(3))" });
    return out; }
  function load(st) {
    if (loading) return loading;
    if (!navigator.onLine) return Promise.reject(new Error('нужен интернет'));
    st('Загружаю Python (Pyodide ' + VER + ', ≈ 30 МБ из cdn.jsdelivr.net)…');
    loading = new Promise(function (ok, no) { var s = document.createElement('script'); s.src = JS; s.crossOrigin = 'anonymous'; s.onload = ok; s.onerror = function () { no(new Error('не удалось загрузить ' + JS)); }; document.head.appendChild(s); })
      .then(function () { return window.loadPyodide({ indexURL: IDX }); })
      .then(function (p) { py = p; st('Загружаю pandas и matplotlib…'); return py.loadPackage(['pandas', 'matplotlib']); })
      .then(function () { py.runPython('import matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\nimport io, base64, glob, os, shlex\nimport pandas as pd\n' + EL.SIM_PY +
          '\ndef _figs():\n    out = []\n    for n in plt.get_fignums():\n        b = io.BytesIO(); plt.figure(n).savefig(b, format="png", dpi=90, bbox_inches="tight"); out.append(base64.b64encode(b.getvalue()).decode())\n    plt.close("all")\n    return out\n'); })
      .catch(function (e) { loading = null; throw e; });
    return loading; }
  function feed() { var x = EL.simResData(); if (!x) return false; ['vec', 'sca', 'csv'].forEach(function (k) { py.FS.writeFile('run.' + k, x[k]); });
    py.runPython("VEC_FILES = ['run.vec']; SCA_FILES = ['run.sca']\nvec = read_vec('run.vec')\nsca, hist = read_sca('run.sca')\nplt.show = lambda *a, **k: None"); return true; }
  EL.simPyPane = function (v) {
    var S = samples(); if (code === null) code = S[0] ? S[0].code : '';
    v.innerHTML = '<div class="pyw"><p class="note">Python прямо в браузере (Pyodide, WebAssembly): pandas и matplotlib. Данные текущей симуляции уже загружены — <code>vec</code> (векторы), <code>sca</code> (скаляры), <code>hist</code> (гистограммы). ' +
      'Pyodide не встроен в эмулятор — загружается по кнопке из интернета (≈ 30 МБ, один раз за сеанс).</p>' +
      '<div class="row">' + (py ? '<span class="ok">Python загружен</span>' : '<button class="pri" data-py="load">Загрузить Python</button>') +
      '<select data-py="smp">' + S.map(function (s, i) { return '<option value="' + i + '">' + esc(s.t) + '</option>'; }).join('') + '</select><button data-py="ins">Вставить образец</button>' +
      '<button class="pri" data-py="run"' + (py ? '' : ' disabled') + '>▶ Выполнить</button></div>' +
      '<textarea class="q pycode" spellcheck="false" rows="12">' + esc(code) + '</textarea><div class="pyst"></div><pre class="pyout"></pre><div class="pyimg"></div></div>';
    var w = v.querySelector('.pyw'), ta = w.querySelector('.pycode'), stl = w.querySelector('.pyst'), out = w.querySelector('.pyout'), img = w.querySelector('.pyimg');
    function st(t, bad) { stl.textContent = t; stl.style.color = bad ? 'var(--bad)' : 'var(--dim)'; }
    if (!navigator.onLine && !py) st('Нужен интернет: Python (Pyodide) загружается с cdn.jsdelivr.net. Без сети — скачайте тетрадку .ipynb и откройте её в Jupyter.', true);
    ta.addEventListener('input', function () { code = ta.value; });
    ta.addEventListener('keydown', function (e) { if (e.key === 'Tab') { e.preventDefault(); var p = ta.selectionStart; ta.value = ta.value.slice(0, p) + '    ' + ta.value.slice(ta.selectionEnd); ta.selectionStart = ta.selectionEnd = p + 4; code = ta.value; }
      if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) w.querySelector('[data-py="run"]').click(); });
    w.addEventListener('click', function (e) { var b = e.target.closest('[data-py]'); if (!b || b.tagName === 'SELECT') return; var k = b.dataset.py;
      if (k === 'ins') { code = S[+w.querySelector('[data-py="smp"]').value].code; ta.value = code; return; }
      if (k === 'load') { b.disabled = true; load(st).then(function () { st('Python готов: выберите образец или напишите свой код и нажмите «Выполнить» (Ctrl+Enter).'); EL.simPyPane(v); })
        .catch(function (er) { b.disabled = false; st('Не удалось загрузить Python: ' + er.message + (navigator.onLine ? '' : ' — нужен интернет'), true); }); return; }
      if (k === 'run') { if (!py) return; out.textContent = ''; img.innerHTML = ''; st('Выполняю…'); var buf = [];
        py.setStdout({ batched: function (s) { buf.push(s); } }); py.setStderr({ batched: function (s) { buf.push(s); } });
        setTimeout(function () { try { if (!feed()) { st('Нет результатов симуляции', true); return; }
            var r = py.runPython(ta.value); if (r !== undefined && r !== null && typeof r !== 'function') buf.push(String(r.toString ? r.toString() : r)); if (r && r.destroy) r.destroy();
            var F = py.globals.get('_figs')(), L = F.toJs(); F.destroy();
            img.innerHTML = L.map(function (b64) { return '<img alt="график" src="data:image/png;base64,' + b64 + '">'; }).join('');
            out.textContent = buf.join('\n'); st('Готово' + (L.length ? ': графиков ' + L.length : ''));
          } catch (er) { out.textContent = buf.join('\n') + (buf.length ? '\n' : '') + String(er.message || er).split('\n').slice(-6).join('\n'); st('Ошибка в коде Python', true); } }, 30); }
    });
  };
})();
