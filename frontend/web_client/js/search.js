$(function () {
	document.getElementById("searchButton").addEventListener("click", discover);
})

function discover() {
	var dayAmount = document.getElementById("Days").value
	var e = document.getElementById("resultsSelect");
	var selectedResult = e.options[e.selectedIndex].text;
	var f = document.getElementById("modeSelect");
	var selectedMode = f.options[f.selectedIndex].text;

	if (selectedResult == 'Top 3') {
		selectedResult = 3;
	} else {
		selectedResult = 5;
	}

	if (selectedMode == 'Hottest') {
		selectedMode = "hot"
	} else {
		selectedMode = "cold"
	}

	var postRequest = {
		'temp': selectedMode,
		'days': dayAmount,
		'count': selectedResult,
		'static': 'false'
	}

	var xhr_discover = new XMLHttpRequest();
	xhr_discover.open("POST", 'http://student04.cse.nd.edu:52109/crypto/', true);
	xhr_discover.onload = function (e) {
		responseDict = JSON.parse(xhr_discover.responseText);
		if (responseDict['result'] == 'success') {
			// give success message
			populate(responseDict['crypto'])
		} else {
			var sContainer = document.getElementById("searchContainer");
			createNotification("danger", sContainer, "Days must be a populated field between 1 and 2000.");
		}
	}
	xhr_discover.send(JSON.stringify(postRequest));
	if (document.getElementById("tableSpot")) {
		var tableSpot = document.getElementById("tableSpot");
		tableSpot.parentNode.removeChild(tableSpot);
	}
}

function populate(crypto_data) {
	var newTableElement = `<table class="table table-hover" id="tableSpot">
		<thead>
			<tr class="table-active">
				<th scope="col">Results:</th>
				<th scope="col"></th>
				<th scope="col"></th>
				<th scope="col"></th>
			</tr>
		</thead>`
	var i = 0;
	for (var a = 0; a < crypto_data.length; a++) {
		i += 1;
		var val = Number(crypto_data[a][1].substring(0, crypto_data[a][1].length - 1));
		if (val >= 0) {
			newTableElement += `<tbody>
			<tr class="table-success">
				<th scope="row">` + i + `.</th>
				<td>` + crypto_data[a][0] + `</td>
				<td>` + "$" + crypto_data[a][2] + `</td>
				<td>` + crypto_data[a][1] + `</td>
			</tr>
		</tbody>`;
		} else {
			newTableElement += `<tbody>
			<tr class="table-danger">
				<th scope="row">` + i + `.</th>
				<td>` + crypto_data[a][0] + `</td>
				<td>` + "$" + crypto_data[a][2] + `</td>
				<td>` + crypto_data[a][1] + `</td>
			</tr>
		</tbody>`;
		}
	}
	newTableElement += `
	</table>`;
	document.getElementById("searchResults").insertAdjacentHTML('beforeend', newTableElement);
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