// Service Worker for Chess Master PWA
const CACHE_NAME = 'chess-master-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/chess_web.py',
  '/manifest.json',
  '/wP.png',
  '/wR.png',
  '/wN.png',
  '/wB.png',
  '/wQ.png',
  '/wK.png',
  '/bP.png',
  '/bR.png',
  '/bN.png',
  '/bB.png',
  '/bQ.png',
  '/bK.png'
];

// Install Service Worker
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch from cache
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Cache hit - return response
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});

// Update service worker
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});