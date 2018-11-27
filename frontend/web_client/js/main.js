// Set up files with NavBar and Modal Inserts
$(function () {
    var path = window.location.pathname;
    var page = path.split("/").pop();
    var pageName = page.split(".")[0];
    $("#navBarInsert").load("res/nav.html", function () {
        // Add active li to navbar
        jQuery("#" + pageName).addClass("active");
        // you can hide top bar elements if the user isn't signed in.
        //jQuery("#home").addClass("d-none");
    });
});