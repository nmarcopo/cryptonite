// Set up files with NavBar and Modal Inserts
$(function () {
    var path = window.location.pathname;
    var page = path.split("/").pop();
    var pageName = page.split(".")[0];
    $("#navBarInsert").load("res/nav.html", function () {
        // Add active li to navbar
        jQuery("#" + pageName).addClass("active");
        // hide top bar elements if the user isn't signed in.
        if (sessionStorage.getItem("cryptoniteLogIn") == null || sessionStorage.getItem("cryptoniteLogIn") == "null") {
            jQuery("#home").addClass("d-none");
            jQuery("#friends").addClass("d-none");
            jQuery("#about").addClass("d-none");
            jQuery("#signOut").addClass("d-none");
            jQuery("#settings").addClass("d-none");
            jQuery("#discover").addClass("d-none");
            jQuery("#imagine").addClass("d-none");
        } else {
            // hide sign up and login buttons if user is signed in
            jQuery("#signUp").addClass("d-none");
            jQuery("#logIn").addClass("d-none");
        }
    });
});