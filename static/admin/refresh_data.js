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
    max: 4096,
    title: "RAM Usage",
    width: 200,
    height: 200,
    textRenderer: function (value) {  // value is the value in MB
      var maxRam = 4096;  // # in MB
      var percentage_used = value / maxRam * 100;
      return percentage_used.toFixed(2) + "%\n" + " (" + value + "MB)";
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
        ramGauge.refresh(data.ram_usage_bytes / 1024 / 1024);
        cpuTempGauge.refresh(data.cpu_temp);
        ramTempGauge.refresh(data.ram_temp);
      },
    });
  }, 1000);
});
