/**
 * Preloading screan
 */
$(window).on('load', 
    function() {
        $('#status').fadeOut();                     // will first fade out the loading animation 
        $('#preloader').delay(500).fadeOut('slow'); // will fade out the white DIV that covers the website. 
        checkTouchScreen();                         // check if the device has a touchscreen
    }
);

$(document).ready(function() {

    /**
     * Click on play button
     */
    $("#play_arrow").click(function(){
        alert("Chachi pistachi");
    });

});

function checkTouchScreen() {
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        $('body').addClass('touch-screen');
        return true;
    } else {
        $('body').removeClass('touch-screen');
        return false;
    }
}