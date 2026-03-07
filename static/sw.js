// Service Worker Básico para permitir a instalação do PWA
self.addEventListener('install', (e) => {
    console.log('[Service Worker] Instalado');
    self.skipWaiting();
});

self.addEventListener('activate', (e) => {
    console.log('[Service Worker] Ativado');
    return self.clients.claim();
});

self.addEventListener('fetch', (e) => {
    // Apenas deixa as requisições passarem normalmente
    e.respondWith(fetch(e.request));
});
