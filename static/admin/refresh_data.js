$(document).ready(function() {
    var cpuGauge = new JustGage({
        id: "cpu-usage",
        value: 0,
        min: 0,
        max: 100,
        title: "CPU Usage"
    });

    var ramGauge = new JustGage({
        id: "ram-usage",
        value: 0,
        min: 0,
        max: 100,
        title: "RAM Usage"
    });

    var cpuTempGauge = new JustGage({
        id: "cpu-temp",
        value: 0,
        min: 0,
        max: 100,
        title: "CPU Temperature"
    });

    var ramTempGauge = new JustGage({
        id: "ram-temp",
        value: 0,
        min: 0,
        max: 100,
        title: "RAM Temperature"
    });

    setInterval(function() {
        $.ajax({
            url: '/system_info',
            type: 'GET',
            success: function(data) {
                cpuGauge.refresh(data.cpu_usage);
                ramGauge.refresh(data.ram_usage);
                cpuTempGauge.refresh(data.cpu_temp);
                ramTempGauge.refresh(data.ram_temp);
            }
        });
    }, 1000);
});