try {
    var tradeSocket = new WebSocket('ws://' + window.location.host + '/ws/trade/');
}
catch (e) {
    var tradeSocket = new WebSocket('wss://' + window.location.host + '/ws/trade/');
}
try {
    var tradeListSocket = new WebSocket('ws://' + window.location.host + '/ws/trade/prices/');
}
catch (e) {
    var tradeListSocket = new WebSocket('wss://' + window.location.host + '/ws/trade/prices/');
}
var main_url = window.location.origin;
var usdtValue = 0;
var pairValue = 0;
var pairUsdtValue = 0;
var sellEquivalent = null;

if(user != 'AnonymousUser'){
    var uValue = document.getElementById('uValue');
    var pValue = document.getElementById('pValue');
    var limit_buy_price = document.getElementById('limit-buy-price');
    var limit_buy_amount = document.getElementById('limit-buy-amount');
    var limit_sell_price = document.getElementById('limit-sell-price');
    var limit_sell_amount = document.getElementById('limit-sell-amount');
    
    uValue.value = 0;
    pValue.value = 0;
    limit_buy_price.value = 0;
    limit_buy_amount.value = 0;
    limit_sell_price.value = 0;
    limit_sell_amount.value = 0;
}

var globPair = pair.split('-')[0];
var createdHistory = [];
var createdOpenOrders = [];
var createdClosedOrders = [];
var createdRecentTrades = [];
var activeAlerts = [];

function tradeSocketOpen() {
    tradeSocket.send(JSON.stringify({'header': 'attribs', 'current_pair': pair, 'page': 'trade'}));
    removeRecentTrades();
    removeHistory();
    removeOpenOrders();
    removeClosedOrders();
}

tradeSocket.onopen = () => {
    tradeSocketOpen()
}

function tradeSocketMessage(e) {
    data = JSON.parse(e.data);
    // console.log(data)
    Object.keys(data).forEach(function(index){
        obj = data[index]
        // console.log(obj)
        header = obj['header']

        if((header == 'trade_response' || header == 'limit_response') && user != 'AnonymousUser'){
            state = obj['state'];
            
            if(state == -1){
                createAlert('danger', obj['message'])
            }
            else if(state == 0){
                if(header == 'trade_response'){
                    createAlert('success', 'Order filled!')
                    uValue.value = 0;
                    pValue.value = 0;
                }else{
                    createAlert('success', 'Order added!');
                    limit_buy_price.value = 0;
                    limit_buy_amount.value = 0;
                    limit_sell_price.value = 0;
                    limit_sell_amount.value = 0;
                }
                
            }else{
                createAlert('danger', 'Insufficient balance!')
            }
        }  
        else if((header=='hist_response' || header=='orders_response') && user!='AnonymousUser'){
            getHistory(obj, header);
        }
        else if(header == 'recent_response'){
            if(obj['pair'] == pair){
                recentTrades(obj);
            }           
        }
        else if(header == 'portfo_response' && user != 'AnonymousUser'){
            getPortfolio(obj);
        }

    })
    try {
        if(document.getElementById('open-limit-orders').childElementCount > 0){
            document.querySelector('.no-data').style.display = 'none';
        }
    }
    catch (e) {}  
}

tradeSocket.onmessage = e => {
    tradeSocketMessage(e)
}

function tradeSocketClose() {
    // createAlert('danger', 'There is a connection issue, please try again!');
}

tradeSocket.onclose = function(e){
    tradeSocketClose(e)
}

function tradeListSocketOpen(e, status) {
    console.log('prices socket is on!!');
    tradeListSocket.send(JSON.stringify({"page": 0, RequestType : 'trade'}));
    
    if (!status) {
        createPricePanel();
    }
}

tradeListSocket.onopen = function (e) {
    tradeListSocketOpen(e, false)
};

function tradeListSocketMessage(e) {

    var message = e.data;
    data = JSON.parse(message)
    priceList(data);
}

tradeListSocket.onmessage = function(e) {
    tradeListSocketMessage(e)
};

function tradeListSocketClose() {

    console.log('Socket closed unexpectedly');
}

tradeListSocket.onclose = function(e) {
    tradeListSocketClose()
};

function getPortfolio(res) {
    var pair = res['cryptoName']
    var usdtAmount = document.getElementById('usdtAmount');
    var pairAmount = document.getElementById('pairAmount');
    
    var usdtAmountLimit = document.getElementById('usdtAmountLimit');
    var pairAmountLimit = document.getElementById('pairAmountLimit');
    
    pairAmount.innerText = `0 ${pair}`
    pairAmountLimit.innerText = `0 ${pair}`
    

    if (res['cryptoName'] == 'USDT') {
        usdtAmount.innerText = `${res['amount'].toFixed(1)} USDT`
        usdtAmountLimit.innerText = `${res['amount'].toFixed(1)} USDT`
        usdtValue = res['amount'].toFixed(1)
    }
    else{
        var amount = res['amount']
        var equivalentAmount = res['equivalentAmount']

        if (amount >= 1) {
            amount = amount.toFixed(1)
        }
        else {
            amount = amount.toFixed(6)
        }

        if (equivalentAmount >= 1) {
            equivalentAmount = equivalentAmount.toFixed(1)
        }
        else {
            equivalentAmount = equivalentAmount.toFixed(4)
        }
        pairAmount.innerText = `${amount} ${pair} = ${equivalentAmount} USDT`
        pairAmountLimit.innerText = `${amount} ${pair} = ${equivalentAmount} USDT`
        pairUsdtValue = equivalentAmount;
        pairValue = res['amount']
    }
    
}

function trade(type, pair) {

    clearAllAlerts();

    var amount = 0;

    if (type == 'buy') {
        amount = `${uValue.value} ${$('#buyPairChanger').text()}`;
    }
    else {
        amount = `${pValue.value} ${$('#sellPairChanger').text()}`;
        
    }               
    if(amount.split(' ')[0] == 0){
        createAlert('danger', type + ' amount can not be 0!')
    }    
    else{
        var reqJson = {
            'header': 'trade_request',
            'orderType': 'market',
            'pair' : `${pair}-USDT`,
            'type' : type,
            'amount' : amount,
            }  
        tradeSocket.send(JSON.stringify(reqJson));
    }
    
}
function limit(type, pair){
    clearAllAlerts();

    var hasError = false;

    if(type == 'buy'){
        var price = parseFloat(limit_buy_price.value);
        var amount = `${limit_buy_amount.value} ${$('#buy-pair').text()}`;
    }
    else{
        var price = parseFloat(limit_sell_price.value);
        var amount = `${limit_sell_amount.value} ${$('#sell-pair').text()}`;
    }

    var amountVal = parseFloat(amount.split(' ')[0]);
    var amountCrp = amount.split(' ')[1];

    if(amountVal == 0 || price == 0){
        hasError = true;
        createAlert('danger', 'amount/price can not be 0!');
    }
    else if(amountCrp == pair){
        var tradeSize = price * amountVal  
    }
    else if(amountCrp != pair){
        var tradeSize = amountVal;
    }
    if(tradeSize < 10){
        hasError = true;
        createAlert('danger', 'minimum trade size is 10 $, but your is ' + tradeSize + '$!');
    }
    
    if(!hasError){
        var reqJson = {
            'header': 'limit_request',
            'orderType': 'limit',
            'pair' : `${pair}-USDT`,
            'type' : type,
            'tradeSize': tradeSize,
            'amount' : amount,
            'price': price
            }  
        tradeSocket.send(JSON.stringify(reqJson));
    
    }

}
function removeHistory() {
    createdHistory.forEach(function(item, index) {
        item.remove();
    })
    createdHistory = []
}
function removeOpenOrders(){
    createdOpenOrders.forEach(function(item, index) {
        item.remove();
    })
    createdOpenOrders = []
}
function removeClosedOrders(){
    createdClosedOrders.forEach(function(item, index) {
        item.remove();
    })
    createdClosedOrders = []
}

function removeRecentTrades() {
    createdRecentTrades.forEach(function(item, index) {
        item.remove();
    })
    createdRecentTrades = []
}

function clearAllAlerts() {
    activeAlerts.forEach(function(item, index) {
        item.remove();
    })
    activeAlerts = []
}

function getHistory(data, header) {
    
    var newNode = document.createElement("ul");
    var removed = false;
    newNode.classList.add("d-flex", "justify-content-between", "market-order-item", "ul");

    var time = document.createElement("li");
    var pair = document.createElement("li");
    var type = document.createElement("li");
    var price = document.createElement("li");
    var amount = document.createElement("li");
    var total = document.createElement("li");
    var iconSpace = document.createElement("li");
    var icon = document.createElement("div");

    time.innerText = data['date'];
    type.innerText = data['type'];
    pair.innerText = data['pair'];
    amount.innerText = parseFloat(data['amount']).toFixed(5);
    total.innerText = data['price'].toFixed(5);
    price.innerText = data['pairPrice'];
    

    if (data['type'] == 'buy') {
        type.classList.add('green')
    }
    else {
        type.classList.add('red')
    }

    newNode.appendChild(time);
    newNode.appendChild(pair);
    newNode.appendChild(type);
    newNode.appendChild(price);
    newNode.appendChild(amount);
    newNode.appendChild(total);
    

    if(header == 'hist_response'){
        if(data['orderType'] == 'market'){
            var parent = document.getElementById("market-orders");
        }else{
            var parent = document.getElementById("closed-limit-orders");
        }
    }
    else if(header == 'orders_response'){
        var parent = document.getElementById("open-limit-orders");
         
        icon.innerText = 'Close'
        icon.classList.add('closeOrderBtn')

        iconSpace.appendChild(icon);
        newNode.appendChild(iconSpace);

        icon.onclick = function(e){
            e.preventDefault();
            tradeSocket.send(JSON.stringify({'header': 'delOrder_request', 'id': e.target.dataset.id}))
            newNode.remove();
            removed = true;
        }
    }
    if(!removed){
        createdHistory.push(newNode);
        parent.prepend(newNode);
    }
       
}

function recentTrades(data) {
    var parent = document.getElementById("recentTradesHistory");
    var newNode = document.createElement("tr");
    var price = document.createElement("td");
    var amount = document.createElement("td");
    var time = document.createElement("td");

    price.innerText = data['price'].toFixed(2);
    amount.innerText = parseFloat(data['amount']).toFixed(5);
    time.innerText = data['time'];

    if (data['type'] == 'buy') {
        price.classList.add('green')
    }
    else {
        price.classList.add('red')
    }

    newNode.appendChild(price);
    newNode.appendChild(amount);
    newNode.appendChild(time);
    createdRecentTrades.push(newNode);
    parent.prepend(newNode);
}

function calcAmount(change, object) {
    var baseValue;
    if (change == 'usdt') {
        if ($('#buyPairChanger').text() == 'USDT')
        {
            baseValue = usdtValue;
        }
        else {
            var price = parseFloat($('#priceLoaded').text().replace(',', ''))
            baseValue = usdtValue / price;
        }
        uValue.value = baseValue * parseFloat(object.innerText.replace('%', '')) / 100
    }
    else if (change == 'pair') {
        if ($('#sellPairChanger').text() == 'USDT')
        {
            baseValue = pairUsdtValue;
        }
        else {
            baseValue = pairValue;
        }
        pValue.value = baseValue * parseFloat(object.innerText.replace('%', '')) / 100
    }
    else if (change == 'limitSell') {
        var limitSell = document.getElementById('limit-sell-amount')
        limitSell.value = pairValue * parseFloat(object.innerText.replace('%', '')) / 100
        calculateTotalLimit('sell')
    }
    else {
        var limitBuy = document.getElementById('limit-buy-amount')
        limitBuy.value = pairValue * parseFloat(object.innerText.replace('%', '')) / 100
        calculateTotalLimit('buy')
    }
}

function calculateTotalLimit(type) {
    if (type == 'buy') {
        var limitBuy = document.getElementById('limit-buy-amount')
        var price = parseFloat(document.getElementById('limit-buy-price').value)
        document.getElementById('totalBuyLimit').innerText = `${price * limitBuy.value} USDT`
    }
    else {
        var limitSell = document.getElementById('limit-sell-amount')
        var price = parseFloat(document.getElementById('limit-sell-price').value)
        document.getElementById('totalSellLimit').innerText = `${price * limitSell.value} USDT`
    }
}

function percentage() {
    var pair = document.getElementById('pairPercentage');
    var usdt = document.getElementById('usdtPercentage');

    var sellPercentageLimit = document.getElementById('usdtPercentageLimit');
    var buyPercentageLimit = document.getElementById('pairPercentageLimit');

    pair.childNodes.forEach(function(item, index) {
        if (item.tagName == 'LI'){
            pair.childNodes[index].addEventListener("click", function() {calcAmount('pair', pair.childNodes[index]);});
        }
    })

    sellPercentageLimit.childNodes.forEach(function(item, index) {
        if (item.tagName == 'LI'){
            sellPercentageLimit.childNodes[index].addEventListener("click", function() {calcAmount('limitBuy', sellPercentageLimit.childNodes[index]);});
        }
    })

    buyPercentageLimit.childNodes.forEach(function(item, index) {
        if (item.tagName == 'LI'){
            buyPercentageLimit.childNodes[index].addEventListener("click", function() {calcAmount('limitSell', buyPercentageLimit.childNodes[index]);});
        }
    })

    usdt.childNodes.forEach(function(item, index) {
        if (item.tagName == 'LI'){
            usdt.childNodes[index].addEventListener("click", function() {calcAmount('usdt', usdt.childNodes[index]);});
        }
    })
}

function validate(evt) {

    var theEvent = evt || window.event;

    // Handle paste
    if (theEvent.type === 'paste') {
      key = event.clipboardData.getData('text/plain');
    } else {
    // Handle key press
      var key = theEvent.keyCode || theEvent.which;
      key = String.fromCharCode(key);
    }
    var regex = /[0-9.]|\./;
    if( !regex.test(key) ) {
    theEvent.returnValue = false;
        if(theEvent.preventDefault) {
            theEvent.preventDefault();
        }
    }
}

function closeAlert(){
    var alertBox = this.parentNode;
    var parent = document.getElementById('alert');
    parent.style.display = 'block';
    alertBox.classList.remove('bounceInRight');
    alertBox.classList.add('bounceOutRight', 'd-none');    
}

function createAlert(type, message) {
    var logos = ['fa-info', 'fa-check', 'fa-exclamation-triangle']

    var parent = document.getElementById('alert');
    parent.style.display = 'block';
    var mainDiv = document.createElement("div")

    var errorTitle = ''
    if (type == 'info') {

        errorTitle = 'Caution'
    }
    else if (type == 'success') {

        errorTitle = 'Success'
    }
    else if (type == 'danger') {

        errorTitle = 'Error'
    }

    mainDiv.classList.add('alert', 'animated', `alert-${type}`, 'bounceInRight')
    
    var secondDiv = document.createElement("div")    
    secondDiv.classList.add('icon', 'pull-left')

    var firstI = document.createElement("i")  

    if (type == 'info') {

        firstI.classList.add('fa', logos[0], 'fa-2x')
    }
    else if (type == 'success') {

        firstI.classList.add('fa', logos[1], 'fa-2x')
    }
    else if (type == 'danger') {

        firstI.classList.add('fa', logos[2], 'fa-2x')
    }


    secondDiv.appendChild(firstI)

    var lastDiv = document.createElement("div")    
    lastDiv.classList.add('copy')
    var title = document.createElement("h4")
    title.innerText = errorTitle    
    var text = document.createElement("p")    
    text.innerText = message    
    lastDiv.appendChild(title)
    lastDiv.appendChild(text)

    var close = document.createElement("a") 
    close.addEventListener('click', closeAlert)   
    close.classList.add('close')
    var closeI = document.createElement("i")    
    closeI.classList.add('fa', 'fa-times')
    close.appendChild(closeI)

    mainDiv.appendChild(secondDiv)
    mainDiv.appendChild(lastDiv)
    mainDiv.appendChild(close)

    activeAlerts.push(mainDiv)
    parent.appendChild(mainDiv)

    setTimeout(function(param){
        parent.style.display = 'none';
        mainDiv.remove()
    }.bind(null), 5000);
}
function priceList(data){
    
    data.forEach(function(obj, index){

        if(index != 2){
            tr_elem = document.getElementById(index + '_tr');
            tr_elem.setAttribute('data-href',`/trade/${obj["pair"]}`);

            tr_elem.onclick = function(){
                window.location = `/trade/${obj["pair"]}`;
            }
            
            document.getElementById(index + '_pair').innerText = `${obj["pair"]}`;
            document.getElementById(index + '_price').innerText = `${obj["price"]}`;

            ch_elem = document.getElementById(index + '_change');
            
            if(obj['24c'] < 0){
                ch_elem.innerText = `${obj["24c"]}`;
                ch_elem.style.color = '#ff231f';
            }else{
                ch_elem.innerText = `+${obj["24c"]}`;
                ch_elem.style.color = '#26de81';
            }
        }
        
             
    })

}
function createPricePanel(){

    var parrent = document.getElementById("markets-list-trade");

    for(let i=0; i<20; i++){
        if(i != 2){
            var tr = document.createElement("tr");
            var pair = document.createElement("td");
            var price = document.createElement("td");
            var change = document.createElement("td");
            
            tr.id = i+"_tr";
            pair.id = i+"_pair";
            price.id = i+"_price";
            change.id = i+"_change";
            
            tr.appendChild(pair);
            tr.appendChild(price);
            tr.appendChild(change);

            parrent.appendChild(tr);
        }
  
    }
    
}
if(user != 'AnonymousUser'){
    percentage();
}

window.onoffline = (event) => {
  createAlert('info', "The network connection has been lost.")
};

window.ononline = (event) => {
    createAlert('info', "You are now connected to the network.")
    tradeSocket.close()
    try {
        var tradeSocket = new WebSocket('ws://' + window.location.host + '/ws/trade/');
    }
    catch (e) {
        var tradeSocket = new WebSocket('wss://' + window.location.host + '/ws/trade/');
    }
    tradeSocket.onopen = e => {
        tradeSocketOpen(e)
    }
    tradeSocket.onmessage = e => {
        tradeSocketMessage(e)
    }
    tradeSocket.onclose = function(e){
        tradeSocketClose(e)
    }

    tradeListSocket.close()
    try {
        var tradeListSocket = new WebSocket('ws://' + window.location.host + '/ws/trade/prices/');
    }
    catch (e) {
        var tradeListSocket = new WebSocket('wss://' + window.location.host + '/ws/trade/prices/');
    }
    tradeListSocket.onopen = function (e) {
        tradeListSocketOpen(e, true)
    };
    tradeListSocket.onmessage = function(e) {
        tradeListSocketMessage(e)
    };
    tradeListSocket.onclose = function(e) {
        tradeListSocketClose(e)
    };
};

document.querySelectorAll('input').forEach( (item, index) => {
    if (index > 0) {

        item.value = ''
    }
})