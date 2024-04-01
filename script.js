var menus_text = ['Γάλα, καφές, τσάι,χυμός , βούτυρο, άρτος, μέλι, ζαμπόν,τυρί', 'Πρώτο Πιάτο: Μπάμιες\nΚυρίως Πιάτο: Κοτόπουλο ψητό με ριζότο ή Μοσχάρι κοκκινιστό με κριθαράκι\nΜπουφές Σαλάτα: Μαρούλι με κρεμμύδια φρέσκα, ρόκα, λόλα λάχανο, άσπρο, κόκκινο, καρότο\nΕπιδόρπιο: Φρούτο Εποχής 2 επιλογές, ', 'Πρώτο Πιάτο: Σούπα του Σεφ\nΚυρίως Πιάτο: Τορτελίνια καρμπονάρα\nτυρί τριμμένο ή Φασολάκια λαδερά με πατάτες\nΜπουφές Σαλάτα: Ντομάτα, πιπεριά, κρεμμύδι, μαρούλι, κρεμμυδάκι φρέσκο ρόκα\n,λόλα\nΕπιδόρπιο: Φρούτο Εποχής 2 επιλογές, Τυρί φέτα'];
var last_update_datetime = "2024-04-01 09:09:35";

function fake_data(){
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





//split-a-string-based-on-multiple-delimiters

function splitStringByDelimiters(str, delimiters) {
    // Escape special characters in delimiters and join them into a regex pattern
    const regexPattern = delimiters.map(delimiter => 
        delimiter.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1")
    ).join("|");

    // Create a RegExp object with global search enabled
    const regex = new RegExp(regexPattern, 'g');

    // Split the string by the constructed RegExp
    return str.split(regex).filter(Boolean); // filter(Boolean) removes empty strings from the result
}



// finds which "ή" serve as a division and which as a subdivision, change divisions with "$", also remove parenthesis
function processString(inputString) {
    // Replace all \n with spaces
    let updatedString = inputString.replace(/\n/g, ' ');
    
    // Remove multiple spaces
    updatedString = updatedString.replace(/\s\s+/g, ' ');
    
    // Find all indexes where the character "ή" appears followed by a space and a Greek capital letter
    // Greek capital letters range from U+0391 to U+03A9
    let regex = /ή (?=[Α-Ω])/g;
    let indexes = [];
    let match;
    
    while ((match = regex.exec(updatedString)) !== null) {
        indexes.push(match.index);
    }
    
    // Replace those "ή" with the "$" character
    for (let i = indexes.length - 1; i >= 0; i--) {
        let index = indexes[i];
        updatedString = updatedString.substring(0, index) + '$' + updatedString.substring(index + 1);
    }
    
    return updatedString.replaceAll("("," ").replaceAll(")"," ");
}

// formats commas
function refineCommas(inputString) {
    // Removes any spaces before commas and ensures one space after each comma.
    // Deletes any commas that are at the end of the string, followed only by whitespaces.
    // Also trims leading and trailing whitespace from the string.
    return inputString.replace(/\s*,\s*/g, ', ').replace(/,+\s*$/, '').trim();
}



//function to parse menus
function parseMenus(menus_text){

    let menus_structured={};

    let breakfast=menus_text[0].toLowerCase();
    let lunch=processString(menus_text[1]).toLowerCase();
    let dinner=processString(menus_text[2]).toLowerCase();

    



    let breakfast_items=breakfast.split(',').map(item => item.trim());
    let breakfast_drinks=breakfast_items.slice(0,4);
    if (breakfast_items[breakfast_items.length -1]!="τυρί"){
    var breakfast_main=breakfast_items[breakfast_items.length - 1];
    var breakfast_slices=breakfast_items.slice(4,breakfast_items.length-1);
    }else{
    var breakfast_main=breakfast_items[breakfast_items.length - 2]+"-"+breakfast_items[breakfast_items.length - 1];
    var breakfast_slices=breakfast_items.slice(4,breakfast_items.length-2);
    }
    let breakfast_parts=[breakfast_main,breakfast_slices.join(', '),breakfast_drinks.join(', ')]
    //console.log(breakfast_drinks);
    //console.log(breakfast_slices);
    //console.log(breakfast_main);

    let split_words=["πρώτο πιάτο","κυρίως πιάτο","μπουφές σαλάτα","επιδόρπιο"]

    lunch=lunch.replaceAll("-"," ").replaceAll("\n"," ").replaceAll(":","");
    let lunch_parts=splitStringByDelimiters(lunch,split_words).map(item => item.trim());
    //console.log(lunch_parts);

    dinner=dinner.replaceAll("-"," ").replaceAll("\n"," ").replaceAll(":","");
    let dinner_parts=splitStringByDelimiters(dinner,split_words).map(item => item.trim());
    //console.log(dinner_parts);

    

    menus_structured={"lunch":lunch_parts,"dinner":dinner_parts,"breakfast":breakfast_parts};
    return menus_structured;



};

function capitalizeFirstLetter(string) {
    return string.trim().charAt(0).toUpperCase() + string.trim().slice(1);
  }

function capitalizeAfterBr(htmlString) {
    return htmlString.replace(/(<br><br>)(.)/g, function(match, p1, p2) {
        return p1 + p2.trim().toUpperCase();
    });
}
  

// Function to add menu options to the HTML
function addMenuItems(menus) {
    // For each meal type (breakfast, lunch, dinner)
    Object.entries(menus).forEach(([mealType, menuItems]) => {
        const menuContainer = document.getElementById(`${mealType}-menu`);
        menuItems.forEach(item => {
            let item_processed = item.replace(/\s*\$\s*/g, "<br><br>");
            item_processed=capitalizeFirstLetter(item_processed);
            item_processed=capitalizeAfterBr(item_processed);
            item_processed=refineCommas(item_processed);
            item_processed=item_processed.replaceAll("<br><br>","</p><hr><p>") //this came later along on top of the <br> separator
            const blob = document.createElement('div');
            blob.className = 'menu-blob';
            blob.innerHTML = `<p>${item_processed}</p>`;
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


// Main
window.addEventListener('load', function() {
    //set last updated tag
    document.getElementById('last-updated').textContent = `Last Updated: ${last_update_datetime}`;


    // parse menu text
    let menus=parseMenus(menus_text);

    // Call the function to add the menu items
    addMenuItems(menus);





    // graphs


    let data_line,data_time;
    data_time=fake_data()
    let capacity = Math.round(Math.random()*100);
    recorded_waittimes=data_time[0]
    projected_waittimes=data_time[1]

    data_line=fake_data()
    recorded_linesizes=data_line[0]
    projected_linesizes=data_line[1]

    plotTimeSeriesData('waitTimeChart',700,'Wait Time (Seconds)',recorded_waittimes,projected_waittimes);
    plotTimeSeriesData('lineSizeChart',1400,'Queue Length (People)',recorded_linesizes,projected_linesizes);
    updateRestaurantCapacity(capacity);

    document.getElementById('current_WaitTime').textContent = recorded_waittimes[recorded_waittimes.length-1].y.toString();
    document.getElementById('current_LineSize').textContent = recorded_linesizes[recorded_linesizes.length-1].y.toString();
    document.getElementById('current_Capacity').textContent = capacity.toString()+"%";


    // menu button listener
    // Add smooth scroll with offset to menu button
    document.querySelector('.nav-item[href="#menu"]').addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default anchor click behavior

        // Remove 'active' class from all nav items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });

        // Add 'active' class to menu button
        this.classList.add('active');

        // Get the position of the "Today's Menu" section
        const menuSection = document.getElementById('todays-menu');
        const offset = 37; // Change this value to the desired offset
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
    document.querySelector('.nav-item[href="#home"]').addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default anchor click behavior

        // Remove 'active' class from all nav items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });

        // Add 'active' class to home button
        this.classList.add('active');

        // Scroll smoothly to the top of the page
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

});