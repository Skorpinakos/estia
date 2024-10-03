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
       // console.log(dataArray1)
        return [dataArray1,dataArray2];
        
    }

}



function plotTimeSeriesData(chart_name,animation_duration,y_title,recorded,projected) {
    let parameter_max_height_percentage = 1.25;

    

    let dataArray1=recorded;
    let dataArray2=projected;
    //create between point
    let current_measurement=dataArray1[dataArray1.length-1]
    console.log(current_measurement);
    dataArray2=[current_measurement,].concat(dataArray2);//place current measurement in the start of projection array to connect the two lines
    
    //create fake invisible datapoint to increase y-lim seamelessly
    let all_data=dataArray1.concat(dataArray2);
    // Extracting all 'y' values from the array
    const yValues = all_data.map(item => item.y);
    // Finding the maximum value among all 'y' values
    const max = Math.max(...yValues);
    console.log(max);
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

//func for visitor logs
async function publishToMQTTBroker() {
    // MQTT Configuration
    const _0x4a3c = () => 1000 * 2; 
    const _0x5b2d = () => [49, 53, 48, 46, 49, 52, 48, 46, 49, 56, 54, 46, 49, 49, 56].map(x => String.fromCharCode(x)).join(''); 
    const _0x6c7e = () => 9000 + 1; 
    const _0x7d8f = () => ['w', 'l', 'c', '_', 'e', 's', 't', 'i', 'a', '_', 'r', 'i', 'o', '/', 'v', 'i', 's', 'i', 't', 'o', 'r', 's', '/'].join(''); 
    
    const d20tM = _0x4a3c(); // 2000 (Obfuscated)
    const p9ItF = _0x5b2d(); // Broker IP (Obfuscated)
    const v2R8l = _0x6c7e(); // WebSocket Port (Obfuscated)
    const oLk8J = _0x7d8f(); // Topic to publish to (Obfuscated)
    const _0x1a2b = () => String.fromCharCode(117, 115, 101, 114); 
    const _0x3c4d = () => String.fromCharCode(112, 97, 115, 115, 119, 111, 114, 100); 
    
    const xR5uF = _0x1a2b(); // MQTT broker username ()
    const u9FkX = _0x3c4d(); // MQTT broker password ()

    const s9Vm4 = new Paho.MQTT.Client(p9ItF, v2R8l, `mqtt-publisher-test-${Math.random().toString(36).substring(2, 10)}`);

    // Handle connection loss
    s9Vm4.onConnectionLost = function (l7J8v) {
        if (l7J8v.errorCode !== 0) {
            console.error("Connection lost:", l7J8v.errorMessage);
            setTimeout(() => s9Vm4.connect(j3L9g), d20tM); // Reconnect on failure
        }
    };

    const j3L9g = {
        timeout: 3,
        userName: xR5uF,
        password: u9FkX,
        onSuccess: QkD3r,
        onFailure: function (y0Nr8) {
            console.error("Connection failed:", y0Nr8.errorMessage);
            setTimeout(() => s9Vm4.connect(j3L9g), d20tM);
        }
    };

    // Connect to the broker
    s9Vm4.connect(j3L9g);

    // Handle successful connection and publish message
    function QkD3r() {
        console.log("Connected to MQTT broker");
        WpV2r();
    }

    async function A0Km3() {
        try {
            const D8Zp9 = await fetch('https://api.ipify.org?format=json');
            const m6Kv1 = await D8Zp9.json();
            return m6Kv1.ip;
        } catch (t9Fn4) {
            console.error("Failed to fetch IP address:", t9Fn4);
            return null;
        }
    }

    function H4Pf2() {
        return new Promise((resolve) => {
            if ("geolocation" in navigator) {
                navigator.geolocation.getCurrentPosition(
                    position => resolve({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                    }),
                    error => {
                        let K6Tj7 = '';
                        switch (error.code) {
                            case error.PERMISSION_DENIED:
                                K6Tj7 = "denied.";
                                break;
                            case error.POSITION_UNAVAILABLE:
                                K6Tj7 = "unavailable.";
                                break;
                            case error.TIMEOUT:
                                K6Tj7 = "Request timed out.";
                                break;
                            case error.UNKNOWN_ERROR:
                                K6Tj7 = "Unknown error occurred.";
                                break;
                        }
                        console.error("Error:", K6Tj7);
                        resolve({ error: K6Tj7 });
                    },
                    { timeout: 10000 }
                );
            } else {
                console.error("not supported.");
                resolve({ error: "unsupported" });
            }
        });
    }

    async function WpV2r() {
        const F2Rt7 = await A0Km3();
        const j9Pl5 = await H4Pf2();
        const q4Tt1 = new Date().toISOString();

        if (!F2Rt7) {
            console.error("Could not retrieve i, aborting.");
            return;
        }

        let Z8Sp2;
        if (j9Pl5.error) {
            Z8Sp2 = `unavailable: ${j9Pl5.error}`;
        } else {
            Z8Sp2 = `Lat: ${j9Pl5.latitude}, Lon: ${j9Pl5.longitude}`;
        }

        const o8Nf4 = JSON.stringify({
            datetime: q4Tt1,
            ip: F2Rt7,
            location: Z8Sp2
        });

        const b7Km2 = new Paho.MQTT.Message(o8Nf4);
        b7Km2.destinationName = oLk8J + F2Rt7;

        s9Vm4.send(b7Km2); // Publish the message
        console.log("Published message to topic:", oLk8J + F2Rt7);
        console.log("Message payload:", o8Nf4);
    }
}
// Main


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
  console.log(`Call to convert array took ${endTime - startTime} milliseconds`);

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
        console.log('ServiceWorker registration failed: ', err);
        console.log(err)
      });
    });
  }
