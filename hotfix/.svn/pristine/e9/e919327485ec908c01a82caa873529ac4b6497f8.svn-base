//初始化
var init = function(){
	$(".personalCTop .font .personalCico").hover(function(){
		layer.tips($(this).attr("title"), $(this), {
		  tips: [1, '#333333'] //还可配置颜色
		});
	},function(){
		
	});		
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

init();