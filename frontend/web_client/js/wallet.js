$(function () {
	// Executes when use presses the - button on any of their crypto. 
	// Removes the list item and deletes the crypto from the user's database.
	$(document).on('click', '#removeButton', function () {
		var tr = this.parentNode.parentNode.parentNode;
		var currencyToDelete = tr.childNodes[1].innerText;
		currencyToDelete = currencyToDelete.substring(0, currencyToDelete.length - 1);
		var putRequest = {
			"coin": currencyToDelete
		}
		var xhr_deleteCurrencyFromWallet = new XMLHttpRequest();

		xhr_deleteCurrencyFromWallet.open("POST", 'http://student04.cse.nd.edu:52109/users/change/' + sessionStorage.getItem("cryptoniteLogIn"), true);
		xhr_deleteCurrencyFromWallet.onload = function (e) {
			responseDict = JSON.parse(xhr_deleteCurrencyFromWallet.responseText);
			if (responseDict['result'] == 'success') {
				tr.parentNode.removeChild(tr);
			} else {
				var nContainer = document.getElementById("notifContainer");
				createNotification("danger", nContainer, "Oops! Looks like the currency didn't delete properly. Try again.");
			}
		}
		xhr_deleteCurrencyFromWallet.send(JSON.stringify(putRequest));
	});

	// Executes when user presses the + button to add a crypto
	document.getElementById("addButton").addEventListener("click", addField);

	// Executes on page load - gets the user's wallet contents and displays them.
	getWalletContents(sessionStorage.getItem("cryptoniteLogIn"));
})

function addField() {
	var cryptoField = document.getElementById("cryptoInput").value.toUpperCase();
	var costField = document.getElementById("costInput").value;
	if (Number(costField) < 0.01) {
		var nContainer = document.getElementById("notifContainer");
		createNotification("danger", nContainer, "Double check input fields. You need to add at least $0.01 of any crypto.");
		return;
	}
	var cryptoL = [cryptoField];
	var putRequest = {
		'crypto': cryptoL
	};
	var xhr_findPrice = new XMLHttpRequest();

	xhr_findPrice.open("PUT", 'http://student04.cse.nd.edu:52109/crypto/', true);
	xhr_findPrice.onload = function (e) {
		responseDict = JSON.parse(xhr_findPrice.responseText);
		if (responseDict['result'] == 'success') {
			var cryptoPrice = responseDict[cryptoField];
			var amount = Number(costField) / Number(cryptoPrice);
			console.log(cryptoField);
			console.log(amount);
			var asset = {}
			asset[cryptoField] = amount;
			var postRequest = {
				'asset': asset
			}
			var xhr_walletAdd = new XMLHttpRequest();
			var uid = sessionStorage.getItem("cryptoniteLogIn");
			console.log(uid);
			xhr_walletAdd.open("POST", 'http://student04.cse.nd.edu:52109/users/' + uid, true);
			xhr_walletAdd.onload = function (f) {
				responseDict = JSON.parse(xhr_walletAdd.responseText);
				console.log(responseDict['result']);
				if (responseDict['result'] != 'success') {
					var nContainer = document.getElementById("notifContainer");
					createNotification("danger", nContainer, "Could not add to wallet.");
				}
				getWalletContents(sessionStorage.getItem("cryptoniteLogIn"));
			}
			xhr_walletAdd.send(JSON.stringify(postRequest));
		} else {
			var nContainer = document.getElementById("notifContainer");
			createNotification("danger", nContainer, "Double check input fields.");
		}
	}
	xhr_findPrice.send(JSON.stringify(putRequest));


}

// Get contents of user's wallet
function getWalletContents(uid) {
	var dynamicContainer = document.getElementById("dynamicallyAddCryptoToWallet");
	if (dynamicContainer.hasChildNodes()) {
		while (dynamicContainer.firstChild) {
			dynamicContainer.removeChild(dynamicContainer.firstChild);
		}
	}
	var xhr_getWalletContents = new XMLHttpRequest();
	xhr_getWalletContents.open("GET", 'http://student04.cse.nd.edu:52109/users/' + uid, true);
	xhr_getWalletContents.onload = function (e) {
		responseDict = JSON.parse(xhr_getWalletContents.responseText);
		if (responseDict['result'] == 'success') {
			// give success message
			console.log(xhr_getWalletContents.responseText);
			walletContentsResp = JSON.parse(xhr_getWalletContents.responseText);
			var container = document.getElementById("dynamicallyAddCryptoToWallet");

			console.log("does the wallet exist: " + walletContentsResp.hasOwnProperty("wallet"));
			if (!walletContentsResp.hasOwnProperty("wallet") || Object.keys(walletContentsResp["wallet"][0]).length == 0) {
				createNotification("info", container.parentNode.parentNode, "Looks like you haven't added anything to your wallet yet. Add some above!");
				return;
			}

			walletArray = walletContentsResp["wallet"][0];
			var cryptoL = [];
			for (const [key, value] of Object.entries(walletArray)) {
				cryptoL.push(key);
			}
			var putRequest = {
				'crypto': cryptoL
			};
			console.log(cryptoL)
			var xhr_findPrice = new XMLHttpRequest();

			var cryptoToWallet = ``;
			xhr_findPrice.open("PUT", 'http://student04.cse.nd.edu:52109/crypto/', true);
			xhr_findPrice.onload = function (e) {
				responseDict = JSON.parse(xhr_findPrice.responseText);
				if (responseDict['result'] == 'success') {
					var amountDict = responseDict;
					delete amountDict['result'];
					console.log(amountDict)
					for (const [key, value] of Object.entries(walletArray)) {
						var dAmount = Number(value) * Number(amountDict[key])
						cryptoToWallet += `<tr class="table-active">
						<td>
							<span class="input-group-text" id="cryptoSymbol">` + key + `</span>
						</td>
						<td>
							<span class="input-group-text">` + "$" + dAmount.toFixed(2) + `</span>
						</td>
						<td>
							<div class="input-group-append">
								<button id="removeButton" class="btn btn-warning" type="button">-</button>
							</div>
						</td>
					</tr>`;
					}
					container.insertAdjacentHTML('beforeend', cryptoToWallet);
				} else {
					// var nContainer = document.getElementById("notifContainer");
					// createNotification("danger", nContainer, "Double check input fields.");
					console.log("fail");
				}
			}
			xhr_findPrice.send(JSON.stringify(putRequest));

		} else {
			var nContainer = document.getElementById("notifContainer");
			createNotification("danger", nContainer, "Days must be a populated field.");
		}
	}
	xhr_getWalletContents.send(null);
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