// Simulated DOM checks of application logic, not browser rendering or native dialog behavior.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync(require('node:path').join(__dirname, '../js/main.js'), 'utf8');
const initSource = fs.readFileSync(require('node:path').join(__dirname, '../js/theme-init.js'), 'utf8');
let checks = 0;
const equal = (a,b) => { assert.deepEqual(a,b); checks++; };
class Element {
  constructor(attrs={}) { this.attrs={...attrs}; this.listeners={}; this.children={}; this.dataset={}; this.classes=new Set(); this.textContent=''; this.focused=false; this.hidden=false; this.top=0;
    this.classList={add:n=>this.classes.add(n),remove:n=>this.classes.delete(n),contains:n=>this.classes.has(n),toggle:(n,v)=>v?this.classes.add(n):this.classes.delete(n)};
  }
  get href() { return new URL(this.attrs.href, 'http://127.0.0.1:8080/index.html').href; }
  get id() { return this.attrs.id; }
  getAttribute(k) { return this.attrs[k] ?? null; }
  setAttribute(k,v) { this.attrs[k]=String(v); }
  removeAttribute(k) { delete this.attrs[k]; }
  addEventListener(n,fn) { (this.listeners[n] ??= []).push(fn); }
  async emit(n,e={}) { for (const fn of this.listeners[n] ?? []) await fn(e); }
  querySelector(s) { return this.children[s] ?? null; }
  querySelectorAll(s) { return this.children[s] ?? []; }
  contains(el) { return el===this || Object.values(this.children).flat().includes(el); }
  closest(s) { return s==='a'?this:this.figure; }
  focus() { this.focused=true; }
  getBoundingClientRect() { return {top:this.top,left:20,right:1000,bottom:600}; }
}
function setup(lang, nativeDialog=true, options={}) {
  const doc=new Element(), win=new Element(), root=new Element();root.lang=lang;
  const themeButton=new Element({'aria-pressed':'false'}), themeMeta=new Element();
  const menu=new Element({'aria-expanded':'false'}), nav=new Element(), chart=new Element({href:'assets/images/projects/bess_dispatch_soc_schedule.png'});
  const dialog=new Element(), img=new Element(), caption=new Element(), close=new Element(), status=new Element();
  const copy=new Element();copy.dataset.email='abufanasa@gmail.com';
  const language=new Element({href:'en/index.html'});
  const sections=['top','projects','experience','skills','contact'].map((id,i)=>{const el=new Element({id});el.top=(i-1)*800+100;return el;});
  const projectLink=new Element({href:'index.html#projects'}), contactLink=new Element({href:'index.html#contact'});
  nav.children.a=[projectLink,contactLink];
  chart.children.img={src:'bess-800.webp',alt:'BESS chart'};
  chart.figure=new Element();chart.figure.children.figcaption={textContent:'12 December 2024: highest margin, not average.'};
  dialog.children={'img':img,'#chart-dialog-caption':caption,'.dialog-close':close};
  if(nativeDialog)dialog.showModal=()=>{dialog.open=true;};
  dialog.close=()=>{dialog.open=false;void dialog.emit('close');};
  const map={'.theme-toggle':themeButton,'meta[name="theme-color"]':themeMeta,'.menu-toggle':menu,'#navigation':nav,'#chart-dialog':dialog,'.copy-email':copy,'.copy-status':status,'.language':language};
  doc.querySelector=s=>map[s] ?? null;
  doc.querySelectorAll=s=>s==='[data-chart]'?[chart]:s==='main > section[id]'?sections:[];
  doc.getElementById=id=>sections.find(s=>s.id===id);doc.documentElement=root;
  const mq=new Element(), colorMQ=new Element();colorMQ.matches=Boolean(options.systemDark);
  win.matchMedia=query=>query.includes('prefers-color-scheme')?colorMQ:mq;
  const stored={value:options.saved};
  win.localStorage={getItem:()=>{if(options.blockRead)throw new Error('Storage denied');return stored.value;},setItem:(key,value)=>{if(options.blockWrite)throw new Error('Storage denied');stored.key=key;stored.value=value;}};
  let observer;
  class Observer {constructor(fn){this.callback=fn;observer=this;}observe(){} }
  win.IntersectionObserver=Observer;
  const navigator={clipboard:{writeText:async email=>{navigator.copied=email;}}};
  const location={href:'http://127.0.0.1:8080/index.html',pathname:'/index.html',hash:'#projects'};
  const environment={document:doc,window:win,navigator,location,URL,IntersectionObserver:Observer};
  vm.runInNewContext(initSource,environment);const earlyTheme=root.getAttribute('data-theme');
  vm.runInNewContext(source,environment);
  return {doc,win,root,menu,nav,chart,dialog,img,caption,close,status,copy,language,sections,projectLink,contactLink,mq,navigator,location,observer,themeButton,themeMeta,colorMQ,stored,earlyTheme};
}
(async () => {
  for (const lang of ['de','en']) {
    const s=setup(lang);
    equal(s.earlyTheme,'light');equal(s.root.getAttribute('data-theme'),'light');equal(s.themeButton.hidden,false);equal(s.themeButton.getAttribute('aria-pressed'),'false');
    s.colorMQ.matches=true;await s.colorMQ.emit('change',{matches:true});equal(s.root.getAttribute('data-theme'),'dark');
    await s.themeButton.emit('click');equal(s.root.getAttribute('data-theme'),'light');equal(s.stored.value,'light');equal(s.stored.key,'aa-portfolio-theme');
    await s.colorMQ.emit('change',{matches:true});equal(s.root.getAttribute('data-theme'),'light');
    await s.themeButton.emit('click');equal(s.root.getAttribute('data-theme'),'dark');equal(s.themeMeta.getAttribute('content'),'#101923');equal(s.themeButton.getAttribute('aria-pressed'),'true');
    equal(s.themeButton.getAttribute('title'),lang==='en'?'Switch to light theme':'Helles Design aktivieren');
    await s.win.emit('storage',{key:'aa-portfolio-theme',newValue:'light'});equal(s.root.getAttribute('data-theme'),'light');
    await s.win.emit('storage',{key:'aa-portfolio-theme',newValue:null});equal(s.root.getAttribute('data-theme'),'dark');
    const restored=setup(lang,true,{saved:'light',systemDark:true});equal(restored.earlyTheme,'light');equal(restored.root.getAttribute('data-theme'),'light');
    const invalid=setup(lang,true,{saved:'unsupported',systemDark:true});equal(invalid.earlyTheme,'dark');equal(invalid.root.getAttribute('data-theme'),'dark');
    const blocked=setup(lang,true,{systemDark:true,blockRead:true,blockWrite:true});equal(blocked.earlyTheme,'dark');await blocked.themeButton.emit('click');equal(blocked.root.getAttribute('data-theme'),'light');
    const reload=setup(lang,true,{saved:s.stored.value});equal(reload.earlyTheme,'dark');
    const auto=setup(lang,true,{systemDark:true});equal(auto.earlyTheme,'dark');auto.colorMQ.matches=false;await auto.colorMQ.emit('change',{matches:false});equal(auto.root.getAttribute('data-theme'),'light');
    await auto.win.emit('storage',{key:'aa-portfolio-theme',newValue:'dark'});equal(auto.root.getAttribute('data-theme'),'dark');await auto.win.emit('storage',{key:null,newValue:null});equal(auto.root.getAttribute('data-theme'),'light');
    equal(s.root.classes.has('nav-ready'),true);equal(s.menu.hidden,false);
    await s.menu.emit('click');equal(s.nav.classes.has('open'),true);equal(s.menu.attrs['aria-expanded'],'true');
    await s.nav.emit('click',{target:s.projectLink});equal(s.nav.classes.has('open'),false);equal(s.sections[1].focused,true);
    await s.menu.emit('click');await s.doc.emit('keydown',{key:'Escape'});equal(s.menu.focused,true);equal(s.nav.classes.has('open'),false);
    await s.menu.emit('click');await s.doc.emit('click',{target:new Element()});equal(s.nav.classes.has('open'),false);
    await s.menu.emit('click');await s.mq.emit('change',{matches:true});equal(s.nav.classes.has('open'),false);
    let prevented=false;
    await s.chart.emit('click',{preventDefault(){prevented=true;}});equal(prevented,true);equal(s.dialog.open,true);
    equal(s.img.src,s.chart.href);equal(s.img.alt,'BESS chart');equal(s.caption.textContent,s.chart.figure.children.figcaption.textContent);
    await s.close.emit('click');equal(s.dialog.open,false);equal(s.chart.focused,true);
    prevented=false;await s.chart.emit('click',{ctrlKey:true,preventDefault(){prevented=true;}});equal(prevented,false);
    await s.chart.emit('click',{preventDefault(){}});await s.dialog.emit('click',{target:s.dialog,clientX:1,clientY:1});equal(s.dialog.open,false);
    await s.copy.emit('click',{currentTarget:s.copy});equal(s.navigator.copied,'abufanasa@gmail.com');equal(s.status.textContent,lang==='en'?'Email address copied.':'E-Mail-Adresse kopiert.');
    s.navigator.clipboard.writeText=async()=>{throw new Error('Denied');};
    await s.copy.emit('click',{currentTarget:s.copy});equal(s.status.textContent.includes('abufanasa@gmail.com'),true);
    equal(s.language.attrs.href,'en/index.html#projects');
    s.location.hash='#contact';await s.win.emit('hashchange');equal(s.language.attrs.href,'en/index.html#contact');
    await s.language.emit('click');equal(s.language.attrs.href,'en/index.html#projects');
    s.sections[1].top=-800;s.sections[2].top=100;s.observer.callback();equal(s.contactLink.attrs['aria-current'],undefined);equal(s.projectLink.attrs['aria-current'],undefined);
    s.sections[4].top=100;s.observer.callback();equal(s.contactLink.attrs['aria-current'],'location');
    s.win.innerHeight=900;s.win.scrollY=3100;s.root.scrollHeight=4000;
    s.sections[4].top=400;await s.language.emit('click');equal(s.language.attrs.href,'en/index.html#contact');
    await s.win.emit('scroll');equal(s.contactLink.attrs['aria-current'],'location');
    const fallback=setup(lang,false);prevented=false;
    await fallback.chart.emit('click',{preventDefault(){prevented=true;}});equal(prevented,false);
    fallback.navigator.clipboard=undefined;
    await fallback.copy.emit('click',{currentTarget:fallback.copy});equal(fallback.status.textContent.includes('abufanasa@gmail.com'),true);
  }
  console.log(JSON.stringify({simulated_dom_assertions:checks,result:'PASS',native_browser_rendering_focus_trapping_escape_and_clipboard_permissions:'NOT TESTED'},null,2));
})().catch(error=>{console.error(error);process.exitCode=1;});
