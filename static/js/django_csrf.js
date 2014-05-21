
function setup_django_csrf(){
    function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    var csrftoken = $.cookie('csrftoken'); //requires jQuery cookie plugin

    $.ajaxSetup({
	crossDomain: false, // obviates need for sameOrigin test
	beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
		xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
	}
    });
}
