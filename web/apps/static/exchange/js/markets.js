var page = 0
try {
    var socket = new WebSocket('ws://' + window.location.host + '/ws/');
}
catch (e) {
    var socket = new WebSocket('wss://' + window.location.host + '/ws/');
}
socket.onopen = function () {
    socket.send(JSON.stringify({"page":0, RequestType : 'market'}));
};

socket.onmessage = function(e) {
    var message = e.data;
    data = JSON.parse(message)
    fillData(data)
};

socket.onclose = function(e) {
    console.log('Socket closed unexpectedly');
};


function fillData(data) {
    Object.keys(data).forEach(function(item, index) {
        obj = data[index]
        document.getElementById(index + '_tr').setAttribute('data-href',`/trade/${obj["symbol"]}-USDT`)
        document.getElementById(index + '_image').src = `${obj["img"]}`
        document.getElementById(index + '_name').innerText = `${obj["symbol"]} (${obj["name"]})`
        document.getElementById(index + '_current_price').innerText = obj['price']
        var change = document.getElementById(index + '_price_change_percentage_24h')
        change.innerText = obj['24c'] + ' %'
        document.getElementById(index + '_total_volume').innerText = obj['vol']
        document.getElementById(index + '_marketCap').innerText = obj['mc']
        document.getElementById(index + '_market_cap_rank').innerText = obj['rank']
        document.getElementById(index + '_high').innerText = obj['24h']
        document.getElementById(index + '_low').innerText = obj['24l']

        if (parseFloat(obj['24c']) > 0) {
            change.classList.remove('red')
            change.classList.add('green')
        }
        else if (parseFloat(obj['24c']) < 0){
            change.classList.remove('green')
            change.classList.add('red')
        }
        else {   
            change.classList.remove('red')
            change.classList.remove('green')
        }
    })
}

function initial() {
    const numberOfCoins = 20;

    var parent = document.getElementById("cryptos")
    var before = document.getElementById("before1")

    var counter = 0
    while (counter < numberOfCoins) {

        var tr = document.createElement("tr")

        var market_cap_rank = document.createElement("td")
        var coin = document.createElement("td")
        var marketCap = document.createElement("td")
        var image = document.createElement("img")
        var current_price = document.createElement("td")
        var price_change_percentage_24h = document.createElement("td")
        var total_volume = document.createElement("td")
        var high = document.createElement("td")
        var low = document.createElement("td")
        var name = document.createElement("div")

        market_cap_rank.id = counter + '_market_cap_rank'
        coin.id = counter + '_coin'
        marketCap.id = counter + '_marketCap'
        current_price.id = counter + '_current_price'
        price_change_percentage_24h.id = counter + '_price_change_percentage_24h'
        total_volume.id = counter + '_total_volume'
        image.id = counter + '_image'
        name.id = counter + '_name'
        high.id = counter + '_high'
        low.id = counter + '_low'
        tr.id = counter + '_tr'

        coin.appendChild(image)
        coin.appendChild(name)
        tr.appendChild(market_cap_rank)
        tr.appendChild(coin)
        tr.appendChild(current_price)
        tr.appendChild(price_change_percentage_24h)
        tr.appendChild(high)
        tr.appendChild(low)
        tr.appendChild(total_volume)
        tr.appendChild(marketCap)

        parent.insertBefore(tr, before)

        counter ++;
    }
}

function pagination() {

    var clickTimeout;
    $('#paginationText').text(page + 1 + '/' + 30)

    $('#paginationPrev').click(function (e) {
        if (page > 0) {
            clearTimeout(clickTimeout);
            page --

            $('#paginationText').text(page + 1 + '/' + 30)

            clickTimeout = setTimeout(function(){
                socket.close()
                try {
                    var socket = new WebSocket('ws://' + window.location.host + '/ws/');
                }
                catch (e) {
                    var socket = new WebSocket('wss://' + window.location.host + '/ws/');
                }
                socket.onopen = function () {
                    socket.send(JSON.stringify({"page":page}));
                };

                socket.onmessage = function(e) {
                    var message = e.data;
                    data = JSON.parse(message)
                    fillData(data)
                };

                socket.onclose = function(e) {
                    console.log('Socket closed unexpectedly');
                };
            }, 500);
        }
    });

    $('#paginationNext').click(function (e) {
        if (page < 29) {
            clearTimeout(clickTimeout);
            page ++

            $('#paginationText').text(page + 1 + '/' + 30)

            clickTimeout = setTimeout(function(){
                socket.close()
                try {
                    var socket = new WebSocket('ws://' + window.location.host + '/ws/');
                }
                catch (e) {
                    var socket = new WebSocket('wss://' + window.location.host + '/ws/');
                }

                socket.onopen = function () {
                    socket.send(JSON.stringify({"page":page, RequestType : 'market'}));
                };

                socket.onmessage = function(e) {
                    var message = e.data;
                    data = JSON.parse(message)
                    fillData(data)
                };

                socket.onclose = function(e) {
                    console.log('Socket closed unexpectedly');
                };
            }, 500);
        }
    });
}

window.onoffline = (event) => {
  console.log("The network connection has been lost.")
};

window.ononline = (event) => {
    console.log("You are now connected to the network.")

    socket.close()
    try {
        var socket = new WebSocket('ws://' + window.location.host + '/ws/');
    }
    catch (e) {
        var socket = new WebSocket('wss://' + window.location.host + '/ws/');
    }
    socket.onopen = function () {
        socket.send(JSON.stringify({"page":page, RequestType : 'market'}));
    };

    socket.onmessage = function(e) {
        var message = e.data;
        data = JSON.parse(message)
        fillData(data)
    };

    socket.onclose = function(e) {
        console.log('Socket closed unexpectedly');
    };
};

initial()
pagination()