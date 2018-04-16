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
                console.log("checking");
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
                    alert("false");
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
    // $('#EventSubmit').on('click', function() {
    //     $.ajax({
    //         url: '/newEvent',
    //         data: $('#newEventForm').serialize(),
    //         type: 'POST',
    //         success: function(response) {
    //             console.log(response);
    //         },
    //         error: function(error) {
    //             console.log(error);
    //         }
    //     });
    // });

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
                function(response)
                {
                    console.log(response);
                    $('#solverAns').text("Answer: " + response.fraction);
                    //fractionSolver();
                }
    })
    })

    $('#PopulateTable').on('click', function() {
        getTable();
    });

    $('#EventSubmit').on('click', function() {
        let user = JSON.parse(localStorage.getItem('userdata'));
        let tempForm = {
            username: user.username,
            eventName: $('#eventName').val(),
            eventTime: $('#eventTime').val(),
            eventUrl: $('#eventUrl').val()
        };
        console.log(tempForm)
        $.ajax({
            url: '/newEvent',
            data: tempForm,
            type: 'POST',
            success: function(response) {
                console.log(response);
                if(response.newEventStatus === true){
                    console.log('Event submit successful')
                    $('#eventName').val("");
                    $('#eventTime').val("");
                    $('#eventUrl').val("");
                    $('#errorMessageNewEvent').text('Success!')
                    $('#eventTableBody').append("<tr><td>" + tempForm.eventName + "</td><td>" + tempForm.eventTime + "</td><td>" + tempForm.eventUrl + "</td></tr>")
                }else{
                    $('#errorMessageNewEvent').text('Event submittal failed. Try again.')
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    function populateUser(){
        let user = JSON.parse(localStorage.getItem('userdata'));
        console.log(user)
        $('#greeting').append(user.username)
    }

    function getTable(){
        tempuser = localStorage.getItem('userdata');
        let parseduser;
        if (tempuser) {
            parseduser = JSON.parse(tempuser);
            let username = parseduser.username;
            console.log(username)
            $.ajax({
                url: '/getEvents',
                data: {
                    temp: username
                },
                contentType: 'application/json',
                dataType: 'json',
                type: 'GET',
                success: function(response) {
                    console.log(response);
                    // $('#PopulateTable').hide();
                    $('#eventTableBody').empty();
                    localStorage.setItem('userevents', JSON.stringify(response.events))
                    response.events.forEach(function(val){
                        $('#eventTableBody').append("<tr><td>" + val.eventName + "</td><td>" + val.eventTime + "</td><td>" + val.eventUrl + "</td></tr>")
                    })
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    }
});
