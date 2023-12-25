// Create the gauges and bar
var cpuUsageGauge = new JustGage({id: "cpu-usage", min: 0, max: 100, title: "CPU Usage"});
var cpuTempGauge = new JustGage({id: "cpu-temp", min: 0, max: 100, title: "CPU Temp"});
var ramUsageBar = new Chart(document.getElementById('ram-usage').getContext('2d'), {
    type: 'bar',
    data: {
        labels: ['RAM Usage'],
        datasets: [{
            label: 'RAM Usage',
            data: [0],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                max: 100
            }
        }
    }
});
var ramTempGauge = new JustGage({id: "ram-temp", min: 0, max: 100, title: "RAM Temp"});

function updateDashboard() {
    $.ajax({
        url: '/system_info',
        type: 'GET',
        success: function(data) {
            // Update the gauges and bar with the new data
            cpuUsageGauge.refresh(data.cpu_usage);
            cpuTempGauge.refresh(data.cpu_temp);
            ramUsageBar.data.datasets[0].data = [data.ram_usage];
            ramUsageBar.update();
            ramTempGauge.refresh(data.ram_temp);
        }
    });
}

// Update the dashboard every second
setInterval(updateDashboard, 1000);