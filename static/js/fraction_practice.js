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
		level = "easy";
		$('#questions').find( "label" ).each(function(elem,index) {
		   $(this).text(generateEquationsWithAnswers(limit));
		});
		$('#fraction_practice').show();
		$('label').css("background-color", "");
		$('#questions').trigger("reset");
		$('#display_results').text("");
		results_per_level = {};
	});
	$('#medium').on('click', function(){
		//console.log('med');
		limit = 20;
		level = "medium";
		$('#questions').find( "label" ).each(function(elem,index) {
		   $(this).text(generateEquationsWithAnswers(limit));
		});
		$('#fraction_practice').show();
		$('label').css("background-color", "");
		$('#questions').trigger("reset");
		$('#display_results').text("");
		results_per_level = {};
	});
	$('#hard').on('click', function(){
		//console.log('hard');
		limit = 30;
		level = "hard";
		$('#questions').find( "label" ).each(function(elem,index) {
		   $(this).text(generateEquationsWithAnswers(limit));
		});
		$('#fraction_practice').show();
		$('label').css("background-color", "");
		$('#questions').trigger("reset");
		$('#display_results').text("");
		results_per_level = {};
		
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
	
	function operators(op, a, b, c, d) {
        if (op == '+') {
            return Number(a / b) + Number(c / d);
        }else if (op == '-'){
            return Number(a/b) - Number(c/d)
        }else if (op == '*') {
            return Number(a / b) * Number(c / d);
        }else {
            return Number(a / b) / Number(c / d);
        }
    }
	
	function generateEquationsWithAnswers(limit){
		//generate fraction
		let numerator1 = Math.floor(Math.random() * limit) + 1;
		let denominator1 = Math.floor(Math.random() * limit) + 1;
		let numerator2 = Math.floor(Math.random() * limit) + 1;
		let denominator2 = Math.floor(Math.random() * limit) + 1;

		let op_list = ['+', '-', '*', '/'];
		console.log(op_list);
		let randop = Math.floor(Math.random() * 4);
		console.log(randop);
		let op = op_list[randop];
		console.log(op);

		let question = numerator1 + '/' + denominator1 + " " + op + " " + numerator2 + '/' + denominator2;
		let answer = operators(op, numerator1, denominator1, numerator2, denominator2);
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

        let user = JSON.parse(localStorage.getItem('userdata'));
        let uid = user.uid;
        console.log(uid);
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
		
	});
	

});