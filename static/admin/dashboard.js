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
  $(".navbar li a").click(function (e) {
    // Verhindert das Standardverhalten des Anker-Links
    e.preventDefault();

    // Entfernt 'active' von allen Links
    $(".navbar li a").removeClass("active");

    // Fügt 'active' zu dem geklickten Link hinzu
    $(this).addClass("active");

    // Hier könntest du zusätzlich Code einfügen, um deine Gauges anzuzeigen
    // Beispiel: $("#id-des-gauge-container").show();
  });
});

$(document).ready(function () {
  // Verstecke zuerst den User Management-Bereich
  $("#user-management").hide();

  // Event-Listener, der auf Klick auf den Link 'User Management' reagiert
  $('a[href="#user-management"]').click(function (e) {
    e.preventDefault();
    $("#user-management").show();
  });

  // Optional: Wenn du möchtest, dass der User Management-Bereich verschwindet, wenn auf andere Links geklickt wird
  $('a:not([href="#user-management"])').click(function () {
    $("#user-management").hide();
  });
});