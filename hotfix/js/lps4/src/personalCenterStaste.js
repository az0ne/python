define(function(require, exports, module) { 

	var th;
	//-------------FUNTION-----------------.
	function signUP(){
		init();
	}
	//------------FUNCTIONEND---------	
	//初始化
	var init=function(){		
		$(".personalCenterStasteList li").each(function(index, element) {
			var percents=$(element).find(".pcircle").attr("percents")
			if(percents){
				setTimeout(function(){
					percents=parseInt(percents,10);				
					$(element).find(".c").attr("stroke-dasharray",parseInt(percents/100*280,10)+" 280");
				},400);
			}
        });
		
	}	
	
	
	module.exports = {
		"init":signUP
	};
	
})