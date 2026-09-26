# -*- coding: utf-8 -*-
# CSS и JS для decks/glava7-application.html (движок перенесён из главы 11)

CSS = r"""
@font-face{font-family:"OswaldL";src:url(__OSW__) format("woff");font-weight:700;font-display:swap}
:root{--bg:#04100f;--panel:rgba(8,32,30,.72);--panel2:rgba(6,24,22,.9);--edge:rgba(45,230,200,.34);--ink:#eafffb;--dim:#8fb8b0;
  --cyan:#2ee6c8;--teal-dim:#16a894;--ice:#7ef5e2;--amber:#f5b83d;--violet:#9b7bff;--red:#ff5c6e;--blue:#4aa8ff;--green:#8ce36a;
  --f:"Golos Text","Inter","Manrope","Segoe UI",system-ui,sans-serif;--hf:"OswaldL","Oswald","Bahnschrift","Arial Narrow",var(--f);
  --mono:"JetBrains Mono","Cascadia Mono","Consolas",ui-monospace,monospace;
  --cut:polygon(14px 0,100% 0,100% calc(100% - 14px),calc(100% - 14px) 100%,0 100%,0 14px);
  --cut6:polygon(6px 0,100% 0,100% calc(100% - 6px),calc(100% - 6px) 100%,0 100%,0 6px);
  --hex:polygon(25% 0,75% 0,100% 50%,75% 100%,25% 100%,0 50%);
  --ez:cubic-bezier(.22,.7,.3,1);--bgi:none;color-scheme:dark}
*{box-sizing:border-box;margin:0;padding:0;border-radius:0}
[hidden]{display:none!important}
html{font-size:clamp(14px,min(1.02vw,1.86vh),28px)}
html,body{height:100%;overflow:hidden;background:var(--bg);color:var(--ink);font-family:var(--f)}
.mono{font-family:var(--mono);font-variant-numeric:tabular-nums}
#deco{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
#deco i{position:absolute;width:46vw;height:46vw;border-radius:50%;filter:blur(120px);opacity:.3;background:#0f8f7c}
#deco i:nth-child(1){left:-14vw;top:-18vw}#deco i:nth-child(2){right:-16vw;bottom:-20vw;background:#2ee6c8;opacity:.16}
#deco b{position:absolute;inset:0;opacity:.35;background-image:radial-gradient(rgba(45,230,200,.35) 1px,transparent 1.4px),repeating-linear-gradient(135deg,transparent 0 46px,rgba(45,230,200,.07) 46px 47px);
  background-size:26px 26px,auto;-webkit-mask-image:radial-gradient(ellipse at 70% 40%,#000 10%,transparent 72%);mask-image:radial-gradient(ellipse at 70% 40%,#000 10%,transparent 72%)}
#deco s{position:absolute;right:3vw;top:8vh;width:22vw;height:40vh;opacity:.18;
  background:linear-gradient(90deg,transparent 0 30%,var(--cyan) 30% 30.4%,transparent 30.4%) 0 0/100% 34px,linear-gradient(transparent 0 60%,var(--cyan) 60% 61%,transparent 61%) 0 0/68px 100%}
#prog{position:fixed;left:0;top:0;height:3px;width:100%;z-index:30;background:rgba(45,230,200,.12)}
#prog i{display:block;height:100%;width:0;background:var(--cyan);box-shadow:0 0 10px var(--cyan);transition:width .3s var(--ez)}
.slide{position:fixed;inset:0;z-index:1;display:none}.slide.on{display:block}
.sc{height:100%;overflow-y:auto;overflow-x:hidden;display:flex;flex-direction:column;padding:clamp(18px,4.5vh,58px) clamp(16px,4.5vw,96px) calc(5rem + 12px);scrollbar-width:thin;scrollbar-color:var(--edge) transparent}
.wrap{margin:auto;width:100%;max-width:104rem;position:relative}
.sh{margin-bottom:1.2rem;display:flex;align-items:flex-end;gap:1.4rem;flex-wrap:wrap}
.sh .snum{font-family:var(--hf);font-size:1rem;color:var(--bg);background:var(--cyan);clip-path:var(--hex);width:3.2rem;height:2.8rem;display:grid;place-items:center;flex:none;margin-bottom:.3rem}
h2{font-family:var(--hf);font-size:2.9rem;line-height:1;font-weight:700;text-transform:uppercase;letter-spacing:.01em;color:#fff}
h2 .o2{display:block;color:var(--cyan);text-shadow:0 0 22px rgba(46,230,200,.45)}
.sub{font-size:.86rem;letter-spacing:.18em;text-transform:uppercase;color:var(--dim);margin-top:.45rem;font-weight:700}
h3{font-family:var(--hf);font-size:1.18rem;font-weight:700;margin-bottom:.55rem;line-height:1.2;text-transform:uppercase;letter-spacing:.03em;color:var(--ice)}
.p{font-size:1.1rem;line-height:1.55;margin-bottom:.8rem;max-width:72ch;color:#d3f0ea}
.p.lg{font-size:1.3rem;max-width:none}.p.sm{font-size:.98rem;margin-bottom:.6rem}
.p b,.bl b,.dl b,.tbl b{color:#fff}.hl{color:var(--cyan);font-weight:700}
.dimp{color:var(--dim)}.mt{margin-top:1rem}
.two{display:grid;grid-template-columns:minmax(0,1fr);gap:1.3rem 2.2rem;align-items:start}
.two.mid{align-items:center}
.vis{display:flex;flex-direction:column;gap:1rem;min-width:0}.txt{min-width:0}
.g2,.g3,.g4{display:grid;grid-template-columns:minmax(0,1fr);gap:.9rem}
.card{position:relative;background:var(--panel);border:1px solid var(--edge);clip-path:var(--cut)}
.card::before{content:"";position:absolute;left:0;top:16px;width:3px;height:34px;background:var(--cyan)}
.dgc{padding:1rem 1.1rem}
.dg{display:block;width:100%;height:auto;max-height:66vh;overflow:visible}
.ph{padding:.45rem;margin:0}.ph img{display:block;width:100%;height:auto;max-height:64vh;object-fit:contain;cursor:zoom-in}
.ph figcaption{font-size:.8rem;color:var(--dim);padding:.4rem .3rem 0}
.thumb{max-width:22rem;margin-top:.8rem}.thumb img{max-height:14rem}
.thumb figcaption::before{content:"";display:inline-block;width:.55em;height:.55em;background:var(--cyan);clip-path:var(--hex);margin-right:.45em}
#zl{position:fixed;inset:0;z-index:85;background:rgba(2,10,9,.94);display:grid;place-items:center;padding:24px;cursor:zoom-out;overflow:auto}#zl[hidden]{display:none}#zi{transform-origin:center center;pointer-events:none}#zl .zhint{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);font:700 12px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--dim);pointer-events:none}.zoomable{cursor:zoom-in}
#lb{position:fixed;inset:0;z-index:80;background:rgba(2,10,9,.96);display:grid;place-items:center;padding:12px;cursor:zoom-out}#lb[hidden]{display:none}#lb img{max-width:100%;max-height:100%;object-fit:contain}
.badge{flex:none;display:inline-grid;place-items:center;width:2.6em;height:2.25em;color:#03120f;font-weight:700;font-family:var(--hf);font-size:.9em;clip-path:var(--hex)}
.b0{background:var(--cyan)}.b1{background:var(--amber)}.b2{background:var(--ice)}.b3{background:var(--violet)}.b4{background:var(--blue)}
.bl{list-style:none;display:flex;flex-direction:column;gap:.75rem}
.bl li{display:flex;gap:.9rem;align-items:flex-start;font-size:1.08rem;line-height:1.45}
.bl.big li{font-size:1.35rem;align-items:center}.bl.sm li{font-size:.96rem}
.dl{list-style:none;display:flex;flex-direction:column;gap:.45rem;margin:.3rem 0 .7rem}
.dl li{position:relative;padding-left:1.3rem;font-size:1rem;line-height:1.45}
.dl li::before{content:"";position:absolute;left:0;top:.42em;width:.62em;height:.55em;background:var(--cyan);clip-path:var(--hex)}
.pn{padding:1rem 1.1rem}.pn.ok::before{background:var(--green)}.pn.warn::before{background:var(--amber)}.pn.bad::before{background:var(--red)}
.pn.ok h3{color:var(--green)}.pn.warn h3{color:var(--amber)}.pn.bad h3{color:var(--red)}
.pn .p{margin-bottom:.4rem}
.pnh{display:flex;gap:.7rem;align-items:center;margin-bottom:.5rem}.pnh h3{margin:0}
.quote{padding:.9rem 1.1rem .9rem 3.2rem;font-size:1rem;line-height:1.5;color:#d3f0ea;margin-top:1rem}
.quote::after{content:"\201C";position:absolute;left:.9rem;top:.2rem;font-family:var(--hf);font-size:2.6rem;color:var(--cyan)}
/* шестиугольные иконки */
.hx{display:inline-block;width:3.1rem;height:3.1rem;flex:none}.hx svg{width:100%;height:100%;overflow:visible}
.hxf{fill:rgba(46,230,200,.07);stroke:var(--cyan);stroke-width:1.5}
.hxi{fill:none;stroke:var(--ice);stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.hx.sm{width:2.3rem;height:2.3rem}.hx.lg{width:4.2rem;height:4.2rem}
.ic{fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
/* карточки протоколов */
.pcards{display:grid;grid-template-columns:minmax(0,1fr);gap:.8rem}
.pc{padding:.9rem 1rem;display:flex;flex-direction:column;gap:.45rem}
.pc .top{display:flex;gap:.7rem;align-items:center}
.pc .nm{font-family:var(--hf);font-size:1.45rem;line-height:1;color:#fff;text-transform:uppercase}
.pc .full{font-size:.78rem;color:var(--cyan);font-family:var(--mono);line-height:1.3}
.pc .d{font-size:.92rem;line-height:1.45;color:#cfe9e3}
.pc.in{border-color:rgba(46,230,200,.6)}
/* таблицы */
.tw{overflow-x:auto;padding:.3rem}.tbl{width:100%;border-collapse:collapse;font-size:1rem}
.tbl.sm{font-size:.88rem}
.tbl th,.tbl td{text-align:left;padding:.5rem .75rem;border-bottom:1px solid rgba(45,230,200,.18);vertical-align:top}
.tbl thead th{color:var(--cyan);font-family:var(--hf);font-weight:700;text-transform:uppercase;font-size:.95rem;letter-spacing:.04em}
.tbl td:first-child{color:#fff;font-weight:700}
.tbl tr.sel td{background:rgba(46,230,200,.1);box-shadow:inset 3px 0 0 var(--cyan)}
/* reveal engine */
[data-s]{opacity:0;transform:translateY(10px);transition:opacity 280ms var(--ez) var(--dl,0ms),transform 280ms var(--ez) var(--dl,0ms),border-color 280ms,box-shadow 280ms}
[data-s].in{opacity:1;transform:none}
tr[data-s]{transform:none}
.an{transition:transform var(--md,1000ms) cubic-bezier(.45,.05,.35,1) var(--dl,0ms),opacity 380ms var(--ez)}
.dr{fill:none;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset 700ms linear,opacity .4s}
.dr.dsh{stroke-dasharray:1}
.arw.on .dr{stroke-dashoffset:0}
.arw .ah{opacity:0;transition:opacity 150ms}
.arw.on .ah{opacity:1;transition-delay:640ms}
.arw.old{opacity:.3}.arw{transition:opacity .4s}
.arw.fail .dr{stroke:var(--red)!important}.arw.fail .ah{fill:var(--red)!important}
.wt{stroke:var(--cyan)}.wb{stroke:var(--blue)}.wa{stroke:var(--amber)}.wv{stroke:var(--violet)}.wr{stroke:var(--red)}.wg{stroke:var(--green)}.wi{stroke:var(--ice)}
.ah.wt{fill:var(--cyan)}.ah.wb{fill:var(--blue)}.ah.wa{fill:var(--amber)}.ah.wv{fill:var(--violet)}.ah.wr{fill:var(--red)}.ah.wg{fill:var(--green)}.ah.wi{fill:var(--ice)}
.arw.on:not(.old) .dr{filter:drop-shadow(0 0 4px currentColor)}
.ni,.ni *{transition:none!important}
.flash{animation:fl 500ms var(--ez) 1}@keyframes fl{0%{opacity:.15}100%{opacity:1}}
/* svg */
.dg text{font-family:var(--f);fill:var(--ink);font-size:18px}
.dg .nlab{font-size:16px;font-weight:700}.dg .nsub{font-size:14px;fill:var(--cyan);font-family:var(--mono)}
.nhx{fill:rgba(8,32,30,.9);stroke:var(--teal-dim);stroke-width:2;transition:stroke .3s,fill .3s}
.sic{fill:none;stroke:var(--ice);stroke-width:1.4;stroke-linecap:round;stroke-linejoin:round}
.nd{transition:filter .3s}
.nd.hot .nhx{stroke:var(--ice);fill:rgba(46,230,200,.16)}.nd.hot{filter:drop-shadow(0 0 10px rgba(46,230,200,.6))}
.nd.bad .nhx{stroke:var(--red);fill:rgba(255,92,110,.14)}.nd.bad .sic{stroke:var(--red)}
.lk{stroke:rgba(45,230,200,.22);stroke-width:2;stroke-dasharray:2 6}
.ll{stroke:rgba(45,230,200,.3);stroke-width:1.5;stroke-dasharray:4 6}
.dg .tag{font-size:15px;font-weight:700;fill:var(--amber);font-family:var(--mono)}
.pk path{fill:#03120f;stroke-width:2}.pk.wt path{stroke:var(--cyan)}.pk.wb path{stroke:var(--blue)}.pk.wa path{stroke:var(--amber)}.pk.wv path{stroke:var(--violet)}.pk.wr path{stroke:var(--red)}.pk.wg path{stroke:var(--green)}.pk.wi path{stroke:var(--ice)}
.dg .pk text{font-size:14px;font-weight:700;font-family:var(--mono)}
.pk.wt text{fill:var(--cyan)}.pk.wb text{fill:var(--blue)}.pk.wa text{fill:var(--amber)}.pk.wv text{fill:var(--violet)}.pk.wr text{fill:var(--red)}.pk.wg text{fill:var(--green)}.pk.wi text{fill:var(--ice)}
.dg .mlab{font-size:16px;font-weight:700}.dg .msub{font-size:13px;fill:var(--dim);font-family:var(--mono)}
.ml.wt .mlab{fill:var(--cyan)}.ml.wb .mlab{fill:var(--blue)}.ml.wa .mlab{fill:var(--amber)}.ml.wv .mlab{fill:var(--violet)}.ml.wr .mlab{fill:var(--red)}.ml.wg .mlab{fill:var(--green)}.ml.wi .mlab{fill:var(--ice)}
.xmark path{stroke:var(--red);stroke-width:4;stroke-linecap:square;fill:none}
.zone{fill:rgba(46,230,200,.035);stroke:rgba(45,230,200,.3);stroke-width:1.5;stroke-dasharray:6 6}
.zone.red{fill:rgba(255,92,110,.05);stroke:rgba(255,92,110,.45)}
.dg .zl{font-size:14px;font-weight:700;fill:var(--dim);letter-spacing:.12em;text-transform:uppercase}
.hb{fill:rgba(8,32,30,.9);stroke:var(--edge);stroke-width:2;transition:stroke .3s,fill .3s}
.dg .hbt{font-weight:700;font-size:16px}
.hbx.hot .hb{stroke:var(--ice);fill:rgba(46,230,200,.18)}.hbx.hot{filter:drop-shadow(0 0 8px rgba(46,230,200,.55))}
.hbx.red .hb{stroke:var(--red);fill:rgba(255,92,110,.15)}.hbx.red .hbt{fill:var(--red)}
.ax{stroke:var(--dim);stroke-width:1.5}
.lbar{fill:rgba(46,230,200,.12);stroke:var(--edge);stroke-width:1.5}
.tmk{stroke:var(--amber);stroke-width:2;stroke-dasharray:5 4}
.dg .tml{font-family:var(--hf);font-size:18px;fill:var(--amber);letter-spacing:.04em}.dg .tml.red{fill:var(--red)}
.lmk{fill:var(--cyan);stroke:var(--cyan);stroke-width:3;filter:drop-shadow(0 0 6px var(--cyan))}
.evl{stroke-width:1.5;stroke-dasharray:3 4}
.peer{stroke:var(--amber);stroke-width:2;stroke-dasharray:6 5;fill:none}
.dg .dots{font-size:40px;fill:var(--dim)}
/* поток: сетка */
.flow{display:flex;flex-direction:column;gap:.6rem}
.flow .dg{max-height:52vh}.wrap>.flow .dg{max-height:58vh}
.flg{display:grid;grid-template-columns:minmax(0,1fr);gap:.8rem;align-items:start}
.flv{min-width:0}
.fpan{background:var(--panel2);border:1px solid var(--edge);clip-path:var(--cut6);padding:.7rem .8rem;display:flex;flex-direction:column;gap:.1rem}
.fpt{font-family:var(--hf);text-transform:uppercase;color:var(--cyan);font-size:.95rem;letter-spacing:.06em;margin-bottom:.35rem}
.fr{display:grid;grid-template-columns:6.4rem minmax(0,1fr);gap:.5rem;font-size:.84rem;padding:.28rem 0;border-bottom:1px solid rgba(45,230,200,.12)}
.fk{color:var(--dim);font-weight:700}.fv{color:var(--ice);word-break:break-word}
.fcap{display:flex;gap:.8rem;align-items:flex-start;min-height:3.1em;border-top:1px solid rgba(45,230,200,.18);padding-top:.6rem}
.fsn{flex:none;color:var(--bg);background:var(--cyan);font-weight:700;font-size:.8rem;padding:.15rem .5rem;clip-path:var(--cut6);min-width:4.2rem;text-align:center}
.fsn:empty{visibility:hidden}
.fct{font-size:1.02rem;line-height:1.45;color:#eafffb}
.seg{display:flex;gap:.5rem;flex-wrap:wrap}
/* URL */
.url{display:flex;flex-wrap:wrap;gap:.3rem;font-family:var(--mono);font-size:1.25rem;align-items:flex-end}
.url .u{display:flex;flex-direction:column;align-items:center;gap:.3rem;padding:.35rem .6rem;border:1px solid transparent;transition:border-color .4s,transform .6s var(--ez),background .4s}
.url .u small{font-family:var(--f);font-size:.72rem;color:var(--dim);opacity:0;transition:opacity .4s}
.url.split .u{border-color:var(--edge);background:rgba(46,230,200,.07)}.url.split .u small{opacity:1}
.url.split .u1{transform:translateX(-.5rem)}.url.split .u3{transform:translateX(.5rem)}
.url .u1 b{color:var(--amber)}.url .u2 b{color:var(--cyan)}.url .u3 b{color:var(--violet)}
/* домен */
.dom{display:flex;justify-content:center;flex-wrap:wrap;gap:.2rem;font-family:var(--hf);font-size:clamp(2rem,4.6vw,4.4rem);letter-spacing:.02em;margin:1rem 0 .6rem}
.dom .dp{padding:.1rem .45rem;border:1px solid rgba(45,230,200,.2);color:#6f948d;transition:color .4s,border-color .4s,box-shadow .4s,background .4s;clip-path:var(--cut6)}
.dom .dot{color:var(--dim);padding:0 .05rem}
.dom .dp.in{color:#fff;border-color:var(--cyan);background:rgba(46,230,200,.1)}
.dom .dp.cur{box-shadow:0 0 18px rgba(46,230,200,.55);color:var(--cyan)}
.dlev{display:grid;grid-template-columns:minmax(0,1fr);gap:.7rem}
/* биты DNS */
.bits{display:grid;grid-template-columns:repeat(16,minmax(0,1fr));gap:3px;margin:.6rem 0}
.bit{font-family:var(--hf);font-size:1rem;text-align:center;padding:.55rem .1rem;background:rgba(46,230,200,.08);border:1px solid var(--edge);color:#fff;cursor:help;transition:background .2s,box-shadow .2s;outline:none}
.bit:hover,.bit:focus-visible,.bit.sel{background:var(--cyan);color:#03120f;box-shadow:0 0 14px rgba(46,230,200,.6)}
.bit.new{border-color:var(--amber)}.bit.new:hover,.bit.new.sel,.bit.new:focus-visible{background:var(--amber)}
.bitsz{display:grid;grid-template-columns:repeat(16,minmax(0,1fr));gap:3px;font-size:.7rem;color:var(--dim);text-align:center;font-family:var(--mono)}
.bdesc{min-height:5.2em;padding:.8rem 1rem;font-size:1rem;line-height:1.45}.bdesc b{color:var(--cyan);font-family:var(--hf);font-size:1.15rem;display:block;margin-bottom:.2rem;text-transform:uppercase}
.hdr{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:3px}
.hdr div{padding:.55rem .7rem;background:rgba(46,230,200,.07);border:1px solid var(--edge);font-family:var(--mono);font-size:.92rem;display:flex;justify-content:space-between;gap:.5rem}
.hdr div span{color:var(--dim);font-size:.78rem}
.hdr .w2{grid-column:span 2}
/* стек секций DNS */
.stack{display:flex;flex-direction:column;gap:.45rem}
.sec{display:grid;grid-template-columns:3.2rem 10rem minmax(0,1fr);gap:.8rem;align-items:center;padding:.7rem .9rem}
.sec .nm{font-family:var(--hf);font-size:1.25rem;text-transform:uppercase;color:#fff}.sec .d{font-size:.92rem;line-height:1.4;color:#cfe9e3}
/* титул */
.tslide .sc{padding:0}.tslide .wrap{max-width:none;height:100%;margin:0}
.title{position:relative;height:100%;display:flex;flex-direction:column;justify-content:center;padding:0 clamp(16px,8vw,170px);background:linear-gradient(90deg,rgba(4,16,15,.99) 38%,rgba(4,16,15,.82) 62%,rgba(4,16,15,.5)),var(--bgi) right center/cover no-repeat}
.kick{font-family:var(--hf);font-size:1.1rem;letter-spacing:.2em;text-transform:uppercase;color:var(--cyan);margin-bottom:.6rem;display:flex;gap:.8rem;align-items:center}
.title h1{font-family:var(--hf);font-size:clamp(2.8rem,8vw,7.2rem);line-height:.92;font-weight:700;text-transform:uppercase;margin-bottom:1.2rem;color:#fff}
.title h1 .o2{color:var(--cyan);text-shadow:0 0 34px rgba(46,230,200,.55)}
.lead{font-size:1.25rem;line-height:1.45;color:#c4e8e1;max-width:40ch;margin-bottom:2rem}
.authors{font-size:1.05rem;line-height:1.6;color:var(--ice)}
.bye h1{font-size:clamp(3rem,10vw,9rem)}
/* тренажёры */
.trn,.quiz{padding:1.3rem 1.4rem}
.tq{font-size:1.2rem;line-height:1.4;margin-bottom:1rem}
.trow{display:flex;flex-wrap:wrap;gap:.7rem;align-items:center}
.btn{font:inherit;font-size:.9rem;font-weight:800;padding:.55rem 1rem;border:1px solid var(--edge);background:rgba(8,32,30,.8);color:var(--ink);cursor:pointer;clip-path:var(--cut6);transition:background .15s,color .15s,border-color .15s;text-transform:uppercase;letter-spacing:.03em}
.btn:hover{border-color:var(--cyan);background:rgba(46,230,200,.14)}.btn:active{background:rgba(46,230,200,.3)}
.btn.pri,.btn.on{background:var(--cyan);border-color:var(--cyan);color:#03120f;box-shadow:0 0 14px rgba(46,230,200,.45)}
.btn:disabled{opacity:.4;cursor:default}
.btn:focus-visible,.opt:focus-visible,#nav button:focus-visible,.ovi:focus-visible,input:focus-visible,.bit:focus-visible{outline:2px solid var(--amber);outline-offset:2px}
.tres{min-height:2.6rem;font-size:1rem;line-height:1.45;margin:.2rem 0 .8rem}
.tres.ok{color:var(--green)}.tres.no{color:var(--red)}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:.6rem}.opts.col{grid-template-columns:1fr}
.opt{font:inherit;text-align:left;font-size:1rem;padding:.7rem 1rem;border:1px solid var(--edge);background:rgba(8,32,30,.7);color:var(--ink);cursor:pointer;clip-path:var(--cut6)}
.opt:hover{border-color:var(--cyan)}
.opt.ok{border-color:var(--green);background:rgba(140,227,106,.15)}.opt.no{border-color:var(--red);background:rgba(255,92,110,.15)}
.qtop{display:flex;justify-content:space-between;color:var(--dim);margin-bottom:.6rem}
.side{display:flex;flex-direction:column;gap:.8rem}
/* nav */
#nav{position:fixed;z-index:40;left:50%;bottom:12px;transform:translateX(-50%);display:flex;align-items:center;gap:.3rem;background:rgba(4,22,20,.94);border:1px solid var(--edge);clip-path:var(--cut6);padding:.35rem .5rem;font-size:14px}
#nav button{font:inherit;font-size:13px;font-weight:800;border:0;background:transparent;color:var(--ink);padding:.42rem .65rem;cursor:pointer;display:inline-flex;align-items:center;gap:.35rem;text-transform:uppercase}
#nav button:hover{background:rgba(46,230,200,.14)}#nav button:disabled{opacity:.35}
#nav svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}
.nsep{width:1px;height:22px;background:var(--edge);margin:0 .2rem}
#ind{font-family:var(--mono);font-size:13px;padding:0 .4rem;white-space:nowrap;display:inline-flex;gap:.45rem;align-items:baseline}#ind i{font-style:normal;font-size:11px;color:var(--dim)}
#ov{position:fixed;inset:0;z-index:60;background:rgba(3,12,11,.97);overflow:auto;padding:clamp(16px,5vh,60px) clamp(16px,6vw,120px)}
#ov h2{margin-bottom:1.2rem;font-size:2rem}
.ovg{display:grid;grid-template-columns:repeat(auto-fill,minmax(14rem,1fr));gap:.6rem}
.ovi{font:inherit;text-align:left;display:flex;gap:.8rem;align-items:center;padding:.7rem .9rem;background:var(--panel);border:1px solid var(--edge);cursor:pointer;color:var(--ink);font-size:.95rem;clip-path:var(--cut6)}
.ovi:hover,.ovi.cur{border-color:var(--cyan)}.ovi .mono{color:var(--cyan);font-weight:800;width:2rem}
@media (min-width:768px){.g2{grid-template-columns:repeat(2,minmax(0,1fr))}.g3{grid-template-columns:repeat(3,minmax(0,1fr))}.g4{grid-template-columns:repeat(2,minmax(0,1fr))}
  .pcards{grid-template-columns:repeat(2,minmax(0,1fr))}.dlev{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:1280px){.two{grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr)}.two.even{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.two.wide{grid-template-columns:minmax(0,.62fr) minmax(0,1.38fr)}
  .pcards{grid-template-columns:repeat(3,minmax(0,1fr))}.g4{grid-template-columns:repeat(4,minmax(0,1fr))}.dlev{grid-template-columns:repeat(4,minmax(0,1fr))}
  .flg{grid-template-columns:minmax(0,1fr) 19rem}.flg.one{grid-template-columns:minmax(0,1fr)}}
@media (max-width:767px){html{font-size:15px}h2{font-size:min(2rem,30px)}.sc{padding-bottom:8rem}.opts{grid-template-columns:1fr}
  .dg{max-height:none}.tbl{min-width:34rem}.bl.big li{font-size:1.15rem}#nav{flex-wrap:wrap;justify-content:center;width:calc(100% - 32px)}
  .title{background:linear-gradient(rgba(4,16,15,.85),rgba(4,16,15,.92)),var(--bgi) center/cover}.bit{font-size:.62rem;padding:.4rem 0}
  .sec{grid-template-columns:2.6rem minmax(0,1fr)}.sec .d{grid-column:span 2}.hdr div{font-size:.78rem}}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{transition:none!important;animation:none!important}}
"""

DECO = '<div id="deco" aria-hidden="true"><i></i><i></i><b></b></div>'

JS = r"""
(function(){
'use strict';
var $=function(s,r){return (r||document).querySelector(s)}, $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
var SCENES=__SCENES__;
var slides=$$('.slide'), N=slides.length, cur=0, step=0;
var RM=window.matchMedia('(prefers-reduced-motion: reduce)');
function recalcMax(s){
  var mx=0; s._els.forEach(function(e){ mx=Math.max(mx,+e.dataset.s||0); });
  (s._scenes||[]).forEach(function(sc){ if(!sc.hidden) mx=Math.max(mx,sc._sp.n); });
  s._max=mx;
}
function bindScene(s,sc){
  var sp=SCENES[sc.dataset.scene]; sc._sp=sp; sc._map={};
  Object.keys(sp.e).forEach(function(id){ var el=$('[data-id="'+id+'"]',sc); if(el){ if(el._b===undefined) el._b=el.getAttribute('class')||''; sc._map[id]=el; } });
  if(!s._scenes) s._scenes=[];
  if(s._scenes.indexOf(sc)<0) s._scenes.push(sc);
  s._scene=sc; recalcMax(s);
}
slides.forEach(function(s){
  s._els=$$('[data-s]',s); s._scenes=[];
  $$('[data-scene]:not([hidden])',s).forEach(function(sc){ bindScene(s,sc); });
  recalcMax(s);
});
function applyScene(sc,k,instant){
  var sp=sc._sp; k=Math.min(k,sp.n);
  Object.keys(sp.e).forEach(function(id){
    var el=sc._map[id], t=sp.e[id]; if(!el) return;
    if(t.p) el.style.transform='translate('+t.p[k][0]+'px,'+t.p[k][1]+'px)';
    if(t.o) el.style.opacity=t.o[k];
    if(t.c){ el.setAttribute('class',(el._b+' '+t.c[k]).trim()); }
    if(t.t && el.textContent!==t.t[k]){ el.textContent=t.t[k]; if(!instant){ el.classList.remove('flash'); void el.getBoundingClientRect(); el.classList.add('flash'); } }
  });
}
function setStep(k,instant){
  var sl=slides[cur]; step=Math.max(0,Math.min(sl._max,k));
  if(instant) sl.classList.add('ni');
  sl._els.forEach(function(e){ e.classList.toggle('in',+e.dataset.s<=step); });
  (sl._scenes||[]).forEach(function(sc){ if(!sc.hidden) applyScene(sc,step,instant); });
  if(instant){ void sl.offsetWidth; sl.classList.remove('ni'); }
}
function upd(){
  var sl=slides[cur], ind=$('#ind');
  ind.innerHTML='<b></b><i></i>';
  ind.firstChild.textContent=(cur+1)+' / '+N;
  ind.lastChild.textContent=sl._max?('шаг '+step+'/'+sl._max):'';
  $('#prog i').style.width=((cur+1)/N*100)+'%';
  $('#b-play').disabled=!sl._max;
  $('#b-prev').disabled=(cur===0&&step===0);
  $('#b-next').disabled=(cur===N-1&&step>=sl._max);
}
function play(){ var sl=slides[cur]; setStep(RM.matches?sl._max:0,true); upd(); }
function go(i,atEnd){
  i=Math.max(0,Math.min(N-1,i));
  slides.forEach(function(s){s.classList.remove('on')}); cur=i; slides[cur].classList.add('on');
  var sc=$('.sc',slides[cur]); if(sc) sc.scrollTop=0;
  setStep(atEnd?slides[cur]._max:0,true);
  try{ history.replaceState(null,'','#'+(cur+1)); }catch(e){}
  upd();
}
function next(){ var sl=slides[cur]; if(step<sl._max){ setStep(step+1,false); upd(); return; } if(cur<N-1) go(cur+1); }
function prev(){ if(step>0){ setStep(step-1,true); upd(); return; } if(cur>0) go(cur-1,true); }
$('#b-prev').onclick=prev; $('#b-next').onclick=next; $('#b-play').onclick=play;
var ov=$('#ov'), ovg=$('.ovg',ov);
slides.forEach(function(s,k){ var b=document.createElement('button'); b.className='ovi'; b.type='button';
  b.innerHTML='<span class="mono">'+(k+1)+'</span><span></span>'; b.lastChild.textContent=s.dataset.label;
  b.onclick=function(){ ov.hidden=true; go(k); }; ovg.appendChild(b); });
function openOv(){ ov.hidden=false; $$('.ovi',ov).forEach(function(b,k){b.classList.toggle('cur',k===cur)}); var c=$('.ovi.cur',ov); if(c)c.focus(); }
$('#b-ov').onclick=openOv;
var lb=$('#lb'); $$('.ph img').forEach(function(im){ im.addEventListener('click',function(){ $('img',lb).src=im.src; $('img',lb).alt=im.alt; lb.hidden=false; }); });
lb.onclick=function(){ lb.hidden=true; };
/* ---- приближение элемента по клику ---- */
var zl=$('#zl'), zi=$('#zi');
var ZSEL='.card,.ph,.ws,.dia,.msg,.srow,.stg,.tile,.art,.slab,.hexn,.dev,.prow,.bigdom,.htab,.fbar,.chain,.stack3d,.urlbar,.ibox,.pnl,.tbl,figure,svg.fig';
function zclose(){ zl.hidden=true; zi.innerHTML=''; }
function zoomEl(el){
  var r=el.getBoundingClientRect(); if(r.width<40||r.height<24) return;
  zi.innerHTML=''; zi.style.transform='none';
  var c=el.cloneNode(true);
  c.removeAttribute('id'); $$('[id]',c).forEach(function(x){x.removeAttribute('id')});
  c.classList.add('in'); $$('[data-s]',c).forEach(function(x){x.classList.add('in')});
  c.style.margin='0'; c.style.width=r.width+'px'; c.style.maxWidth='none'; c.style.maxHeight='none';
  zi.appendChild(c); zl.hidden=false;
  var b=zi.getBoundingClientRect();
  var k=Math.min((innerWidth-60)/b.width,(innerHeight-70)/b.height,3.2);
  if(!isFinite(k)||k<1) k=1; if(k<1.08) k=1.08;
  zi.style.transform='scale('+k.toFixed(3)+')';
}
document.addEventListener('click',function(e){
  if(!zl.hidden){ zclose(); return; }
  if(!lb.hidden||!ov.hidden) return;
  var t=e.target; if(!t.closest) return;
  if(t.closest('button,a,input,select,textarea,#nav,#ov,.tw,.bits,.opt,[data-sw],.ph img')) return;
  var el=t.closest(ZSEL); if(!el||!el.closest('.slide.on')) return;
  e.preventDefault(); zoomEl(el);
});
$$(ZSEL.split(',').join(',')).forEach(function(el){ el.classList.add('zoomable'); });
var dbuf='', dtm=null;
document.addEventListener('keydown',function(e){
  var t=e.target, tag=t.tagName;
  if(e.ctrlKey||e.metaKey||e.altKey) return;
  if(tag==='INPUT'){ if(e.key==='Escape') t.blur(); return; }
  if(!zl.hidden){ if(e.key==='Escape'||e.key===' '||e.key==='Enter'){ e.preventDefault(); zclose(); } return; }
  if(!lb.hidden){ if(e.key==='Escape'||e.key===' '||e.key==='Enter'){ e.preventDefault(); lb.hidden=true; } return; }
  if(e.key==='Escape'){ e.preventDefault(); ov.hidden?openOv():(ov.hidden=true); return; }
  if(!ov.hidden) return;
  switch(e.key){
    case 'ArrowRight': case 'ArrowDown': case 'PageDown': e.preventDefault(); next(); return;
    case 'ArrowLeft': case 'ArrowUp': case 'PageUp': e.preventDefault(); prev(); return;
    case ' ': if(tag==='BUTTON') return; e.preventDefault(); next(); return;
    case 'Home': e.preventDefault(); go(0); return;
    case 'End': e.preventDefault(); go(N-1); return;
  }
  var k=e.key.toLowerCase();
  if(k==='r'||k==='к'){ play(); return; }
  if(/^[0-9]$/.test(e.key)){ dbuf+=e.key; clearTimeout(dtm); dtm=setTimeout(function(){ var n=parseInt(dbuf,10); dbuf=''; if(n>=1&&n<=N) go(n-1); },550); }
});
/* перелистывание колесом отключено — только стрелки и кнопки */
var tx=0,ty=0,tt=0;
window.addEventListener('touchstart',function(e){ var p=e.changedTouches[0]; tx=p.clientX; ty=p.clientY; tt=Date.now(); },{passive:true});
window.addEventListener('touchend',function(e){ var p=e.changedTouches[0], dx=p.clientX-tx, dy=p.clientY-ty;
  if(Date.now()-tt>700||Math.abs(dx)<60||Math.abs(dx)<Math.abs(dy)*1.4) return; if(e.target.closest&&e.target.closest('.tw,input,.bits')) return; dx<0?next():prev(); },{passive:true});

/* ---- переключатели сценариев (DNS рекурсивный / итеративный и др.) ---- */
$$('[data-sw]').forEach(function(box){
  var s=box.closest('.slide'), btns=$$('[data-to]',box);
  btns.forEach(function(b){ b.onclick=function(){
    btns.forEach(function(x){ x.classList.toggle('on',x===b); x.setAttribute('aria-pressed',x===b); });
    $$('[data-scene]',s).forEach(function(c){ c.hidden=c.dataset.scene!==b.dataset.to; });
    bindScene(s,$('[data-scene="'+b.dataset.to+'"]',s)); if(slides[cur]===s) play(); }; });
});
/* ---- биты флагов DNS ---- */
$$('.bitbox').forEach(function(bx){
  var d=$('.bdesc',bx), bs=$$('.bit',bx);
  function sh(b){ bs.forEach(function(x){x.classList.toggle('sel',x===b)}); d.innerHTML='<b></b><span></span>'; d.firstChild.textContent=b.dataset.n; d.lastChild.textContent=b.dataset.d; }
  bs.forEach(function(b){ b.addEventListener('mouseenter',function(){sh(b)}); b.addEventListener('focus',function(){sh(b)}); b.addEventListener('click',function(){sh(b)}); });
});

function rnd(n){ return Math.floor(Math.random()*n); }
function shuffle(a){ a=a.slice(); for(var i=a.length-1;i>0;i--){ var j=rnd(i+1), t=a[i]; a[i]=a[j]; a[j]=t; } return a; }
function choice(pre,gen,keep){
  var tot=0, ok=0; if(!$('#'+pre+'-q')) return;
  function nx(){ var q=gen(), o=$('#'+pre+'-o'), done=false; $('#'+pre+'-q').innerHTML=q.q; o.innerHTML=''; var r=$('#'+pre+'-r'); r.textContent=''; r.className='tres';
    (keep?q.o:shuffle(q.o)).forEach(function(t){ var b=document.createElement('button'); b.type='button'; b.className='opt'; b.textContent=t;
      b.onclick=function(){ if(done) return; done=true; var good=t===q.o[q.a||0];
        $$('.opt',o).forEach(function(x){ if(x.textContent===q.o[q.a||0]) x.classList.add('ok'); }); if(!good) b.classList.add('no');
        tot++; if(good) ok++; r.textContent=(good?'Верно. ':'Неверно. ')+q.e; r.className='tres '+(good?'ok':'no');
        var sc=$('#'+pre+'-sc'); if(sc) sc.textContent=ok+' / '+tot; };
      o.appendChild(b); }); }
  $('#'+pre+'-nx').onclick=nx; nx();
}
var TR=__TRAIN__;
function pool(list,idx){ return list.map(function(x){return x[idx]}).filter(function(v,i,a){return a.indexOf(v)===i}); }
var last={};
function pick(key,list){ var x; do{ x=list[rnd(list.length)]; }while(list.length>1&&x===last[key]); last[key]=x; return x; }
choice('t1',function(){ var m=pick('t1',TR.task), all=pool(TR.task,1); return {q:m[0], o:[m[1]].concat(shuffle(all.filter(function(x){return x!==m[1]})).slice(0,3)), a:0, e:m[2]}; });
choice('t2',function(){ var m=pick('t2',TR.port), all=pool(TR.port,1); return {q:'Порт <b class="mono">'+m[0]+'</b>. Какой протокол его использует?', o:[m[1]].concat(shuffle(all.filter(function(x){return x!==m[1]})).slice(0,3)), a:0, e:m[2]}; });
choice('t3',function(){ var m=pick('t3',TR.dhcp); return {q:m[0], o:m[1], a:m[2], e:m[3]}; },true);
choice('t4',function(){ var m=pick('t4',TR.dom), all=['Корневой домен','Домен верхнего уровня (TLD)','Домен второго уровня (SLD)','Поддомен','Обозначение веб-сайта']; return {q:'В имени <b class="mono">'+m[0]+'</b> часть <b class="mono">'+m[1]+'</b> — это…', o:all, a:all.indexOf(m[2]), e:m[3]}; },true);
(function(){
  var Q=__QUIZ__, i=0, got=Q.map(function(){return -1}); if(!$('#qz-q')) return;
  function sc(){ return got.filter(function(g,k){return g===Q[k].a}).length; }
  function render(){ var q=Q[i]; $('#qz-n').textContent=(i+1)+' / '+Q.length; $('#qz-q').textContent=q.q;
    var o=$('#qz-o'); o.innerHTML=''; var e=$('#qz-e'); e.textContent=''; e.className='tres';
    q.o.forEach(function(t,k){ var b=document.createElement('button'); b.type='button'; b.className='opt'; b.textContent=t; b.onclick=function(){ if(got[i]<0) got[i]=k; show(); }; o.appendChild(b); });
    if(got[i]>=0) show(); $('#qz-sc').textContent='верно: '+sc(); $('#qz-pv').disabled=i===0; $('#qz-nx').textContent=i===Q.length-1?'Начать заново':'Следующий вопрос'; }
  function show(){ var q=Q[i], bs=$$('.opt',$('#qz-o')); bs[q.a].classList.add('ok'); if(got[i]!==q.a) bs[got[i]].classList.add('no');
    var e=$('#qz-e'); e.textContent=(got[i]===q.a?'Верно. ':'Неверно. ')+q.e; e.className='tres '+(got[i]===q.a?'ok':'no'); $('#qz-sc').textContent='верно: '+sc(); }
  $('#qz-nx').onclick=function(){ if(i===Q.length-1){ got=Q.map(function(){return -1}); i=0; } else i++; render(); };
  $('#qz-pv').onclick=function(){ if(i>0){ i--; render(); } };
  render();
})();
var h=parseInt((location.hash||'').slice(1),10);
go(h>=1&&h<=N?h-1:0);
})();
"""
