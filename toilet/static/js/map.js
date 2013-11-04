<script type="text/javascript"
src="https://maps.googleapis.com/maps/api/js?sensor=true">
</script>

function showMap(from, lat, lng) {
 var toilet_address = new google.maps.LatLng(lat, lng);
 var mapOptions = {
    zoom: 15,
    center: toilet_address,
    mapTypeId: google.maps.MapTypeId.ROADMAP
 }
 var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
 // Try W3C Geolocation (Preferred)
 var directionsService = new google.maps.DirectionsService();
 var directionsRequest = {
    origin: from,
    destination: toilet_address,
    travelMode: google.maps.DirectionsTravelMode.DRIVING,
    unitSystem: google.maps.UnitSystem.METRIC
 };
 directionsService.route(
    directionsRequest,
    function(response, status)
    {
    if (status == google.maps.DirectionsStatus.OK)
    {
      new google.maps.DirectionsRenderer({
        map: map,
        directions: response
      });
    }
    else
      $("#error").append("Unable to retrieve your route<br />");
    }
 );
}

$(document).ready(function() {
// If the browser supports the Geolocation API
if (typeof navigator.geolocation == "undefined") {
  $("#error").text("Your browser doesn't support the Geolocation API");
  return;
}
$("#from-link").click(function(event) {
  event.preventDefault();
  var addressId = this.id.substring(0, this.id.indexOf("-"));

  navigator.geolocation.getCurrentPosition(function(position) {
       var geocoder = new google.maps.Geocoder();
       geocoder.geocode({
         "location": new google.maps.LatLng(position.coords.latitude, position.coords.longitude)
       },
       function(results, status) {
         if (status == google.maps.GeocoderStatus.OK)
           $("#" + addressId).val(results[0].formatted_address);
         else
           $("#error").append("Unable to retrieve your address<br />");
       });
     },
     function(positionError){
       $("#error").append("Error: " + positionError.message + "<br />");
     },
     {
       enableHighAccuracy: true,
       timeout: 10 * 1000 // 10 seconds
     });
});

$("#calculate-route").submit(function(event) {
  event.preventDefault();
  showMap($("#from").val());
});
});

function loadScript() {
 var script = document.createElement("script");
 script.src = showMap();
 document.body.appendChild(script);
}
window.onload = loadScript;

