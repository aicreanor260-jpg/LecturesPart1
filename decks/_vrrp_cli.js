/* Учебная модель ESR VRRP. Не подключается к реальному оборудованию. */
(function(root){
'use strict';
const clone = value => JSON.parse(JSON.stringify(value));
const pick = list => list[Math.floor(Math.random()*list.length)];
const ipv4 = value => /^\d+\.\d+\.\d+\.\d+$/.test(value) && value.split('.').every(n=>Number(n)>=0&&Number(n)<=255);
const ipnum = value => value.split('.').reduce((n,v)=>n*256+Number(v),0);
function prompt(s){ return (s.task&&s.task.router||'ESR')+(s.mode==='exec'?'#':s.mode==='config'?'(config)#':s.iface.includes('.')?'(config-subif)#':'(config-if-gi)#'); }
function makeTask(lab){
  const priority=pick([110,120,150,200]),router=pick(['R1','R2']);
  const dual=lab==='dual', groups=[];
  if(dual){
    groups.push({iface:'gi1/0/1.10',address:router==='R1'?'10.10.1.2/24':'10.10.1.3/24',id:100,vip:'10.10.1.1',priority:router==='R1'?priority:10,peerIP:router==='R1'?'10.10.1.3':'10.10.1.2',peerPriority:router==='R1'?10:priority,role:router==='R1'?'Master':'Backup',preempt:true});
    groups.push({iface:'gi1/0/1.20',address:router==='R1'?'10.10.2.3/24':'10.10.2.2/24',id:200,vip:'10.10.2.1',priority:router==='R1'?10:priority,peerIP:router==='R1'?'10.10.2.2':'10.10.2.3',peerPriority:router==='R1'?priority:10,role:router==='R1'?'Backup':'Master',preempt:true});
  }else{
    groups.push({iface:router==='R1'?'gi1/0/1':'gi1/0/2',address:router==='R1'?'10.10.1.2/24':'10.10.1.3/24',id:pick([100,200]),vip:'10.10.1.1',priority,peerIP:router==='R1'?'10.10.1.3':'10.10.1.2',peerPriority:100,role:'Master',preempt:true});
  }
  return {lab:dual?'dual':'single',router,priority,groups};
}
function createSession(task){return {task:task||makeTask('single'),mode:'exec',iface:null,interfaces:{},committed:null,confirmed:false,revision:0,commitRevision:-1};}
function freshInterface(){return {address:null,firewallDisabled:false,id:null,vip:null,priority:100,enabled:false,preempt:true};}
function ifaceName(value){
  const m=value.toLowerCase().replace(/\s+/g,'').match(/^(?:gi|gigabitethernet)(1\/0\/[12](?:\.(?:10|20))?)$/);
  return m?'gi'+m[1]:null;
}
function activeGroups(s){return Object.entries(s.committed||{}).filter(([,i])=>i.id!==null);}
function groupState(s,name,cfg){
  if(!cfg.enabled||!cfg.address||!cfg.vip||!cfg.id||!cfg.firewallDisabled)return 'Initialize';
  if(cfg.address.split('/')[0]===cfg.vip)return 'Master';
  const expected=s.task.groups.find(g=>g.iface===name&&g.id===cfg.id&&g.vip===cfg.vip);
  if(!expected)return 'Master';
  if(!cfg.preempt)return 'Backup';
  return cfg.priority>expected.peerPriority||(cfg.priority===expected.peerPriority&&ipnum(cfg.address.split('/')[0])>ipnum(expected.peerIP))?'Master':'Backup';
}
function showVrrp(s,id){
  const all=activeGroups(s).filter(([,c])=>id===undefined||c.id===id);
  if(!all.length)return id===undefined?'VRRP: применённых процессов нет.':'% Процесс VRRP '+id+' не найден.';
  if(id!==undefined){
    const [name,c]=all[0],mac='00:00:5e:00:01:'+c.id.toString(16).padStart(2,'0');
    return ['VRRP ID:                       '+c.id,'VRRP Version:                  2','Interface:                     '+name,'Priority:                      '+(c.address&&c.address.split('/')[0]===c.vip?255:c.priority),'State:                         '+groupState(s,name,c),'Source IP address:             '+(c.address||'--'),'Virtual IP address:            '+(c.vip?c.vip+'/32':'--'),'Virtual MAC address:           '+mac,'Preemption:                    '+(c.preempt?'Enabled':'Disabled'),'Advertisement interval:        1 second'].join('\n');
  }
  return ['Virtual router  Virtual IP          Priority  Preemption  State',...all.map(([name,c])=>String(c.id).padEnd(16)+(c.vip?c.vip+'/32':'--').padEnd(20)+String(c.address&&c.address.split('/')[0]===c.vip?255:c.priority).padEnd(10)+(c.preempt?'Enabled':'Disabled').padEnd(12)+groupState(s,name,c))].join('\n');
}
function configLines(s){
  const lines=[];
  for(const [name,c] of Object.entries(s.interfaces)){
    lines.push('interface '+name);
    if(c.address)lines.push(' ip address '+c.address);
    if(c.firewallDisabled)lines.push(' ip firewall disable');
    if(c.id!==null)lines.push(' vrrp id '+c.id);
    if(c.vip)lines.push(' vrrp ip '+c.vip);
    if(c.priority!==100)lines.push(' vrrp priority '+c.priority);
    if(!c.preempt)lines.push(' vrrp preempt disable');
    if(c.enabled)lines.push(' vrrp');
    lines.push('exit');
  }
  return lines.length?lines.join('\n'):'! Конфигурация интерфейсов пуста';
}
function runCommand(s,input){
  const cmd=String(input).trim().replace(/\s+/g,' '),low=cmd.toLowerCase();
  const result=(ok,output='')=>({ok,output,prompt:prompt(s)});
  const error=message=>result(false,'% '+message);
  if(!cmd)return result(true);
  let m;
  if(low==='end'){s.mode='exec';s.iface=null;return result(true);}
  if(low==='exit'){
    if(s.mode==='interface'){s.mode='config';s.iface=null;}else if(s.mode==='config')s.mode='exec';
    return result(true);
  }
  if(low==='configure'||low==='configure terminal'||low==='conf'){
    if(s.mode!=='exec')return error('Команда configure доступна из привилегированного режима.');
    s.mode='config';return result(true);
  }
  const isDo=low.startsWith('do '),op=isDo?low.slice(3):low;
  if(op.startsWith('show ')){
    if(s.mode!=='exec'&&!isDo)return error('В режиме конфигурации используйте do show ...');
    if(op==='show running-config')return result(true,configLines(s)+(s.revision!==s.commitRevision?'\n! Есть неприменённые изменения. Выполните do commit и do confirm.':''));
    if(op==='show vrrp')return result(true,showVrrp(s));
    if((m=op.match(/^show vrrp (\d+)$/))){const id=Number(m[1]);if(id<1||id>255)return error('VRID должен быть от 1 до 255.');return result(true,showVrrp(s,id));}
    return error('Неизвестная команда show.');
  }
  if(op==='commit'||op==='confirm'){
    if(s.mode!=='exec'&&!isDo)return error('В режиме конфигурации используйте do '+op+'.');
    if(op==='commit'){s.committed=clone(s.interfaces);s.commitRevision=s.revision;s.confirmed=false;return result(true,'Configuration committed. Выполните confirm для подтверждения.');}
    if(s.committed===null)return error('Сначала выполните commit.');
    if(s.commitRevision!==s.revision)return error('После изменений требуется новый commit.');
    s.confirmed=true;return result(true,'Configuration confirmed.');
  }
  if(isDo)return error('Неизвестная команда после do.');
  if((m=low.match(/^interface (.+)$/))){
    if(s.mode==='exec')return error('Сначала выполните configure.');
    const name=ifaceName(m[1]);if(!name)return error('Допустимы Gi1/0/1, Gi1/0/2 и подинтерфейсы .10/.20.');
    s.iface=name;s.mode='interface';if(!s.interfaces[name])s.interfaces[name]=freshInterface();return result(true);
  }
  if(s.mode!=='interface')return error('Неизвестная команда или неверный режим. Выберите интерфейс.');
  const cfg=s.interfaces[s.iface];
  function update(field,value){if(cfg[field]!==value){cfg[field]=value;s.revision++;s.confirmed=false;}return result(true);}
  if((m=low.match(/^ip address (\S+)(?: (\S+))?$/))){
    let address=m[1];
    if(m[2]){
      if(!ipv4(address)||!ipv4(m[2]))return error('Некорректный IP-адрес или маска.');
      const bits=m[2].split('.').map(n=>Number(n).toString(2).padStart(8,'0')).join('');
      if(!/^1*0*$/.test(bits))return error('Некорректная маска сети.');
      address+='/'+bits.replace(/0/g,'').length;
    }
    const parts=address.split('/');if(parts.length!==2||!ipv4(parts[0])||!/^\d+$/.test(parts[1])||Number(parts[1])>32)return error('Используйте IPv4-адрес/префикс, например 10.10.1.2/24.');
    return update('address',parts[0]+'/'+Number(parts[1]));
  }
  if(low==='ip firewall disable')return update('firewallDisabled',true);
  if((m=low.match(/^vrrp id (\d+)$/))){const n=Number(m[1]);if(n<1||n>255)return error('VRID должен быть от 1 до 255.');return update('id',n);}
  if((m=low.match(/^vrrp priority (\d+)$/))){const n=Number(m[1]);if(n<1||n>254)return error('Приоритет должен быть от 1 до 254.');return update('priority',n);}
  if((m=low.match(/^vrrp ip (\S+)$/))){const parts=m[1].split('/');if(parts.length>2||!ipv4(parts[0])||(parts[1]!==undefined&&(!/^\d+$/.test(parts[1])||Number(parts[1])>32)))return error('Некорректный виртуальный IPv4-адрес.');return update('vip',parts[0]);}
  if(low==='vrrp preempt disable')return update('preempt',false);
  if(low==='no vrrp preempt disable')return update('preempt',true);
  if(low==='vrrp'){
    if(!cfg.id||!cfg.vip)return error('Сначала задайте vrrp id и vrrp ip.');
    return update('enabled',true);
  }
  return error('Неизвестная команда.');
}
function solution(task){
  const lines=['configure'];
  task.groups.forEach(g=>{lines.push('interface '+g.iface,'ip address '+g.address,'ip firewall disable','vrrp id '+g.id,'vrrp ip '+g.vip,'vrrp priority '+g.priority,g.preempt?'no vrrp preempt disable':'vrrp preempt disable','vrrp','exit');});
  lines.push('do commit','do confirm','end','show vrrp');return lines;
}
function checkTask(s,task){
  task=task||s.task;const checks=[];
  function add(label,ok){checks.push({label,ok:Boolean(ok)});}
  task.groups.forEach(g=>{
    const c=s.interfaces[g.iface]||{},tag=g.iface+' · ';
    add(tag+'собственный IP '+g.address,c.address===g.address);
    add(tag+'межсетевой экран отключён',c.firewallDisabled);
    add(tag+'VRID '+g.id,c.id===g.id);
    add(tag+'виртуальный IP '+g.vip,c.vip===g.vip);
    add(tag+'приоритет '+g.priority,c.priority===g.priority);
    add(tag+'VRRP включён',c.enabled);
    add(tag+'вытеснение '+(g.preempt?'включено':'отключено'),c.preempt===g.preempt);
    add(tag+'роль '+g.role,Boolean(s.committed&&s.committed[g.iface]&&groupState(s,g.iface,s.committed[g.iface])===g.role));
  });
  add('Изменения применены (commit)',s.committed!==null&&s.commitRevision===s.revision);
  add('Изменения подтверждены (confirm)',s.confirmed&&s.commitRevision===s.revision);
  return {ok:checks.every(c=>c.ok),checks};
}
function sendPacket(s){
  const lines=s.task.groups.map(g=>{
    const c=(s.committed||{})[g.iface];
    const ok=Boolean(c&&c.address===g.address&&c.firewallDisabled&&c.id===g.id&&c.vip===g.vip&&c.enabled);
    const role=ok?groupState(s,g.iface,c):'Initialize';
    return (ok?'✓ ':'✗ ')+'Шлюз '+g.vip+': '+(ok?(role==='Master'?'доступен через '+s.task.router:'доступен через соседний Master; '+s.task.router+' — Backup'):'VRRP или интерфейс ещё не настроен и не применён');
  });
  return lines.join('\n');
}
const api={createSession,runCommand,makeTask,checkTask,solution,prompt,sendPacket};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
root.VRRP_CLI=api;
if(typeof document==='undefined')return;
document.querySelectorAll('.v-cli').forEach(box=>{
  const el=selector=>box.querySelector(selector),out=el('[data-cli-out]'),input=el('[data-cli-input]'),pr=el('[data-cli-prompt]'),taskEl=el('[data-cli-task]'),res=el('[data-cli-result]'),sol=el('[data-cli-solution]');
  if(!out||!input||!pr||!taskEl||!res||!sol)return;
  let s,history=[],hist=0;
  const print=text=>{if(text){const row=document.createElement('div');row.textContent=text;out.appendChild(row);out.scrollTop=out.scrollHeight;}};
  const sync=()=>{pr.textContent=prompt(s);};
  function newTask(){
    const task=makeTask(box.dataset.lab);s=createSession(task);out.textContent='';res.textContent='';sol.hidden=true;sol.style.display='none';sol.textContent=solution(task).join('\n');history=[];hist=0;
    taskEl.textContent='Учебная модель ESR, не реальное устройство. Настройте '+task.router+'. Соседний маршрутизатор и коммутация уже подготовлены. '+task.groups.map(g=>g.iface+': IP '+g.address+', VRID '+g.id+', VIP '+g.vip+', Priority '+g.priority+', роль '+g.role+'.').join(' ')+' Включите VRRP и вытеснение, примените и подтвердите конфигурацию.';
    print('Eltex ESR · учебная консоль VRRP\nВведите configure для начала.');sync();
  }
  input.addEventListener('keydown',e=>{
    if(e.key==='Enter'){
      e.preventDefault();e.stopPropagation();const command=input.value;print(prompt(s)+' '+command);if(command.trim())history.push(command);hist=history.length;input.value='';const r=runCommand(s,command);print(r.output);sync();res.textContent='';
    }else if(e.key==='ArrowUp'||e.key==='ArrowDown'){
      e.preventDefault();e.stopPropagation();hist=Math.max(0,Math.min(history.length,hist+(e.key==='ArrowUp'?-1:1)));input.value=history[hist]||'';
    }
  });
  box.addEventListener('click',e=>{
    const button=e.target.closest('[data-cli-action]');if(!button)return;
    const action=button.dataset.cliAction;
    if(action==='new')newTask();
    if(action==='solution'){const visible=sol.hidden||sol.style.display==='none';sol.hidden=!visible;sol.style.display=visible?'block':'none';if(root.PT_FIT)root.PT_FIT();}
    if(action==='check'){const report=checkTask(s);res.textContent=(report.ok?'Задание выполнено.\n':'Проверьте настройки:\n')+report.checks.map(c=>(c.ok?'✓ ':'✗ ')+c.label).join('\n');}
    if(action==='send')res.textContent=sendPacket(s);
    if(action==='reconnect'){s.mode='exec';s.iface=null;print('\nПодключение восстановлено. Конфигурация сохранена в учебной сессии.');sync();}
    input.focus();
  });
  newTask();
});
})(typeof globalThis!=='undefined'?globalThis:this);
