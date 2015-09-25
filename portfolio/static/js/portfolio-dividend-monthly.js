/*
 *
 * This function used on /portfolio/txn/1/divbyyear/<year>/
 *
 */
(function() {

    var divYear = $('#dividendYear').text();
    var prevDivYear = (parseInt(divYear) - 1).toString();
    var years = [prevDivYear, divYear];
    var seriesOptions = [],
    seriesCounter = 0;

    // Dividends by month chart
     var dividendOptions = {
        chart: {
            renderTo: 'chart_panel',
            type: 'column',
        },
        legend: {enabled: false},
        title: {text: 'Dividends per month'},
        subtitle: {text: divYear + ' and ' + prevDivYear},
        xAxis: {title: {text: null}, labels: {rotation: 0}},
	yAxis: {
            title: {
                text: 'Dividend per month (€)'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: seriesOptions,
    };

    $.each(years, function (i, year) {
	var chartDataUrl = "/portfolio/api/v1/transactions/dividend/" + year + "/";
	$.getJSON(chartDataUrl,
		  function(data) {
		      dividendOptions.xAxis.categories = data['chart_data']['months'];
		      seriesOptions[i] = {
			  name: 'Year ' + year,
			  data: data['chart_data']['sums']
		      };
		      // As we're loading the data asynchronously, we don't know what order it will arrive. So
		      // we keep a counter and create the chart when all the data is loaded.
		      seriesCounter += 1;
		      if (seriesCounter === years.length) {
			  var chart = new Highcharts.Chart(dividendOptions);
		      }
		  })
	    .fail(function() {
		console.log( "error" );
	    });
    });
}) ();

