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
})(jQuery);
function studyInfo(t){
	var $th = t;
	return $.ajax({
		cache: false,
		type: "POST",
		url:"/home/s/ajax_studing_div/",
		//url:"data/dd.html",
		data:{"domain_name":$th.attr("pid")},
		dataType:"html",
		beforeSend:function(XMLHttpRequest){
			$th.css("pointer-events","none");
		},
		success: function(data) {
			$("#pcSBasis .pcSmodalDiv").html(data);
			$("#pcSBasis").modal("show");
		},
		complete: function(XMLHttpRequest){
			$th.css("pointer-events","auto");
		}
	});
}
//表单
function iform($th){
	$(".pcsRadio").statisticsRadio();	
	//提交学习基础
	var qisValid=$("#pcInfoForm").Validform({
		btnSubmit:".personalCbtn",
		ajaxPost:true,
		tiptype:function(msg,o,cssctl){
			//msg：提示信息;
			//o:{obj:*,type:*,curform:*},
			//obj指向的是当前验证的表单元素（或表单对象，验证全部验证通过，提交表单时o.obj为该表单对象），
			//type指示提示的状态，值为1、2、3、4， 1：正在检测/提交数据，2：通过验证，3：验证失败，4：提示ignore状态, 
			//curform为当前form对象;
			//cssctl:内置的提示信息样式控制函数，该函数需传入两个参数：显示提示信息的对象 和 当前提示的状态（既形参o中的type）;
			var typeCss="error";
			if(o.obj.attr("type")=="radio"){
				o.obj.parent().parent().parent().removeClass("reder");
				if(o.type!=2)
					o.obj.parent().parent().parent().addClass("reder");
			}
		},
		beforeCheck:function(curform){
		},
		beforeSubmit:function(curform){				
			$("#pcInfoForm .personalCbtn").css("pointer-events","none");
		},
		callback:function(data){
			if(data.status=="404") return;
			if($th.attr("pt")){
				$("#pcSBasisMeg").modal({show:true, keyboard:false,backdrop: 'static'});
				$("#pcSBasisMeg .personalCbtn").attr("href",$th.attr("href"));
			}
			else
				location.href=location.href;
			$("#pcInfoForm .personalCbtn").css("pointer-events","auto");
		}
	});
	qisValid.resetForm();
}
//------------FUNCTIONEND---------	
//初始化
var init = function(){
	var oClose = $('.zy_close');

	$(".personalCTop .font .personalCico").hover(function(){
		layer.tips($(this).attr("title"), $(this), {
		  tips: [1, '#333333'] //还可配置颜色
		});
	},function(){
		
	});	
	oClose.on({"click":function(){
		$(this).parent().parent().parent().parent().parent().modal("hide");
	}
	});		
	$(".showpcSBasis").click(function(){
		var $th=$(this);
		$.when(studyInfo($th)).then(function(a){
			iform($th);
		});		
		return false;	
	});
	$('#pcSBasisMeg').on('hide.bs.modal', function (e) {
		location.reload();
	});	
	if($("#finish-lessoninfo").length > 0){
		$("#finish-lessoninfo").modal({show:true, keyboard:false,backdrop: 'static'});
		$("#finish-lessoninfo").find('button').on('click',function(){
			$(this).parent().parent().parent().parent().parent().modal("hide");
		});
	}
}
init();