$(document).ready(function () {
  var cpuGauge = new JustGage({
    id: "cpu-usage",
    value: 0,
    min: 0,
    max: 100,
    title: "CPU Usage",
    width: 200,
    height: 200,
  });

  var ramGauge = new JustGage({
    id: "ram-usage",
    value: 0,
    min: 0,
    max: 100,
    title: "RAM Usage",
    width: 200,
    height: 200,
    textRenderer: function (value) {
      var absoluteValue = (4096 * 1024 * value) / 100;
      return value + "% (" + absoluteValue.toFixed(2) + " MB)";
    },
  });

  var cpuTempGauge = new JustGage({
    id: "cpu-temp",
    value: 0,
    min: 0,
    max: 100,
    title: "CPU Temperature",
    width: 200,
    height: 200,
  });

  var ramTempGauge = new JustGage({
    id: "ram-temp",
    value: 0,
    min: 0,
    max: 100,
    title: "RAM Temperature",
    width: 200,
    height: 200,
  });

  setInterval(function () {
    $.ajax({
      url: "/system_info",
      type: "GET",
      success: function (data) {
        cpuGauge.refresh(data.cpu_usage);
        //  # totalRam should be the total RAM in MB
        ramGauge.refresh(data.ram_usage_bytes / (4096 * 1024));
        cpuTempGauge.refresh(data.cpu_temp);
        ramTempGauge.refresh(data.ram_temp);
      },
    });
  }, 1000);
});
