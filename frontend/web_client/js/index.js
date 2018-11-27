// Support submit button for login
function signUpSubmit() {
    var uidNode = document.getElementById("inputEmailSignUp");
    var passNode = document.getElementById("inputPasswordSignUp");
    var passConfNode = document.getElementById("inputPasswordSignUpConfirm");
    var loginContainer = uidNode.parentNode.parentNode;

    var uid = uidNode.value;
    var pass = passNode.value;
    var passConf = passConfNode.value;

    if (pass == passConf) {
        var putRequest = {
            'user': uid,
            'pwd': pass
        }
        var xhr_putNewUser = new XMLHttpRequest();
        xhr_putNewUser.open("POST", 'http://student04.cse.nd.edu:52109/users/');
        xhr_putNewUser.onload = function (e) {
            responseDict = JSON.parse(xhr_putNewUser.responseText);
            console.log(xhr_putNewUser.responseText);
            if (responseDict['result'] == 'success') {
                // give success message, make sure user can't immediately request another username
                console.log("success");
                uidNode.setAttribute("readonly", '""');
                passNode.setAttribute("readonly", '""');
                passConfNode.setAttribute("readonly", '""');
                createNotification("green", loginContainer);
            } else {
                // do something else
                console.log('failure');
                createNotification("red", loginContainer);
            }
        }
        xhr_putNewUser.send(JSON.stringify(putRequest));
    } else {
        createNotification("red", loginContainer);
    }
}
$(function () {
    $("#modalInsert").load("res/modalSignUp.html", function () {
        document.getElementById("signUpSubmitButton").addEventListener("click", signUpSubmit);
    });
})

function createNotification(color, loginContainer) {
    var messageHTML;
    if (color == "red") {
        messageHTML = `<div class="alert alert-dismissible alert-danger">
        <button type="button" class="close" data-dismiss="alert">&times;</button>
        <strong>Oh snap!</strong> Change a few things up and try submitting again.
        </div>`
    } else if (color == "green") {
        messageHTML = `<div class="alert alert-dismissible alert-success">
        <button type="button" class="close" data-dismiss="alert">&times;</button>
        <strong>Well done!</strong> You successfully read this important alert message.
        </div>`
    }

    var message = document.createElement("div");
    message.innerHTML = messageHTML;
    loginContainer.appendChild(message);
    setTimeout(() => {
        loginContainer.removeChild(message);
    }, 5000);
}