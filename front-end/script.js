const y_lim_ratio=1.2;

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
                backgroundColor: 'rgb(75, 192, 192,0.2'
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
});
