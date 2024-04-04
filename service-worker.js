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
  'media/seat.svg',
  'media/users.svg',
  'media/back.webp'
];

const getRootUrl = () => {
  const url = new URL(window.location);
  url.pathname = url.pathname.replace(/\/[^/]*$/, '/');
  return url.toString();
};

const rootURL = getRootUrl();

// Install event - cache the application shell individually
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        const cachePromises = urlsToCache.map(urlToCache => {
          return cache.add((rootURL+urlToCache).replaceAll("//","/")).catch(error => {
            console.error(`Caching failed for ${(rootURL+urlToCache).replaceAll("//","/")}:`, error);
            // Optionally, accumulate the errors in an array or object if you need to report or log them.
          });
        });
        return Promise.all(cachePromises).then(() => {
          console.log('All assets are cached');
        }).catch(error => {
          console.error('One or more assets failed to cache during the installation:', error);
          // It might be a good idea to fail the installation if critical resources are not cached successfully.
          throw error;
        });
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  var cacheWhitelist = [CACHE_NAME];
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
        return fetch(event.request);
      })
  );
});
