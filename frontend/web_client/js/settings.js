$(function () {
    console.log("function loaded");
    document.getElementById("submitEmailChangeButton").addEventListener("click", changeEmail);
    document.getElementById("submitPasswordChangeButton").addEventListener("click", changePassword);
    document.getElementById("deleteUser").addEventListener("click", deleteUser);
});

function changeEmail() {
    var currentEmail = sessionStorage.getItem("cryptoniteLogIn");
    var newEmail = document.getElementById("inputChangeEmailNew").value;
    var newEmailConf = document.getElementById("inputChangeEmailNewConf").value;
    var passwd = document.getElementById("inputChangeEmailPass").value;
    var loginContainer = document.getElementById("changeEmailForm");

    // Check if email field does not contain an email
    // regex source: https://stackoverflow.com/questions/46155/how-to-validate-an-email-address-in-javascript
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (!re.test(String(newEmail).toLowerCase())) {
        createNotification("danger", loginContainer, "Your email address is not valid. Please enter a valid email.");
        return;
    }

    // Check if new emails match
    if (newEmail == newEmailConf && newEmail != "" && newEmailConf != "" && currentEmail != "") {
        // Send POST request to create a new user
        var postRequest = {
            'user': currentEmail,
            'pwd': passwd,
            'new_user': newEmail
        }
        var xhr_putNewUser = new XMLHttpRequest();
        xhr_putNewUser.open("PUT", 'http://student04.cse.nd.edu:52109/users/change/', true);
        xhr_putNewUser.onload = function (e) {
            responseDict = JSON.parse(xhr_putNewUser.responseText);
            console.log(xhr_putNewUser.responseText);
            if (responseDict['result'] == 'success') {
                // give success message
                console.log("success");
                console.log(xhr_putNewUser.responseText);

                createNotification("success", loginContainer, "Well Done! You successfully changed your email address to " + newEmail + ". ");
                sessionStorage.setItem("cryptoniteLogIn", newEmail);
            } else {
                // fails when there is already an existing user
                console.log('failure');
                createNotification("danger", loginContainer, "Oh snap! That current username isn't quite right. Try logging in, or creating a new user.");
            }
        }
        xhr_putNewUser.send(JSON.stringify(postRequest));
    } else {
        createNotification("danger", loginContainer, "Oh snap! Change a few things up and try submitting again.");
    }
}

function changePassword() {
    var currentEmail = sessionStorage.getItem("cryptoniteLogIn");
    var currentPassword = document.getElementById("inputChangePasswordCurrent").value;
    var newPassword = document.getElementById("inputChangePasswordNew").value;
    var newPasswordConf = document.getElementById("inputChangePasswordNewConf").value;
    var loginContainer = document.getElementById("changePasswordForm");

    // Check if new emails match
    if (newPassword == newPasswordConf && newPassword != "" && (currentEmail != null || currentEmail != "null")) {
        console.log(currentEmail);

        // Send POST request to create a new user
        var putRequest = {
            'pwd': currentPassword,
            'new_pwd': newPassword
        }
        var xhr_putNewUser = new XMLHttpRequest();
        xhr_putNewUser.open("PUT", 'http://student04.cse.nd.edu:52109/users/' + currentEmail, true);
        xhr_putNewUser.onload = function (e) {
            responseDict = JSON.parse(xhr_putNewUser.responseText);
            console.log(xhr_putNewUser.responseText);
            if (responseDict['result'] == 'success') {
                // give success message
                console.log("success");
                console.log(xhr_putNewUser.responseText);

                createNotification("success", loginContainer, "Well Done! You successfully changed your password");
            } else {
                // fails when there is already an existing user
                console.log('failure');
                createNotification("danger", loginContainer, "Oh snap! Something went wrong, try again.");
            }
        }
        xhr_putNewUser.send(JSON.stringify(putRequest));
    } else {
        createNotification("danger", loginContainer, "Oh snap! Change a few things up and try submitting again.");
    }
}

function deleteUser() {
    $("#settingsModal").modal("hide");
    $("#confirmDeleteUser").modal("show");
    $("#confirmDeleteAccountButton").click(function () {
        var currentEmail = sessionStorage.getItem("cryptoniteLogIn");
        var passwd = document.getElementById("passwordDeleteUser").value;
        var passwdConf = document.getElementById("passwordDeleteUserConfirm").value;
        var loginContainer = document.getElementById("deleteConfContent");
        if (passwd == passwdConf && (currentEmail != null && currentEmail != "null")) {
            // Send PUT request to delete account
            var putRequest = {
                'pwd': passwd
            }
            var xhr_putNewUser = new XMLHttpRequest();
            xhr_putNewUser.open("PUT", 'http://student04.cse.nd.edu:52109/users/change/' + currentEmail, true);
            xhr_putNewUser.onload = function (e) {
                responseDict = JSON.parse(xhr_putNewUser.responseText);
                console.log(xhr_putNewUser.responseText);
                if (responseDict['result'] == 'success') {
                    // give success message
                    console.log("success");
                    console.log(xhr_putNewUser.responseText);
                    createNotification("success", loginContainer, "You successfully deleted your account. Now returning to our login screen.");
                    sessionStorage.setItem("cryptoniteLogIn", null);
                    setTimeout(() => {
                        window.location.replace("index.html");
                    }, 4000);
                } else {
                    // fails when there is already an existing user
                    console.log('failure');
                    createNotification("danger", loginContainer, "Oh snap! Something went wrong, try again.");
                }
            }
            xhr_putNewUser.send(JSON.stringify(putRequest));
        } else {
            createNotification("danger", loginContainer, "Oh snap! Your passwords might not match, or you may need to log out and back in.");
        }
    });
}

// Function to create a notification pop up 
function createNotification(alertType, loginContainer, messageText) {
    var messageHTML = `<div class="alert alert-dismissible alert-${alertType}">
    <button type="button" class="close" data-dismiss="alert">&times;</button>
    ${messageText}
    </div>`;
    var message = document.createElement("div");
    message.innerHTML = messageHTML;
    loginContainer.appendChild(message);

    // Automatically delete the message after 5 seconds.
    var timeoutSecs = 8;
    setTimeout(() => {
        loginContainer.removeChild(message);
    }, timeoutSecs * 1000);
}