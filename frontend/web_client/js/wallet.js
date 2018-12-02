$(function () {
    document.getElementById("removeButton").addEventListener("click", discover);
    document.getElementById("addButton").addEventListener("click", addField);
})

function addField(){
	var cryptoField = document.getElementById("cryptoInput").value;
	var costField = document.getElementById("costInput").value;
	var cryptoL = [cryptoField];
	var putRequest = {
		'crypto' : cryptoL
	};
	var xhr_findPrice = new XMLHttpRequest();
    
	xhr_findPrice.open("PUT", 'http://student04.cse.nd.edu:52109/crypto/', true);
    xhr_findPrice.onload = function (e) {
        responseDict = JSON.parse(xhr_findPrice.responseText);
        if (responseDict['result'] == 'success') {
			var cryptoPrice = responseDict[cryptoField];
			var amount = Number(costField)/Number(cryptoPrice);
			console.log(cryptoField);
			console.log(amount);
			var asset = {}
			asset[cryptoField] = amount;
			var postRequest = {
				'asset':asset
			}
			var xhr_walletAdd = new XMLHttpRequest();
			var uid = sessionStorage.getItem("cryptoniteLogIn");
			console.log(uid);
			xhr_walletAdd.open("POST", 'http://student04.cse.nd.edu:52109/users/'+uid,true);
			xhr_walletAdd.onload = function (f) {
				responseDict = JSON.parse(xhr_walletAdd.responseText);
				console.log(responseDict['result']);
				if (responseDict['result'] != 'success'){
        			var nContainer = document.getElementById("notifContainer");
					createNotification("danger",nContainer,"Could not add to wallet.");
				}
			}
			xhr_walletAdd.send(JSON.stringify(postRequest));
		} 
        else {
        	var nContainer = document.getElementById("notifContainer");
			createNotification("danger",nContainer,"Double check input fields.");
		}
    }
    xhr_findPrice.send(JSON.stringify(putRequest));


}

function discover() {
    var dayAmount = document.getElementById("Days").value;
    var e = document.getElementById("resultsSelect");
    var selectedResult = e.options[e.selectedIndex].text;
    var f = document.getElementById("modeSelect");
    var selectedMode = f.options[f.selectedIndex].text;
    
    if(selectedResult == 'Top 3'){
        selectedResult = 3;
    }
    else{
        selectedResult = 5;
    }

    if(selectedMode == 'Hottest'){
        selectedMode = 'hot'
    }
    else{
        selectedMode = 'cold'
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
        	populate(responseDict["crypto"])	
		} 
        else {
        	var sContainer = document.getElementById("searchContainer");
			createNotification("danger",sContainer,"Days must be a populated field.");
		}
    }
    xhr_discover.send(JSON.stringify(postRequest));
	if(document.getElementById("tableSpot")){
		var tableSpot = document.getElementById("tableSpot");
		tableSpot.parentNode.removeChild(tableSpot);
	}
}

function populate(crypto_data){
	var newTableElement = `<table class="table table-hover" id="tableSpot">
		<thead>
			<tr class="table-active">
				<th scope="col">Results:</th>
				<th scope="col"></th>
				<th scope="col"></th>
			</tr>
		</thead>`
	var i = 0;
	for (const [key, value] of Object.entries(crypto_data)) {
	  i += 1;
	  var val = Number(value.substring(0, value.length -1));
	  if(val >= 0){
	  	newTableElement += `<tbody>
			<tr class="table-success">
				<th scope="row">`+i+`.</th>
				<td>`+key+`</td>
				<td>`+value+`</td>
			</tr>
		</tbody>`;
	  }
	  else{
	  	newTableElement += `<tbody>
			<tr class="table-danger">
				<th scope="row">`+i+`.</th>
				<td>`+key+`</td>
				<td>`+value+`</td>
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
