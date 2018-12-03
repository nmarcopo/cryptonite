$(function () {
    document.getElementById("imagineAddButton").addEventListener("click", function () {
        var newTableElement = `<tr class="table-secondary">
        <th scope="row">
            <input type="number" min="1" class="form-control border imagineDaysInput" aria-label="Days">
        </th>
        <td>
            <select class="form-control border imagineCryptoInput" id="modeSelect">
                <option>BTC</option>
                <option>ETH</option>
                <option>XRP</option>
                <option>BCH</option>
                <option>EOS</option>
                <option>XLM</option>
                <option>LTC</option>
                <option>ADA</option>
                <option>XMR</option>
                <option>USDT</option>
                <option>TRX</option>
                <option>DASH</option>
                <option>IOTA</option>
                <option>BSV</option>
                <option>XEM</option>
            </select>
        </td>
        <td>
            <input type="number" min="0.00001" class="form-control border imagineAmountInput" aria-label="Amount">
        </td>
        <td>
            <button id="imagineRemoveButton" class="btn btn-warning" type="button">-</button>
        </td>
    </tr>`;
        document.getElementById("imagineTableBody").insertAdjacentHTML('beforeend', newTableElement);
    });
    $(document).on('click', '#imagineRemoveButton', function () {
        var tr = this.parentNode.parentNode;
        tr.parentNode.removeChild(tr);
    });
    document.getElementById("imagineSearchButton").addEventListener("click", sendImagineRequest);
});

function sendImagineRequest() {
    daysInput = document.getElementsByClassName("imagineDaysInput");
    cryptoInput = document.getElementsByClassName("imagineCryptoInput");
    amountInput = document.getElementsByClassName("imagineAmountInput");
    var loginContainer = document.getElementById("imagineTableCard");

    if (daysInput.length < 1) {
        createNotificationImagine("danger", loginContainer, "Oops! You don't have any existing imagines. Press the + button, fill one out, and try again.");
        return;
    }

    bigDict = {
        'static': 'false'
    }
    assetDict = [];
    for (let index = 0; index < daysInput.length; index++) {
        const dayObj = daysInput[index];
        const day = dayObj.value;
        const crypto = cryptoInput[index].value;
        const amount = amountInput[index].value;
        if (day == "" || crypto == "" || amount == "") {
            createNotificationImagine("danger", loginContainer, "Oops! You must have not filled in a value for one of your Imagine fields. Fill those in and try again.");
            return;
        }
        cryptoDict = {}
        cryptoDict[crypto] = [day, amount];
        assetDict.push(cryptoDict);
    }
    bigDict["asset"] = assetDict;

    // Send PUT request to get crypto information
    var xhr_putImagine = new XMLHttpRequest();
    xhr_putImagine.open("PUT", 'http://student04.cse.nd.edu:52109/crypto/whatif/', true);
    xhr_putImagine.onload = function (e) {
        responseDict = JSON.parse(xhr_putImagine.responseText);
        if (responseDict['result'] == 'success') {
            // give success message
            $("#imagineProgress").addClass("d-none");
            console.log(xhr_putImagine.responseText);
            createResponseVisuals(JSON.parse(xhr_putImagine.responseText), loginContainer);
        } else {
            // fails on server error
            $("#imagineProgress").addClass("d-none");
            console.log(xhr_putImagine.responseText);
            createNotificationImagine("danger", loginContainer, "Oh snap! Something went wrong, try again.");
        }
    }
    if (document.getElementById("totalMoneyCard")) {
        var moneyCard = document.getElementById("totalMoneyCard");
        moneyCard.parentNode.removeChild(moneyCard);
    }
    $("#imagineProgress").removeClass("d-none");
    console.log("this happened just before request sent");
    xhr_putImagine.send(JSON.stringify(bigDict));
    console.log("this happened after request sent");
    console.log(bigDict);
    // {'asset':[{'BTC':2, "XRP":100}]}
}

function createResponseVisuals(response, container) {
    var netProfit = Number(response["Net Profit"]);
    netProfit > 0 ? profLoss = "Profit" : profLoss = "Loss";
    netProfit > 0 ? madeLost = "made" : madeLost = "lost";
    netProfit > 0 ? joke = "Too bad you didn't actually invest!" : joke = "Thankfully, this is just a game!";
    var totalMoneyCard = `<div id=totalMoneyCard><canvas id="myChart" width="400" height="400"></canvas>
    <br><div class="d-flex justify-content-center"><div class="text-center">
<div class="card border-primary mb-3" style="max-width: 20rem;">
    <div class="card-header">Your Net ` + profLoss + `:</div>
        <div class="card-body">
            <h4 class="card-title">$` + netProfit + `</h4>
            <p class="card-text">You would have ` + madeLost + ' $' + netProfit + `! ` + joke + ` Check out our <a href=discover.html>Discover tool</a> for some wise investment advice for when you make a real investment</p>
        </div>
    </div>
</div>
</div>`
    container.insertAdjacentHTML('beforeend', totalMoneyCard);
    cryptos = []
    profitPercentage = []
    response["breakdown"].forEach(element => {
        cryptos.push(element['crypto'] + " " + element['days'] + " days");
        profitPercentage.push(Number(element['profit percentage']));
    });
    var ctx = document.getElementById("myChart").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        showTooltips: false,
        data: {
            labels: cryptos,
            datasets: [{
                label: 'Investment Results (By Percent Change of 1 Coin)',
                data: profitPercentage,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

// Function to create a notification pop up 
function createNotificationImagine(alertType, loginContainer, messageText) {
    var messageHTML = `<br><div class="alert alert-dismissible alert-${alertType}">
    <button type="button" class="close" data-dismiss="alert">&times;</button>
    ${messageText}
    </div>`;
    var message = document.createElement("div");
    message.innerHTML = messageHTML;
    loginContainer.appendChild(message);

    // Automatically delete the message after 5 seconds.
    var timeoutSecs = 4;
    setTimeout(() => {
        loginContainer.removeChild(message);
    }, timeoutSecs * 1000);
}