$(document).ready(function () {
  // Define the gauges
  var cpuGauge = new JustGage({
    id: "cpuGauge",
    value: 0,
    min: 0,
    max: 100,
    title: "CPU Usage",
    label: "%",
  });

  var memGauge = new JustGage({
    id: "memoryGauge",
    value: 0,
    min: 0,
    max: 4096,
    title: "Memory Usage",
    label: "MB",
  });

  var cpuTempGauge = new JustGage({
    id: "cpuTempGauge",
    value: 0,
    min: 0,
    max: 120,
    title: "CPU Temp",
    label: "°C",
  });

  var ramTempGauge = new JustGage({
    id: "ramTempGauge",
    value: 0,
    min: 0,
    max: 120,
    title: "RAM Temp",
    label: "°C",
  });

  // Function to update gauges
  function updateGauges() {
    $.getJSON("/system_info", function (data) {
      cpuGauge.refresh(data.cpu_usage);
      memGauge.refresh(data.ram_usage_percent);
      cpuTempGauge.refresh(data.cpu_temperature);
      ramTempGauge.refresh(data.ram_temperature);

      // Update absolute memory usage text
      $("#memory_usage_absolute").text(
        (data.ram_usage_bytes / 1048576).toFixed(2) + " MB"
      );
    });
  }

  // Update gauges every second
  setInterval(updateGauges, 1000);
});
