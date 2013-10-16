
$(document).ready(function(){
    $('.panel-button').on('click', function(){
	$(this).next().toggle();
	$(this).find('.panel-button-icon').toggleClass("icon-chevron-down");
	$(this).find('.panel-button-icon').toggleClass("icon-chevron-up");
    });
});



/** Inline toilet reviews **/

/** Toilet review listings **/
