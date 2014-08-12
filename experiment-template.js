var numberOfQuestions = 10; 

// or if you have a fixed stim set that all participants will see, use
//		var numberOfQuestions = stimuli.length;
//		var stimuli = shuffle([YOUR_STIMULI]);
// and then in the stepExperiment function, on each trial pick a random stimulus using
// 		var thisTrialStimulus = stimuli.shift();

$(document).ready(function() {
    showSlide("instructions");
    $("#instructions #mustaccept").hide();
});

var data = {};

function intro () {
	if (turk.previewMode) {
    	$("#instructions #mustaccept").show();
	} else {
    	showSlide("intro");
    }
}

var counter = 0;

function stepExperiment () {
	if (counter < numberOfQuestions) {
// or "if (stimuli.length > 0) {...}", etc: test whether it's time to end the experiment
		counter = counter + 1;
		var startTime = (new Date()).getTime();
		showSlide("stage");
		qdata = {};
// insert main experiment code here
    	$("#continue").click(function() {
    		if (ANSWER_IS_NOT_VALID) {
// test for answer meeting relevant parameters -- e.g., all questions answered
// if no, show some text saying so and ask them to answer appropriately
    		} else { // advance to next question
    			$("#continue").unbind('click'); 
// unbind this fxn from the button after use, so we can reuse the button
    			qdata.questionOrder = counter;
    			qdata.rt = (new Date()).getTime() - startTime;
    			data['q' + counter + 'data'] = qdata; 
// add trial data to data array, which we'll eventually submit to MTurk
    			experiment.next();
    		}
    	});
// if you're using a progress bar, uncomment next line to advance that
// $('.bar').css('width', (200.0 * counter / numberOfQuestions) + 'px');	
    } else {
    	showSlide("debrief");
	    $("#lgerror").hide();
	    $("#lgbox").keypress(function(e){ 
// Important! This function captures return so that it doesn't restart experiment!
	    	if (e.which == 13) {
	    		return false;
	    	}
	    });
	    $("#debriefSubmit").click(function(){
// tailor this function to your debrief questions.
			var lang = document.getElementById("lgbox").value;
			if (lang.length > 5) {
			    data.push(lang);
			    showSlide("finished");
			    setTimeout(function() { turk.submit({data})}, 1000);
			}
			return false;
		});
    }
}

function showSlide(id) {
	$(".slide").hide();
	$("#"+id).show();
}

function shuffle(v) { // non-destructive.
    newarray = v.slice(0);
    for(var j, x, i = newarray.length; i; j = parseInt(Math.random() * i), x = newarray[--i], newarray[i] = newarray[j], newarray[j] = x);
    return newarray;
};

function random(a,b) {
    if (typeof b == "undefined") {
	a = a || 2;
	return Math.floor(Math.random()*a);
    } else {
	return Math.floor(Math.random()*(b-a+1)) + a;
    }
}

Array.prototype.random = function() { return this[random(this.length)]; }