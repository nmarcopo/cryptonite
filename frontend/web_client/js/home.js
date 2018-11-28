// Runs when page is loaded.
$(document).ready(function () {
    $("#modalInsert").load("res/modalLoginError.html", function () {
        // Present an error if user is not logged in.
        if (sessionStorage.getItem("cryptoniteLogIn") != "true") {
            $("#logInErrorModal").modal("show");
        }
        $("#signOutButton").click(function () {
            sessionStorage.setItem("cryptoniteLogIn", "false");
            console.log("signed out");
        });
    });
})