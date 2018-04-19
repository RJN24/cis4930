var ctx = document.getElementById('results_chart').getContext('2d');
var resultsChart = new Chart(ctx, {
  type: 'horizontalBar',
  data: {
    labels: ['Your Score:', 'Average Score:', 'High Score'],
    datasets: [{
      label: 'Scores',
      data: [3,12,20],
      backgroundColor: "rgba(80, 228, 251, 0.95)"
    }]
  }
});