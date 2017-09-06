/*******************************
* 查询筛选框
* @author ZhouYi
* @2016.03.14
*******************************/
;(function($){
	var defaults = {
		topLayerCss:"topLayerTxt" 		//顶层框css
		,"layerdlCss":"fLayerdl"		//选项css
		,"height":100					//下拉框滚动的高度,0为不设高度
        ,"boEnter":false                //回车触发搜索
		,onVclick:function(){}			//选值事件 	function(value)
		,onkeyup:function(){}			//keyup事件
		,onarrowupdown:function(){}		//上线箭头的回调事件	function(i),i为0是上，1为下
        ,onload:function(){}            //加载完成
	};
	$.fn.textFiltered=function(options){
		if(this.length == 0) return this;
		if(this.length > 1){
			this.each(function(){$(this).textFiltered(options)});
			return this;
		}

		var slider = {};
		var el = this;

		var childNum=el.children().length;

		var init=function(){
			slider.settings = $.extend({}, defaults, options);
			slider.viewport=$(el);
			slider.viewport.addClass("sManage_Seltxt");
			var div=$('<div></div>').addClass(slider.settings.topLayerCss);
			slider.dl=$("<dl></dl>").addClass(slider.settings.layerdlCss).css("display","none");
			if(slider.settings.height!=0) slider.dl.css({"maxHeight":slider.settings.height+"px","overflow-y":"auto"});
			slider.viewport.replaceWith(div);
			div.append(slider.viewport).append(slider.dl);
			var arrayCode=[20,16,17,91,18,37,39];
			slider.viewport.keyup(function(e){
				if(e.keyCode==38||e.keyCode==40){
					var i=0;if(e.keyCode==40) i=1;
					var dH=slider.dl.find(".dH");
					if(i){
						if(dH.length==0){
							slider.dl.children().eq(0).addClass("dH")
						}
						else{
							(dH.next().length>0)&&(dH.removeClass("dH").next().addClass("dH"));
							if(dH.offset().top-dH.parent().offset().top+dH.height()>=slider.settings.height){
								slider.dl.animate({"scrollTop":slider.dl.scrollTop()+dH.height()},100);
							}
						}
					}
					else{
						if(dH.length==0){
							slider.dl.children(":last-child").addClass("dH");
							slider.dl.animate({"scrollTop":1000},100);
						}
						else{
							(dH.prev().length>0)&&(dH.removeClass("dH").prev().addClass("dH"));
							if(dH.offset().top-dH.parent().offset().top<slider.dl.scrollTop()){
								slider.dl.animate({"scrollTop":slider.dl.scrollTop()-dH.height()},100);
							}
						}
					}

					slider.settings.onarrowupdown(i);
				}
				else if(e.keyCode==13){
					if(slider.dl.find(".dH").length>0){el.val(slider.dl.find(".dH").html());slider.dl.hide();slider.settings.onVclick.call(el,slider.dl.find(".dH").attr("val"),slider.dl.find(".dH").attr("v2"));}
                    else if(slider.settings.boEnter){
                        slider.settings.onkeyup.call(el,true);
                    }
				}
				else if(arrayCode.indexOf(e.keyCode)<0){
					el.clear();
					slider.settings.onkeyup.call(el);
					slider.dl.show();
				}
			});
			slider.viewport.dblclick(function(e){
				el.clear();
				slider.settings.onkeyup.call(el);
				slider.dl.show();
			})
			slider.dl.click(function(ev){
				var ev = ev || window.event;
    			var target = ev.target || ev.srcElement;
				el.val(target.innerHTML);
				slider.settings.onVclick.call(el,target.getAttribute("val"),target.getAttribute("v2"));
			})
			$("body,html").click(function(e){
				if (e.target.className.indexOf("sManage_Seltxt") == -1) {
					slider.dl.hide();
				}
			});
            slider.settings.onload.call(el);
		}
		el.addNode=function(key,value,v2){
			slider.dl.append('<dd val="'+key+'" v2="'+v2+'">'+value+'</dd>')
		}
		el.removeNode=function(key){
			slider.dl.find('[val="'+key+'"]').remove();
		}
		el.clear=function(key){
			slider.dl.children().remove();
		}
		//---------------FUNTION------------------

		init();
		//返回jQuery对象
		return this;
	}
})($);
