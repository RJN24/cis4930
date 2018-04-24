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
        let data = JSON.parse(localStorage.getItem('userdata'));
        let user = {"User": String(data.uid)};
        console.log(user);
        $.ajax({
            url: '/get_stats',
			data: JSON.stringify(user),
            type: 'POST',
			contentType: "application/json",
			dataType: "json",
		success: function(data) {
			console.log(data);
			var scores = data;
//getBarGraphData();
	var chartData = {
				labels: ['Level 1', 'Level 2', 'Level 3'],
				datasets : [
					{
						label: 'Player Score',
						backgroundColor: 'rgba(200, 200, 200, 0.75)',
						borderColor: 'rgba(200, 200, 200, 0.75)',
						hoverBackgroundColor: 'rgba(200, 200, 200, 1)',
						hoverBorderColor: 'rgba(200, 200, 200, 1)',
						data: [scores.user_level_1_average, scores.user_level_2_average, scores.user_level_3_average]
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