let pageBody = document.getElementById("page-body");

let aktuellesBtn = document.getElementById("aktuelles-btn");
let privatesBtn = document.getElementById("privates-btn");
let learningBtn = document.getElementById("learning-btn");
let cafeBtn = document.getElementById("cafe-btn");
let settingsBtn = document.getElementById("settings-btn");

function switchContent(frameName){
    pageBody.src = `/${frameName}`;
    
    aktuellesBtn.className = frameName === "aktuelles" ? "navigation-button-selected" : "navigation-button-base";
    privatesBtn.className = frameName === "privates" ? "navigation-button-selected" : "navigation-button-base";
    learningBtn.className = frameName === "learning" ? "navigation-button-selected" : "navigation-button-base";
    cafeBtn.className = frameName === "cafe" ? "navigation-button-selected" : "navigation-button-base";
    
    // Assuming there is a separate Flask route to serve the settings page.
    settingsBtn.className = frameName === "settings" ? "settings-button-selected" : "settings-button-base";
}
