define(function(require, exports, module) {
    var $ = require('jquery');
    require('./bxslider.js')($);
    $('.teach_bxslider,.stu_bxslider').bxSlider({
        captions: true,
        auto: true
    });

	function addNodes(){	
	    var nodesNum = 0;    
	    function addNodes(myId,myNodes){
	        nodesNum = myId.length;
	        myNodes.append("<em>/ "+nodesNum+"</em>");
	    }
	   	addNodes($(".addTeacher_container .works_bxslider .bx-pager-item"),$(".works_bxslider .bx-pager"));
		addNodes($(".addTeacher_container .student_bxslider .bx-pager-item"),$(".student_bxslider .bx-pager"));
	}
	addNodes();
	
	var evt = "onorientationchange" in window ? "orientationchange" : "resize";
	window.addEventListener(evt,function(){
	 	addNodes();
	});

	var teacherIntroduceDiv = $('.addTeacher_banner .teacher');
	teacherIntroduceDiv.css({"height":teacherIntroduceDiv.height(),"margin-top":(470-teacherIntroduceDiv.height())/2});
});
