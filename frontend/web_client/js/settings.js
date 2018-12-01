$(function () {
    console.log("function loaded");
    document.getElementById("submitEmailChangeButton").addEventListener("click", changeEmail);
});

function changeEmail() {
    var currentEmail = sessionStorage.getItem("cryptoniteLogIn");
    var newEmail = document.getElementById("inputChangeEmailNew").value;
    var newEmailConf = document.getElementById("inputChangeEmailNewConf").value;
    var password = document.getElementById("inputChangeEmailPass").value;
    var loginContainer = document.getElementById("changeEmailForm");
    
    // Check if email field does not contain an email
    // regex source: https://stackoverflow.com/questions/46155/how-to-validate-an-email-address-in-javascript
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (!re.test(String(newEmail).toLowerCase())) {
        createNotification("danger", loginContainer, "Your email address is not valid. Please enter a valid email.");
        return;
    }

    // Check if new emails match
    if (newEmail == newEmailConf && newEmail != "" && newEmailConf != "") {
        // Send POST request to create a new user
        var postRequest = {
            'user': currentEmail,
            'pwd': password,
            'new_user' : newEmail
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
                createNotification("danger", loginContainer, "Oh snap! Thats current username isn't quite right. Try logging in, or creating a new user.");
            }
        }
        xhr_putNewUser.send(JSON.stringify(postRequest));
    } else {
        createNotification("danger", loginContainer, "Oh snap! Change a few things up and try submitting again.");
    }
}

function changePassword() {
    var currentEmail = sessionStorage.getItem("cryptoniteLogIn");
    var newEmail = document.getElementById("inputChangeEmailNew").value;
    var newEmailConf = document.getElementById("inputChangeEmailNewConf").value;
    var password = document.getElementById("inputChangeEmailPass").value;
    var loginContainer = document.getElementById("changeEmailForm");
    
    // Check if email field does not contain an email
    // regex source: https://stackoverflow.com/questions/46155/how-to-validate-an-email-address-in-javascript
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (!re.test(String(newEmail).toLowerCase())) {
        createNotification("danger", loginContainer, "Your email address is not valid. Please enter a valid email.");
        return;
    }

    // Check if new emails match
    if (newEmail == newEmailConf && newEmail != "" && newEmailConf != "") {
        // Send POST request to create a new user
        var postRequest = {
            'user': currentEmail,
            'pwd': password,
            'new_user' : newEmail
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
                createNotification("danger", loginContainer, "Oh snap! Thats current username isn't quite right. Try logging in, or creating a new user.");
            }
        }
        xhr_putNewUser.send(JSON.stringify(postRequest));
    } else {
        createNotification("danger", loginContainer, "Oh snap! Change a few things up and try submitting again.");
    }
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
    var timeoutSecs = 5
    setTimeout(() => {
        loginContainer.removeChild(message);
    }, timeoutSecs * 1000);
}