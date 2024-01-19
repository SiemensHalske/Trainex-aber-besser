$(document).ready(function () {
  // Verstecke zuerst beide Bereiche
  $(".grid-container, .management-container_master").hide();

  // Event-Listener für '#dashboard'
  $('a[href="#dashboard"]').click(function (e) {
    e.preventDefault();
    $(".grid-container").show();
    $(".management-container_master").hide();
  });

  // Event-Listener für '#usermanagement'
  $('a[href="#usermanagement"]').click(function (e) {
    e.preventDefault();
    $(".management-container_master").show();
    $(".grid-container").hide();
  });

  // Entfernen von 'active' und Hinzufügen zu dem geklickten Link
  $(".navbar li a").click(function (e) {
    e.preventDefault();
    $(".navbar li a").removeClass("active");
    $(this).addClass("active");
  });

  // Optional: Verstecke beide Bereiche, wenn auf andere Links geklickt wird
  $('a:not([href="#dashboard"], [href="#usermanagement"])').click(function () {
    $(".grid-container, .management-container_master").hide();
  });
});