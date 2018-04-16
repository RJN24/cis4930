$(document).ready(function(){
	
	function gcd_rec(a, b) {
		if (b) {
			return gcd_rec(b, a % b);
		} else {
			return Math.abs(a);
		}
	}
	
	
	let numerator = null, denominator = null;
	function generateFraction(){
		//generate fraction
		numerator = Math.floor(Math.random() * 20) + 1;
		denominator = Math.floor(Math.random() * 20) + 1;
		$('#fraction').text(numerator + "/" + denominator);
		let gcf = gcd_rec(numerator, denominator);
		
		
		if(gcf != 1){ 
			numerator /= gcf;
			denominator /= gcf;
		}

	}
	

	generateFraction();

	$('#form_Answer').submit(function( event ) {
		
		let answer = $('#answer').val().match(/(-?\d+)(?=\/{1}(-?\d+)|)/).slice(1).map(Number);
		
		if(numerator === answer[0] && denominator === answer[1]){
			$('#feedback').text('Correct.');
		}
		else if(denominator === 1 && numerator === answer[0]){
			$('#feedback').text('Correct.');
		}
		else{
			let correction = 'Incorrect. The correct answer was ' + numerator + "/" + denominator;
			if(denominator === 1){
				correction += ' or' + numerator;
			}
			$('#feedback').text(correction);

		}
		
		
		
		
			
	});

});