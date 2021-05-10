$(document).ready(function() {

    // ----------------------------------
    // Sidebar
    // ----------------------------------
    $("#sidebar-btn").on("click", function() {
        $("#sidebar").toggleClass("inactive");
        $(this).toggleClass("inactive");
    });

    // ----------------------------------
    // Searchbar
    // ----------------------------------
    $("#searchbar-bar").on("keypress", function(e) {
        // searchbar event listener for enter key
        if (e.which == 13) {
            $("form#searchbar-form").submit();
            return false;
        }
    });

    // ----------------------------------
    // Like Button
    // ----------------------------------
    $("#like-btn").on("click", function() {
        fetch("/toggle-like/" + video_id_js, {
            method: "POST",
        })
        .then(response=> response.json())
        .then(res => {
            console.log(res);
            //toggle state of like button
            if ($("#like-btn-text").text() == "Liked") {
                $("#like-btn-text").text("Like");
            } else{
                $("#like-btn-text").text("Liked");
            }
            $("#like-btn").toggleClass('btn-primary btn-danger');
            $("#like-btn-icon").toggleClass('bi-heart bi-heart-fill');
        });
    });

});

// ----------------------------------
// Add To Playlist Button
// ----------------------------------
function addToPlaylist(playlist_id) {
    fetch("/add-to-playlist/" + playlist_id + '/' + video_id_js, {
        method: "POST",
    })
    .then(response=> response.json())
    .then(res => {
        $("#video-alert-text").text(res.message);
        $('#playlist-alert').addClass('show');
        setTimeout(function(){
            $('#playlist-alert').removeClass('show');
            // hide alert after 3 seconds
          }, 3000);
    });
}