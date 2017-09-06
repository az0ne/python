define(function(require, exports, module) { 
	var th;
	//-------------FUNTION-----------------.
	function personalCenter(){
		init();
	}
	//------------FUNCTIONEND---------	
	//初始化
	var init=function(){		
		$(".pCcourseList li").each(function(index, element) {
			var percents=$(element).find(".pcircle").attr("percents");
			if(percents){
				setTimeout(function(){
					percents=parseInt(percents,10);				
					$(element).find(".c").attr("stroke-dasharray",parseInt(percents/100*280,10)+" 280");
				},400);
			}
        });

		var isRegist = $('#user_center_course_record').val();// $('#');
		//模块弹出
		if(isRegist == 'true'){
			$("#interestCourse").modal('show');
		}

		var index = 0,oLis,oSpan;
			oLis = $("#interestCourse .modal-body li");
			oSpan = $("#interestCourse .modal-footer span");
		oSpan.click(function(){
			pages = parseInt((oLis.length-1)/6);//获取页数
			if(index < pages){
				index++;
			}else{
				index = 0;
			}
			//隐藏所以li,再显示需要显示的li
			oLis.hide().slice(6*index,6*(index+1)).fadeIn();
		});

		if(oLis.length<=6){
			oSpan.unbind("click");//当li个数小于等于6个时，取消点击事件
		};
		
	}

	
	module.exports = {
		"init":personalCenter
	};
	
})