function set_position_cookie (lat, lng) {
  document.cookie =   "lat" + "=" + lat + "; "
  document.cookie =   "lng" + "=" + lng + "; "
}

function get_position_cookie_lat() {
  return document.cookie.replace(/(?:(?:^|.*;\s*)lat\s*\=\s*([^;]*).*$)|^.*$/, "$1");
}

function get_position_cookie_lng() {
  return document.cookie.replace(/(?:(?:^|.*;\s*)lng\s*\=\s*([^;]*).*$)|^.*$/, "$1");
}