$(document).ready(function () {
  // Verstecke zuerst die Gauges
  $(".grid-container").hide();

  // Event-Listener, der auf Klick auf den Link '#dashboard' reagiert
  $('a[href="#dashboard"]').click(function (e) {
    // Verhindere das Standardverhalten des Links
    e.preventDefault();

    // Zeige die Gauges an
    $(".grid-container").show();
  });

  // Optional: Wenn du möchtest, dass die Gauges verschwinden, wenn auf andere Links geklickt wird
  $('a:not([href="#dashboard"])').click(function () {
    $(".grid-container").hide();
  });
});

$(document).ready(function () {
  $(".navbar li a").click(function () {
    // Remove the class 'active' if it exists on any link
    $(".navbar li a").removeClass("active");

    // Add the class 'active' to the clicked link
    $(this).addClass("active");
  });
});
