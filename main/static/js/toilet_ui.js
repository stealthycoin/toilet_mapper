/** Template helper functions **/
window.templateStatus = {};

function loadTemplate(url, varname) {
    $.ajax({
        url: url,
        success: function (data) {
            window.templateStatus[varname] = Handlebars.compile(data);
        }
    });
}

function isTemplateLoaded(varname) {
    return window.templateStatus[varname] !== undefined;
}

function getTemplate(varname) {
    if (window.templateStatus[varname] === undefined) {
        throw "Template " + varname + " has not been loaded";
    }
    return window.templateStatus[varname];
}

/** Panelly UI stuff */
function bind_panels() {
    $('.panel-button').each(function () {
        if (!$(this).data('panelbound')) {
            $(this).on('click', function () {
                if (!$(this).next().is(":visible")) {
                    $('html, body').animate({
                        scrollTop: $(this).offset().top - 100
                    }, 500);
                }
                $(this).next().toggle();
                $(this).find('.panel-button-icon').toggleClass("icon-chevron-down");
                $(this).find('.panel-button-icon').toggleClass("icon-chevron-up");
            });
            $(this).data('panelbound', true);
        }
    });
}

$(document).ready(function () {
    bind_panels();
});

/** Form stuff **/
function form_error(form_id, message) {
    $('#' + form_id + " .error").remove();
    $('#' + form_id).append("<div class='error'>" + message + "</div>");
}

/* Stars for reviews */
function generateStars(i) {
    i = Math.round(i * 2) / 2
    var a = '';
    var j;
    for (j = 0; j < Math.floor(i); j++) {
        a += "<span class='icon-star'></span>";
    }
    if (j - i !== 0) {
        a += "<span class='icon-star-half-full'></span>";
        i = j + 1;
    }
    for (j = i; j < 5; j++) {
        a += "<span class='icon-star-empty'></span>";
    }
    return a;
}


/** Toilet Listings **/
var numToiletsLoaded = 0;
var toiletsLoading = false;
loadTemplate("/static/handlebars/toilet.html", "toilet");

function loadToiletListings(div_id, i, filter) {
    //for the love of all that is holy abstract this out later please
    //not checking for existence because I am assuming there is a global
    //in window I should be able to access, just cant find it.
    var location;
    navigator.geolocation.getCurrentPosition(function(position) {
	location = new google.maps.LatLng(position.coords.latitude,
					      position.coords.longitude);
    });

	
    //i was originally being appended when adding, silly JS thought it was a string...
    i = Number(i);
    i = i || 10;

    if (toiletsLoading) return;
    //Keep trying until the toilet template has been loaded
    if (!isTemplateLoaded("toilet")) {
        setTimeout("loadToiletListings('" + div_id + "', '" + i + "', " + JSON.stringify(filter) + " );", 50);
        return;
    }
    template = getTemplate("toilet");
    toiletsLoading = true;
    //Appendable parameters to send to tapi
    var params = {
        noun: "toilet",
        verb: "retrieve",
        data: {
            start: numToiletsLoaded,
            end: numToiletsLoaded + i
        },
        callback: function (data) {
            console.log("Callbaaaack");
            //For each toilet that we look up set the attributes
            for (o in data) {
                console.log(data[o]);
                var params = {};
                params.pk = data[o].pk;
                params.stars = generateStars(data[o].ranking || 3.5);
                params.date = data[o].fields.date.slice(0, 10);
                params.name = data[o].fields.name;
                params.num_reviews = data[o].count || 42;
		console.log(window);
		//please fix this someday
		var toilet_pos = new google.maps.LatLng(data[o].fields.lat,
							data[o].fields.lng);
		var dist = distHaversine(location, toilet_pos);
		params.distance = dist;
                $('#' + div_id).append(template(params));
            }
            //This doesn't do anything. Have to manually set toiletsLoading
            //to false before a call if it has already been called
            toiletsloading = false;
            numToiletsLoaded += i;
        }
    };

    //append filter arguments to params.data
    if (filter !== undefined) {
        jQuery.extend(params.data, filter);
        console.log(params.data + "  woop");
    }
    console.log(params.data);

    tapi(params);
}

//this should not live here but its the haversign function 
function distHaversine(p1, p2) {
    var torad = function(x) {return x*Math.PI/180;};
    var R = 3959;
    var dLat  = torad(p2.lat()-p1.lat());
    var dLong = torad(p2.lng()-p1.lng());

    var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(torad(p1.lat())) * Math.cos(torad(p2.lat())) * Math.sin(dLong/2) * Math.sin(dLong/2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    var d = R * c;

    return d.toFixed(1);
}


//This is sort of a janky way to fix the bugs we faced when doing searches
//toiletsLoading isn't reset properly and numToiletsLoaded is incrementing each call
//causing no results to be returned
function searchReset() {
    toiletsLoading = false;
    numToiletsLoaded = 0;
}
