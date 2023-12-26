// Get the dashboard link element
const dashboardLink = document.querySelector('a[href="#dashboard"]');

// Get the main gauges container element
const mainGaugesContainer = document.querySelector(".main-gauges");

// Add click event listener to the dashboard link
dashboardLink.addEventListener("click", function (event) {
  event.preventDefault();

  // Toggle the visibility of the main gauges container
  mainGaugesContainer.classList.toggle("visible");
});
