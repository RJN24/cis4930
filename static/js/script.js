$(document).ready(function(){
    $('#FracSolverComponent').hide();
    $('#homeComponent').hide();
    $('#Login').on('click', function() {
        $.ajax({
            url: '/login',
            data: $('#formLogin').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                if(response.auth === true){
                    localStorage.setItem('userdata', JSON.stringify(response.user));
                    if($( '#loginComponent' ).is(":visible")){
                        $('#loginComponent').hide();
                        $('#FracSolverComponent').hide();

                        $('#homeComponent').show();
                    }

                    else{
                        $('#homeComponent').show();
                        $('#FracSolverComponent').hide();
                    }

                }else{
                    $('#errorMessageLogin').text('Incorrect username and/or password.')
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
    $('#Register').on('click', function() {
        $.ajax({
            url: '/register',
            data: $('#formRegister').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                if(response.registered === true){
                    $('#myForm').trigger("reset");
                    $('#errorMessageReg').text('Registration successful!')
                }else{
                    $('#errorMessageReg').text('Registration failed. Try again.')
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('#fracSolverButton').on('click', function() {
        $('#homeComponent').show();
        $('#FracSolverComponent').show();
    })

    $('#EnterFrac').on('click', function() {
        $.ajax({
            url: '/fracSolver',
            data: $('#formFracInput').serialize(),
            type: 'POST',
            success:
                function (response) {
                    console.log(response);
                    $('#solverAns').text("Answer: " + response.fraction);
                    //fractionSolver();
                }
        })
    })
    $('#fracPracticeButton').on('click', function() {
        location.href = '/fraction_practice.html';
    })
});