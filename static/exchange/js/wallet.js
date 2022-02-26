socket = new WebSocket('ws://' + window.location.host + '/ws/wallet/');

socket.onopen = function () {
    socket.send(JSON.stringify({"page":0}));
};

socket.onmessage = function(e) {
    var message = e.data;
    chartData = JSON.parse(message)

    document.getElementById('totalMargin').innerText = chartData['total']
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
    var data = google.visualization.arrayToDataTable(chartData['assetAllocation']);

    var options = {
      width: 600,
      hwight: 450,
      backgroundColor: { fill:'transparent' },
      color: 'white',
      pieHole: 0.4,
      legend: {position: 'top', textStyle: {color: 'white', fontSize: 16}},
      pieSliceText: 'percentage',
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
                        return value + ' %';
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
                                return  tooltipItems.yLabel + " %";
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

socket.onclose = function(e) {
    console.error('Socket closed unexpectedly');
};