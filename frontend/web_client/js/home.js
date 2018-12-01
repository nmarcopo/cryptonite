// Runs when page is loaded.
$(document).ready(function () {
    $("#modalInsert").load("res/modalLoginError.html", function () {
        // Present an error if user is not logged in.
        console.log(sessionStorage.getItem("cryptoniteLogIn"));
        if (sessionStorage.getItem("cryptoniteLogIn") == null || sessionStorage.getItem("cryptoniteLogIn") == "null") {
            $("#logInErrorModal").modal("show");
        }
        $("#signOutButton").click(function () {
            sessionStorage.setItem("cryptoniteLogIn", null);
        });
    });
    $("#settingsInsert").load("res/modalSettings.html", function () {
        console.log("settings loaded");
    });
    $("#userNameText").html(sessionStorage.getItem("cryptoniteLogIn"));
})