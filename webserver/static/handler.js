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
        var action = {"button":"player"};
        // Send the variable
        $.ajax({
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            url: '/_post_data',
            dataType : 'json',
            data : JSON.stringify(action),
            success : function(result) {
                // Change the symbols depending on the status
                $("#player").text( ((result['data'][0]['playing'] == true) ? "pause":"play_arrow") );
                console.log('Well received signal'); 
            },error : function(result){
                console.log(result);
            }
        });
    });

    /**
     * Click on the next or previous song
     */
    $("#prev, #next").click(function(){
        // Create a JSON file that will be sent to
        // the server indicating which button
        // has been clicked
        if($(this).attr("id") == "prev"){
            var simb = "prev";
        } else{
            var simb = "next";
        }
        var action = {"button":simb};
        // Send the variable
        $.ajax({
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            url: '/_post_data',
            dataType : 'json',
            data : JSON.stringify(action),
            success : function(result) {
                changeSong(result['data']);
                console.log('Well received signal'); 
            },error : function(result){
                console.log(result);
            }
        });
    });

    /**
     * Select a new song by the list
     */
    $(".music .song").click(function(){
        var action = {
            "button":"new_song",
            "song":$(".info",this).attr("id")
        };
        console.log(action);
        // Send the variable
        $.ajax({
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            url: '/_post_data',
            dataType : 'json',
            data : JSON.stringify(action),
            success : function(result) {
                changeSong(result['data']);
                console.log('Well received signal'); 
            },error : function(result){
                console.log(result);
            }
        });
    });

    /**
     * Change the visual information of the current song.
     * @param {dict} result : data that the server has returned. It contains
     * the information about the new song that is playing
     */
    function changeSong(result){
        var current_song = result[0]['current_song'];
        if ( ($(".main_cover").attr("id")) != current_song ){
            // New song, new ID
            $(".main_cover").attr("id",current_song)
            // Change the image
            $(".main_cover").attr("style", newCover(current_song, true));
            // Change the title of the song
            $(".player-ui .title h3").text(result[1][current_song]['title'])
            // Change the artist of the song
            $(".player-ui .small p").text(result[1][current_song]['artist'])
            $("#player").text("pause");
        }
    }

    /**
     * Get the new cover
     * @param {int} index : which cover it's going to be used
     * @param {bool} main_cover : if the change is for the current song or not. It will
     * be always true in our app
     */
    function newCover(index, main_cover){
        var new_cover_style = "";
        if (main_cover == true){
            new_cover_style = (
                "background: linear-gradient(rgba(0, 0, 0, 0.3), " + 
                "rgba(0, 0, 0, 0.4)), url('static/covers/"+ index + ".jpg') center bottom;\n" +
                "background-size: cover;"
            );
        } else{
			new_cover_style = (
                "background: url('static/covers/{{ i }}.jpg') center center;\n" +
                "background-size: cover;"
            );
        }
        return new_cover_style;
    }
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