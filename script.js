

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
        return [dataArray1,dataArray2];
    }

}



function plotTimeSeriesData(chart_name,animation_duration,y_title,recorded,projected) {
    let parameter_max_height_percentage = 1.25;

    

    let dataArray1=recorded;
    let dataArray2=projected;
    //create between point
    let current_measurement=dataArray1[dataArray1.length-1]
    dataArray2=[current_measurement,].concat(dataArray2);//place current measurement in the start of projection array to connect the two lines
    
    //create fake invisible datapoint to increase y-lim seamelessly
    let all_data=dataArray1.concat(dataArray2);
    // Extracting all 'y' values from the array
    const yValues = all_data.map(item => item.y);
    // Finding the maximum value among all 'y' values
    const max = Math.max(...yValues);
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
  

  let update_period_minutes = 3;

  function schedulePageReload(lastUpdateStr) {
    const lastUpdate = new Date(lastUpdateStr);
    const now = new Date();
    const update_period = parseInt(update_period_minutes * 60 * 1000); // update period in milliseconds
    const standarddelay = 60 * 1000; // 60 seconds in milliseconds

    let delay;

    if ((now - lastUpdate) < update_period) {
        // If less than two minutes have passed since the last update
        delay = update_period - (now - lastUpdate);
    } else {
        // If more than two minutes have passed
        delay = standarddelay;
    }

    setTimeout(function() {
        window.location.reload(true);  // Force a reload from the server
    }, delay);
}


// Main
import {menus_text} from './data.js';
import {last_update_datetime} from './data.js';

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
    data_time=fake_data("minutes")
    let capacity = Math.round(Math.random()*100);
    let recorded_waittimes=data_time[0]
    let projected_waittimes=data_time[1]

    data_line=fake_data("size")
    let recorded_linesizes=data_line[0]
    let projected_linesizes=data_line[1]

    plotTimeSeriesData('waitTimeChart',200,'Wait Time (Minutes)',recorded_waittimes,projected_waittimes);
    plotTimeSeriesData('lineSizeChart',500,'Queue Length (People)',recorded_linesizes,projected_linesizes);
    updateRestaurantCapacity(capacity);

    document.getElementById('current_WaitTime').textContent = recorded_waittimes[recorded_waittimes.length-1].y.toString()+"'";
    document.getElementById('current_LineSize').textContent = recorded_linesizes[recorded_linesizes.length-1].y.toString();
    document.getElementById('current_Capacity').textContent = capacity.toString()+"%";


    // menu button listener
    // Add smooth scroll with offset to menu button
    document.querySelector('.bottom-nav .navbar a[href="#todays-menu"]').addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default anchor click behavior

        // Remove 'active' class from all nav items
        document.querySelectorAll('.navbar a').forEach(item => {
            item.classList.remove('active');
        });

        // Add 'active' class 
        this.classList.add('active');

        // Get the position of the "Today's Menu" section
        const menuSection = document.getElementById('todays-menu');
        const offset = 45; // Change this value to the desired offset
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