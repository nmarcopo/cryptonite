$(function () {
    document.getElementById("searchButton").addEventListener("click", discover);
})

function discover() {
    var dayAmount = document.getElementById("Days").value
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

    console.log(selectedResult)
    console.log(selectedMode)

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
        console.log(xhr_discover.responseText);
        console.log(responseDict)
        if (responseDict['result'] == 'success') {
            // give success message
            console.log("success");
            console.log(responseDict)
        } 
        else {
            console.log('failure');
        }
    }
    xhr_discover.send(JSON.stringify(postRequest));
}