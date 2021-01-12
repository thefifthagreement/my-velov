/* Project specific Javascript goes here. */
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };
        document.getElementById("latitude").innerHTML = `latitude:${pos.lat}`
        document.getElementById("longitude").innerHTML = `longitude:${pos.lng}`
      },
      () => {
        console.log("Error: Your browser doesn't support geolocation.")
      }
    );
  } else {
    // Browser doesn't support Geolocation
    console.log("Error: The Geolocation service failed.")
  }
}
