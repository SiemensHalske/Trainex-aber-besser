var cpuUsageGauge = new JustGage({
    id: "cpuUsageGauge",
    value: 0,
    min: 0,
    max: 100,
    title: "CPU Usage"
});

var cpuTempGauge = new JustGage({
    id: "cpuTempGauge",
    value: 0,
    min: 0,
    max: 100,
    title: "CPU Temperature"
});

var ramUsageGauge = new JustGage({
    id: "ramUsageGauge",
    value: 0,
    min: 0,
    max: 100,
    title: "RAM Usage %"
});

var ramUsageBar = document.getElementById('ramUsageBar');

function updateSystemInfo() {
    $.ajax({
        url: '/system_info',
        method: 'GET',
        success: function(data) {
            cpuUsageGauge.refresh(data.cpu_usage);
            cpuTempGauge.refresh(data.cpu_temperature);
            ramUsageGauge.refresh(data.ram_usage_percent);

            var ramUsageMB = data.ram_usage_bytes / 1048576; // Convert bytes to MB
            ramUsageBar.style.width = data.ram_usage_percent + '%';
            ramUsageBar.innerText = ramUsageMB.toFixed(2) + ' MB'; // Display RAM usage in MB
        }
    });
}

setInterval(updateSystemInfo, 1000);