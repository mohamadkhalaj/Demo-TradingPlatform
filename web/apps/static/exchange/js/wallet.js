// assets socket data
var assetsObj = [];
try {
  assetSocket = new WebSocket('ws://' + window.location.host + '/ws/wallet/');
}
catch (e) {
  assetSocket = new WebSocket('wss://' + window.location.host + '/ws/wallet/');
}

assetSocket.onopen = function () {
    assetSocket.send(JSON.stringify({"start":1}));
};

assetSocket.onmessage = function(e) {
    var message = e.data;
    assetData = JSON.parse(message);
    $('#totalMargin').text(assetData['available'] + ' $');
    $('#availableMargin').text(assetData['total'] + ' $');
    $('#waiting').remove();
    $('#waitingAvailable').remove();
    $('#waitingTotal').remove();

    removeAssets();
    createAssets(assetData['assets']);
};

assetSocket.onclose = function(e) {
    console.log('Socket closed unexpectedly');
};

function removeAssets() {
    assetsObj.forEach(function(item, index) {
        item.remove();
    })
    assetsObj = []
}

function createAssets(data) {

    var parent = document.getElementById("assetsDiv")
    var before = document.getElementById("beforeAssets")

    Object.keys(data).forEach(function(item, index) {
        obj = data[index]

        var a = document.createElement("a")

        var first = document.createElement("div")
        var image = document.createElement("img")
        var second = document.createElement("div")
        var h2 = document.createElement("h2")

        var third = document.createElement("div")
        var h3 = document.createElement("h3")
        var br = document.createElement("br")
        var p = document.createElement("p")

        var symbol = obj["symbol"];
        if (symbol == 'USDT') {
            var symbol = 'BTC';
        }
        
        a.setAttribute('href',`/trade/${symbol}-USDT`)
        a.classList.add('nav-link', 'd-flex', 'justify-content-between', 'align-items-center')
        a.setAttribute('target','_blank')

        first.classList.add('d-flex')
        image.src = `${obj["img"]}`
        h2.innerText = `${obj["symbol"]}`

        if (obj['amount'] < 1) {

          h3.innerText = obj['amount'].toFixed(6)
        }
        else {
          h3.innerText = obj['amount'].toFixed(1) 
        }
        h3.classList.add('float-right', 'smallFont')

        p.innerText = obj['total'].toFixed(1) + ' $'  
        p.classList.add('float-right')

        second.appendChild(h2)
        first.appendChild(image)
        first.appendChild(second)

        third.appendChild(h3)
        third.appendChild(br)
        third.appendChild(p)

        a.appendChild(first)
        a.appendChild(third)
        
        assetsObj.push(a)

        parent.insertBefore(a, before)
    })
}
// end asset socket



// charts socket data

function socketMessage(e) {
    var message = e.data;
    chartData = JSON.parse(message)

    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);

    $('#waitingAssetAllocation').remove();
    function drawChart() {
    var data = google.visualization.arrayToDataTable(chartData['assetAllocation']);

    var options = {
      width: 600,
      hwight: 450,
      backgroundColor: { fill:'transparent' },
      color: 'white',
      pieHole: 0.4,
      legend: {position: 'top', textStyle: {color: 'gray', fontSize: 16}},
      pieSliceText: 'label',
    };

    var chart = new google.visualization.PieChart(document.getElementById('assetAllocation'));
      chart.draw(data, options);
    }

    var pnlDiv = document.getElementById('pnlDiv')
    if (chartData['pnl']) {
      pnlDiv.classList.remove('d-none')
      var xValues = chartData['pnl'][0]
      var yValues = chartData['pnl'][1]
      var barColors = [];

      yValues.forEach(function(item, index) {
        yValues[index] = item.toFixed(2)
        if (item > 0) {
          barColors.push('green')
        }
        else {
          barColors.push('red')
        }
      })


      new Chart("pnl", {
        type: "bar",
        data: {
          labels: xValues,
          datasets: [{
            backgroundColor: barColors,
            data: yValues
          }]
        },
        options: {
          legend: {display: false},
          title: {
            display: true,
          },
          scales: {
              xAxes: [{
                  ticks: {
                      autoSkip: true,
                      maxTicksLimit: 20,
                  },
                  scaleLabel: {
                    display: true,
                    labelString: 'Day'
                  }
              }],
              yAxes: [{
                  ticks: {
                    callback: function(value, index, ticks) {
                        return value + ' $';
                    },
                  },
                  scaleLabel: {
                    display: true,
                    labelString: 'PNL'
                  }
              }],
          },
          tooltips: {
                  enabled: true,
                  mode: 'single',
                  callbacks: {
                           label: function (tooltipItems, data) {
                                return  tooltipItems.yLabel + " $";
                           }
                  }
         }
        },
      });
    }
    else {
      pnlDiv.classList.add('d-none')
    }
};

try {
  socket = new WebSocket('ws://' + window.location.host + '/ws/wallet/chart/');
}
catch (e) {
  socket = new WebSocket('wss://' + window.location.host + '/ws/wallet/chart/');
}

socket.onopen = function () {
    socket.send(JSON.stringify({"start":1}));
};

socket.onmessage = function(e) {
  socketMessage(e)
}

socket.onclose = function(e) {
    console.log('Socket closed unexpectedly');
};
// end char socket data

window.onoffline = (event) => {
  console.log("The network connection has been lost.")
};

window.ononline = (event) => {
    console.log("You are now connected to the network.")

    assetSocket.close()
    try {
      assetSocket = new WebSocket('ws://' + window.location.host + '/ws/wallet/');
    }
    catch (e) {
      assetSocket = new WebSocket('wss://' + window.location.host + '/ws/wallet/');
    }

    assetSocket.onopen = function () {
        assetSocket.send(JSON.stringify({"start":1}));
    };

    assetSocket.onmessage = function(e) {
        var message = e.data;
        assetData = JSON.parse(message);
        $('#totalMargin').text(assetData['total'] + ' $');
        $('#waiting').remove();
        $('#waitingTotal').remove();

        removeAssets();
        createAssets(assetData['assets']);
    };

    assetSocket.onclose = function(e) {
        console.log('Socket closed unexpectedly');
    };

    socket.close()
    try {
      socket = new WebSocket('ws://' + window.location.host + '/ws/wallet/chart/');
    }
    catch (e) {
      socket = new WebSocket('wss://' + window.location.host + '/ws/wallet/chart/');
    }

    socket.onopen = function () {
        socket.send(JSON.stringify({"start":1}));
    };

    socket.onmessage = function(e) {
      socketMessage(e)
    }

    socket.onclose = function(e) {
        console.log('Socket closed unexpectedly');
    };
};