(function ($) {
  'use strict';
  // Depth Chart
  function DepthChart() {
    // Add data
    chart.dataSource.url =
      'https://poloniex.com/public?command=returnOrderBook&currencyPair=BTC_ETH&depth=50';
    chart.dataSource.reloadFrequency = 30000;
    chart.dataSource.adapter.add('parsedData', function (data) {
      // Function to process (sort and calculate cummulative volume)
      function processData(list, type, desc) {
        // Convert to data points
        for (var i = 0; i < list.length; i++) {
          list[i] = {
            value: Number(list[i][0]),
            volume: Number(list[i][1]),
          };
        }

        // Sort list just in case
        list.sort(function (a, b) {
          if (a.value > b.value) {
            return 1;
          } else if (a.value < b.value) {
            return -1;
          } else {
            return 0;
          }
        });

        // Calculate cummulative volume
        if (desc) {
          for (var i = list.length - 1; i >= 0; i--) {
            if (i < list.length - 1) {
              list[i].totalvolume = list[i + 1].totalvolume + list[i].volume;
            } else {
              list[i].totalvolume = list[i].volume;
            }
            var dp = {};
            dp['value'] = list[i].value;
            dp[type + 'volume'] = list[i].volume;
            dp[type + 'totalvolume'] = list[i].totalvolume;
            res.unshift(dp);
          }
        } else {
          for (var i = 0; i < list.length; i++) {
            if (i > 0) {
              list[i].totalvolume = list[i - 1].totalvolume + list[i].volume;
            } else {
              list[i].totalvolume = list[i].volume;
            }
            var dp = {};
            dp['value'] = list[i].value;
            dp[type + 'volume'] = list[i].volume;
            dp[type + 'totalvolume'] = list[i].totalvolume;
            res.push(dp);
          }
        }
      }

      // Init
      var res = [];
      processData(data.bids, 'bids', true);
      processData(data.asks, 'asks', false);

      return res;
    });

    // Set up precision for numbers
    chart.numberFormatter.numberFormat = '#,###.####';

    // Create axes
    var xAxis = chart.xAxes.push(new am4charts.CategoryAxis());
    xAxis.dataFields.category = 'value';
    //xAxis.renderer.grid.template.location = 0;
    xAxis.renderer.minGridDistance = 50;
    xAxis.tooltip.disabled = true;
    xAxis.renderer.grid.template.disabled = true;
    xAxis.renderer.paddingBottom = 10;

    var yAxis = chart.yAxes.push(new am4charts.ValueAxis());
    yAxis.tooltip.disabled = true;
    yAxis.renderer.grid.template.disabled = true;

    // Create series
    var series = chart.series.push(new am4charts.StepLineSeries());
    series.dataFields.categoryX = 'value';
    series.dataFields.valueY = 'bidstotalvolume';
    series.strokeWidth = 1;
    series.stroke = am4core.color('#26de81');
    series.fill = series.stroke;
    series.fillOpacity = 0.5;
    series.tooltip.getFillFromObject = false;
    series.tooltip.background.fill = am4core.color('#26de81');
    series.tooltip.background.stroke = am4core.color('#26de81');
    series.tooltipText =
      'Ask: [bold]{categoryX}[/]\nTotal volume: [bold]{valueY}[/]\nVolume: [bold]{bidsvolume}[/]';

    var series2 = chart.series.push(new am4charts.StepLineSeries());
    series2.dataFields.categoryX = 'value';
    series2.dataFields.valueY = 'askstotalvolume';
    series2.strokeWidth = 1;
    series2.stroke = am4core.color('#ff231f');
    series2.fill = series2.stroke;
    series2.fillOpacity = 0.5;
    series2.tooltip.getFillFromObject = false;
    series2.tooltip.background.fill = am4core.color('#ff231f');
    series2.tooltip.background.stroke = am4core.color('#ff231f');
    series2.tooltipText =
      'Ask: [bold]{categoryX}[/]\nTotal volume: [bold]{valueY}[/]\nVolume: [bold]{asksvolume}[/]';

    var series3 = chart.series.push(new am4charts.ColumnSeries());
    series3.dataFields.categoryX = 'value';
    series3.dataFields.valueY = 'bidsvolume';
    series3.strokeWidth = 0;
    series3.fill = am4core.color('#2a2e39');
    series3.fillOpacity = 0.1;

    var series4 = chart.series.push(new am4charts.ColumnSeries());
    series4.dataFields.categoryX = 'value';
    series4.dataFields.valueY = 'asksvolume';
    series4.strokeWidth = 0;
    series4.fill = am4core.color('#2a2e39');
    series4.fillOpacity = 0.1;

    // Add cursor
    chart.cursor = new am4charts.XYCursor();
  }

  if (document.getElementById('darkDepthChart')) {
    function am4themes_dark(target) {
      if (target instanceof am4core.InterfaceColorSet) {
        target.setFor('stroke', am4core.color('#000000'));
        target.setFor('fill', am4core.color('#2b2b2b'));
        target.setFor('primaryButton', am4core.color('#6794dc'));
        target.setFor('primaryButtonHover', am4core.color('#6771dc'));
        target.setFor('primaryButtonDown', am4core.color('#68dc75'));
        target.setFor('primaryButtonActive', am4core.color('#68dc75'));
        target.setFor('primaryButtonText', am4core.color('#FFFFFF'));
        target.setFor('primaryButtonStroke', am4core.color('#6794dc'));
        target.setFor('secondaryButton', am4core.color('#3b3b3b'));
        target.setFor('secondaryButtonHover', am4core.color('#3b3b3b'));
        target.setFor('secondaryButtonDown', am4core.color('#3b3b3b'));
        target.setFor('secondaryButtonText', am4core.color('#bbbbbb'));
        target.setFor('secondaryButtonStroke', am4core.color('#3b3b3b'));
        target.setFor('grid', am4core.color('#6DC0D5'));
        target.setFor('background', am4core.color('#000000'));
        target.setFor('alternativeBackground', am4core.color('#ffffff'));
        target.setFor('text', am4core.color('#ffffff'));
        target.setFor('alternativeText', am4core.color('#000000'));
        target.setFor('disabledBackground', am4core.color('#bbbbbb'));
      }
    }
    // Themes begin
    am4core.useTheme(am4themes_dark);
    // Themes end

    var chart = am4core.create('darkDepthChart', am4charts.XYChart);
    chart.zoomOutButton.background.fill = am4core.color(
      'rgba(255, 255, 255, 0.11)'
    );
    chart.zoomOutButton.icon.stroke = am4core.color('#ebebeb');
    chart.zoomOutButton.background.states.getKey(
      'hover'
    ).properties.fill = am4core.color('#00cc93');
    DepthChart();
  }

  if (document.getElementById('lightDepthChart')) {
    var chart = am4core.create('lightDepthChart', am4charts.XYChart);
    chart.zoomOutButton.background.fill = am4core.color('rgba(0, 0, 0, 0.09)');
    chart.zoomOutButton.icon.stroke = am4core.color('rgba(0, 0, 0, 0.40)');
    chart.zoomOutButton.background.states.getKey(
      'hover'
    ).properties.fill = am4core.color('#00cc93');
    DepthChart();
  }

  if (document.getElementById('marketsChartBtcLight')) {
    am4core.ready(function () {
      // Create chart
      var chart = am4core.create('marketsChartBtcLight', am4charts.XYChart);

      chart.data = generateChartData();

      var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
      dateAxis.baseInterval = {
        timeUnit: 'minute',
        count: 1,
      };
      dateAxis.tooltip.disabled = true;
      dateAxis.renderer.grid.template.disabled = true;
      dateAxis.renderer.labels.template.disabled = true;
      dateAxis.renderer.ticks.template.disabled = true;
      dateAxis.renderer.paddingBottom = 15;

      var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
      valueAxis.tooltip.disabled = true;
      valueAxis.renderer.grid.template.disabled = true;
      valueAxis.renderer.labels.template.disabled = true;
      valueAxis.renderer.ticks.template.disabled = true;

      var series = chart.series.push(new am4charts.LineSeries());
      series.dataFields.dateX = 'date';
      series.dataFields.valueY = 'prices';
      series.tooltipText = 'prices: [bold]{valueY}[/]';
      series.fillOpacity = 0.1;
      series.fill = am4core.color('#00cc93');
      series.stroke = am4core.color('#00cc93');
      series.tooltip.getFillFromObject = false;
      series.tooltip.background.fill = am4core.color('#2a2e39');
      series.tooltip.background.stroke = am4core.color('#2a2e39');

      chart.cursor = new am4charts.XYCursor();
      chart.cursor.lineY.opacity = 1;
      dateAxis.start = 0;
      dateAxis.keepSelection = true;
      chart.zoomOutButton.background.fill = am4core.color(
        'rgba(0, 0, 0, 0.09)'
      );
      chart.zoomOutButton.icon.stroke = am4core.color('rgba(0, 0, 0, 0.40)');
      chart.zoomOutButton.background.states.getKey(
        'hover'
      ).properties.fill = am4core.color('#00cc93');

      function generateChartData() {
        var chartData = [];
        // current date
        var firstDate = new Date();
        // now set 500 minutes back
        firstDate.setMinutes(firstDate.getDate() - 500);

        // and generate 500 data items
        var prices = 500;
        for (var i = 0; i < 500; i++) {
          var newDate = new Date(firstDate);
          // each time we add one minute
          newDate.setMinutes(newDate.getMinutes() + i);
          // some random number
          prices += Math.round(
            (Math.random() < 0.5 ? 1 : -1) * Math.random() * 10
          );
          // add data item to the array
          chartData.push({
            date: newDate,
            prices: prices,
          });
        }
        return chartData;
      }
    });
  }

  if (document.getElementById('marketsChartEthLight')) {
    am4core.ready(function () {
      // Create chart
      var chart = am4core.create('marketsChartEthLight', am4charts.XYChart);

      chart.data = generateChartData();

      var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
      dateAxis.baseInterval = {
        timeUnit: 'minute',
        count: 1,
      };
      dateAxis.tooltip.disabled = true;
      dateAxis.renderer.grid.template.disabled = true;
      dateAxis.renderer.labels.template.disabled = true;
      dateAxis.renderer.ticks.template.disabled = true;
      dateAxis.renderer.paddingBottom = 15;

      var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
      valueAxis.tooltip.disabled = true;
      valueAxis.renderer.grid.template.disabled = true;
      valueAxis.renderer.labels.template.disabled = true;
      valueAxis.renderer.ticks.template.disabled = true;

      var series = chart.series.push(new am4charts.LineSeries());
      series.dataFields.dateX = 'date';
      series.dataFields.valueY = 'prices';
      series.tooltipText = 'prices: [bold]{valueY}[/]';
      series.fillOpacity = 0.1;
      series.fill = am4core.color('#f74745');
      series.stroke = am4core.color('#f74745');
      series.tooltip.getFillFromObject = false;
      series.tooltip.background.fill = am4core.color('#2a2e39');
      series.tooltip.background.stroke = am4core.color('#2a2e39');

      chart.cursor = new am4charts.XYCursor();
      chart.cursor.lineY.opacity = 1;
      dateAxis.start = 0;
      dateAxis.keepSelection = true;
      chart.zoomOutButton.background.fill = am4core.color(
        'rgba(0, 0, 0, 0.09)'
      );
      chart.zoomOutButton.icon.stroke = am4core.color('rgba(0, 0, 0, 0.40)');
      chart.zoomOutButton.background.states.getKey(
        'hover'
      ).properties.fill = am4core.color('#f74745');

      function generateChartData() {
        var chartData = [];
        // current date
        var firstDate = new Date();
        // now set 500 minutes back
        firstDate.setMinutes(firstDate.getDate() - 500);

        // and generate 500 data items
        var prices = 500;
        for (var i = 0; i < 500; i++) {
          var newDate = new Date(firstDate);
          // each time we add one minute
          newDate.setMinutes(newDate.getMinutes() + i);
          // some random number
          prices += Math.round(
            (Math.random() < 0.5 ? 1 : -1) * Math.random() * 10
          );
          // add data item to the array
          chartData.push({
            date: newDate,
            prices: prices,
          });
        }
        return chartData;
      }
    });
  }

  if (document.getElementById('marketsChartLtcLight')) {
    am4core.ready(function () {
      // Create chart
      var chart = am4core.create('marketsChartLtcLight', am4charts.XYChart);

      chart.data = generateChartData();

      var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
      dateAxis.baseInterval = {
        timeUnit: 'minute',
        count: 1,
      };
      dateAxis.tooltip.disabled = true;
      dateAxis.renderer.grid.template.disabled = true;
      dateAxis.renderer.labels.template.disabled = true;
      dateAxis.renderer.ticks.template.disabled = true;
      dateAxis.renderer.paddingBottom = 15;

      var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
      valueAxis.tooltip.disabled = true;
      valueAxis.renderer.grid.template.disabled = true;
      valueAxis.renderer.labels.template.disabled = true;
      valueAxis.renderer.ticks.template.disabled = true;

      var series = chart.series.push(new am4charts.LineSeries());
      series.dataFields.dateX = 'date';
      series.dataFields.valueY = 'prices';
      series.tooltipText = 'prices: [bold]{valueY}[/]';
      series.fillOpacity = 0.1;
      series.fill = am4core.color('#00cc93');
      series.stroke = am4core.color('#00cc93');
      series.tooltip.getFillFromObject = false;
      series.tooltip.background.fill = am4core.color('#2a2e39');
      series.tooltip.background.stroke = am4core.color('#2a2e39');

      chart.cursor = new am4charts.XYCursor();
      chart.cursor.lineY.opacity = 1;
      dateAxis.start = 0;
      dateAxis.keepSelection = true;
      chart.zoomOutButton.background.fill = am4core.color(
        'rgba(0, 0, 0, 0.09)'
      );
      chart.zoomOutButton.icon.stroke = am4core.color('rgba(0, 0, 0, 0.40)');
      chart.zoomOutButton.background.states.getKey(
        'hover'
      ).properties.fill = am4core.color('#00cc93');

      function generateChartData() {
        var chartData = [];
        // current date
        var firstDate = new Date();
        // now set 500 minutes back
        firstDate.setMinutes(firstDate.getDate() - 500);

        // and generate 500 data items
        var prices = 500;
        for (var i = 0; i < 500; i++) {
          var newDate = new Date(firstDate);
          // each time we add one minute
          newDate.setMinutes(newDate.getMinutes() + i);
          // some random number
          prices += Math.round(
            (Math.random() < 0.5 ? 1 : -1) * Math.random() * 10
          );
          // add data item to the array
          chartData.push({
            date: newDate,
            prices: prices,
          });
        }
        return chartData;
      }
    });
  }
  if (document.getElementById('marketsChartKcsLight')) {
    am4core.ready(function () {
      // Create chart
      var chart = am4core.create('marketsChartKcsLight', am4charts.XYChart);

      chart.data = generateChartData();

      var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
      dateAxis.baseInterval = {
        timeUnit: 'minute',
        count: 1,
      };
      dateAxis.tooltip.disabled = true;
      dateAxis.renderer.grid.template.disabled = true;
      dateAxis.renderer.labels.template.disabled = true;
      dateAxis.renderer.ticks.template.disabled = true;
      dateAxis.renderer.paddingBottom = 15;

      var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
      valueAxis.tooltip.disabled = true;
      valueAxis.renderer.grid.template.disabled = true;
      valueAxis.renderer.labels.template.disabled = true;
      valueAxis.renderer.ticks.template.disabled = true;

      var series = chart.series.push(new am4charts.LineSeries());
      series.dataFields.dateX = 'date';
      series.dataFields.valueY = 'prices';
      series.tooltipText = 'prices: [bold]{valueY}[/]';
      series.fillOpacity = 0.1;
      series.fill = am4core.color('#f74745');
      series.stroke = am4core.color('#f74745');
      series.tooltip.getFillFromObject = false;
      series.tooltip.background.fill = am4core.color('#2a2e39');
      series.tooltip.background.stroke = am4core.color('#2a2e39');

      chart.cursor = new am4charts.XYCursor();
      chart.cursor.lineY.opacity = 1;
      dateAxis.start = 0;
      dateAxis.keepSelection = true;
      chart.zoomOutButton.background.fill = am4core.color(
        'rgba(0, 0, 0, 0.09)'
      );
      chart.zoomOutButton.icon.stroke = am4core.color('rgba(0, 0, 0, 0.40)');
      chart.zoomOutButton.background.states.getKey(
        'hover'
      ).properties.fill = am4core.color('#00cc93');

      function generateChartData() {
        var chartData = [];
        // current date
        var firstDate = new Date();
        // now set 500 minutes back
        firstDate.setMinutes(firstDate.getDate() - 500);

        // and generate 500 data items
        var prices = 500;
        for (var i = 0; i < 500; i++) {
          var newDate = new Date(firstDate);
          // each time we add one minute
          newDate.setMinutes(newDate.getMinutes() + i);
          // some random number
          prices += Math.round(
            (Math.random() < 0.5 ? 1 : -1) * Math.random() * 10
          );
          // add data item to the array
          chartData.push({
            date: newDate,
            prices: prices,
          });
        }
        return chartData;
      }
    });
  }

  if (document.getElementById('marketsChartBtcDark')) {
    am4core.ready(function () {
      // Create chart
      var chart = am4core.create('marketsChartBtcDark', am4charts.XYChart);

      chart.data = generateChartData();

      var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
      dateAxis.baseInterval = {
        timeUnit: 'minute',
        count: 1,
      };
      dateAxis.tooltip.disabled = true;
      dateAxis.renderer.grid.template.disabled = true;
      dateAxis.renderer.labels.template.disabled = true;
      dateAxis.renderer.ticks.template.disabled = true;
      dateAxis.renderer.paddingBottom = 15;

      var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
      valueAxis.tooltip.disabled = true;
      valueAxis.renderer.grid.template.disabled = true;
      valueAxis.renderer.labels.template.disabled = true;
      valueAxis.renderer.ticks.template.disabled = true;

      var series = chart.series.push(new am4charts.LineSeries());
      series.dataFields.dateX = 'date';
      series.dataFields.valueY = 'prices';
      series.tooltipText = 'prices: [bold]{valueY}[/]';
      series.fillOpacity = 0.1;
      series.fill = am4core.color('#00cc93');
      series.stroke = am4core.color('#00cc93');
      series.tooltip.getFillFromObject = false;
      series.tooltip.background.fill = am4core.color('#2a2e39');
      series.tooltip.background.stroke = am4core.color('#2a2e39');

      chart.cursor = new am4charts.XYCursor();
      chart.cursor.lineY.opacity = 1;
      dateAxis.start = 0;
      dateAxis.keepSelection = true;
      chart.zoomOutButton.background.fill = am4core.color(
        'rgba(255, 255, 255, 0.11)'
      );
      chart.zoomOutButton.icon.stroke = am4core.color('#ebebeb');
      chart.zoomOutButton.background.states.getKey(
        'hover'
      ).properties.fill = am4core.color('#00cc93');

      function generateChartData() {
        var chartData = [];
        // current date
        var firstDate = new Date();
        // now set 500 minutes back
        firstDate.setMinutes(firstDate.getDate() - 500);

        // and generate 500 data items
        var prices = 500;
        for (var i = 0; i < 500; i++) {
          var newDate = new Date(firstDate);
          // each time we add one minute
          newDate.setMinutes(newDate.getMinutes() + i);
          // some random number
          prices += Math.round(
            (Math.random() < 0.5 ? 1 : -1) * Math.random() * 10
          );
          // add data item to the array
          chartData.push({
            date: newDate,
            prices: prices,
          });
        }
        return chartData;
      }
    });
  }

  if (document.getElementById('marketsChartEthDark')) {
    am4core.ready(function () {
      // Create chart
      var chart = am4core.create('marketsChartEthDark', am4charts.XYChart);

      chart.data = generateChartData();

      var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
      dateAxis.baseInterval = {
        timeUnit: 'minute',
        count: 1,
      };
      dateAxis.tooltip.disabled = true;
      dateAxis.renderer.grid.template.disabled = true;
      dateAxis.renderer.labels.template.disabled = true;
      dateAxis.renderer.ticks.template.disabled = true;
      dateAxis.renderer.paddingBottom = 15;

      var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
      valueAxis.tooltip.disabled = true;
      valueAxis.renderer.grid.template.disabled = true;
      valueAxis.renderer.labels.template.disabled = true;
      valueAxis.renderer.ticks.template.disabled = true;

      var series = chart.series.push(new am4charts.LineSeries());
      series.dataFields.dateX = 'date';
      series.dataFields.valueY = 'prices';
      series.tooltipText = 'prices: [bold]{valueY}[/]';
      series.fillOpacity = 0.1;
      series.fill = am4core.color('#f74745');
      series.stroke = am4core.color('#f74745');
      series.tooltip.getFillFromObject = false;
      series.tooltip.background.fill = am4core.color('#2a2e39');
      series.tooltip.background.stroke = am4core.color('#2a2e39');

      chart.cursor = new am4charts.XYCursor();
      chart.cursor.lineY.opacity = 1;
      dateAxis.start = 0;
      dateAxis.keepSelection = true;
      chart.zoomOutButton.background.fill = am4core.color(
        'rgba(255, 255, 255, 0.11)'
      );
      chart.zoomOutButton.icon.stroke = am4core.color('#ebebeb');
      chart.zoomOutButton.background.states.getKey(
        'hover'
      ).properties.fill = am4core.color('#f74745');

      function generateChartData() {
        var chartData = [];
        // current date
        var firstDate = new Date();
        // now set 500 minutes back
        firstDate.setMinutes(firstDate.getDate() - 500);

        // and generate 500 data items
        var prices = 500;
        for (var i = 0; i < 500; i++) {
          var newDate = new Date(firstDate);
          // each time we add one minute
          newDate.setMinutes(newDate.getMinutes() + i);
          // some random number
          prices += Math.round(
            (Math.random() < 0.5 ? 1 : -1) * Math.random() * 10
          );
          // add data item to the array
          chartData.push({
            date: newDate,
            prices: prices,
          });
        }
        return chartData;
      }
    });
  }

  if (document.getElementById('marketsChartLtcDark')) {
    am4core.ready(function () {
      // Create chart
      var chart = am4core.create('marketsChartLtcDark', am4charts.XYChart);

      chart.data = generateChartData();

      var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
      dateAxis.baseInterval = {
        timeUnit: 'minute',
        count: 1,
      };
      dateAxis.tooltip.disabled = true;
      dateAxis.renderer.grid.template.disabled = true;
      dateAxis.renderer.labels.template.disabled = true;
      dateAxis.renderer.ticks.template.disabled = true;
      dateAxis.renderer.paddingBottom = 15;

      var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
      valueAxis.tooltip.disabled = true;
      valueAxis.renderer.grid.template.disabled = true;
      valueAxis.renderer.labels.template.disabled = true;
      valueAxis.renderer.ticks.template.disabled = true;
      var series = chart.series.push(new am4charts.LineSeries());
      series.dataFields.dateX = 'date';
      series.dataFields.valueY = 'prices';
      series.tooltipText = 'prices: [bold]{valueY}[/]';
      series.fillOpacity = 0.1;
      series.fill = am4core.color('#00cc93');
      series.stroke = am4core.color('#00cc93');
      series.tooltip.getFillFromObject = false;
      series.tooltip.background.fill = am4core.color('#131722');
      series.tooltip.background.stroke = am4core.color('#131722');

      chart.cursor = new am4charts.XYCursor();
      chart.cursor.lineY.opacity = 1;
      dateAxis.start = 0;
      dateAxis.keepSelection = true;
      chart.zoomOutButton.background.fill = am4core.color(
        'rgba(255, 255, 255, 0.11)'
      );
      chart.zoomOutButton.icon.stroke = am4core.color('#ebebeb');
      chart.zoomOutButton.background.states.getKey(
        'hover'
      ).properties.fill = am4core.color('#00cc93');

      function generateChartData() {
        var chartData = [];
        // current date
        var firstDate = new Date();
        // now set 500 minutes back
        firstDate.setMinutes(firstDate.getDate() - 500);

        // and generate 500 data items
        var prices = 500;
        for (var i = 0; i < 500; i++) {
          var newDate = new Date(firstDate);
          // each time we add one minute
          newDate.setMinutes(newDate.getMinutes() + i);
          // some random number
          prices += Math.round(
            (Math.random() < 0.5 ? 1 : -1) * Math.random() * 10
          );
          // add data item to the array
          chartData.push({
            date: newDate,
            prices: prices,
          });
        }
        return chartData;
      }
    });
  }
  if (document.getElementById('account-wallet-chart')) {
    am4core.ready(function () {
      // Create chart
      var chart = am4core.create('account-wallet-chart', am4charts.XYChart);

      chart.data = generateChartData();

      var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
      dateAxis.baseInterval = {
        timeUnit: 'minute',
        count: 1,
      };
      dateAxis.tooltip.disabled = true;
      dateAxis.renderer.grid.template.disabled = true;
      dateAxis.renderer.labels.template.disabled = true;
      dateAxis.renderer.ticks.template.disabled = true;
      dateAxis.renderer.paddingBottom = 15;

      var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
      valueAxis.tooltip.disabled = true;
      valueAxis.renderer.grid.template.disabled = true;
      valueAxis.renderer.labels.template.disabled = true;
      valueAxis.renderer.ticks.template.disabled = true;

      var series = chart.series.push(new am4charts.LineSeries());
      series.dataFields.dateX = 'date';
      series.dataFields.valueY = 'prices';
      series.tooltipText = 'prices: [bold]{valueY}[/]';
      series.fillOpacity = 0.1;
      series.fill = am4core.color('#007bff');
      series.stroke = am4core.color('#007bff');
      series.tooltip.getFillFromObject = false;
      series.tooltip.background.fill = am4core.color('#2a2e39');
      series.tooltip.background.stroke = am4core.color('#2a2e39');

      chart.cursor = new am4charts.XYCursor();
      chart.cursor.lineY.opacity = 1;
      dateAxis.start = 0;
      dateAxis.keepSelection = true;
      chart.zoomOutButton.background.fill = am4core.color(
        'rgba(0, 0, 0, 0.09)'
      );
      chart.zoomOutButton.icon.stroke = am4core.color('rgba(0, 0, 0, 0.40)');
      chart.zoomOutButton.background.states.getKey(
        'hover'
      ).properties.fill = am4core.color('#00cc93');

      function generateChartData() {
        var chartData = [];
        // current date
        var firstDate = new Date();
        // now set 500 minutes back
        firstDate.setMinutes(firstDate.getDate() - 500);

        // and generate 500 data items
        var prices = 500;
        for (var i = 0; i < 500; i++) {
          var newDate = new Date(firstDate);
          // each time we add one minute
          newDate.setMinutes(newDate.getMinutes() + i);
          // some random number
          prices += Math.round(
            (Math.random() < 0.5 ? 1 : -1) * Math.random() * 10
          );
          // add data item to the array
          chartData.push({
            date: newDate,
            prices: prices,
          });
        }
        return chartData;
      }
    });
  }
  // make tr linkable
  $('.markets-pair-list tbody tr').click(function () {
    window.location = $(this).data('href');
  });

  $('.markets-list-trade tr').click(function () {
    window.location = $(this).data('href');
  });
  // click to full screen
  function toggleFullscreen(elem) {
    elem = elem || document.documentElement;
    if (
      !document.fullscreenElement &&
      !document.mozFullScreenElement &&
      !document.webkitFullscreenElement &&
      !document.msFullscreenElement
    ) {
      if (elem.requestFullscreen) {
        elem.requestFullscreen();
      } else if (elem.msRequestFullscreen) {
        elem.msRequestFullscreen();
      } else if (elem.mozRequestFullScreen) {
        elem.mozRequestFullScreen();
      } else if (elem.webkitRequestFullscreen) {
        elem.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
      }
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.msExitFullscreen) {
        document.msExitFullscreen();
      } else if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen();
      } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
      }
    }
  }
  $('#clickFullscreen').on('click', function () {
    toggleFullscreen();
  });

  // data for market chart
  var optionsForIndiv = {
    bezierCurve: true,
    legend: {
      display: false,
    },
    scales: {
      xAxes: [
        {
          gridLines: {
            display: false,
            drawBorder: false,
          },
          ticks: {
            display: false,
          },
        },
      ],
      yAxes: [
        {
          gridLines: {
            display: false,
            drawBorder: false,
          },
          ticks: {
            display: false,
            beginAtZero: true,
          },
        },
      ],
    },
    elements: {
      point: {
        radius: 0,
      },
    },
  };

  // for market line chart
  var chartsIndiv = document.getElementsByClassName('markets-capital-chart');
  if (chartsIndiv.length > 0) {
    for (let chart of chartsIndiv) {
      let data = JSON.parse(chart.dataset.charts);
      let bg = chart.dataset.bg;
      let border = chart.dataset.border;

      let canvas = chart.querySelector('canvas');
      let ctx = canvas.getContext('2d');

      var gradient = ctx.createLinearGradient(255, 35, 19, 255);
      gradient.addColorStop(0.1, bg);
      gradient.addColorStop(1, 'transparent');
      let lineChartData = {
        labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        datasets: [
          {
            backgroundColor: gradient,
            borderColor: '#' + border,
            borderWidth: 2,
            data: data,
            bezierCurve: true,
          },
        ],
      };
      new Chart(ctx, {
        type: 'line',
        data: lineChartData,
        options: optionsForIndiv,
      });
    }
  }

  var chartsIndiv = document.getElementsByClassName(
    'markets-capital-chart-bar'
  );
  if (chartsIndiv.length > 0) {
    for (let chart of chartsIndiv) {
      let data = JSON.parse(chart.dataset.charts);
      let bg = chart.dataset.bg;
      let border = chart.dataset.border;

      let canvas = chart.querySelector('canvas');
      let ctx = canvas.getContext('2d');

      var gradient = ctx.createLinearGradient(255, 35, 19, 255);
      gradient.addColorStop(0.3, bg);
      gradient.addColorStop(1, 'transparent');
      let lineChartData = {
        labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        datasets: [
          {
            backgroundColor: gradient,
            borderColor: '#' + border,
            borderWidth: 2,
            data: data,
            bezierCurve: true,
          },
        ],
      };
      new Chart(ctx, {
        type: 'bar',
        data: lineChartData,
        options: optionsForIndiv,
      });
    }
  }

  // change theme
  var ThemeOn = false;
  $('#changeThemeLight').on('click', function (e) {
    ThemeOn = !ThemeOn;
    localStorage.setItem('theme', ThemeOn);
    if (ThemeOn) {
      $('#changeThemeLight a i').attr('class', 'icon ion-md-moon');
      $('header').attr('class', 'dark-bb');
      $('body').attr('id', 'dark');

      $('#searchParent').attr('style', 'background-Color: white');
      $('#inputBox').attr('style', 'background-Color: #131722');

      $('.navbar-brand img').attr('src', '/static/exchange/img/logo-light.svg');
    } else {
      $('#changeThemeLight a i').attr('class', 'icon ion-md-sunny');
      $('header').attr('class', 'light-bb');
      $('body').attr('id', 'light');

      $('#searchParent').attr('style', 'background-Color: aliceblue');
      $('#inputBox').attr('style', 'background-Color: aliceblue');

      $('.navbar-brand img').attr('src', '/static/exchange/img/logo-dark.svg');
    }
  });

  $('#changeThemeDark').on('click', function (e) {
    ThemeOn = !ThemeOn;
    localStorage.setItem('theme', ThemeOn);
    if (window.location.pathname.includes("/account/trade/") && !auto) {
      window.location.reload()
    }
    if (window.location.pathname.includes("/account/trade/")) {
      auto = false;
    }
    if (ThemeOn) {
      $('#changeThemeDark a i').attr('class', 'icon ion-md-sunny');

      $('#searchParent').attr('style', 'background-Color: aliceblue');
      $('#inputBox').attr('style', 'background-Color: aliceblue');

      $('header').attr('class', 'light-bb');
      $('body').attr('id', 'light');
      $('.navbar-brand img').attr('src', '/static/exchange/img/logo-dark.svg');
    } else {
      $('#changeThemeDark a i').attr('class', 'icon ion-md-moon');

      $('#searchParent').attr('style', 'background-Color: white');
      $('#inputBox').attr('style', 'background-Color: #131722');

      $('header').attr('class', 'dark-bb');
      $('body').attr('id', 'dark');
      $('.navbar-brand img').attr('src', '/static/exchange/img/logo-light.svg');
    }
  });
})(jQuery);

$(function() {     
      $('#buyPairChanger').on('click',function(e) {

          if ($(this).text() == "USDT")
             $(this).text(globPair)
          else
             $(this).text("USDT");
      });
  });

$(function() {     
      $('#sellPairChanger').on('click',function(e) {

          if ($(this).text() == "USDT")
             $(this).text(globPair)
          else
             $(this).text("USDT");
      });
  });