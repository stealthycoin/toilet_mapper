var first_run = true;
function showMap(from) {
    //clear prev directions from the page
    $("#step_panel").html("");
    lat=$('#lat').val();//||36.991366;
    lng=$('#lng').val();//||-122.059844;
    //decide on which travel option the user chose
    var travelOption = google.maps.DirectionsTravelMode.WALKING;
    if($('#dropDown').val() === 'DRIVING')
        travelOption = google.maps.DirectionsTravelMode.DRIVING;
    else if($('#dropDown').val() === 'TRANSIT')
        travelOption = google.maps.DirectionsTravelMode.TRANSIT;
    else if($('#dropDown').val() === 'BICYCLING')
        travelOption = google.maps.DirectionsTravelMode.BICYCLING;
    var toilet_address = new google.maps.LatLng(lat, lng);
    var mapOptions = {
        zoom: 17,
        center: toilet_address,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    var map = new google.maps.Map(document.getElementById("map"), mapOptions);
    var marker = new google.maps.Marker({
        position: toilet_address,
        map: map,
        title: $('#toilet_name').val()
    });
    // Try W3C Geolocation (Preferred)
    var directionsService = new google.maps.DirectionsService();
    var directionsDisplay = new google.maps.DirectionsRenderer();
    var directionsRequest = {
        origin: from,
        destination: toilet_address,
        travelMode: travelOption,
        unitSystem: google.maps.UnitSystem.SI
    };
    directionsDisplay.setMap(map);
    directionsDisplay.setPanel(document.getElementById('step_panel'));
    directionsService.route(directionsRequest, function(response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
        }
    });
}

function registerMapForm() {
  $("#from-link").click(function(event) {
    event.preventDefault();
    current_address(
      function (address){
        $("#from").val(address);
        if(first_run) {
            $('#calculate-route').submit();
            first_run=false;
        }
      },
      function (failure){
        $("#error").append("Error: " + failure + "<br/>");
      }
    );
  });
  $("#calculate-route").submit(function(event) {
    event.preventDefault();
    showMap($("#from").val());
  });
}

function listen_get_postition_button(button_id, address_field, error_field) {
  $("#"+button_id).click(function(event) {
      current_address(
      function (address){
        $("#"+address_field).val(address);
      },
      function (failure){
        $("#"+error_field).append("Error: " + failure + "<br/>");
      }
    );
  });
}

function current_pos(callback){
  navigator.geolocation.getCurrentPosition(
      callback
      ,function(positionError){
          failure(positionError.message);
      },
      {
          enableHighAccuracy: true,
          timeout: 10 * 1000 // 10 seconds
      }
  );
}

function pos_to_address(position, address) {
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode(
        {
            "location": new google.maps.LatLng(position.coords.latitude, 
                                               position.coords.longitude)
        },
        function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                //in case of success return the address
                address(results[0].formatted_address);
            }
            else
                failure("Unable to retrieve your address");
        }
    );
}

function current_address(address, failure) {
    var lat = get_position_cookie_lat();
    var lng = get_position_cookie_lng();
    if(lat !== undefined && lng !== undefined)
        return pos_to_address({ coords: {latitude: lat
                                         ,longitude: lng
                                        }}, address);

  // If the browser supports the Geolocation API
    if (typeof navigator.geolocation == "undefined") 
        failure("Your browser doesn't support the Geolocation API");
    
    current_pos(function(p){ pos_to_address(p, address); });
    
}

function loadMap(){
    showMap($("#from").val());
}

function address_to_coordinates(address, success, fail)
{
    var gc   = new google.maps.Geocoder();
    var opts = { 'address' : address };
    gc.geocode(opts, function (results, status)
    {
        if (status == google.maps.GeocoderStatus.OK)
        {   
            var loc  = results[0].geometry.location;
            success(loc.lat(), loc.lng());  
        }
        else
        {
            fail("Unable to retrieve the coordinates<br/>");
        }
    });
}

function listenKeyTimer(item_id, id_thinking, id_success, id_fail, time_sec)
{
   //setup before functions
   var typingTimer;
   var doneTypingInterval = time_sec*1000;  

   //on keyup, start the countdown
   $('#'+item_id).keyup(function(){
       typingTimer = setTimeout(doneTyping, doneTypingInterval);
   });

   //on keydown, clear the countdown 
   $('#'+item_id).keydown(function(){
       clearTimeout(typingTimer);
       $('#'+id_thinking).show();
       $('#'+id_fail).hide();
       $('#'+id_success).hide();
   });
   //user is "finished typing"
   function doneTyping () {
      $('#'+id_thinking).show();
      $('#'+id_fail).hide();
      $('#'+id_success).hide();
      address_to_coordinates($('#'+item_id).val(),
         function success(lat, lng){
            $('#'+id_thinking).hide();
            $('#'+id_fail).hide();
            $('#'+id_success).show();
         },
         function fail(fail_message){
            $('#'+id_thinking).hide();
            $('#'+id_fail).show();
            $('#'+id_success).hide();
         }
      );
   }
}

google.maps.event.addDomListener(window,'load',loadMap);
