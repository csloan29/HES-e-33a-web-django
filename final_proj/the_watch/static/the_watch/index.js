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

});