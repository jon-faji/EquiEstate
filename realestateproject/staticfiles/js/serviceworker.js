const CACHE_NAME = 'realestate-cache-v1';
const ASSETS_TO_CACHE = [
    '/dashboard/',
    '/accounts/login/',
    '/static/js/main.js',
    '/static/css/main.css',
    '/static/images/logo.png',
];

self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
});

self.addEventListener('fetch', function(e) {
    e.respondWith(
        caches.match(e.request).then(function(response) {
            return response || fetch(e.request);
        })
    );
});