define(function(require, exports, module) { 
	var captchaObjF,captchaObjF2,captcha,register_form_submit,th;
	//-------------FUNTION-----------------.
	function signUP(c1,c2,c3,r1,t){
		captcha=c1;captchaObjF=c2;captchaObjF2=c3;register_form_submit=r1;th=t;init();
	}
	//------------FUNCTIONEND---------	
	//初始化
	var init=function(){
		//注册表单键盘事件
		$("#email_register_form").keydown(function(event){
			if(event.keyCode == 13)
				register_form_submit();
		});
		$('.sign-left .form-control').focus(function(){
			$(this).next('label').css({'transform': 'translateY(-18px)'});
		});
		$('.sign-left .form-control').blur(function(){
			if($(this).val() == ''){
				$(this).next('label').css({'transform': 'translateY(0px)'});
			}else{
				$(this).next('label').css({'color':'#5ECFBA'});
			}
		});
	
		var $div_li = $('.sign-tabs li');
		var OFF1 = true;
		var OFF2 = true;
		var refresh_count = 0;
	
		if(OFF1){
			captcha(".tab-pane.active .captcha1", 'mobile/');
			OFF1 = false;
		}
	   
	
		$div_li.on('click',function(){
				
			$(this).addClass('active').siblings().removeClass('active');
			$('.tab-pane.active .captcha').siblings('.v_sign_tips').removeClass('error').html('').show(500);
			$("label[for=mobile_code]").siblings('.m_sign_tips').removeClass('error success').html('').show(500);
			$("label[for=password_m]").siblings('.p_sign_tips').removeClass('error success').html('8-20位，区分大小写，不支持空格').show(500);
			$("label[for=email]").siblings('.e_sign_tips').removeClass('error success').html('').show(500);
			$("label[for=password]").siblings('.e_sign_tips').removeClass('error success').html('8-20位，区分大小写，不支持空格').show(500);
			var index = $div_li.index(this);
			if(OFF1 && index == 0){
				captcha(".tab-pane.active .captcha1", 'mobile/');
				OFF1 = false;
				
			}
			
			if(OFF2 && index == 1){
				captcha(".tab-pane.active .captcha2", 'email/');
				OFF2 = false;
				
			}
			if(captchaObjF) {
				if(refresh_count > 18){
					window.location.reload();
				}
				refresh_count++;
				captchaObjF.refresh();
			}
			if(captchaObjF2) {
				if(refresh_count > 18){
					window.location.reload();
				}
				refresh_count++;
				captchaObjF2.refresh();
			}
			
			$('#verify_form').hide().siblings('#mobile_register_form').show();
			$('#email_form').hide().siblings('#email_register_form').show();
	
			if($('.active .form-control').val() != ''){
				$('.form-control').val('').next('label').css({'transform': 'translateY(0px)','color':'#999999'});
			}
			$('.tab-content .tab-pane').eq(index).addClass('active').siblings().removeClass('active');
		});
		
		$('#id_mobile_code').on('blur keyup', function(){
			var userMobile = $(this).val(),mobile_code=$("label[for=mobile_code]");
			var telReg = /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/g;
			if(userMobile == null || userMobile == ''){
				mobile_code.siblings('.m_sign_tips').removeClass('success').addClass('error').html('请输入你的手机号').show(500);
			}else if(telReg.test(userMobile)){
				mobile_code.siblings('.m_sign_tips').removeClass('error').addClass('success').html('').show(500);
			}else if(!telReg.test(userMobile)){
				mobile_code.siblings('.m_sign_tips').removeClass('success').addClass('error').html('手机号码格式不正确').show(500);
			}
		});
		$('#id_password_m').on('blur keyup',function(){
			var password_m=$("label[for=password_m]");
			if($(this).val() == null || $(this).val() == ''){
				password_m.siblings('.p_sign_tips').removeClass('success').addClass('error').html('请输入密码').show(500);
			}else if($(this).val().length < 8){
				password_m.siblings('.p_sign_tips').removeClass('success').addClass('error').html('8-20位，区分大小写，不支持空格').show(500);
			}else{
				password_m.siblings('.p_sign_tips').removeClass('error').addClass('success').html('').show(500);
			}
		});
		$('#id_email').on('blur keyup', function(){
			var userEmail = $(this).val(),email=$("label[for=email]");
			var emailReg = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
			if(userEmail == null || userEmail == ''){
				email.siblings('.e_sign_tips').removeClass('success').addClass('error').html('请输入你的邮箱').show(500);
			}else if(emailReg.test(userEmail)){
				email.siblings('.e_sign_tips').removeClass('error').addClass('success').html('').show(500);
			}else if(!emailReg.test(userEmail)){
				email.siblings('.e_sign_tips').removeClass('success').addClass('error').html('注册账号需为邮箱格式').show(500);
			}else{
				email.siblings('.e_sign_tips').removeClass('error').addClass('success').html('').show(500);
			}
		});
		$('#id_password').on('blur keyup',function(){
			var password=$("label[for=password]");
			if($(this).val() == null || $(this).val() == ''){
				password.siblings('.e_sign_tips').removeClass('success').addClass('error').html('请输入密码').show(500);
			}else if($(this).val().length < 8){
				password.siblings('.e_sign_tips').removeClass('success').addClass('error').html('8-20位，区分大小写，不支持空格').show(500);
			}else{
				password.siblings('.e_sign_tips').removeClass('error').addClass('success').html('').show(500);
			}
		});
		//注册
		$(".sign-left .btn-micv5").click(function(){
			register_form_submit($(this).attr("typeF"));
		});
		//再次发送
		$("#send-verify").click(function(){
			th.send_sms_code('verify_form','verify-tips');
		});
		
		$("#email_form .sendE a").unbind().click(function(){
			sendECount=setInterval(zy_Countdown,1000);
			$(".zy_success").removeClass("upmove");
			$(this).parent().hide();
			$(".sendE2").show().find("span").html("60s");	
			$.ajax({
				 type: "GET",
				 url: "/user/send_again_email",
				 data: {username:$('#id_email').val()},
				 dataType: "html",
				 success: function(data){
					 zy_str="验证邮件发送成功";
					 if(data)
						zy_Countdown();
				 },
				error:function(){
					zy_str="验证邮件发送失败";
				}
	
			 });
		});
	}	
	
	
	module.exports = {
		"init":signUP
	};
	
})