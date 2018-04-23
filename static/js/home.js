$(document).ready(function(){
    $('#FracSolverComponent').hide();
    $('#fracPracticeButton').on('click', function() {
        location.href = '/fraction_practice.html';
    })

    $('#RedFracButton').on('click', function() {
        location.href = '/reduction_practice.html';
    })

    $('#fracSolverButton').on('click', function() {
        $('#homeComponent').hide();
        $('#FracSolverComponent').show();
    })

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
    })

    $('#logout').on('click', function() {
        localStorage.clear();
        location.href = '/';
    })
});