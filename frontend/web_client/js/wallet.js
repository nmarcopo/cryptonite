// onload function
$(function () {
	// Executes when use presses the - button on any of their crypto. 
	// Removes the list item and deletes the crypto from the user's database.
	$(document).on('click', '#removeButton', function () {
		var tr = this.parentNode.parentNode.parentNode;
		var currencyToDelete = tr.childNodes[1].innerText;
		currencyToDelete = currencyToDelete.substring(0, currencyToDelete.length - 1);
		// gets payload ready for request
		var putRequest = {
			"coin": currencyToDelete
		}
		var xhr_deleteCurrencyFromWallet = new XMLHttpRequest();
		// request to delete from wallet
		xhr_deleteCurrencyFromWallet.open("POST", 'http://student04.cse.nd.edu:52109/users/change/' + sessionStorage.getItem("cryptoniteLogIn"), true);
		xhr_deleteCurrencyFromWallet.onload = function (e) {
			responseDict = JSON.parse(xhr_deleteCurrencyFromWallet.responseText);
			// if it's removed from wallet, removes from HTML
			if (responseDict['result'] == 'success') {
				tr.parentNode.removeChild(tr);
			} 
			// else notify user
			else {
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

// function for add button
function addField() {
	// grabs fields for request
	var cryptoField = document.getElementById("cryptoInput").value.toUpperCase();
	var costField = document.getElementById("costInput").value;
	// wrong input
	console.log(Number(costField))
	if (Number(costField) < 0.01) {
		var nContainer = document.getElementById("notifContainer");
		createNotification("danger", nContainer, "Double check input fields. You need to add at least $0.01 of any crypto.");
		return;
	}
	// calculates the amount of bitcoins from how much money user put in
	var asset = {}
	// gets payload for POST request to add to user wallet
	asset[cryptoField] = costField;
	var postRequest = {
		'asset': asset
	}
	// POST request to add to user wallet
	var xhr_walletAdd = new XMLHttpRequest();
	var uid = sessionStorage.getItem("cryptoniteLogIn");
	xhr_walletAdd.open("POST", 'http://student04.cse.nd.edu:52109/users/' + uid, true);
	xhr_walletAdd.onload = function (f) {
		responseDict = JSON.parse(xhr_walletAdd.responseText);
		// if failure notify
		if (responseDict['result'] != 'success') {
			var nContainer = document.getElementById("notifContainer");
			createNotification("danger", nContainer, "Could not add to wallet.");
		}
		getWalletContents(sessionStorage.getItem("cryptoniteLogIn"));
	}
	xhr_walletAdd.send(JSON.stringify(postRequest));
}

// Get contents of user's wallet
function getWalletContents(uid) {
	var dynamicContainer = document.getElementById("dynamicallyAddCryptoToWallet");
	// removes previous wallet results in the HTML
	if (dynamicContainer.hasChildNodes()) {
		while (dynamicContainer.firstChild) {
			dynamicContainer.removeChild(dynamicContainer.firstChild);
		}
	}
	// request to get user's wallet
	var xhr_getWalletContents = new XMLHttpRequest();
	xhr_getWalletContents.open("GET", 'http://student04.cse.nd.edu:52109/users/' + uid, true);
	// function on request
	xhr_getWalletContents.onload = function (e) {
		responseDict = JSON.parse(xhr_getWalletContents.responseText);
		// if succeeds
		if (responseDict['result'] == 'success') {
			// give success message
			walletContentsResp = JSON.parse(xhr_getWalletContents.responseText);
			var container = document.getElementById("dynamicallyAddCryptoToWallet");
			if (!walletContentsResp.hasOwnProperty("wallet") || Object.keys(walletContentsResp["wallet"][0]).length == 0) {
				createNotification("info", container.parentNode.parentNode, "Looks like you haven't added anything to your wallet yet. Add some above!");
				return;
			}
			// changes wallet cryptos into list of just the cryptos
			walletArray = walletContentsResp["wallet"][0];
			var cryptoL = [];
			for (const [key, value] of Object.entries(walletArray)) {
				cryptoL.push(key);
			}
			var putRequest = {
				'crypto': cryptoL
			};
			var xhr_findPrice = new XMLHttpRequest();

			var cryptoToWallet = ``;
			// request to get price for each crypto in user's wallet
			xhr_findPrice.open("PUT", 'http://student04.cse.nd.edu:52109/crypto/', true);
			xhr_findPrice.onload = function (e) {
				responseDict = JSON.parse(xhr_findPrice.responseText);
				if (responseDict['result'] == 'success') {
					var amountDict = responseDict;
					delete amountDict['result'];
					// adds table entry to HTML for each crypto in wallet
					for (const [key, value] of Object.entries(walletArray)) {
						var dAmount = Number(value) * Number(amountDict[key])
						cryptoToWallet += `<tr class="table-active">
						<td>
							<span class="input-group-text" id="cryptoSymbol">` + key + `</span>
						</td>
						<td>
							<span class="input-group-text">` + "$" + amountDict[key].toFixed(2) + `</span>
						</td>
						<td>
							<span class="input-group-text">` + "$" + dAmount.toFixed(2) + `</span>
						</td>
						<td>
							<span class="input-group-text">` + Number(value).toFixed(2) + `</span>
						</td>
						<td>
							<div class="input-group-append">
								<button id="removeButton" class="btn btn-warning" type="button">-</button>
							</div>
						</td>
					</tr>`;
					}
					container.insertAdjacentHTML('beforeend', cryptoToWallet);
				}
			}
			xhr_findPrice.send(JSON.stringify(putRequest));

		} 
		// if fails
		else {
			var nContainer = document.getElementById("notifContainer");
			createNotification("danger", nContainer, "Error grabbing user's wallet.");
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
