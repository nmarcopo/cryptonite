// Auto run when index.html Welcome page is loaded
$(function () {
    if (sessionStorage.getItem("cryptoniteLogIn") != null && sessionStorage.getItem("cryptoniteLogIn") != "null") {
        window.location.replace('home.html');
    }
    $("#modalInsert").load("res/modalSignUp.html", function () {
        document.getElementById("signUpSubmitButton").addEventListener("click", signUpSubmit);
        document.getElementById("logInSubmitButton").addEventListener("click", logInSubmit);
    });
})

// Support submit button for sign up
function signUpSubmit() {
    // Get nodes for inputs
    var uidNode = document.getElementById("inputEmailSignUp");
    var passNode = document.getElementById("inputPasswordSignUp");
    var passConfNode = document.getElementById("inputPasswordSignUpConfirm");
    // Get node of containing modal for appending messages to
    var loginContainer = uidNode.parentNode.parentNode;

    // Get the text that was typed in the inputs
    var uid = uidNode.value;
    var pass = passNode.value;
    var passConf = passConfNode.value;

    // Check if email field does not contain an email
    // regex source: https://stackoverflow.com/questions/46155/how-to-validate-an-email-address-in-javascript
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (!re.test(String(uid).toLowerCase())) {
        createNotification("danger", loginContainer, "Your email address is not valid. Please enter a valid email.");
        return;
    }

    // Check if passwords match
    if (pass == passConf && uid != "" && pass != "") {
        // Send POST request to create a new user
        var postRequest = {
            'user': uid,
            'pwd': pass
        }
        var xhr_putNewUser = new XMLHttpRequest();
        xhr_putNewUser.open("POST", '//marcopo.li:52109/users/', true);
        xhr_putNewUser.onload = function (e) {
            responseDict = JSON.parse(xhr_putNewUser.responseText);
            if (responseDict['result'] == 'success') {
                // give success message, make sure user can't immediately request another username
                uidNode.setAttribute("readonly", '""');
                passNode.setAttribute("readonly", '""');
                passConfNode.setAttribute("readonly", '""');
                createNotification("success", loginContainer, "Well Done! You successfully created an account. Please close this window.");
            } else {
                // fails when there is already an existing user
                createNotification("danger", loginContainer, "Oh snap! Username already exists. Try logging in, or creating a new user.");
            }
        }
        xhr_putNewUser.send(JSON.stringify(postRequest));
    } else {
        createNotification("danger", loginContainer, "Oh snap! Change a few things up and try submitting again.");
    }
}

// Handle login
function logInSubmit() {
    // put request to /users/, send json user, pwd
    // Get nodes for inputs
    var uidNode = document.getElementById("inputEmailLogIn");
    var passNode = document.getElementById("inputPasswordLogIn");
    // Get node of containing modal for appending messages to
    var loginContainer = uidNode.parentNode.parentNode;

    // Get the text that was typed in the inputs
    var uid = uidNode.value;
    var pass = passNode.value;

    // Check if email field does not contain an email
    // regex source: https://stackoverflow.com/questions/46155/how-to-validate-an-email-address-in-javascript
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (!re.test(String(uid).toLowerCase())) {
        createNotification("danger", loginContainer, "Your email address is not valid. Please enter a valid email.");
        return;
    }

    if (pass != "") {
        // Send request to login to server
        var putRequest = {
            'user': uid,
            'pwd': pass
        }
        var xhr_putNewUser = new XMLHttpRequest();
        xhr_putNewUser.open("PUT", '//marcopo.li:52109/users/', true);
        xhr_putNewUser.onload = function (e) {
            responseDict = JSON.parse(xhr_putNewUser.responseText);
            if (responseDict['result'] == 'success') {
                // give success message, make sure user can't immediately request another username
                uidNode.setAttribute("readonly", '""');
                passNode.setAttribute("readonly", '""');
                createNotification("success", loginContainer, "Well Done! You successfully logged in.");
                sessionStorage.setItem("cryptoniteLogIn", uid);
                setTimeout(() => {
                    window.location.replace('home.html');
                }, 1500);

            } else {
                // fails when there is already an existing user
                createNotification("danger", loginContainer, "Oh snap! Your information wasn't correct.");
            }
        }
        xhr_putNewUser.send(JSON.stringify(putRequest));
    } else {
        createNotification("danger", loginContainer, "Please enter a password.");
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