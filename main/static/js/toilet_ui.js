
$(document).ready(function(){
    $('.panel-button').on('click', function(){
	$(this).next().toggle();
	$(this).find('.panel-button-icon').toggleClass("icon-chevron-down");
	$(this).find('.panel-button-icon').toggleClass("icon-chevron-up");
    });
});


function form_error(form_id, message){
    $('#'+form_id+" .error").remove();
    $('#'+form_id).append("<div class='error'>"+message+"</div>");
}

/* Stars for reviews */
function generateStars(i){
    i = Math.round(i * 2) / 2
    var a = '';
    var j; 
    for(j = 0; j < Math.floor(i); j++){
        a += "<span class='icon-star'></span>";
    }
    if(j - i !== 0){
        a += "<span class='icon-star-half-full'></span>";
        i = j + 1; 
    }
    for(j = i; j < 5; j++){
        a += "<span class='icon-star-empty'></span>";
    }
    return a;
}


/** Inline toilet reviews **/

/** Toilet review listings **/
