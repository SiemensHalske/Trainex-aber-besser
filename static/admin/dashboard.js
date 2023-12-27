$(document).ready(function () {
  // Verstecke zuerst beide Bereiche
  $("#dashboard, #usermanagement").hide();

  // Event-Listener für '#dashboard'
  $('a[href="#dashboard"]').click(function (e) {
    e.preventDefault();
    $("#dashboard").show();
    $("#usermanagement").hide();
  });

  // Event-Listener für '#usermanagement'
  $('a[href="#usermanagement"]').click(function (e) {
    e.preventDefault();
    $("#usermanagement").show();
    $("#dashboard").hide();
  });

  // Entfernen von 'active' und Hinzufügen zu dem geklickten Link
  $(".navbar li a").click(function (e) {
    e.preventDefault();
    $(".navbar li a").removeClass("active");
    $(this).addClass("active");
  });

  // Optional: Verstecke beide Bereiche, wenn auf andere Links geklickt wird
  $('a:not([href="#dashboard"], [href="#usermanagement"])').click(function () {
    $("#dashboard, #usermanagement").hide();
  });
});