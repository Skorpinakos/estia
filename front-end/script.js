document.addEventListener('DOMContentLoaded', function() {
    const waitTimesData = {
        labels: ['10 AM', '11 AM', '12 PM', '1 PM', '2 PM'],
        datasets: [
            {
                // Segment before 12 PM
                label: 'Recorded',
                data: [5, 20, 30, null, null], // Use null to create breaks in the line
                borderColor: 'rgb(75, 192, 192)', // Original color
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
        datasets: [{
            label: 'Line Size (people)',
            data: [30, 40, 50, 60, 70],
            fill: true,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgb(255, 99, 132)',
            pointBackgroundColor: 'rgb(255, 99, 132)',
            tension: 0.4,
            borderWidth: 2,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: 'rgb(75, 192, 192)',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 3
        }]
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
                display: true,
                title: {
                    display: true,
                    text: 'Size'
                }
            }
        },
        animation: {
            duration: 1000, // general animation time
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
                display: true,
                title: {
                    display: true,
                    text: 'Wait Time'
                }
            }
        },
        animation: {
            duration: 1500, // general animation time
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
