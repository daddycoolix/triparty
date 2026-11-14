/* Triparty service worker v1.13.0
   רשת קודם: כשיש אינטרנט תמיד נטענת הגרסה החדשה מהאתר.
   בלי אינטרנט נפתח העותק השמור מהביקור האחרון. */
const CACHE="triparty-v1";
const CORE=["./","./index.html","./app.html","./manifest.webmanifest","./icon-192.png","./icon-512.png","./apple-touch-icon.png","./favicon-32.png","./cities.json"];
self.addEventListener("install",e=>{
  e.waitUntil(caches.open(CACHE).then(c=>Promise.all(CORE.map(u=>c.add(new Request(u,{cache:"reload"})).catch(()=>{})))));
  self.skipWaiting();
});
self.addEventListener("activate",e=>{
  e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));
});
self.addEventListener("fetch",e=>{
  const r=e.request;
  if(r.method!=="GET")return;
  const u=new URL(r.url);
  if(u.origin!==self.location.origin)return;          /* תמונות, שערים ומפות: כרגיל, בלי שמירה */
  e.respondWith(
    fetch(r).then(res=>{
      if(res&&res.ok){const copy=res.clone(); caches.open(CACHE).then(c=>c.put(r,copy)).catch(()=>{});}
      return res;
    }).catch(()=>caches.match(r,{ignoreSearch:true}).then(m=>m||
      (r.mode==="navigate"?caches.match("./index.html"):undefined)).then(m=>m||Response.error()))
  );
});
