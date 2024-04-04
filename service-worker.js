const CACHE_NAME = 'sense-campus-patras-v1';
const urlsToCache = [
  '/index.html',
  '/styles.css', 
  '/script.js',  
  '/manifest.json',
  '/media/icons/icon_64.png',
  '/media/icons/icon_192.png',
  '/media/icons/icon_256.png',
  '/media/icons/icon_512.png',
  '/data.js',
  'media/clock.svg',
  'media/chair.svg',
  'media/seat.svg',
  'media/users.svg',
  'media/back.webp'
];

// Install event - cache the application shell
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  var cacheWhitelist = ['sense-campus-patras-v1'];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Fetch event - Serve cached content when offline
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return the response from the cached version
        if (response) {
          return response;
        }

        // Not in cache - return the result from the live server
        // This will require access to the network, so if you really
        // don't want to use fetch at all, you could omit these lines
        // and not serve anything when the request isn't in the cache.
        return fetch(event.request);
      })
  );
});