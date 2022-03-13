var tradeSocket = new WebSocket('ws://' + window.location.host + '/ws/trade/');
var tradeListSocket = new WebSocket('ws://' + window.location.host + '/ws/trade/prices/');

var main_url = window.location.origin;
var usdtValue = 0;
var pairValue = 0;
var pairUsdtValue = 0;
var uValue = document.getElementById('uValue');
var pValue = document.getElementById('pValue');
uValue.value = 0;
pValue.value = 0;
var getOrderType = document.querySelector('.nav-link');
var globPair = 'BTC'
var createdHistory = [];
var createdRecentTrades = [];
var activeAlerts = [];

tradeSocket.onopen = function(e){
    console.log('socket is on !!!');
    tradeSocket.send(JSON.stringify({'header': 'attribs', 'current_pair': pair, 'page': 'trade'}));
    removeRecentTrades();
    removeHistory();
}

tradeSocket.onmessage = function(e){

    data = JSON.parse(e.data);
    // console.log(data)
    Object.keys(data).forEach(function(index){
        obj = data[index]
        // console.log(obj)
        header = obj['header']

        if(header == 'trade_response'){
            state = obj['state'];
            if(state == 0){
                createAlert('success', 'Order filled!')
                document.getElementById('uValue').value = `0`;
                document.getElementById('pValue').value = `0`;
                
            }else{
                createAlert('danger', 'Insufficient balance!')
            }
        }  
        else if(header == 'hist_response'){
            getHistory(obj);
        }
        else if(header == 'recent_response'){
            recentTrades(obj);
        }
        else if(header == 'portfo_response'){
            getPortfolio(obj);
        }

    })
   
}
tradeSocket.onclose = function(e){
    createAlert('danger', 'There is a connection issue, please try again!');
}

tradeListSocket.onopen = function () {
    console.log('prices socket is on!!');
    tradeListSocket.send(JSON.stringify({"page":0}));
    createPricePanel();
};

tradeListSocket.onmessage = function(e) {
    var message = e.data;
    data = JSON.parse(message)
    priceList(data);
};

tradeListSocket.onclose = function(e) {
    console.log('Socket closed unexpectedly');
};

function getPortfolio(res) {
    pair = res['cryptoName']
    var usdtAmount = document.getElementById('usdtAmount');
    var pairAmount = document.getElementById('pairAmount');
    
    pairAmount.innerText = `0 ${pair}`
    

    if (res['cryptoName'] == 'USDT') {
        usdtAmount.innerText = `${res['amount'].toFixed(1)} USDT`
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

    if(getOrderType.classList.contains('active')){
        orderType = 'limit';
    }else{
        orderType = 'market';
    }

    var reqJson = {
        'header': 'trade_request',
        'orderType': orderType,
        'pair' : `${pair}-USDT`,
        'type' : type,
        'amount' : amount,
    }

    tradeSocket.send(JSON.stringify(reqJson));  
}

function removeHistory() {
    createdHistory.forEach(function(item, index) {
        item.remove();
    })
    createdHistory = []
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

function getHistory(data) {
    var parent = document.getElementById("orders");
    var newNode = document.createElement("ul");
    newNode.classList.add("d-flex", "justify-content-between", "market-order-item", "ul");

    var time = document.createElement("li");
    var pair = document.createElement("li");
    var type = document.createElement("li");
    var price = document.createElement("li");
    var amount = document.createElement("li");
    var total = document.createElement("li");

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

    createdHistory.push(newNode);
    parent.prepend(newNode);
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
    else {
        if ($('#sellPairChanger').text() == 'USDT')
        {
            baseValue = pairUsdtValue;
        }
        else {
            baseValue = pairValue;
        }
        pValue.value = baseValue * parseFloat(object.innerText.replace('%', '')) / 100
    }
}

function percentage() {
    var pair = document.getElementById('pairPercentage');
    var usdt = document.getElementById('usdtPercentage');

    pair.childNodes.forEach(function(item, index) {
        if (item.tagName == 'LI'){
            pair.childNodes[index].addEventListener("click", function() {calcAmount('pair', pair.childNodes[index]);});
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
    alertBox.classList.remove('bounceInRight');
    alertBox.classList.add('bounceOutRight', 'd-none');    
}

function createAlert(type, message) {
    var logos = ['fa-info', 'fa-check', 'fa-exclamation-triangle']

    var parent = document.getElementById('alert');
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
        mainDiv.remove()
    }.bind(null), 5000);
}
function priceList(data){
    
    data.forEach(function(obj, index){

        tr_elem = document.getElementById(index + '_tr');
        tr_elem.setAttribute('data-href',`/account/trade/${obj["symbol"]}-USDT`);

        tr_elem.onclick = function(){
            window.location = `/account/trade/${obj["symbol"]}-USDT`;
        }
        
        document.getElementById(index + '_pair').innerText = `${obj["symbol"]}-USDT`;
        document.getElementById(index + '_price').innerText = `${obj["price"]}`;

        ch_elem = document.getElementById(index + '_change');
        ch_elem.innerText = `${obj["24c"]}`;

        if(obj['24c'] < 0){
            ch_elem.style.color = '#ff231f';
        }else{
            ch_elem.style.color = '#26de81';
        }
             
    })

}
function createPricePanel(){

    var parrent = document.getElementById("markets-list-trade");

    for(let i=0; i<20; i++){
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
percentage();
// getHistory();