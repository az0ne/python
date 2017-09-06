var TimeGOobj,timeNum=10,captchaEmail;

function TimeGO(){
	if(timeNum<=1){
		clearInterval(TimeGOobj);
		location.href=$("#newMegPassword .personalCbtn").attr("href");
	}
	timeNum--;
	$("#newMegPassword .p2 .color5e").html(timeNum+"s");
}
//邮箱验证
function sendEmail(){
	$.ajax({
        type: "POST",
        url: "/home/settings/send_email_again/",
        dataType: "json",
        success: function(data) {
            if(data.success){
				$("#newMeg").modal("show");
			}
			else{alert(data.message);}		
        }
    })
}
//添加修改邮箱
function addEmail(){
	var $th=$(this);
	$.ajax({
		type: "POST",
		url:"/home/settings/bind_email/sendemail/",
		data:{"email":$("#newEmail .pcsBasicTableTxt").val(),"type":"verifyEmail",
			'geetest_challenge': $('#newEmail .geetest_challenge').attr('value'),
			'geetest_validate': $('#newEmail .geetest_validate').attr('value'),
			'geetest_seccode': $('#newEmail .geetest_seccode').attr('value')},
		dataType:"json",
		beforeSend:function(XMLHttpRequest){
			$th.css("pointer-events","none");
		},
		success: function(data) {						
			if(data.success){
				$("#newMeg").modal("show");
			}
			else{
				$("#newEmail .megError").html(data.message).slideDown();
			}			
		},
		complete: function(XMLHttpRequest){
			$th.css("pointer-events","auto");
		}
	});
}
//------------FUNCTIONEND---------	
//初始化
var init = function(){
	$(".personalCTop .font .personalCico").hover(function(){
		layer.tips($(this).attr("title"), $(this), {
		  tips: [1, '#333333'] //还可配置颜色
		});
	},function(){
		
	});	
	//修改密码
	var qisValid = $("#newPasswordForm").Validform({
		btnSubmit:".personalCbtn",
		ajaxPost:true,
		datatype:{
			"pw":function(gets,obj,curform,regxp){
				//参数gets是获取到的表单元素值，obj为当前表单元素，curform为当前验证的表单，regxp为内置的一些正则表达式的引用;
				var reg1=/^[^\s]+$/;		
				var val=obj.val(); 
				if(reg1.test(obj.val())){
					if(val.length>=8&&val.length<=50)
						return true;
					else
						return "请填写8~50位的字符"
				}else{return "不能有空格";}
				return false;
	 
				//注意return可以返回true 或 false 或 字符串文字，true表示验证通过，返回字符串表示验证失败，字符串作为错误提示显示，返回false则用errmsg或默认的错误提示;
			}
		},
		tiptype:function(msg,o,cssctl){
			var typeCss="error";
			if(o.obj.attr("type")=="password"){
				o.obj.removeClass("er");
				o.obj.parent().find(".error").remove();					
				if(o.type!=2){
					o.obj.addClass("er");
					o.obj.parent().append("<span class='validform "+typeCss+"'>"+msg+"</span>");
				}
			}
		},
		beforeCheck:function(curform){
			
		},
		beforeSubmit:function(curform){
			//$("#id_save_post").attr("disabled","disabled");
		},
		callback:function(data){
			if(data.success){
				$("#newMegPassword").modal({show:true, keyboard:false,backdrop: 'static'});timeNum=10;
				TimeGOobj=setInterval(TimeGO,1000);
			}
			else{
				$("#newPassword .megError").html(data.message).slideDown();
			}		
		}
	});
	qisValid.resetForm();
	$(".personalCenterSsetting_table td.t>a").click(function(){
		if($(this).hasClass("vEmail")){
			sendEmail();
			return ;
		}
		if($(this).hasClass("addEmail")){
			$("#newEmail .pt span").html("新增邮箱");
		}			 
		else{
			$("#newEmail .pt span").html("修改邮箱");
		}
		$("#newEmail").modal("show");
		$(".captchaMy").children().remove();
		captcha(".captchaMy","verifyEmail/",function(cap){
			captchaEmail = cap;
		});
	});
	//关闭消息
	$("#newMeg .cl").click(function(){
		$(".modal").modal("hide");
	});
	$("#newEmail .personalCbtn").click(addEmail);
	$('#newMeg').on('hide.bs.modal', function (e) {
		location.reload();
	});
	$('.zy_close').on({"click":function(){
		$(this).parent().parent().parent().parent().parent().modal("hide");
	}});
}

init();