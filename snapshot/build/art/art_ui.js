/* ================= יצירות: חלון בחירה, "בסיסי (כלול)" ו"כל היצירות" (v1.18.0) ================= */
(function(){
  /* v1.19.0: ההגדרות מגיעות מקובץ ההגדרות (triparty-art-settings.json): מוטמע, מהאתר, או מה שהוחל בפאנל המנהל במכשיר */
  const SKEY="triparty_art_settings";
  function embeddedSettings(){try{const e=document.getElementById("tpArtSettings");return e?JSON.parse(e.textContent):null;}catch(e){return null;}}
  function validSettings(o){return !!(o&&typeof o==="object"&&Array.isArray(o.packs)&&Array.isArray(o.types)&&Array.isArray(o.pop)&&Array.isArray(o.area)&&o.cities&&typeof o.cities==="object");}
  let SITE=null;   /* הקובץ שנטען מהאתר */
  function localSettings(){try{const o=JSON.parse(localStorage.getItem(SKEY)||"null");return validSettings(o)?o:null;}catch(e){return null;}}
  function settings(){return localSettings()||SITE||embeddedSettings()||{packs:[],types:[],pop:[["הכל",0]],area:["מרכז העיר","כל העיר"],defaults:{},cities:{}};}
  function settingsSource(){return localSettings()?"local":(SITE?"site":"embedded");}
  let PK=[],TY=[],POP=[],AREA=[],PKALL=[],CFG={},EXP="",FILE="";
  /* איחוד ברירות המחדל עם ההגדרות של העיר הנוכחית */
  function configure(){
    const S=settings(), c=(S.cities||{})[CITYEN||""]||(S.cities||{})[CITY||""]||{};
    const packs=(c.packs||S.packs||[]).map(x=>[String(x[0]),String(x[1])]);
    PK=(c.local&&c.local[0]?[[String(c.local[0]),String(c.local[1]||c.local[0])]]:[]).concat(packs.filter(x=>!(c.local&&x[0]===c.local[0])));
    if(!PK.some(x=>x[0]==="fac"))PK.push(["fac","פסלים על חזיתות"]);
    TY=(c.types||S.types||[]).map(String); POP=(c.pop||S.pop||[["הכל",0]]).map(x=>[String(x[0]),+x[1]||0]);
    AREA=(c.area||S.area||["מרכז העיר","כל העיר"]).map(String);
    PKALL=PK.map(p=>p[0]).filter(k=>k!=="fac");
    CFG=Object.assign({on:1,all:1},S.defaults||{},c.defaults||{},{on:c.on===undefined?1:+c.on,all:c.all===undefined?1:+c.all,source:c.source||""});
    EXP=c.exp||S.exp||"פסלים, אנדרטאות, מזרקות ותבליטים - חופשי";
    FILE=(c.file||S.file||"triparty-{city}-art.json");
  }
  const def=()=>{const d={packs:PKALL.slice(),types:TY.slice(),pop:Math.min(+CFG.pop||0,Math.max(POP.length-1,0)),area:AREA.length>1?Math.min(+CFG.area||0,AREA.length-1):0};if(+CFG.fac)d.packs.push("fac");return d;};
  const A={pool:null,loading:false,err:"",tab:0,s:[],applied:0,extraN:0,base:0};
  configure(); A.s=[def(),def()];
  window.ARTSTATE=A;
  window.artSettings=settings; window.artSettingsSource=settingsSource; window.artEmbeddedSettings=embeddedSettings;
  /* תצוגה קריאה: שורה לכל מפתח, ושורה לכל עיר */
  function fmtSettings(o){
    const line=(k,v)=>' '+JSON.stringify(k)+': '+JSON.stringify(v);
    const out=[]; for(const k of Object.keys(o)){
      if(k==="cities"&&o.cities&&typeof o.cities==="object"){out.push(' "cities": {\n'+Object.keys(o.cities).map(c=>'  '+JSON.stringify(c)+': '+JSON.stringify(o.cities[c])).join(',\n')+'\n }');}
      else out.push(line(k,o[k]));}
    return '{\n'+out.join(',\n')+'\n}';
  }
  window.artSettingsText=()=>fmtSettings(settings()); window.artFmtSettings=fmtSettings;
  /* החלה במכשיר (פאנל מנהל): null מבטל את ההגדרה המקומית וחוזר לקובץ שבאתר/המוטמע */
  window.artApplySettings=function(o){
    if(o===null){try{localStorage.removeItem(SKEY);}catch(e){}}
    else{if(!validSettings(o))throw new Error("bad");try{localStorage.setItem(SKEY,JSON.stringify(o));}catch(e){}}
    reconfigure();
  };
  function reconfigure(){
    configure(); load(); A.pool=null; A.err=""; removeExtras();
    if(A.applied&&A.tab===1&&hasArt()){fetchPool().then(()=>{addExtras();try{restoreSel();}catch(e){}render();});}
    else{try{restoreSel();}catch(e){}render();}
    if(dlg&&dlg.classList.contains("on"))paint();
  }
  /* טעינת הקובץ מהאתר (פעם אחת), עם עותק במטמון לעבודה בלי רשת */
  async function fetchSettings(){
    const url=builtinBase()+"triparty-art-settings.json"; let j=null;
    try{const r=await fetch(url,{cache:"no-cache"}); if(!r.ok)throw new Error("HTTP "+r.status);
      const copy=r.clone(); j=await r.json(); try{const c=await caches.open("triparty-art");await c.put(url,copy);}catch(e){}
    }catch(e){try{const c=await caches.open("triparty-art");const m=await c.match(url);if(m)j=await m.json();}catch(e2){}}
    if(validSettings(j)){const emb=embeddedSettings(); if(!emb||JSON.stringify(j)!==JSON.stringify(emb)){SITE=j;return true;}}
    return false;
  }
  const key=()=>"triparty_art_"+(CITYEN||CITY);
  function load(){
    A.tab=+CFG.tab===1&&CFG.all?1:0;A.s=[def(),def()];A.applied=0;
    try{const o=JSON.parse(localStorage.getItem(key())||"null");
      if(o&&Array.isArray(o.s)&&o.s.length===2){A.s=o.s.map(x=>{const d=Object.assign(def(),x);
        d.packs=(d.packs||[]).filter(k=>k==="fac"||PKALL.includes(k)); if(!d.packs.some(k=>k!=="fac"))d.packs=PKALL.concat(d.packs);
        d.types=(d.types||[]).filter(t=>TY.includes(t)); if(!d.types.length)d.types=TY.slice();
        d.pop=Math.min(Math.max(+d.pop||0,0),POP.length-1); d.area=Math.min(Math.max(+d.area||0,0),AREA.length-1); return d;});
        A.tab=o.tab&&CFG.all?1:0;A.applied=o.applied?1:0;}}catch(e){}
  }
  function save(){try{localStorage.setItem(key(),JSON.stringify({tab:A.tab,s:A.s,applied:A.applied}));}catch(e){}}
  const fileURL=()=>builtinBase()+FILE.replace("{city}",String(CITYEN||"").replace(/\s+/g,""));
  const hasArt=()=>!!CFG.on&&items.some(it=>it.aw);
  window.artEnabled=()=>!!CFG.on;

  /* התאמה של יצירה לבחירה */
  function match(aw,score,s,skip){
    const p=aw.p||[];
    if(skip!=="packs"&&p.includes("fac")&&!s.packs.includes("fac"))return false;
    if(skip!=="packs"){const allP=PKALL.every(k=>s.packs.includes(k));
      if(!allP&&!p.some(k=>s.packs.includes(k)))return false;}
    if(skip!=="types"&&s.types.length<TY.length&&!s.types.includes(aw.t))return false;
    if(skip!=="pop"&&POP[s.pop][1]&&!(score>=POP[s.pop][1]))return false;
    if(skip!=="area"&&s.area===0&&!aw.z)return false;
    return true;
  }
  /* מאגר היצירות של הלשונית: בסיסי = מה שבקובץ העיר, כל היצירות = בסיסי + הקובץ הנפרד */
  function poolFor(tab){
    const base=items.filter(it=>it.aw&&!it.aw.x).map(it=>({aw:it.aw,s:it.score}));
    if(!tab)return base;
    return A.pool?base.concat(A.pool.map(o=>({aw:o.aw,s:o.s}))):base;
  }
  async function fetchPool(){
    if(A.pool||A.loading)return;
    A.loading=true;A.err="";paint();
    const url=fileURL();let j=null;
    try{
      const r=await fetch(url,{cache:"no-cache"}); if(!r.ok)throw new Error("HTTP "+r.status);
      const copy=r.clone(); j=await r.json();
      try{const c=await caches.open("triparty-art");await c.put(url,copy);}catch(e){}
    }catch(e){
      try{const c=await caches.open("triparty-art");const m=await c.match(url);if(m)j=await m.json();}catch(e2){}
    }
    A.loading=false;
    if(j&&Array.isArray(j.items)){const have=new Set(items.filter(it=>it.aw).map(it=>it.aw.k));A.pool=j.items.filter(o=>o.aw&&!have.has(o.aw.k));}
    else A.err="בטעינה הראשונה נדרש חיבור לרשת";
    paint();
  }
  /* הוספה של היצירות שנבחרו ל"כל היצירות" לסוף הרשימה, כך שיופיעו בכל מקום ביישום */
  function removeExtras(){
    const n=items.findIndex(it=>it.aw&&it.aw.x); if(n<0)return;
    items.splice(n); [...SEL].forEach(i=>{if(i>=n)SEL.delete(i);}); [...HID].forEach(i=>{if(i>=n)HID.delete(i);});
    A.extraN=0;
  }
  function addExtras(){
    removeExtras();
    if(!A.applied||A.tab!==1||!A.pool)return;
    const s=A.s[1], list=A.pool.filter(o=>match(o.aw,o.s,s));
    const built=buildItems(list.map(o=>[o.c,o.h,o.e,o.la,o.ln,"",o.d,o.ho,o.co,o.ti||""]));
    built.forEach((it,i)=>{const o=list[i];
      it.score=o.s;it.iq=o.iq;it.thumb=o.th||null;it.pv=null;it.pvs=null;it.srcTxt=o.st||"";it.trDone=1;
      it.age=o.ag||null;it.kid=o.kd||null;it.dist=o.dt||null;it.x=o.x||null;it.ko=0;it.ak=null;
      it.aw=Object.assign({},o.aw,{x:1}); it.txt+=" יצירה "+(o.aw.t||"");});
    items.push(...built); A.extraN=built.length;
    if(typeof rankItems==="function")rankItems();
  }
  function artInView(it){
    if(!it.aw)return false;
    const tab=A.applied?A.tab:0;
    if(tab===0&&it.aw.x)return false;
    return match(it.aw,it.score,A.s[tab]);
  }
  window.artInView=artInView;

  /* ---------- חלון הבחירה ---------- */
  let dlg=null;
  function build(){
    dlg=document.createElement("div"); dlg.id="artdlg"; dlg.setAttribute("role","dialog"); dlg.setAttribute("aria-label","אילו יצירות להציג");
    dlg.innerHTML='<div class="artbox"><div class="arthd"><b>אילו יצירות להציג?</b><button type="button" class="artx" aria-label="סגור">✕</button></div>'+
      '<div class="arttabs"></div><p class="artexp">פסלים, אנדרטאות, מזרקות ותבליטים - חופשי</p><p class="artnet"></p>'+
      '<div class="artbody"><div class="artsec">א. חבילות נושא</div><div class="artpills" data-g="packs"></div>'+
      '<div class="artsec">ב. סוג היצירה</div><div class="artpills" data-g="types"></div>'+
      '<div class="artsec">ג. פופולריות</div><div class="artpills" data-g="pop"></div>'+
      '<div class="artsec">ד. אזור</div><div class="artpills" data-g="area"></div></div>'+
      '<div class="artft"><div class="arttot">יוצגו<b>0</b><span></span></div><button type="button" class="artgo">החל</button></div></div>';
    document.body.appendChild(dlg);
    dlg.addEventListener("click",e=>{
      if(e.target===dlg||e.target.closest(".artx")){close();return;}
      const t=e.target.closest(".arttab"); if(t){if(+t.dataset.i===1&&!CFG.all)return; A.tab=+t.dataset.i; if(A.tab===1)fetchPool(); paint(); return;}
      if(e.target.closest(".artgo")){apply();return;}
      const b=e.target.closest(".artpill"); if(!b||b.classList.contains("zero")&&!b.classList.contains("on"))return;
      const g=b.parentNode.dataset.g, s=A.s[A.tab], v=b.dataset.v;
      if(g==="packs"){
        if(v==="*")s.packs=PKALL.concat(s.packs.includes("fac")?["fac"]:[]);
        else if(v==="fac"){s.packs=s.packs.includes("fac")?s.packs.filter(k=>k!=="fac"):s.packs.concat("fac");}
        else{const all=PKALL.every(k=>s.packs.includes(k));
          if(all)s.packs=[v].concat(s.packs.includes("fac")?["fac"]:[]);
          else if(s.packs.includes(v)){if(s.packs.filter(k=>k!=="fac").length>1)s.packs=s.packs.filter(k=>k!==v);}
          else s.packs=s.packs.concat(v);}
      }else if(g==="types"){
        if(v==="*")s.types=TY.slice();
        else if(s.types.length===TY.length)s.types=[v];
        else if(s.types.includes(v)){if(s.types.length>1)s.types=s.types.filter(k=>k!==v);}
        else s.types=s.types.concat(v);
      }else if(g==="pop")s.pop=+v; else if(g==="area")s.area=+v;
      paint();
    });
  }
  const nf=n=>Number(n).toLocaleString("he-IL");
  function paint(){
    if(!dlg)return;
    const s=A.s[A.tab], pool=poolFor(A.tab), all=A.tab===1&&!A.pool;
    const baseN=poolFor(0).length, allN=A.pool?baseN+A.pool.length:null;
    dlg.querySelector(".arttabs").innerHTML=
      '<button type="button" class="arttab'+(A.tab===0?" on":"")+'" data-i="0">בסיסי (כלול)<small>'+nf(baseN)+'</small></button>'+
      '<button type="button" class="arttab'+(A.tab===1?" on":"")+(CFG.all?"":" off")+'" data-i="1"'+(CFG.all?"":' disabled')+'>כל היצירות<small>'+(allN?nf(allN):(CFG.all?"":"בקרוב"))+'</small></button>';
    dlg.querySelector(".artexp").textContent=EXP;
    const net=dlg.querySelector(".artnet");
    net.style.display=A.tab===1?"block":"none";
    net.textContent=A.loading?"טוען את כל היצירות…":(A.err||"בטעינה הראשונה נדרש חיבור לרשת");
    net.classList.toggle("bad",!!A.err);
    const cnt=(skip,fn)=>pool.filter(o=>match(o.aw,o.s,s,skip)&&fn(o)).length;
    const pill=(v,label,on,n,gen)=>'<button type="button" class="artpill'+(gen?" gen":"")+(on?" on":"")+(n===0&&!gen?" zero":"")+'" data-v="'+v+'">'+esc(label)+(n!==null?" · "+nf(n):"")+'</button>';
    const allP=PKALL.every(k=>s.packs.includes(k)), allT=s.types.length===TY.length;
    dlg.querySelector('[data-g="packs"]').innerHTML=pill("*","הכל",allP,null,1)+
      PK.map(([k,n])=>pill(k,n,k==="fac"?s.packs.includes("fac"):(!allP&&s.packs.includes(k)),all?null:cnt("packs",o=>{const q=o.aw.p||[];return q.includes(k)&&(k==="fac"||!q.includes("fac")||s.packs.includes("fac"));}))).join("");
    dlg.querySelector('[data-g="types"]').innerHTML=pill("*","הכל",allT,null,1)+
      TY.map(t=>pill(t,t,!allT&&s.types.includes(t),all?null:cnt("types",o=>o.aw.t===t))).join("");
    dlg.querySelector('[data-g="pop"]').innerHTML=POP.map((p,i)=>pill(i,p[0]+(p[1]?" · דירוג "+p[1]+"+":""),s.pop===i,null)).join("");
    dlg.querySelector('[data-g="area"]').innerHTML=AREA.map((a,i)=>pill(i,a,s.area===i,null)).join("");
    const n=all?null:pool.filter(o=>match(o.aw,o.s,s)).length;
    const tot=dlg.querySelector(".arttot");
    tot.querySelector("b").textContent=n===null?"…":nf(n);
    tot.querySelector("span").textContent=A.tab?"יצירות מתוך כל המאגר":"יצירות מתוך הבסיסי";
    dlg.querySelector(".artgo").disabled=A.tab===1&&!A.pool;
  }
  function open(){ if(!dlg)build(); if(A.applied&&A.tab===1)fetchPool(); dlg.classList.add("on"); paint(); }
  function close(){ if(dlg)dlg.classList.remove("on"); }
  function apply(){
    A.applied=1; save(); addExtras();
    try{restoreSel();}catch(e){}
    close(); render();
  }
  window.openArtDlg=open;
  /* אחרי טעינת עיר: שחזור הבחירה, וטעינת "כל היצירות" אם נבחרה */
  let _sf=null;
  window.artAfterCity=async function(){
    if(!_sf)_sf=fetchSettings().then(ch=>{if(ch&&!localSettings()){reconfigure();}}).catch(()=>{});
    configure(); A.pool=null;A.err="";A.extraN=0;load();
    if(A.applied&&A.tab===1&&hasArt()){await fetchPool(); addExtras(); try{restoreSel();}catch(e){} render();}
  };
  document.addEventListener("click",e=>{if(e.target.closest(".artopen"))open();});
})();
