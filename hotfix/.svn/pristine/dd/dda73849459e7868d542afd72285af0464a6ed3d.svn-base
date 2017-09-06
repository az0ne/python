define(function(require, exports, module) { 

	var th;
	//-------------FUNTION-----------------.
	function personalCenterSjob(){
		init();
	}
	//------------FUNCTIONEND---------	
	//初始化
	var init=function(){
		$(".personalCenterSinfoList li .pcICO11").click(function(){
			$(this).parent().hide().next().show();
		});
		$(".personalCenterSinfoList li .tableU td.sub .personalCbtn").click(function(){
			$(this).parent().hide().prev().show();
			$(this).parent().prev().find("b").html($(this).prev().val());
			var dataT={"career_course_id":$(this).attr("pid"),"position":$(this).prev().val()};
			if($(this).hasClass("a2")){
				dataT={"career_course_id":$(this).attr("pid"),"industry":$(this).prev().val()};
			}
			$.ajax({
				type: "POST",
				url:"/home/s/ajax_save_job/",
				data:dataT,
				dataType:"html",
				beforeSend:function(XMLHttpRequest){
				},
				success: function(data) {
				},
				complete: function(XMLHttpRequest){
				}
			});
		});
		
	}	
	
	
	module.exports = {
		"init":personalCenterSjob
	};
	
})