document.addEventListener('DOMContentLoaded', function() {
    const waitTimesData = {
        labels: ['10 AM', '11 AM', '12 PM', '1 PM', '2 PM'],
        datasets: [{
            label: 'Wait Time (mins)',
            data: [5, 10, 15, 20, 25],
            fill: true,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgb(75, 192, 192)',
            pointBackgroundColor: 'rgb(75, 192, 192)',
            tension: 0.4,
            borderWidth: 2,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: 'rgb(255, 99, 132)',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 3
        }]
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
                    text: 'Size'
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
        options: chartOptionsLine
    });

    const lineSizeCtx = document.getElementById('lineSizeChart').getContext('2d');
    new Chart(lineSizeCtx, {
        type: 'line',
        data: lineSizesData,
        options: chartOptionsTime
    });
});
