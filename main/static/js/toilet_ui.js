
$(document).ready(function(){
    $('.panel-button').on('click', function(){
	$(this).next().toggle();
	$(this).find('.panel-button-icon').toggleClass("icon-chevron-down");
	$(this).find('.panel-button-icon').toggleClass("icon-chevron-up");
    });


    $('#rate-bathroom-form').submit(function(e){
        if(!$( '#rate-bathroom-form' ).parsley( 'isValid' )) return;
        event.preventDefault(); 
        $.ajax({
            url : '/toilet/review/'
            ,type : 'POST'
            ,data : {
                rating: $('#inputRating').val()
                ,review: $('#inputReview').val()
            }
        });        
    });
});



