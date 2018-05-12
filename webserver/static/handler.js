/**
 * Preloading screen
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
    $("#player").click(function(){
        // Create a JSON file that will be sent to
        // the server indicating the play arrow has been
        // clicked
        var action = [{"button":"player"}];
        // Send the variable
        $.ajax({
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            url: '/_post_data',
            dataType : 'json',
            data : JSON.stringify(action),
            success : function(result) {
                // Change the symbols depending on the status
                $("#player").text( ((result['data']['status'] == "playing") ? "pause":"play_arrow") );
                console.log('Well received signal'); 
            },error : function(result){
                console.log(result);
            }
        });
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