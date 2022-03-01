var tradeSocket = new WebSocket('ws://' + window.location.host + '/ws/trade/');

var main_url = window.location.origin;
var usdtValue = 0;
var pairValue = 0;
var pairUsdtValue = 0;
var uValue = document.getElementById('uValue');
var pValue = document.getElementById('pValue');
var getOrderType = document.querySelector('.nav-link');
uValue.value = 0;
pValue.value = 0;
var globPair = 'BTC'
var createdHistory = [];
var createdRecentTrades = [];
var activeAlerts = [];

tradeSocket.onopen = function(e){
    console.log('socket is on !!!');
}
tradeSocket.onmessage = function(e){
    data = JSON.parse(e.data);
    console.log(data)
    header = data['header'];
    
    if(header == 'trade_response'){
        state = data['state'];
        if(state == 0){
            createAlert('success', 'Order filled!')
        }else{
            createAlert('danger', 'Insufficient balance!')
        }
    }  
}
tradeSocket.onclose = function(e){
    createAlert('danger', 'There is a connection issue, please try again!');
}

function getPortfolio(pair) {

    globPair = pair
    var usdtAmount = document.getElementById('usdtAmount');
    var pairAmount = document.getElementById('pairAmount');

    usdtAmount.innerText = '0 USDT'
    pairAmount.innerText = `0 ${pair}`

    const url = `${main_url}/portfolio/`
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.timeout = 30000;
    xhr.ontimeout = function () { console.log('time out'); }
    xhr.responseType = 'json';

    xhr.onreadystatechange = function(e) {
        if (this.status === 200 && xhr.readyState == 4) {
            res = this.response;
            Object.keys(res).forEach(function(item, index) {

                if (res[item]['cryptoName'] == pair && pair != 'USDT') {
                    pairAmount.innerText = `${res[item]['amount'].toFixed(5)} ${pair} = ${res[item]['equivalentAmount'].toFixed(5)} USDT`
                    pairUsdtValue = res[item]['equivalentAmount'].toFixed(5);
                    pairValue = res[item]['amount']
                }
                if (res[item]['cryptoName'] == 'USDT') {
                    usdtAmount.innerText = `${res[item]['amount'].toFixed(5)} USDT`
                    usdtValue = res[item]['amount']
                }
            })
        }
        else {
            console.log(this.status)
        }
    };
    try {
        xhr.send();
    } catch(err) {
        console.log('error')
    }
}

function trade(type, pair) {
    
    clearAllAlerts();

    var amount = 0;
    if(type == 'buy') {
        amount = `${uValue.value} ${$('#buyPairChanger').text()}`;
    }else{
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

function getHistory() {

    removeHistory()
    const url = `${main_url}/tradinghistory`
    // console.log(url);
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.timeout = 30000;
    xhr.ontimeout = function () { console.log('time out'); }
    xhr.responseType = 'json';

    xhr.onreadystatechange = function(e) {
        if (this.status === 200 && xhr.readyState == 4) {
            res = this.response;
            var parent = document.getElementById("open-orders")
            var before = document.getElementById("before")
            Object.keys(res).forEach(function(item, index) {
                var newNode = document.createElement("ul")
                newNode.classList.add("d-flex", "justify-content-between", "market-order-item", "ul")

                var time = document.createElement("li")
                var pair = document.createElement("li")
                var type = document.createElement("li")
                var price = document.createElement("li")
                var amount = document.createElement("li")
                var total = document.createElement("li")

                time.innerText = res[index]['time']
                type.innerText = res[index]['type']
                pair.innerText = res[index]['pair']
                // price.innerText = res[index]['pairPrice'].toFixed(5)
                amount.innerText = parseFloat(res[index]['amount'].split(' ')[0]).toFixed(5) + ' ' + res[index]['amount'].split(' ')[1]
                total.innerText = res[index]['price'].toFixed(5)

                if (res[index]['type'] == 'buy') {
                    type.classList.add('green')
                }
                else {
                    type.classList.add('red')
                }

                newNode.appendChild(time)
                newNode.appendChild(pair)
                newNode.appendChild(type)
                newNode.appendChild(price)
                newNode.appendChild(amount)
                newNode.appendChild(total)

                createdHistory.push(newNode)

                parent.insertBefore(newNode, before)
            })
        }
        else {
            console.log(this.status)
        }
    };
    try {
        xhr.send();
    } catch(err) {
        console.log('error')
    }
}

function recentTrades() {

    removeRecentTrades()
    const url = `${main_url}/recentTrades`
    // console.log(url);
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.timeout = 30000;
    xhr.ontimeout = function () { console.log('time out'); }
    xhr.responseType = 'json';

    xhr.onreadystatechange = function(e) {
        if (this.status === 200 && xhr.readyState == 4) {
            res = this.response;
            var parent = document.getElementById("recentTradesHistory")
            var before = document.getElementById("beforeRecent")
            Object.keys(res).forEach(function(item, index) {
                // console.log(res[index])
                var newNode = document.createElement("tr")

                var pair = document.createElement("td")
                var price = document.createElement("td")
                var amount = document.createElement("td")

                pair.innerText = res[index]['pair']
                price.innerText = res[index]['pairPrice'].toFixed(5)
                amount.innerText = parseFloat(res[index]['amount'].split(' ')[0]).toFixed(5) + ' ' + res[index]['amount'].split(' ')[1]

                if (res[index]['type'] == 'buy') {
                    price.classList.add('green')
                }
                else {
                    price.classList.add('red')
                }

                newNode.appendChild(pair)
                newNode.appendChild(price)
                newNode.appendChild(amount)

                createdRecentTrades.push(newNode)

                parent.appendChild(newNode)
                // parent.insertBefore(newNode, before)
            })
        }
        else {
            console.log(this.status)
        }
    };
    try {
        xhr.send();
    } catch(err) {
        console.log('error')
    }
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
percentage();
getHistory();
// recentTrades();