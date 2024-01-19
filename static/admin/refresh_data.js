$(document).ready(function () {
  // Define the gauges
  var cpuGauge = new JustGage({
    id: "cpuGauge",
    value: 0,
    min: 0,
    max: 100,
    title: "CPU Usage",
    label: "%",
    decimals: 1, // Set the number of decimal places
  });

  var memGauge = new JustGage({
    id: "memoryGauge",
    value: 0,
    min: 0,
    max: 4096,
    title: "Memory Usage",
    label: "MB",
    decimals: 3, // Set the number of decimal places
  });

  var cpuTempGauge = new JustGage({
    id: "cpuTempGauge",
    value: 0,
    min: 0,
    max: 120,
    title: "CPU Temp",
    label: "°C",
    decimals: 2, // Set the number of decimal places
  });

  var ramTempGauge = new JustGage({
    id: "ramTempGauge",
    value: 0,
    min: 0,
    max: 120,
    title: "RAM Temp",
    label: "°C",
    decimals: 2, // Set the number of decimal places
  });

  function updateGauges() {
    // Check if the dashboard tab is active before updating gauges
    if ($('a[href="#dashboard"]').hasClass("active")) {
      $.getJSON("/system_info", function (data) {
        console.log(data);
        cpuGauge.refresh(data.cpu_usage);
        memGauge.refresh(data.ram_usage_bytes / 1048576); // Convert to MB
        cpuTempGauge.refresh(data.cpu_temperature);
        ramTempGauge.refresh(data.ram_temperature);

        // Update absolute memory usage text
        $("#memory_usage_absolute").text(
          (data.ram_usage_bytes / 1048576).toFixed(2) + " MB"
        );
      });
    }
  }

  // Initial call to update gauges
  updateGauges();

  // Set interval to update gauges every second if dashboard is active
  setInterval(updateGauges, 1000);

  // Add click event to update gauges when the dashboard tab is clicked
  $('a[href="#dashboard"]').click(function () {
    // Add 'active' class to dashboard link
    $(this).addClass("active");
    // Immediately update gauges when dashboard is clicked
    updateGauges();
  });

  // Add click event to remove 'active' class when other tabs are clicked
  $('a[href]:not([href="#dashboard"])').click(function () {
    // Remove 'active' class from dashboard link
    $('a[href="#dashboard"]').removeClass("active");
  });
});
