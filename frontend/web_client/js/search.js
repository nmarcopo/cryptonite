// on load function
$(function () {
	// search button connection
	document.getElementById("searchButton").addEventListener("click", discover);
})

// funtion for the discover search button press
function discover() {
	// how many days
	var dayAmount = document.getElementById("Days").value
	
	// how many results
	var e = document.getElementById("resultsSelect");
	var selectedResult = e.options[e.selectedIndex].text;
	
	// which mode
	var f = document.getElementById("modeSelect");
	var selectedMode = f.options[f.selectedIndex].text;

	// selected text changes to the value of the number for the request
	if (selectedResult == 'Top 3') {
		selectedResult = 3;
	} else {
		selectedResult = 5;
	}

	// changes the selected text to correct text for the request
	if (selectedMode == 'Hottest') {
		selectedMode = "hot"
	} else {
		selectedMode = "cold"
	}

	// payload for request
	var postRequest = {
		'temp': selectedMode,
		'days': dayAmount,
		'count': selectedResult,
		'static': 'false'
	}

	// POST request
	var xhr_discover = new XMLHttpRequest();
	xhr_discover.open("POST", 'http://student04.cse.nd.edu:52109/crypto/', true);
	// function when post request is sent 
	xhr_discover.onload = function (e) {
		responseDict = JSON.parse(xhr_discover.responseText);
		// if request succeeds
		if (responseDict['result'] == 'success') {
			// calls function to populate search results
			populate(responseDict['crypto'])
		// if request fails
		} else {
			// Notification
			var sContainer = document.getElementById("searchContainer");
			createNotification("danger", sContainer, "Days must be a populated field between 1 and 2000.");
		}
	}
	// sends post request
	xhr_discover.send(JSON.stringify(postRequest));
	// removes previous search results if they exist
	if (document.getElementById("tableSpot")) {
		var tableSpot = document.getElementById("tableSpot");
		tableSpot.parentNode.removeChild(tableSpot);
	}
}

// function to populate search results
function populate(crypto_data) {
	// adds header of table to html file
	var newTableElement = `<table class="table table-hover" id="tableSpot">
		<thead>
			<tr class="table-active">
				<th scope="col">Results:</th>
				<th scope="col"></th>
				<th scope="col"></th>
				<th scope="col"></th>
			</tr>
		</thead>`
	// counter for search table
	var i = 0;
	for (var a = 0; a < crypto_data.length; a++) {
		i += 1;
		var val = Number(crypto_data[a][1].substring(0, crypto_data[a][1].length - 1));
		// if crypto went up, use green when adding html for table
		if (val >= 0) {
			newTableElement += `<tbody>
			<tr class="table-success">
				<th scope="row">` + i + `.</th>
				<td>` + crypto_data[a][0] + `</td>
				<td>` + "$" + crypto_data[a][2] + `</td>
				<td>` + crypto_data[a][1] + `</td>
			</tr>
		</tbody>`;
		// if crypto went down, use red when adding html for table
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
	// finish table in html
	newTableElement += `
	</table>`;
	// adds the html to the document
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
