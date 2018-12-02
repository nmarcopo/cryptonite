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
            <input type="number" min="0" class="form-control border imagineAmountInput" aria-label="Amount">
        </td>
        <td>
            <button id="imagineRemoveButton" class="btn btn-warning" type="button">-</button>
        </td>
    </tr>`;
        document.getElementById("imagineTableBody").insertAdjacentHTML('beforeend', newTableElement);
    });
    $(document).on('click','#imagineRemoveButton',function(){
        var tr = this.parentNode.parentNode;
        tr.parentNode.removeChild(tr);
    });
    document.getElementById("imagineSearchButton").addEventListener("click", sendImagineRequest);
});

function sendImagineRequest(){
    console.log("yo");
    console.log(document.getElementsByClassName("imagineDaysInput"));
    console.log(document.getElementsByClassName("imagineCryptoInput"));
    console.log(document.getElementsByClassName("imagineAmountInput"));
}