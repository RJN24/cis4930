//function getBarGraphData(){
// $.get(
//        'http://localhost:5000/get_stats',
//        function (data) {
//            displayBarChart(data)
//        },
//        'json'
//        );
//}

$(document).ready(function(){
	$.ajax({
		url: 'http://localhost:5000/get_stats',
		method: "GET",
		success: function(data) {
			console.log(data);
			var scores = data;

//getBarGraphData();
	var chartData = {
				labels: player,
				datasets : [
					{
						label: 'Player Score',
						backgroundColor: 'rgba(200, 200, 200, 0.75)',
						borderColor: 'rgba(200, 200, 200, 0.75)',
						hoverBackgroundColor: 'rgba(200, 200, 200, 1)',
						hoverBorderColor: 'rgba(200, 200, 200, 1)',
						data: scores
					}
				]
			};

var ctx = document.getElementById('results_chart').getContext('2d');
var resultsChart = new Chart(ctx, {
  type: 'horizontalBar',
  data: chartData,
  backgroundColor: "rgba(80, 228, 251, 0.95)"
		});
		},
		error: function(data) {
			console.log(data);
		}
	});
//}
//})
})