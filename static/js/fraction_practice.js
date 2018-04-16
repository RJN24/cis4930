$(document).ready(function(){
	let questions = {}, results_per_level = {}, final_results = {};
	let limit = null;
	let numCorrect = 0;
	let operation = null, level = null;
	
	
	$('#fraction_practice').hide();
	$('#select_operator').hide();
	
	$('#easy').on('click', function(){
		//console.log('easy');
		limit = 10;
		$('#select_difficulty').hide();
		$('#select_operator').show();
		$('#addition_button').trigger('click');
		level = "easy";
	});
	$('#medium').on('click', function(){
		//console.log('med');
		limit = 20;
		$('#select_difficulty').hide();
		$('#select_operator').show();
		$('#addition_button').trigger('click');
		level = "medium";
	});
	$('#hard').on('click', function(){
		//console.log('hard');
		limit = 30;
		$('#select_difficulty').hide();
		$('#select_operator').show();
		$('#addition_button').trigger('click');
		level = "hard";
		
	});	
	
	$('#addition_button').on('click', function(){
		questions = {};
		$('#questions').find( "label" ).each(function(elem,index) {
		   $(this).text(generateEquationsWithAnswers("+", limit));
		});
		$('#fraction_practice').show();
		operation = "Addition";
		$('label').css("background-color", "");
		$('#questions').trigger("reset");
		$('#display_results').text("");
		results_per_level = {};
		//console.log(questions);

	});
	$('#subtraction_button').on('click', function(){
		questions = {};
		$('#questions').find( "label" ).each(function(elem,index) {
		   $(this).text(generateEquationsWithAnswers("-", limit));
		});
		$('#fraction_practice').show();
		operation = "Subtraction";
		$('label').css("background-color", "");
		$('#questions').trigger("reset");
		$('#display_results').text("");
		results_per_level = {};
		//console.log(questions);
	});
	$('#multiplication_button').on('click', function(){
		questions = {};
		$('#questions').find( "label" ).each(function(elem,index) {
		   $(this).text(generateEquationsWithAnswers("*", limit));
		});
		$('#fraction_practice').show();
		operation = "Multiplication";
		$('label').css("background-color", "");
		$('#questions').trigger("reset");
		$('#display_results').text("");
		results_per_level = {};
		//console.log(questions);
	});
	$('#division_button').on('click', function(){
		questions = {};
		$('#questions').find( "label" ).each(function(elem,index) {
		   $(this).text(generateEquationsWithAnswers("/", limit));
		});
		$('#fraction_practice').show();
		operation = "Division";
		$('label').css("background-color", "");
		$('#questions').trigger("reset");
		$('#display_results').text("");
		results_per_level = {};
		//console.log(questions);
	});
	
	$('#level_button').on('click', function(){
		$('#fraction_practice').hide();
		$('#select_operator').hide();
		$('#select_difficulty').show();
		results_per_level = {};
		final_results = {};
	});
	
	function gcd_rec(a, b) {
		if (b) {
			return gcd_rec(b, a % b);
		} else {
			return Math.abs(a);
		}
	}
	
	var operators = {
    '+': function(a, b, c, d) { return Number(a/b) + Number(c/d) },
    '-': function(a, b, c, d) { return Number(a/b) - Number(c/d) },
	'*': function(a, b, c, d) { return Number(a/b) * Number(c/d) },
	'/': function(a, b, c, d) { return Number(a/b) / Number(c/d) }
    };
	
	function generateEquationsWithAnswers(op, limit){
		//generate fraction
		let numerator1 = Math.floor(Math.random() * limit) + 1;
		let denominator1 = Math.floor(Math.random() * limit) + 1;
		let numerator2 = Math.floor(Math.random() * limit) + 1;
		let denominator2 = Math.floor(Math.random() * limit) + 1;

		let question = numerator1 + '/' + denominator1 + " " + op + " " + numerator2 + '/' + denominator2;
		let answer = operators[op](numerator1, denominator1, numerator2, denominator2);
		questions[question] = answer;
		//console.log(question);
		return question;
	}		
		
	function reduced(a, b){
		let gcf = gcd_rec(a, b);
		//console.log(gcf);
		if(gcf != 1){ 
			return false;
		}
		return true;
	}

	$('#save').on('click', function() {
		$('#questions').find("input[type=text]").each(function(elem,index) {
			//console.log($(this).val());
			let user_answer = $(this).val().match(/(-?\d+)(?=\/{1}(-?\d+)|)/).slice(1).map(Number);
			
			$this = $(this);
			$label = $('label[for="'+ $this.attr('id') +'"]');
			if ($label.length > 0 ) {
				if(user_answer[1] === NaN && questions[$label.text()] === user_answer[0]){
					//console.log('correct');
					$label.css("background-color", "green");
					numCorrect += 1;
				}
				else if(user_answer[1] === 1 || !reduced(user_answer[0], user_answer[1])){
					//console.log('not reduced');
					$label.css("background-color", "yellow");
				}
				else if (questions[$label.text()] === user_answer[0]/user_answer[1]){
					//console.log("correct");
					$label.css("background-color", "green");
					numCorrect += 1;
				}
				else{
					//console.log("incorrect");
					$label.css("background-color", "red");
				}
			}
			
		});
		//console.log("Number correct for " + operation + " : " + numCorrect);


		results_per_level[operation] = numCorrect;


		final_results[level] = results_per_level;

        console.log(final_results);
        $('#display_results').text("Level " + level + " : " + results_per_level[operation] + "/10 correct");
		$.ajax({
            url: '/results',
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
		
	});
	

});