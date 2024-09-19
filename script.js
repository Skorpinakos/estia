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
  
let update_period_minutes = 7;

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

// Main
import {menus_text} from './data.js';
import {last_update_datetime} from './data.js';
import {future_group1,future_group2,historic_group1,historic_group2} from './data.js';

window.addEventListener('load', function() {
    






    //set last updated tag
    document.getElementById('last-updated').textContent = `Last Updated: ${last_update_datetime}`;
    schedulePageReload(last_update_datetime);


    // parse menu text
    let menus=menus_text;

    // Call the function to add the menu items
    addProcessedMenuItemsToDOM(menus);





    // graphs


    let data_line,data_time;
    data_time=[convertArray(historic_group1),convertArray(future_group1)]//fake_data("minutes")
    //console.log([convertArray(historic_group1),convertArray(future_group1)])
    //console.log(fake_data("minutes"))
    
    let recorded_waittimes=data_time[0]
    let projected_waittimes=data_time[1]
    

    data_line=[convertArray(historic_group2),convertArray(future_group2)]//fake_data("size")
    let recorded_linesizes=data_line[0]
    let projected_linesizes=data_line[1]


    let capacity = Math.round(100*(recorded_waittimes[recorded_waittimes.length-1].y+recorded_linesizes[recorded_linesizes.length-1].y)/(recorded_waittimes.reduce((max, item) => (item.y > max ? item.y : max), -Infinity)+recorded_linesizes.reduce((max, item) => (item.y > max ? item.y : max), -Infinity)));

    plotTimeSeriesData('waitTimeChart',200,'Waiting Area Occupancy',recorded_waittimes,projected_waittimes);
    plotTimeSeriesData('lineSizeChart',500,'Restaurant Occupancy',recorded_linesizes,projected_linesizes);
    updateRestaurantCapacity(capacity);

    document.getElementById('current_WaitTime').textContent = recorded_waittimes[recorded_waittimes.length-1].y.toString();
    document.getElementById('current_LineSize').textContent = recorded_linesizes[recorded_linesizes.length-1].y.toString();
    document.getElementById('current_Capacity').textContent = capacity.toString()+"%";

    // Scroll smoothly to the top of the page
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });


    // menu button listener
    // Add smooth scroll with offset to menu button
    document.querySelector('.bottom-nav .navbar a[href="#todays-menu"]').addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default anchor click behavior
        e.stopPropagation(); 

        // Remove 'active' class from all nav items
        document.querySelectorAll('.navbar a').forEach(item => {
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
            behavior: 'smooth'
        });
    });

    // home button listener
    // Add smooth scroll to home button
    document.querySelector('.bottom-nav .navbar a[href="#home"]').addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default anchor click behavior
        e.stopPropagation(); 

        // Remove 'active' class from all nav items
        document.querySelectorAll('.navbar a').forEach(item => {
            item.classList.remove('active');
        });

        // Add 'active' class 
        this.classList.add('active');

        // Scroll smoothly to the top of the page
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

});

document.querySelector('.bottom-nav .navbar .more-btn').addEventListener('click', function(e) {

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