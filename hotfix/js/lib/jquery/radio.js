/*******************************
* radio
* @author 验收时间
* @2013.05.20
*******************************/
define(function() { return function($) {
;(function($){
	$.fn.statisticsRadio=function(){
		if(this.length == 0) return this;
		if(this.length > 1){
			this.each(function(){$(this).statisticsRadio()});
			return this;
		}
		var th=this;
		th.children("input").click(function(){
			$("input[name='"+this.name+"']").each(function(index, element) {
                if(element.checked){
					$(this).parent().addClass("rH");
				}
				else{
					$(this).parent().removeClass("rH");
				}
            });
		});
	}
})(jQuery)
}});
