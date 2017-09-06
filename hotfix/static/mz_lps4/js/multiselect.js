;(function($){
	var defaults = {
		model:"sort" 						//sort：排序，multiplechoice：多选
		,"arrayname":["时间升序","时间降序"]	//选项显示名称(类型Array)
		,"arrayvalue":[1,0]					//选项对应的值(类型Array)
		,"selectvalue":1					//选中项，对应arrayvalue中的值
		,"mcname":["全部","全部"]				//多选是所有的名称和值,[显示值，值],仅在model:multiplechoice中有效
		,"height":0							//显示高度 ,0不限制
		,onSelect:function(){}				//选中的触发事件
	};
	$.fn.multiselect=function(options){
		if(this.length == 0) return this;
		if(this.length > 1){
			this.each(function(){$(this).multiselect(options)});
			return this;
		}
		
		var slider = {};
		var el = this;
		
		var childNum=el.children().length;
		
		var init=function(){
			slider.settings = $.extend({}, defaults, options);
			slider.viewport=$(el);
			if(slider.settings.model=="sort"){initSort();}
			else if(slider.settings.model=="multiplechoice"){initMechoice();}
			slider.viewport.click(function(e){
				if(el.children(".zcheckbox").css("display")=="none")
					el.children(".zcheckbox").show();
				else{
					if(slider.settings.model=="sort") el.children(".zcheckbox").hide();
				}
				e.stopPropagation();	
			});
			$("body,html").click(function(e){
				if (e.target.className.indexOf(el.attr("class")) == -1) {
					$(".zcheckbox").hide();
				}
			});
		}
		el.goToSlideN=function(slideIndex){
			goToSlide(slideIndex,"next");
		}
		//---------------FUNTION------------------
		function sClick(e){
			$(this).addClass("dH").siblings().removeClass("dH");
			slider.settings.onSelect(e,$(this).attr("val"));
		}
		function smClick(e){
			if($(this).attr("val")==slider.settings.mcname[1]){
				$(this).addClass("sel").siblings().removeClass("sel");
			}
			else{
				$(this).parent().children().eq(0).removeClass("sel");
				($(this).hasClass("sel"))?$(this).removeClass("sel"):$(this).addClass("sel");
			}			
			var val=[];
			$(this).parent().children(".sel").each(function(index, element) {
				if($(this).attr("val")!=slider.settings.mcname[1])
                	val.push($(this).attr("val"))
            });
			slider.settings.onSelect(e,val);
		}
		function initSort(){
			var div=$("<div style='display:none;'></div>").addClass("zcheckbox times");
			div.html("<dl></dl>");
			var sortSign="up";
			for(var i=0;i<slider.settings.arrayname.length;i++){
				if(i!=0) sortSign='down';
				div.children().append('<dd class="'+sortSign+(slider.settings.selectvalue==slider.settings.arrayvalue[i]?' dH':'')+'" val="'+slider.settings.arrayvalue[i]+'"><i></i>'+slider.settings.arrayname[i]+'</dd>');
			}
			div.find("dd").click(sClick);
			slider.viewport.append(div);
		}
		function initMechoice(){
			var div=$("<div style='display:none;'></div>").addClass("zcheckbox multiselect");
			if(slider.settings.height!=0){div.css({"maxHeight":slider.settings.height+"px","overflow-y":"auto","overflow-x":"hidden"})}
			div.html("<dl></dl>");
			var optiondl=div.children();
			slider.settings.arrayname.insert(0,slider.settings.mcname[0]);
			slider.settings.arrayvalue.insert(0,slider.settings.mcname[1]);
			for(var i=0;i<slider.settings.arrayname.length;i++){
				optiondl.append('<dd class="'+(slider.settings.selectvalue==slider.settings.arrayvalue[i]?'sel':'')+'" val="'+slider.settings.arrayvalue[i]+'"><i></i>'+slider.settings.arrayname[i]+'</dd>');
			}
			div.find("dd").click(smClick);
			slider.viewport.append(div);
		}
		init();
		//返回jQuery对象
		return this;
	} 
})(jQuery)