/* Lyceum service worker. VERSION is stamped by scripts/build.py from the content hash, so every deploy refreshes the cache. */
const VERSION="__VERSION__";
const CACHE="lyceum-"+VERSION;
const ASSETS=["./","./index.html","./manifest.webmanifest","./icons/icon-192.png","./icons/icon-512.png","./icons/icon-512-maskable.png","./icons/apple-touch-icon.png"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()));});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener("fetch",e=>{
  const r=e.request; if(r.method!=="GET")return;
  const url=new URL(r.url); if(url.origin!==self.location.origin)return;
  const isPage=r.mode==="navigate"||url.pathname.endsWith("/")||url.pathname.endsWith("/index.html");
  if(isPage){
    /* network first, so updates arrive when online; cached page when offline */
    e.respondWith(fetch(r).then(res=>{const copy=res.clone();caches.open(CACHE).then(c=>c.put("./index.html",copy));return res;}).catch(()=>caches.match("./index.html")));
    return;
  }
  e.respondWith(caches.match(r).then(hit=>hit||fetch(r).then(res=>{const copy=res.clone();caches.open(CACHE).then(c=>c.put(r,copy));return res;})));
});
