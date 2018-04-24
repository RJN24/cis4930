$(document).ready(function(){
    $('#FracSolverComponent').hide();
    $('#fracPracticeButton').on('click', function() {
        location.href = '/fraction_practice.html';
    });

    $('#RedFracButton').on('click', function() {
        location.href = '/reduction_practice.html';
    });

    $('#fracSolverButton').on('click', function() {
        $('#homeComponent').hide();
        $('#FracSolverComponent').show();
    });

    $('#EnterFrac').on('click', function() {
        $.ajax({
            url: '/home.html/fracSolver',
            data: $('#formFracInput').serialize(),
            type: 'POST',
            success:
                function (response) {
                    console.log(response);
                    $('#solverAns').text("Answer: " + response.fraction);
                    $('#frac').val("");
                    //fractionSolver();
                }
        })
    });

    $('#Results').on('click', function() {
        let data = JSON.parse(localStorage.getItem('userdata'));
        let user = {"User": String(data.uid)};
        console.log(user);
        $.ajax({
            url: '/get_stats',
			data: JSON.stringify(user),
            type: 'POST',
			contentType: "application/json",
			dataType: "json",
            success: function(response) {
                console.log('submitted');
                console.log(response)
            },
            error: function(error) {
				console.log('ERROR');
				console.log(error);
            }
        });
        location.href = '/static/results.html';
    });

    $('#logout').on('click', function() {
        localStorage.clear();
        location.href = '/';
    })
});