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
						label: 'User Average Score',
						backgroundColor: 'rgba(12, 88, 252, 0.97)',
						borderColor: 'rgba(200, 200, 200, 0.75)',
						hoverBackgroundColor: 'rgba(12, 88, 252, 0.07)',
						hoverBorderColor: 'rgba(200, 200, 200, 1)',
						data: [(scores.user_level_1_average *100) , (scores.user_level_2_average*100), (scores.user_level_3_average*100)]
					},{
                        label: 'Total Average Score',
                        backgroundColor: 'rgba(153,255,51,1)',
						borderColor: 'rgba(200, 200, 200, 0.75)',
						hoverBackgroundColor: 'rgba(12, 88, 252, 0.07))',
						hoverBorderColor: 'rgba(200, 200, 200, 1)',
						data: [(scores.all_level_1_average*100), (scores.all_level_2_average*100), (scores.all_level_3_average*100)]
					}
				]
			};

var ctx = document.getElementById('results_chart').getContext('2d');
var resultsChart = new Chart(ctx, {
  type: 'horizontalBar',
  data: chartData
		});
		},
		error: function(data) {
			console.log(data);
		}
	});
//}
//})
})