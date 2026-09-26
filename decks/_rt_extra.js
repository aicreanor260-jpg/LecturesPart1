/* ================= тренажёр «Выбор маршрута» ================= */
(function(){
  var box=document.getElementById('trn'); if(!box) return;
  var sl=box.closest('.slide');
  var R=[['192.168.1.0',24,'LAN'],['10.0.0.0',8,'R2'],['10.20.0.0',16,'R3'],['10.20.30.0',24,'R4'],['172.20.0.0',16,'R3'],['0.0.0.0',0,'R5']];
  var mode='show', cur=null;
  function ip(s){ var p=String(s).trim().split('.'); if(p.length!==4) return null; var n=0;
    for(var i=0;i<4;i++){ if(!/^\d{1,3}$/.test(p[i])) return null; var v=+p[i]; if(v>255) return null; n=n*256+v; } return n; }
  function match(a,r){ if(r[1]===0) return true; var m=Math.pow(2,32)-Math.pow(2,32-r[1]); return Math.floor(a/Math.pow(2,32-r[1]))===Math.floor(ip(r[0])/Math.pow(2,32-r[1])); }
  function best(a){ var b=-1; R.forEach(function(r,k){ if(match(a,r)&&(b<0||r[1]>R[b][1])) b=k; }); return b; }
  function rows(){ return [].slice.call(sl.querySelectorAll('#trt tbody tr')); }
  function clear(){ rows().forEach(function(r){ r.classList.remove('hl','bad','dim'); });
    ['LAN','R2','R3','R4','R5'].forEach(function(p){ act(sl,[0,'undraw',p]); }); }
  function explain(a){ var ok=[]; R.forEach(function(r,k){ if(match(a,r)) ok.push(r[0]+'/'+r[1]); }); return 'Подходят: '+ok.join(', ')+'. Самый длинный префикс: <b>'+(function(){var b=best(a);return R[b][0]+'/'+R[b][1];})()+'</b>.'; }
  function show(k,a){ var tr=rows()[k]; rows().forEach(function(r,i){ if(i!==k&&!match(a,R[i])) r.classList.add('dim'); }); tr.classList.add('hl'); act(sl,[0,'draw',R[k][2],700]); }
  var msg=document.getElementById('trmsg'), inp=document.getElementById('trip');
  function run(){ clear(); var a=ip(inp.value); if(a===null){ msg.innerHTML='<span class="no">Введите IP-адрес в виде 10.20.30.77 (четыре числа от 0 до 255).</span>'; return; }
    cur=a; if(mode==='show'){ var b=best(a); show(b,a); msg.innerHTML='<span class="ok">Пакет уходит на '+(R[b][2]==='LAN'?'локальную сеть напрямую':R[b][2])+'.</span> '+explain(a); }
    else msg.innerHTML='Адрес <b>'+inp.value.trim()+'</b>: нажмите на строку таблицы, которая сработает.'; }
  sl.querySelector('#trt tbody').addEventListener('click',function(e){ var tr=e.target.closest('tr'); if(!tr||mode!=='self'||cur===null) return;
    var k=rows().indexOf(tr), b=best(cur); clear();
    if(k===b){ show(b,cur); msg.innerHTML='<span class="ok">Верно.</span> '+explain(cur); }
    else { tr.classList.add('bad'); show(b,cur); msg.innerHTML='<span class="no">Не эта строка'+(match(cur,R[k])?': она подходит, но префикс /'+R[k][1]+' короче':': адрес в неё не входит')+'.</span> '+explain(cur); } });
  [].slice.call(box.querySelectorAll('[data-m]')).forEach(function(b){ b.onclick=function(){ mode=b.dataset.m; [].slice.call(box.querySelectorAll('[data-m]')).forEach(function(x){x.classList.toggle('on',x===b)}); run(); }; });
  function rnd(n){ return Math.floor(Math.random()*n); }
  document.getElementById('trnew').onclick=function(){
    var g=[function(){return '10.20.30.'+rnd(256)}, function(){var o=rnd(256); if(o===30)o=31; return '10.20.'+o+'.'+rnd(256)}, function(){var o=rnd(256); if(o===20)o=21; return '10.'+o+'.'+rnd(256)+'.'+rnd(256)},
      function(){return '172.20.'+rnd(256)+'.'+rnd(256)}, function(){return '192.168.1.'+(1+rnd(254))}, function(){return (11+rnd(150))+'.'+rnd(256)+'.'+rnd(256)+'.'+rnd(256)}];
    inp.value=g[rnd(g.length)](); run(); };
  document.getElementById('trgo').onclick=run;
  inp.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); run(); } });
  sl._init=function(){ run(); };
})();
