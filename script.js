function convertArray(arr) {
    return arr.map(item => {
        return {
            x: new Date(item.x), // Convert the "x" field to a Date object
            y: Math.abs(item.y) // Keep "y" as it is
        };
    });
}

function fake_data(mode){
    if(mode=="size"){
        // Generate random data points for two arrays with timestamps
        const now = new Date();
        const fiveHoursBefore = new Date(now.getTime() - 1 * 60 * 60 * 1000);
        const fiveHoursAfter = new Date(now.getTime() + 1 * 60 * 60 * 1000);
        const dataArray1 = [];
        const dataArray2 = [];
    
        let value = 40;
        for (let time = new Date(fiveHoursBefore); time <= fiveHoursAfter; time.setMinutes(time.getMinutes() + 1)) {
            value=value+Math.round(Math.random()*15)-6;
            if (time<now){
            dataArray1.push({ x: new Date(time), y: value });
            }else{
            dataArray2.push({ x: new Date(time), y: value});
        }
        }
        return [dataArray1,dataArray2];
    }else{
        // Generate random data points for two arrays with timestamps
        const now = new Date();
        const fiveHoursBefore = new Date(now.getTime() - 1 * 60 * 60 * 1000);
        const fiveHoursAfter = new Date(now.getTime() + 1 * 60 * 60 * 1000);
        const dataArray1 = [];
        const dataArray2 = [];
    
        let value = 6;
        for (let time = new Date(fiveHoursBefore); time <= fiveHoursAfter; time.setMinutes(time.getMinutes() + 1)) {
            value=Math.abs(value+Math.round(Math.random()*2)-1)+1;
            if (time<now){
            dataArray1.push({ x: new Date(time), y: value });
            }else{
            dataArray2.push({ x: new Date(time), y: value});
        }
        value=value-1;
        }
       //console.log(dataArray1)
        return [dataArray1,dataArray2];
        
    }

}



function plotTimeSeriesData(chart_name,animation_duration,y_title,recorded,projected) {
    let parameter_max_height_percentage = 1.25;

    

    let dataArray1=recorded;
    let dataArray2=projected;
    //create between point
    let current_measurement=dataArray1[dataArray1.length-1]
    //console.log(current_measurement);
    dataArray2=[current_measurement,].concat(dataArray2);//place current measurement in the start of projection array to connect the two lines
    
    //create fake invisible datapoint to increase y-lim seamelessly
    let all_data=dataArray1.concat(dataArray2);
    // Extracting all 'y' values from the array
    const yValues = all_data.map(item => item.y);
    // Finding the maximum value among all 'y' values
    const max = Math.max(...yValues);
    //console.log(max);
    let y_lim = parameter_max_height_percentage*max;



    // Set up the chart
    const ctx = document.getElementById(chart_name).getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [
                {
                    label:"Invisible",
                    data: [{x:current_measurement.x,y:y_lim},],
                    pointRadius:0,
                

                },
                {
                    label: "Current",
                    data: [current_measurement,],
                    borderColor: 'rgb(236, 88, 20)', // Original color
                    backgroundColor: 'rgb(236, 88, 20)',
                    pointRadius:5,
                    hoverRadius:10
                },
                {
                    label: 'Recorded',
                    data: dataArray1,
                    borderColor: 'rgba(236, 88, 20, 0.9)', // Original color
                    fill: true,
                    backgroundColor: "rgba(236, 88, 20,0.3)",
                    pointRadius: 0,
                    
                },
                {
                    label: 'Projected',
                    data: dataArray2,
                    borderColor: 'rgba(128, 128,128, 0.2)',
                    fill: true,
                    backgroundColor: "rgba(128, 128, 128,0.05)",
                    pointRadius: 0,
                    
                }

                

            ]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }},
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            parser: 'HH:mm',
                            tooltipFormat: 'h:mm a',
                            unit: 'minute',
                            stepSize: 30, // Adjust based on your data
                            displayFormats: {
                                minute: 'h:mm a',
                                hour: 'h:mm a'
                            }
                        },
                        ticks: {
                            autoSkip: true,
                            maxTicksLimit: 20,
                            major: {
                                enabled: true
                            },
                            // Custom tick formatting
                            callback: function(value, index, values) {
                                // Convert the value (timestamp) to a Date object
                                const date = new Date(value);
                                // Format the time as "h:mm a" ensuring consistent spacing
                                const formattedTime = this.getLabelForValue(value).replace(/\sAM$/, 'AM').replace(/\sPM$/, 'PM');
                                // Return the formatted time for display
                                return formattedTime;
                            }
                        },
                        afterBuildTicks: (scale) => {
                            scale.ticks = scale.ticks.filter(tick => {
                                const date = new Date(tick.value);
                                const minutes = date.getMinutes();
                                return minutes === 0 || minutes === 30;
                            });
                        },
                        min: dataArray1[0].x,
                        max: dataArray2[dataArray2.length-1].x
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: y_title
                        }
                    }
                }
                ,
            animation: {
                duration: animation_duration, // general animation time
            },
            elements: {
                line: {
                    tension: 0.95 // This makes the lines smoother (0 for straight, 1 for max smoothness)
                }
            },
            
            
        }

        
    });
}




// Modified addProcessedMenuItemsToDOM to accept pre-processed items
function addProcessedMenuItemsToDOM(processedMenus) {
    Object.entries(processedMenus).forEach(([mealType, processedItems]) => {
        const menuContainer = document.getElementById(`${mealType}-menu`);
        processedItems.forEach(itemProcessed => {
            const blob = document.createElement('div');
            blob.className = 'menu-blob';
            blob.innerHTML = `<p>${itemProcessed}</p>`;
            menuContainer.appendChild(blob);
        });
    });
}


// Function to update the restaurant capacity
function updateRestaurantCapacity(percentage) {
    // Ensure the percentage is within bounds
    percentage = Math.max(0, Math.min(percentage, 100));

    // Update the capacity bar width
    const capacityBar = document.getElementById('capacity-bar');
    capacityBar.style.width = percentage + '%';

    // Update the capacity text
    const capacityText = document.getElementById('current_Capacity');
    capacityText.textContent = percentage + '%';
}

const getRootUrl = () => {
    const url = new URL(window.location);
    url.pathname = url.pathname.replace(/\/[^/]*$/, '/');
    return url.toString();
  };
  
let update_period_minutes = 10;

function schedulePageReload(lastUpdateStr) {
    const lastUpdate = new Date(lastUpdateStr);
    const now = new Date();
    const update_period = parseInt(update_period_minutes * 60 * 1000); // Update period in milliseconds
    const standardDelay = 60 * 1000; // 60 seconds in milliseconds

    let delay = (now - lastUpdate) < update_period ? update_period - (now - lastUpdate) : standardDelay;

    // Start the countdown timer
    updateTimer(delay);

    setTimeout(function() {
        window.location.reload(true);  // Force a reload from the server
    }, delay);
}

// Function to update the timer on the page
function updateTimer(duration) {
    let secondsLeft = duration / 1000; // Convert milliseconds to seconds
    const timerElement = document.getElementById('timer');
    const interval = setInterval(function () {
        const minutes = parseInt(secondsLeft / 60, 10);
        const seconds = parseInt(secondsLeft % 60, 10);

        timerElement.textContent = `${minutes < 10 ? '0' + minutes : minutes}:${seconds < 10 ? '0' + seconds : seconds}`;

        if (--secondsLeft < 0) {
            clearInterval(interval); // Stop the interval when time runs out
            timerElement.textContent = "00:00"; // Reset timer display
        }
    }, 1000);
}
async function publishToMQTTBroker() {
    // MQTT Configuration
    const host = "labserver.sense-campus.gr"; // Broker hostname
    const port = 9002; // WebSocket Secure Port
    const topic = "wlc_estia_rio/visitors/"; // Topic to publish to
    const reconnectTimeout = 2000;

    const clientId = "client" + Math.random().toString(16).substr(2, 8); // Random client ID
    const client = new Paho.MQTT.Client(host, port, clientId);

    client.onConnectionLost = function (responseObject) {
        if (responseObject.errorCode !== 0) {
            setTimeout(() => client.connect(options), reconnectTimeout); // Reconnect on failure
        }
    };

    const options = {
        cleanSession: true, // Clean session
        timeout: 3600, // Timeout after 30 seconds
        useSSL: true, // Use SSL/TLS connection for WSS
        onSuccess: onConnect,
        onFailure: function (message) {
            setTimeout(() => client.connect(options), reconnectTimeout);
        }
    };

    // Connect
    client.connect(options);

    function onConnect() {
        publishMessage();
    }

    // Fetch the user's IP address
    async function getUserIp() {
        try {
            const response = await fetch('https://api.ipify.org?format=json');
            const data = await response.json();
            return data.ip;
        } catch (error) {
            return null;
        }
    }

// Detect the user's browser
function detectBrowser() {
    const userAgent = navigator.userAgent;

    if (userAgent.includes("Firefox")) return "Firefox";
    if (userAgent.includes("Edg")) return "Microsoft Edge";
    if (userAgent.includes("OPR") || userAgent.includes("Opera")) return "Opera";
    if (userAgent.includes("Chrome") && !userAgent.includes("Edg") && !userAgent.includes("OPR")) return "Chrome";
    if (userAgent.includes("Safari") && !userAgent.includes("Chrome")) return "Safari";

    return "unknown"; // Default if the browser is unrecognized
}


    // Detect platform (Android, iOS, Windows, macOS, Linux)
    function detectPlatform() {
        const userAgent = navigator.userAgent || navigator.vendor || window.opera;

        if (/android/i.test(userAgent)) return "Android";
        if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) return "iOS";
        if (/Win/i.test(userAgent)) return "Windows";
        if (/Mac/i.test(userAgent) && !/iPhone|iPad|iPod/.test(userAgent)) return "macOS";
        if (/Linux/i.test(userAgent)) return "Linux";

        return "unknown";
    }

    // Detect device model (best effort based on user agent)
    function getDeviceModel() {
        const userAgent = navigator.userAgent;

        const modelMatch = userAgent.match(/\(([^)]+)\)/);
        return modelMatch ? modelMatch[1] : "unknown";
    }

    // Detect if running as a PWA
    function isRunningAsPWA() {
        return (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true);
    }

    // Detect if running in a native app webview
    function detectNativeApp() {
        const userAgent = navigator.userAgent;

        if (userAgent.includes("MyAppWebView")) { // Adjust this if your app has a custom identifier
            return true;
        }

        if (window.AndroidInterface) {
            return true;
        }

        if (userAgent.includes("iPhone") && !userAgent.includes("Safari")) {
            return true;
        }

        return false;
    }

    // Detect network type (WiFi or cellular)
    function getNetworkType() {
        const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
        if (connection) {
            // Prefer `connection.type` if available, as it might give "wifi" or "cellular" directly
            if (connection.type) {
                return connection.type;
            }
            // Fallback to `effectiveType` for an approximation of the network quality
            return connection.effectiveType;
        }
        return "unknown";
    }
    

    // Detect screen size
    function getScreenSize() {
        return {
            width: window.screen.width,
            height: window.screen.height
        };
    }

    // Fetch the user's GPS coordinates and speed with detailed error handling
    function getGpsLocation() {
        return new Promise((resolve) => {
            if ("geolocation" in navigator) {
                navigator.geolocation.getCurrentPosition(
                    position => resolve({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                        speed: position.coords.speed !== null ? position.coords.speed : "unavailable"
                    }),
                    error => {
                        let errorMessage = '';
                        switch (error.code) {
                            case error.PERMISSION_DENIED:
                                errorMessage = "User denied";
                                break;
                            case error.POSITION_UNAVAILABLE:
                                errorMessage = "Location unavailable";
                                break;
                            case error.TIMEOUT:
                                errorMessage = "Request timed out";
                                break;
                            case error.UNKNOWN_ERROR:
                                errorMessage = "An unknown error occurred";
                                break;
                        }
                        resolve({ error: errorMessage, speed: "unavailable" });
                    },
                    { timeout: 10000 }
                );
            } else {
                resolve({ error: "Geolocation not supported", speed: "unavailable" });
            }
        });
    }

    async function publishMessage() {
        const ip = await getUserIp();
        const gpsLocation = await getGpsLocation();
        const dateTime = new Date().toISOString();
    
        if (!ip) {
            console.error("Could not retrieve IP, aborting.");
            return;
        }
    
        let locationInfo;
        if (gpsLocation.error) {
            locationInfo = `not available: ${gpsLocation.error}`;
        } else {
            locationInfo = `Lat: ${gpsLocation.latitude}, Lon: ${gpsLocation.longitude}`;
        }
    
        // Detect environment details
        const platform = detectPlatform();
        const deviceModel = getDeviceModel();
        const isPWA = isRunningAsPWA();
        const isNativeApp = detectNativeApp();
        const networkType = getNetworkType();
        const screenSize = getScreenSize();
        const browser = detectBrowser(); // Add browser detection
    
        const messagePayload = JSON.stringify({
            datetime: dateTime,
            ip: ip,
            location: locationInfo,
            speed: gpsLocation.speed,
            environment: {
                platform: platform,
                deviceModel: deviceModel,
                isPWA: isPWA,
                isNativeApp: isNativeApp,
                networkType: networkType,
                screenSize: screenSize,
                browser: browser // Include browser in payload
            }
        });
    
        const message = new Paho.MQTT.Message(messagePayload);
        message.destinationName = topic + ip;
    
        client.send(message); 
    }
}




// Declare global variables
let menus_text, last_update_datetime, future_group1, future_group2, historic_group1, historic_group2;

// Use a version or timestamp for cache busting
const version = new Date().getTime(); 

window.addEventListener('load', function () {
  // Dynamic import within the 'load' event
  import(`./data.js?v=${version}`)
    .then((module) => {
      // Assign the imported values to global variables
      menus_text = module.menus_text;
      last_update_datetime = module.last_update_datetime;
      future_group1 = module.future_group1;
      future_group2 = module.future_group2;
      historic_group1 = module.historic_group1;
      historic_group2 = module.historic_group2;

      // Now that the module is loaded, execute the rest of your code
      executeRestOfScript();
    })
    .catch((error) => {
      console.error('Failed to load module:', error);
    });
});

// Function that contains the rest of the code (inside the 'load' event)
function executeRestOfScript() {

  //log visitor
  publishToMQTTBroker();

  // Set last updated tag
  document.getElementById('last-updated').textContent = `Last Updated: ${last_update_datetime}`;
  schedulePageReload(last_update_datetime);

  // Parse menu text
  let menus = menus_text;

  // Call the function to add the menu items
  addProcessedMenuItemsToDOM(menus);

  // Graphs
  let data_line, data_time;
  var startTime = performance.now();
  data_time = [convertArray(historic_group1), convertArray(future_group1)]; //fake_data("minutes")
  var endTime = performance.now();
  //console.log(`Call to convert array took ${endTime - startTime} milliseconds`);

  let recorded_waittimes = data_time[0];
  let projected_waittimes = data_time[1];

  data_line = [convertArray(historic_group2), convertArray(future_group2)]; //fake_data("size")
  let recorded_linesizes = data_line[0];
  let projected_linesizes = data_line[1];

  let capacity = Math.round(
    100 *
      (recorded_waittimes[recorded_waittimes.length - 1].y + recorded_linesizes[recorded_linesizes.length - 1].y) /
      ([...recorded_linesizes, ...projected_linesizes].reduce((max, item) => (item.y > max ? item.y : max), -Infinity) +
        [...recorded_waittimes, ...projected_waittimes].reduce((max, item) => (item.y > max ? item.y : max), -Infinity))
  );

  plotTimeSeriesData('waitTimeChart', 200, 'Waiting Area Occupancy', recorded_waittimes, projected_waittimes);
  plotTimeSeriesData('lineSizeChart', 500, 'Restaurant Occupancy', recorded_linesizes, projected_linesizes);
  updateRestaurantCapacity(capacity);

  document.getElementById('current_WaitTime').textContent = recorded_waittimes[recorded_waittimes.length - 1].y.toString();
  document.getElementById('current_LineSize').textContent = recorded_linesizes[recorded_linesizes.length - 1].y.toString();
  document.getElementById('current_Capacity').textContent = capacity.toString() + '%';

  // Scroll smoothly to the top of the page
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  });

  // Menu button listener
  document.querySelector('.bottom-nav .navbar a[href="#todays-menu"]').addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default anchor click behavior
    e.stopPropagation();

    // Remove 'active' class from all nav items
    document.querySelectorAll('.navbar a').forEach((item) => {
      item.classList.remove('active');
    });

    // Add 'active' class
    this.classList.add('active');

    // Get the position of the "Today's Menu" section
    const menuSection = document.getElementById('todays-menu');
    const offset = 35; // Change this value to the desired offset
    const bodyRect = document.body.getBoundingClientRect().top;
    const sectionRect = menuSection.getBoundingClientRect().top;
    const sectionPosition = sectionRect - bodyRect;

    // Scroll to the "Today's Menu" section with the offset
    window.scrollTo({
      top: sectionPosition - offset, // Adjusts the final position by the offset
      behavior: 'smooth',
    });
  });

  // Home button listener
  document.querySelector('.bottom-nav .navbar a[href="#home"]').addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default anchor click behavior
    e.stopPropagation();

    // Remove 'active' class from all nav items
    document.querySelectorAll('.navbar a').forEach((item) => {
      item.classList.remove('active');
    });

    // Add 'active' class
    this.classList.add('active');

    // Scroll smoothly to the top of the page
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  });
}

document.querySelector('.bottom-nav .navbar .more-butn').addEventListener('click', function(e) {

    // Remove 'active' class from all nav items
    document.querySelectorAll('.navbar a').forEach(item => {
        item.classList.remove('active');
    });

    // Add 'active' class 
    this.classList.add('active');

    setTimeout(function() {
        location.reload(); // Reloads the page after a delay
    }, 150);
});


// add service worker



if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      const rootURL = getRootUrl();
      //console.log(rootURL);
      navigator.serviceWorker.register(rootURL+'service-worker.js').then(registration => {
        //console.log('ServiceWorker registration successful with scope: ', registration.scope);
      }, err => {
        //console.log('ServiceWorker registration failed: ', err);
        //console.log(err)
      });
    });
  }
