/* Offline-first: alle bestanden van de app lokaal bewaren. */
const CACHE = "oliebollen-v2.0.0";
const BESTANDEN = ["./", "index.html", "app.css", "app.js", "qrcode.js", "manifest.webmanifest", "icon.svg", "icon-192.png", "icon-512.png"];
self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(BESTANDEN)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET" || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(
    caches.match(e.request, { ignoreSearch: true }).then((hit) => hit || fetch(e.request).then((res) => {
      const kopie = res.clone();
      if (res.ok) caches.open(CACHE).then((c) => c.put(e.request, kopie));
      return res;
    }).catch(() => caches.match("index.html")))
  );
});
