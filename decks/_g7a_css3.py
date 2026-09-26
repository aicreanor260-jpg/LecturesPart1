CSS3 = r"""
.dv.rp{filter:drop-shadow(0 0 10px rgba(46,230,200,.35))}
.nd.hot .dv.rp{filter:drop-shadow(0 0 18px rgba(126,245,226,.95))}.nd.bad .dv.rp{filter:drop-shadow(0 0 16px rgba(255,92,110,1)) hue-rotate(160deg)}
.dv.rp.red{filter:drop-shadow(0 0 10px rgba(255,92,110,.8)) hue-rotate(170deg)}.dv.rp.blue{filter:drop-shadow(0 0 10px rgba(74,168,255,.7)) hue-rotate(40deg)}
.dvl2{font-family:var(--hf);font-size:16px;fill:#fff;paint-order:stroke;stroke:#03120f;stroke-width:4px}

html{font-size:clamp(14px,min(1vw,1.82vh),30px)}
.p.sm,.pcb .d,.pc.sm .pcb .d,.lrow span,.tile .tt,.dots li,.hsteps li,.cbox span,.ibox,.qbar,.addr>div,.addr b,.kv,.tbl2,.pns,.code,.ws,.stga,.stgl{font-size:max(.95rem,15px)!important}
.lrow b,.tile b,.prow em,.dvbs{font-size:max(1.02rem,16px)!important}
.dg text{font-size:21px}.dg .nlab{font-size:19px}.dg .nsub,.dg .tag{font-size:16px}.dg .mlab{font-size:18px}.dg .msub{font-size:15px}.dg .pk text{font-size:16px}
.fct{font-size:1.15rem}
.ih h2{font-size:clamp(1.8rem,3vw,3.4rem);overflow-wrap:anywhere;hyphens:auto}.ih.big h2{font-size:clamp(2rem,3.8vw,4.4rem)}.fr{font-size:.95rem}
.ih h2 .o2:not(.in){font-size:.74em;line-height:1}
.ih.big h2 .o2:not(.in){font-size:.56em}
.flow .dg{max-height:44vh}.wrap>.flow .dg{max-height:52vh}
.sc{padding-top:clamp(14px,3vh,40px)}

.prow{display:grid;grid-template-columns:auto minmax(0,1fr) minmax(0,1fr);gap:.8rem;align-items:center;padding:.35rem .6rem;border:1px solid rgba(45,230,200,.22);background:rgba(8,32,30,.55);clip-path:var(--cut6)}
.prow b{display:block;font-family:var(--hf);font-size:1.15rem;color:#fff}.prow span{display:block;font-size:.76rem;color:var(--dim)}.prow em{font-style:normal;font-size:.84rem;color:#d3f0ea;border-left:1px solid rgba(45,230,200,.3);padding-left:.8rem}
.pns.sp{letter-spacing:.3em;text-transform:uppercase;color:var(--cyan);font-family:var(--hf)}
.goal{display:flex;justify-content:space-between;align-items:center;margin-bottom:.6rem}
.title .tart{position:absolute;right:3vw;top:50%;transform:translateY(-50%);width:44vw;height:80vh;pointer-events:none}
.tglobe{position:absolute;right:0;top:0;width:34vw;opacity:.85;filter:drop-shadow(0 0 30px rgba(46,230,200,.45))}
.tlap{position:absolute;left:4vw;bottom:6vh}
.tic{position:absolute}.tic.t0{left:6vw;top:10vh}.tic.t1{left:18vw;top:2vh}.tic.t2{right:4vw;bottom:24vh}.tic.t3{left:2vw;top:36vh}.tic.t4{right:26vw;bottom:6vh}.tic.t5{right:2vw;top:4vh}
.tic .hx{filter:drop-shadow(0 0 12px rgba(46,230,200,.7))}
.title{background:radial-gradient(ellipse at 75% 50%,rgba(46,230,200,.12),transparent 60%),var(--bg)!important}
.title>*:not(.tart){position:relative;z-index:1}
.art.col{flex-direction:column;gap:.3rem}.arrd{width:2px;height:1rem;background:var(--cyan)}
.mini-list{font-size:.72rem;line-height:1.5;border:1px solid var(--edge);padding:.3rem .5rem;background:#031716;color:#dff}
.pc.sm .pcb .d{font-size:.8rem}.pc.sm .pct .nm{font-size:1.3rem}.pc.sm .nb{width:2.3rem;height:2rem;font-size:1.05rem}.pc.sm .art .bigic{width:3.2rem;height:3.2rem}
.lane{display:flex;flex-direction:column;gap:1rem;text-align:center;font-family:var(--hf);color:#dff}
.lanebar{position:relative;display:flex;justify-content:center;gap:1.4rem;padding-bottom:.4rem}
.lanebar .mline{position:absolute;left:0;right:0;bottom:0;margin:0}
.fly{transition:transform 1.2s var(--ez) var(--dl,0ms),opacity .4s var(--dl,0ms)!important}
.fly.up{transform:translateX(-40%)}.fly.dn{transform:translateX(40%)}.fly.in{transform:none}
.plist{display:flex;flex-direction:column;gap:.4rem;text-align:center}.plist small{font-size:.7rem;color:var(--dim)}
.pstack{display:flex;flex-direction:column;gap:2px}.pstack div{font-family:var(--hf);font-size:1.2rem;text-align:center;padding:.45rem;border:1px solid var(--cyan);background:rgba(46,230,200,.18);color:#fff}
.pstack div:first-child{background:rgba(46,230,200,.4)}
.rtag{position:absolute;right:1.2rem;bottom:1rem;font-family:var(--hf);font-size:1.2rem;text-transform:uppercase;color:#fff;text-align:right}
.plus{display:grid;grid-template-columns:1fr auto 1fr auto 1fr;gap:.5rem;align-items:center}.plus>span{font-family:var(--hf);font-size:2rem;color:var(--cyan)}
.chain{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:.4rem;position:relative}
.chain .tile:not(:last-child)::after{content:"";position:absolute;right:-.5rem;top:1.4rem;border-left:8px solid var(--cyan);border-top:6px solid transparent;border-bottom:6px solid transparent}
.chain .tile{position:relative;clip-path:none}
.bn{font-family:var(--hf);font-size:1.6rem;color:var(--cyan);margin-right:.5rem}
.c5{display:flex;flex-direction:column}.c5 .c5v{flex:1;display:flex;flex-direction:column;justify-content:center;margin:.5rem 0}.c5 .pnh h3{font-size:1rem}
.stg{padding:.8rem}.stg .pnh h3{font-size:1rem;text-transform:uppercase}
.stgd{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:.3rem;margin:.4rem 0}
.stga{text-align:center;font-size:.72rem}.stga small{display:block;color:inherit;margin-bottom:.2rem}.stga .mline{margin:.25rem 0}
.stgl{display:flex;justify-content:space-between;font-size:.78rem;font-weight:700;color:#fff;border-bottom:1px solid rgba(45,230,200,.2);padding-bottom:.4rem;margin-bottom:.4rem}
.okc{display:flex;justify-content:center}
.nb-blue{background:var(--blue);box-shadow:0 0 14px rgba(74,168,255,.6)}.nb-grn{background:var(--green);box-shadow:0 0 14px rgba(140,227,106,.6)}.nb-vio{background:var(--violet);box-shadow:0 0 14px rgba(155,123,255,.6)}
.nb-amb{background:var(--amber);box-shadow:0 0 14px rgba(245,184,61,.6)}.nb-red{background:var(--red);box-shadow:0 0 14px rgba(255,92,110,.6)}.nb-teal{background:var(--cyan)}
.drow{padding:.8rem 1rem}
.dsec{display:flex;flex-direction:column;gap:.7rem;max-width:62rem;position:relative;z-index:1}
.dsrow{display:grid;grid-template-columns:minmax(0,1fr) 4rem minmax(0,1.3fr);align-items:center}
.dsrow .slab{font-size:1.4rem;padding:.9rem 1.4rem;transform:perspective(700px) rotateX(18deg)}.dsrow .slab b{font-family:var(--hf);font-weight:700}
.dsl{height:2px;background:var(--cyan);box-shadow:0 0 6px var(--cyan);position:relative}.dsl::before,.dsl::after{content:"";position:absolute;top:-4px;width:10px;height:10px;border-radius:50%;background:var(--cyan)}.dsl::before{left:-4px}.dsl::after{right:-4px}
.cbox{border:1px solid var(--edge);background:rgba(6,26,24,.85);padding:.5rem .7rem;clip-path:var(--cut6)}.cbox b{display:block;font-family:var(--hf);font-size:1.1rem;color:var(--cyan)}.cbox span{font-size:.8rem;color:#d3f0ea;line-height:1.35}
.htab{border:1.5px solid var(--cyan);box-shadow:0 0 24px rgba(46,230,200,.3),inset 0 0 30px rgba(46,230,200,.12);background:rgba(8,40,38,.8)}
.htab .hr{display:flex;border-bottom:1px solid rgba(45,230,200,.4)}.htab .hr:last-child{border-bottom:0}
.htab .hr.full{justify-content:center;position:relative;padding:.55rem}.htab .hr.full small{position:absolute;right:.8rem;top:.7rem}
.htab b{font-family:var(--hf);font-size:1.2rem;color:#fff}.htab small{font-size:.75rem;color:var(--dim)}
.htab .bits8>div{display:flex;flex-direction:column;align-items:center;padding:.45rem .2rem;border-right:1px solid rgba(45,230,200,.4)}.htab .bits8>div:last-child{border-right:0}
.fbar{display:flex;border:1.5px solid var(--cyan);box-shadow:0 0 22px rgba(46,230,200,.35);background:rgba(8,40,38,.8);clip-path:var(--cut6)}
.fb{display:flex;flex-direction:column;align-items:center;padding:.7rem .2rem;border-right:1px solid rgba(45,230,200,.4);outline:none}.fb:last-child{border-right:0}
.fb b{font-family:var(--hf);font-size:1.35rem;color:#fff}.fb small{font-size:.8rem;color:var(--dim)}.fb.new{background:rgba(245,184,61,.15)}.fb.new b{color:var(--amber)}
.fc{display:flex;flex-direction:column;padding:.8rem}.fc h3{color:#fff;font-size:1.3rem}.fc .p{flex:1}.fc .hx{align-self:center}
.bigdom{display:flex;justify-content:center;align-items:center;gap:.3rem;margin:1rem 0;padding:.8rem;border:1px solid var(--edge);background:rgba(4,20,19,.7);clip-path:var(--cut)}
.bigdom i{font-style:normal;font-family:var(--hf);font-size:3rem;color:#fff}
.bd{font-family:var(--hf);font-size:clamp(2rem,4.2vw,4.4rem);padding:.2rem 1rem;border:2px solid currentColor;background:rgba(3,20,19,.8);text-shadow:0 0 18px currentColor;box-shadow:0 0 18px -4px currentColor}
.netl{position:relative;height:2px;border-top:2px dashed var(--cyan);text-align:center}.netl span{position:relative;top:-1.6rem;font-family:var(--mono);font-size:.9rem;color:#fff}
.half{padding:1.2rem 1.3rem}
.qcloud{display:flex;flex-wrap:wrap;gap:.8rem;align-items:center;justify-content:center}.hx.red .hxf{stroke:var(--red)}.hx.red .hxi{stroke:var(--red)}
.pcmd{display:flex;flex-direction:column;gap:.25rem;font-family:var(--mono);font-size:.78rem}
.pl{display:grid;grid-template-columns:1fr 2.5rem 1fr;align-items:center;gap:.4rem;opacity:0;transition:opacity .3s var(--dl,0ms)}
.in .pl,.pcmd.in .pl{opacity:1}
.pl .sv{color:var(--green)}.pl .cl{color:var(--cyan)}
.pl .dir{height:2px;background:var(--dim);position:relative}.pl .dir::after{content:"";position:absolute;top:-4px;border-top:5px solid transparent;border-bottom:5px solid transparent}
.pl .dir.l::after{left:-2px;border-right:8px solid var(--dim)}.pl .dir.r::after{right:-2px;border-left:8px solid var(--dim)}
.g-tr{right:-3rem;top:-8rem;width:22rem}.g-r{right:-2rem;top:-6rem;width:28rem}.g-c{inset:0;margin:auto;width:16rem;position:absolute}
.lrow.bad{border-color:rgba(255,92,110,.6);background:rgba(60,14,20,.45)}.lrow.bad b{color:var(--red)}
.lrow .hn,.lrow .nb,.lrow .badge{display:grid!important;place-items:center;color:#03120f!important;font-weight:700;line-height:1}
.lrow .hn{font-size:.95rem!important}.lrow .nb{font-size:1.15rem!important}
.lrow.plain2{border:0;background:none;clip-path:none;padding:.3rem 0;font-size:.86rem;color:#d3f0ea}
.pn.big h3{font-size:1.5rem}
.fan1,.fan2{transform-origin:left}.fan1{transform:rotate(-9deg)}.fan2{transform:rotate(9deg)}
"""

CSS3 += """
/* ---- интерактивная структура заголовка (наведение открывает описание) ---- */
.dhdrcard{padding:1.1rem 1.3rem;clip-path:none!important;overflow:visible}
.ruler{display:flex;justify-content:space-between;color:var(--dim);font-size:.78rem;margin-bottom:.35rem}
.dhdr{display:flex;flex-direction:column;gap:.35rem}
.dhrow{display:grid;grid-template-columns:repeat(var(--n,1),minmax(0,1fr));gap:.3rem}
.dfld{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:.1rem;
  min-height:3.4rem;padding:.35rem;border:1.5px solid var(--c,var(--cyan));background:rgba(46,230,200,.07);cursor:help;outline:none;transition:background .15s,box-shadow .15s}
.dfld.f-cy{--c:var(--cyan)}.dfld.f-bl{--c:var(--blue)}.dfld.f-am{--c:var(--amber)}.dfld.f-vi{--c:var(--violet)}
.dfld.f-rd{--c:var(--red)}.dfld.f-gr{--c:var(--green)}.dfld.f-dm{--c:rgba(143,184,176,.55)}
.dfld b{font-family:var(--hf);font-size:1.02rem;line-height:1.1;color:#fff;text-transform:uppercase}
.dfld .mono{font-size:.72rem!important;color:var(--dim)}
.dfld:hover,.dfld:focus-visible{background:rgba(46,230,200,.2);box-shadow:0 0 16px rgba(46,230,200,.35);z-index:6}
.tip{position:absolute;left:50%;bottom:calc(100% + 10px);transform:translate(-50%,6px);width:min(26rem,78vw);background:#06201d;border:1px solid var(--edge);
  color:#eafffb;font-family:var(--f);font-size:.9rem;line-height:1.45;text-transform:none;text-align:left;padding:.7rem .85rem;clip-path:var(--cut6);
  opacity:0;pointer-events:none;transition:opacity .15s,transform .15s;z-index:7;box-shadow:0 10px 30px rgba(0,0,0,.6)}
.dhrow:first-child .tip{bottom:auto;top:calc(100% + 10px);transform:translate(-50%,-6px)}
.dfld:hover .tip,.dfld:focus-visible .tip{opacity:1;transform:translate(-50%,0)}
@media (max-width:1100px){.dfld b{font-size:.82rem}.dfld{min-height:2.9rem}}
"""

CSS3 += """
/* ---- захваты Wireshark: перенос строк, чтобы текст не обрезался ---- */
.ws.wsw{white-space:pre-wrap;overflow-wrap:anywhere;font-size:.82rem;line-height:1.7;padding:.7rem .9rem}
.ws.wsw .rd,.ws.wsw .hl{-webkit-box-decoration-break:clone;box-decoration-break:clone;padding:0 .12em}
"""

CSS3 += """
/* ---- «веер» широковещательных запросов: ровные горизонтальные стрелки ---- */
.fanw{display:flex;flex-direction:column;gap:.55rem;justify-content:center}
.fanlab{text-align:center;font-family:var(--hf);line-height:1.25;margin-bottom:.45rem}
.fanlab small{display:block;font-size:.78rem;opacity:.85}
.fanl{display:flex;align-items:center;height:2.2rem}
.fanl .mline{flex:1;margin:0}
.fansrv{display:flex;flex-direction:column;gap:.55rem;align-items:center;justify-content:center}
.fang{column-gap:.9rem}
.card.red .alert{margin-top:.7rem}
"""
