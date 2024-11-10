const CACHE_NAME = 'sense-campus-patras-v2';
const urlsToCache = [
  'manifest.json',
  'media/icons/icon_64.png',
  'media/icons/icon_192.png',
  'media/icons/icon_256.png',
  'media/icons/icon_512.png',
  'media/clock.svg',
  'media/seat.svg',
  'media/users.svg',
  'media/back.webp',
  'favicon.ico'
];

// Install event - cache the application shell
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        //console.log('Opened cache');
        return cache.addAll(urlsToCache).catch(error => {
          console.error('Caching failed for one or more resources:', error);
          throw error; // Re-throw the error to make sure the Service Worker installation fails.
        });
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
            //console.log('Deleting old cache:', cacheName);
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

        return fetch(event.request);
      })
  );
});