define(function(require, exports, module) {
	require('radio')($);require('Validform')($);
	
	//-------------FUNTION-----------------.
	//构造函数
	function statisticsL(th){
		init();
	}
	function init(){
		//表单--单选
		$(".statisticsRadio").statisticsRadio();
		var qisValid=$("#ques_info_save").Validform({
			btnSubmit:"#id_save_post",
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
					o.obj.parent().parent().find(".validform").remove();
					if(o.type!=2)
						o.obj.parent().parent().append("<span class='validform "+typeCss+"'>"+msg+"</span>");
				}
				else if(o.obj.hasClass("statisticsTxt")){
					o.obj.parent().find(".validform").remove();
					if(o.type!=2)
						o.obj.parent().append("<span class='validform "+typeCss+"'>"+msg+"</span>");
				}
			},
			beforeCheck:function(curform){
				
			},
			beforeSubmit:function(curform){
				$("#id_save_post").attr("disabled","disabled");
			},
			callback:function(data){
				if (data.status == "failure") {
					$("#get_data").text(data.msg).addClass("bg-danger").addClass("tips-error").fadeIn().delay(3000).fadeOut();
				} else {
					$("#get_data").text(data.msg).addClass("bg-success").addClass("tips-error").fadeIn().delay(3000).fadeOut(function(){
						window.location.href = $("#ques_info_save").attr("tourl");
					});
				}
			}
		});
		qisValid.resetForm();
		
	}
	//-------------FUNTIONEND-----------------	
	module.exports = {
		"init":statisticsL
	};
})