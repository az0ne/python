/* Damon: Progress Bar*/
// function progressBarSim(al){
// 	var bar = $('#progressBar');
// 	var status = $('#status');
// 	status.html(al + '%');
// 	bar.val(al);
// 	al++;
	
// 	var sim = setTimeout('progressBarSim('+ al +')',300);

// 	if(al == 100){
// 		status.html('100%');
// 		bar.val(100);
// 		clearTimeout(sim);
// 		$('#finalMessage').html('Progress is complete');
// 	}
// }

// var amountLoaded = 0;
// progressBarSim(amountLoaded);

(function( $ ){
  // Simple wrapper around jQuery animate to simplify animating progress from your app
  // Inputs: Progress as a percent, Callback
  // TODO: Add options and jQuery UI support.
  $.fn.animateProgress = function(progress,speed, callback) {    
    return this.each(function() {
		if(!speed) speed=2000;
      $(this).animate({
        width: progress+'%'
      }, {
        duration: speed,
        easing: 'swing',
        step: function( progress ){
          var labelEl = $('#d-status', this),
              valueEl = $('.d-value');
          valueEl.text(Math.ceil(progress) + '%');
        },
        complete: function(scope, i, elem) {
          if (callback) {
            callback.call(this, i, elem );
          };
        }

      });
    });
  };
})( jQuery );


