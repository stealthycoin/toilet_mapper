// Lat, Long, Bearing in degrees
// Distance in miles
function destPoint(latDeg, lonDeg, bearingDeg, distance){
    var brng = Math.PI / 180 * bearingDeg;
    lat1 = Math.PI / 180 * latDeg;
    lon1 = Math.PI / 180 * lonDeg;
    var R = 3956.6; // Radius of the Earth
    var aD = distance / R; //angular distance
    var lat2 = Math.asin( Math.sin(lat1)*Math.cos(aD) + 
                          Math.cos(lat1)*Math.sin(aD)*Math.cos(brng));
    var lon2 = lon1 + Math.atan2(Math.sin(brng)*Math.sin(aD)*Math.cos(lat1), 
                                 Math.cos(aD)-Math.sin(lat1)*Math.sin(lat2));
    return {lat: 180 * lat2 / Math.PI, lon: 180 * lon2 / Math.PI};
}

//Returns the corner points of a square of width squareWidth
// centered on (lat, lon)
function squareBounds(lat, lon, squareWidth){
    return { 
        x_left: destPoint(lat, lon, 0, squareWidth/2).lat
        , x_right: destPoint(lat, lon, 180, squareWidth/2).lat
        , y_top: destPoint(lat, lon, 270, squareWidth/2).lon
        , y_bottom: destPoint(lat, lon, 90, squareWidth/2).lon
    }
}

function distance_from_current(latDeg1, lonDeg1, latDeg2, lonDeg2){
    console.log(latDeg1, lonDeg1, latDeg2, lonDeg2);
    lat1 = Math.PI / 180 * latDeg1;
    lon1 = Math.PI / 180 * lonDeg1;
    lat2 = Math.PI / 180 * latDeg2;
    lon2 = Math.PI / 180 * lonDeg2;
    var R = 3956.6; // Radius of the Earth
    var dLat = lat2 - lat1;
    var dLon = lon2 - lon1;

    var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(lat1) * Math.cos(lat2); 
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
    console.log("Computed distance: "+R*c);
    return Math.round(R * c * 10) / 10;
}
