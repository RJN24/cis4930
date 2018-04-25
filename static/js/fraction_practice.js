$(document).ready(function(){



	let questions = {}, final_results = {};
	let numCorrect = null;
	let operation = null, level = null;

	$('#fraction_practice').hide();

	$('#easy').on('click', function(){
	    $('span').text("");
	    questions = {};
		//console.log('easy');
		level = "easy";
		$('#questions').find( "label" ).each(function(elem,index) {
		   $(this).text(generateEquationsWithAnswers(level, 10));
		});
		$('#fraction_practice').show();
		$('#questions').trigger("reset");
		$('#display_results').text("");
		console.log(questions);
	});
	$('#medium').on('click', function(){
		question = {};
		level = "medium";
		$('#questions').find( "label" ).each(function(elem,index) {
		   $(this).text(generateEquationsWithAnswers(level, 10));
		});
		$('#fraction_practice').show();
		$('span').text("");
		$('#questions').trigger("reset");
		$('#display_results').text("");
	});
	$('#hard').on('click', function(){
	    $('span').text("");
	    questions = {};
		//console.log('hard');
		level = "hard";
		$('#questions').find( "label" ).each(function(elem,index) {
		   $(this).text(generateEquationsWithAnswers(level, 20));
		});
		$('#fraction_practice').show();
		$('label').css("background-color", "");
		$('#questions').trigger("reset");
		$('#display_results').text("");
	});

	function gcd_rec(a, b) {
		if (b) {
			return gcd_rec(b, a % b);
		} else {
			return Math.abs(a);
		}
	}

	function operators(op, a, b, c, d) {
        if (op == '+') {
            //return Number(a / b) + Number(c / d);
            return (new Fraction(a,b)).add(new Fraction(c,d));
        }else if (op == '-'){
            //return Number(a/b) - Number(c/d)
            return (new Fraction(a,b)).subtract(new Fraction(c,d));
        }else if (op == '*') {
            //return Number(a / b) * Number(c / d);
            return (new Fraction(a,b)).multiply(new Fraction(c,d));
        }else {
            //return Number(a / b) / Number(c / d);
            return (new Fraction(a,b)).divide(new Fraction(c,d));
        }
    }

	function generateEquationsWithAnswers(level, limit){
	    let op_list = ['+', '-', '*', '/'];
        let numerator1, denominator1, numerator2, denominator2;

	    if (level === "easy"){
	        denominator1 = Math.floor(Math.random() * (9 - 1) + 1);
	        denominator2 = denominator1;
            numerator1 = Math.floor(Math.random() * (9 - 1) + 1);
            numerator2 = Math.floor(Math.random() * (9 - 1) + 1);


	    }
	    else if (level === "medium"){
	        denominator1 = Math.floor(Math.random() * (9 - 1) + 1);
	        denominator2 = Math.floor(Math.random() * (9 - 1) + 1);
            numerator1 = Math.floor(Math.random() * (9 - 1) + 1);
            numerator2 = Math.floor(Math.random() * (9 - 1) + 1);
	    }
	    else{
	        denominator1 = Math.floor(Math.random() * limit) + 10;
	        denominator2 = Math.floor(Math.random() * limit) + 10;
            numerator1 = Math.floor(Math.random() * limit) + 10;
            numerator2 = Math.floor(Math.random() * limit) + 10;
	    }

		let randop = Math.floor(Math.random() * 4);
		let op = op_list[randop];

		let question = numerator1 + '/' + denominator1 + " " + op + " " + numerator2 + '/' + denominator2;
		let answer = operators(op, numerator1, denominator1, numerator2, denominator2);
		questions[question] = answer;
		//console.log(question);
		return question;
	}


	function reduced(a){
		let gcf = gcd_rec(a.numerator, a.denominator);
		if(gcf != 1){
			return false;
		}
		return true;
	}

    function equalFractions(a,b){
        return a.numerator === b.numerator && a.denominator === b.denominator;
    }

    function printCorrectAnswer(a){
        if(a.denominator != 1){
            return a.numerator + "/" +a.denominator;
        }
        else
            return a.numerator;

    }

	$('#save').on('click', function(event) {
		numCorrect = 0;
        let submit_form = true;

		$('#questions').find("input[type=text]").each(function(elem,index) {
		    let user_answer = null;
            $this = $(this);
            $label = $('label[for="'+ $this.attr('id') +'"]');
            $span = $('span[for="'+ $this.attr('id') +'"]');
            let correct_answer = questions[$label.text()];

			if ($(this).val() === ''){ //empty field
			    //tell user invalid response
			    $span.text("*Please provide an answer").css("color", "red");
			    submit_form = false;
			    return;
			}

			try{
			    user_answer = $(this).val().match(/(-?\d+)(?=\/{1}(-?\d+)|)/).slice(1).map(Number);
            }
            catch(err){
                $span.text("*Please enter a fraction or integer for an answer").css("color", "red");
                submit_form = false;
			    return;
            }

            if(isNaN(user_answer[1])){ //one integer for answer
                if(correct_answer.denominator === 1 && user_answer[0] === correct_answer.numerator){
                    console.log("correct");
                    $span.text("Correct").css("color", "green");
                    numCorrect += 1;
                }
                else{
                    console.log("incorrect");
                    $span.text("Wrong, Correct answer: " + printCorrectAnswer(correct_answer)).css('color', 'red');
                }
            }
            else{
                user_answer = { numerator: user_answer[0], denominator: user_answer[1] };
                if(user_answer.denominator === 1 || (user_answer.numerator/user_answer.denominator ===  correct_answer.numerator/correct_answer.denominator && !reduced(user_answer))){
                    console.log("not reduced");
                    $span.text("Not Reduced").css("color", "yellow").css("background-color", "SeaShell");;
                }
                else if(equalFractions(user_answer, correct_answer)){
                    console.log("correct");
                    $span.text("Correct").css("color", "green");
                    numCorrect += 1;
                }
                else{
                    console.log("incorrect");
                    $span.text("Wrong, Correct answer: " + printCorrectAnswer(correct_answer)).css('color', 'red');
                }
            }






		});

        if(submit_form != false){
            $('#display_results').text("For Level " + level + " Number Correct: " + numCorrect + "/10");
            let user = JSON.parse(localStorage.getItem('userdata'));
            let uid = user.uid;
            let final_results = {"User": String(uid), "Level": level, "Correct": numCorrect};

            console.log(final_results);
            $('#display_results').text(numCorrect + "/10 for level: " + level);
            $.ajax({
                url: '/post_results',
                data: JSON.stringify(final_results),
                type: 'POST',
                contentType: "application/json",
                dataType: "json",
                success: function(response) {
                    console.log('submitted');
                },
                error: function(error) {
                    console.log('ERROR');
                    console.log(error);
                }
            });

        }


	});
});
