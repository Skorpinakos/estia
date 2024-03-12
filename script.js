/*const y_lim_ratio=1.2;

document.addEventListener('DOMContentLoaded', function() {
    const waitTimesData = {
        labels: ['10 AM', '11 AM', '12 PM', '1 PM', '2 PM'],
        datasets: [
            {
                // Segment before 12 PM
                label: 'Recorded',
                data: [5, 20, 30, null, null], // Use null to create breaks in the line
                borderColor: 'rgb(75, 192, 192)', // Original color
                fill: true,
                backgroundColor: 'rgb(75, 192, 192,0.2'
                // other properties remain the same
            },
            {
                // Segment between 12 PM and 2 PM you wish to change
                label: 'Estimate',
                data: [null, null, 30, 45, 70], // Highlighted segment
                borderColor: 'rgba(255, 99, 132, 0.5)', // Changed color and transparency
                // other properties adapted for this segment
            },

        ]
    };

    const lineSizesData = {
        labels: ['10 AM', '11 AM', '12 PM', '1 PM', '2 PM'],
        datasets: [
            {
                // Segment before 12 PM
                label: 'Recorded',
                data: [15, 40, 30, null, null], // Use null to create breaks in the line
                borderColor: 'rgb(75, 192, 192)', // Original color
                fill: true,
                backgroundColor: 'rgb(75, 192, 192,0.2)'
                // other properties remain the same
            },
            {
                // Segment between 12 PM and 2 PM you wish to change
                label: 'Estimate',
                data: [null, null, 30, 20, 5], // Highlighted segment
                borderColor: 'rgba(255, 99, 132, 0.5)', // Changed color and transparency
                // other properties adapted for this segment
            },

        ]
    };


    const chartOptionsLine = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                mode: 'index',
                intersect: false,
            },
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            x: {
                display: true,
                title: {
                    display: true,
                    text: 'Time of Day'
                }
            },
            y: {
                beginAtZero: true,
                suggestedMax: Math.round(Math.max(Math.max(...lineSizesData.datasets[0].data.map(v => v === null ? 0 : v)),Math.max(...lineSizesData.datasets[1].data.map(v => v === null ? 0 : v)))*y_lim_ratio/10)*10, //find the max value between predicted and recorded and set y-lim to that + 10% 
                display: true,
                title: {
                    display: true,
                    text: 'Line Size (People)'
                }
            }
        },
        animation: {
            duration: 1500, // general animation time
        },
    };

    const chartOptionsTime = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                mode: 'index',
                intersect: false,
            },
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            x: {
                display: true,
                title: {
                    display: true,
                    text: 'Time of Day'
                }
            },
            y: {
                beginAtZero: true,
                max: Math.round(Math.max(Math.max(Math.max(...waitTimesData.datasets[0].data.map(v => v === null ? 0 : v)),Math.max(...waitTimesData.datasets[1].data.map(v => v === null ? 0 : v))))*y_lim_ratio/10)*10, //find the max value between predicted and recorded and set y-lim to that + 10% 
                display: true,
                title: {
                    display: true,
                    text: 'Wait Time (Minutes)'
                }
            }
        },
        animation: {
            duration: 2500, // general animation time
        },
    };

    const waitTimeCtx = document.getElementById('waitTimeChart').getContext('2d');
    new Chart(waitTimeCtx, {
        type: 'line',
        data: waitTimesData,
        options: chartOptionsTime
    });

    const lineSizeCtx = document.getElementById('lineSizeChart').getContext('2d');
    new Chart(lineSizeCtx, {
        type: 'line',
        data: lineSizesData,
        options: chartOptionsLine
    });
});*/
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

    

    let dataArray1=recorded;
    let dataArray2=projected;
    //create between point
    let current_measurement=dataArray1[dataArray1.length-1]
    dataArray2=[current_measurement,].concat(dataArray2);//place current measurement in the start of projection array to connect the two lines



    // Set up the chart
    const ctx = document.getElementById(chart_name).getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [
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
                        parser: 'HH:mm', // This ensures the format of the time being parsed
                        tooltipFormat: 'HH:mm'
                    },
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: 20, // Adjust based on your preference
                        major: {
                            enabled: true // this will include major ticks with a different styling
                        }
                    },
                    afterBuildTicks: (scale) => {
                        scale.ticks = scale.ticks.filter(tick => {
                            // Check if the tick corresponds to a full or half hour
                            const date = new Date(tick.value);
                            const minutes = date.getMinutes();
                            return minutes == 0 || minutes == 30;
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
            },
            animation: {
                duration: animation_duration, // general animation time
            },
            
            
        }

        
    });
}

let data_line,data_time;
let recorded,projected;
let recorded_people,projected_people

data_time=fake_data()
recorded_waittimes=data_time[0]
projected_waittimes=data_time[1]

data_line=fake_data()
recorded_linesizes=data_line[0]
projected_linesizes=data_line[1]

plotTimeSeriesData('waitTimeChart',1000,'Wait Time (Seconds)',recorded_waittimes,projected_waittimes);
plotTimeSeriesData('lineSizeChart',2500,'Line Size (People)',recorded_linesizes,projected_linesizes);

document.getElementById('current_WaitTime').textContent = recorded_waittimes[recorded_waittimes.length-1].y;
document.getElementById('current_LineSize').textContent = recorded_linesizes[recorded_linesizes.length-1].y;
