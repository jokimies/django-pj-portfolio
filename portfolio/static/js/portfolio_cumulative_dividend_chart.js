/*
 *
 * This function used at /portfolio/txn/<id>/div
 *
 */

(function() {

    var thisYear = new Date().getFullYear();
    var prevYear = thisYear - 1;
    var thisMonth = new Date().getMonth();
    var years = [prevYear, thisYear];
    var seriesOptions = [],
    seriesCounter = 0;

    /* Cumulative dividend sum chart */
    var dividendOptionsCumulative = {
        chart: {
            renderTo: 'chart_panel',
            type: 'line',
        },
        legend: {enabled: false},
        title: {text: 'Cumulative dividends per month'},
        subtitle: {text: prevYear + ' and ' + thisYear},
        xAxis: {title: {text: null}, labels: {rotation: 0}},
	yAxis: {
            title: {
                text: 'Cumulative sum (€)'
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
	var yearUrl = "/portfolio/api/v1/transactions/dividend/" + year.toString() + "/";

	$.getJSON(yearUrl,
		  function(data) {
		      var cumulativeSums = [];
		      cumulativeSums[0] = data['chart_data']['sums'][0] 
		      for (j = 1; j < 12; j++) {
			  if (year === thisYear && j === thisMonth+1) {
			      break;
			  }
			  cumulativeSums[j] = cumulativeSums[j-1] + data['chart_data']['sums'][j] 
		      }

		      dividendOptionsCumulative.xAxis.categories = data['chart_data']['months'];
		      seriesOptions[i] = {
			  name: 'Year ' + year.toString(),
			  data: cumulativeSums
		      };
		      // As we're loading the data asynchronously, we don't know what order it will arrive. So
		      // we keep a counter and create the chart when all the data is loaded.
		      seriesCounter += 1;

		      if (seriesCounter === years.length) {
			  var chart = new Highcharts.Chart(dividendOptionsCumulative); 
		      }
		      
		  })
	    .fail(function() {
		console.log( "error" );
	    });
    });

})();
