define(function(require, exports, module) { 
	var $ = require('jquery');
	require('function');
	require('bootstrap')($);
	if($('.index').length > 0){

	}else {
		require('./search.js').Search();
	}
	
	/*
     *意见反馈显示/关闭提示
     */
    $(".personalFeedbackLmenu a").mouseover(function(){
        $(this).addClass("active");
        $(this).siblings(".feedboxTip").stop().slideDown(150).animate({"opacity":"1"},400);
    });
    $(".feedboxTip .closed").click(function(){
        $(this).parent().siblings("a").removeClass("active");
        $(this).parent().stop().animate({"opacity":"0"},250).slideUp(500);
    });
	/*
	 * @ 图片查看弹窗
	 * @ img_src是/uploads/图片相对的路径
	 */
	function imgPopup(img_src){
	    var html = '';

	    html += '<div id="imgzoom"><i class="imgzoom-close"></i><div id="imgzoom-image-ctn">';
	    html += '<img class="img" src="'+ img_src +'" alt=""/>';
	    html += '</div></div>';

	    $('body').append(html);

	    var oImg    = $('#imgzoom-image-ctn');
	    var Dheight = $(window).height()-56;
	    oImg.find('.img').load(function(){
	        var ddh = oImg.outerHeight(),
	            ddw = oImg.outerWidth(),
	            whF = oImg.outerWidth()/oImg.outerHeight();

	        if(oImg.outerWidth()>ddh){
	            if(Dheight<oImg.outerHeight()){
	                ddh = Dheight - 20;
	                ddw = ddh * whF;
	            }
	        }else{
	            if(ddw > 1160){ ddw = 1160;ddh = 1160/whF;}
	        }

	        oImg.css({'left': '50%','top': '50%','marginLeft': -ddw/2,'marginTop':-ddh/2});
	    });

	    $('#imgzoom').height(Dheight).fadeIn('fast','linear');

	    $('.imgzoom-close').on('click',function(event){$('#imgzoom').remove();});
	};

	/* 
	 * @ 倒计时
	 * @ Day : 天数
	 * @ intDiff : 倒计时总秒数量
	 */

	function cutTimer(intDiff,obj){
	    window.setInterval(function(){
	        var day = 0,
	            hour = 0,
	            minute = 0,
	            second = 0;//时间默认值      
	        if(intDiff > 0){
	            day = Math.floor(intDiff / (60 * 60 * 24));
	            hour = Math.floor(intDiff / (60 * 60)) - (day * 24);
	            minute = Math.floor(intDiff / 60) - (day * 24 * 60) - (hour * 60);
	            second = Math.floor(intDiff) - (day * 24 * 60 * 60) - (hour * 60 * 60) - (minute * 60);
	        }
	        if (minute <= 9) {minute = '0' + minute};
	        if (second <= 9) {second = '0' + second};
	        $(obj + '#day_show').html(day+"天");
	        $(obj + '#hour_show').html( hour +'时');
	        $(obj + '#minute_show').html(minute +'分');
	        $(obj + '#second_show').html(second +'秒');
	        intDiff--;
	    }, 1000);
	}

	/*
	 * @ 选项卡
	 * @ tab_menu: 选项卡按钮class
	 * @ tab_box: 选项卡内容class
	 * @ active: 选项卡按钮添加选中样式 
	 * @ type: 动画类型
	 */
	function tab(options){
		var define = {
			'tabNav': '.tab_menu > li',
			'tabBox': '.tab_box > div',
			'select': 'active',
			'type': 'show'
		};
		var option = options;
		$.extend(define, options);
	    var oUl = $(define.tabNav || option.tabNav);
	    oUl.click(function(){
	        $(this).addClass(define.select || option.select).siblings().removeClass(define.select || option.select);
	        var index = oUl.index(this);
	        switch(define.type){
	        	case 'show': $(define.tabBox || option.tabBox).eq(index).show().siblings().hide();
	        	break;
	        	case 'slide': $(define.tabBox || option.tabBox).eq(index).slideDown(300).siblings().slideUp(300);
	        	break;
	        	case 'fade': $(define.tabBox || option.tabBox).eq(index).fadeIn(300).siblings().fadeOut(300);
	        	break;
	        }	        
	    });
	}

	/* 用户昵称截取 */
	var _Login = $('.topRight').attr('login');
	if(_Login == 'True'){
		var _nickName = $('.nick_name a:first-child');
		if(_nickName.attr('data-name').length >= 4){
			_nickName.text(_nickName.attr('data-name').substring(0,4)+'...');
		}else{
			_nickName.text(_nickName.attr('data-name'));
		}
	}

	// 搜索跳转
	function sreachBtn(str){
		location.href="/course/list/?catagory="+str;
	}
	// 顶部登录事件
	function topRightLogin(){
		login_popup();
	}
	// 弹出登陆框
	function login_popup(msg){
		$('#id_account_l').val("");
		$('#id_password_l').val("");
		$('#id_email').val("");
		$('#id_password').val("");
		$('#id_captcha_1').val("");
		$('#id_mobile').val("");
		$('#id_mobile_code').val("");
		$('#id_password_m').val("");
		$('#id_captcha_m_1').val("");
		$('#id_captcha_1').val("");
		$('#login-form-tips').hide();
		$('#findpassword-tips').hide();
		$('#mobile_code_password-tips').hide();
		$('#register-tips').hide();
		$('#loginModal').modal('show');
		if(typeof(msg) != 'undefined'){
			$('#loginModal #login-form-tips').show().html(msg);
		}
	}
	// 登录表单提交
	function login_form_submit(tips_id){	
		$.ajax({
			cache: false,
			type: "POST",
			url:"/user/login/",
			data:$('#login_form').serialize(),
			async: true,
			beforeSend:function(XMLHttpRequest){
				$("#login_btn").html("登录中...");
				$("#login_btn").attr("disabled","disabled");
			},
			success: function(data) {
				if(data.account_l){
					$("#login-form-tips").html(data.account_l).show(500);
					$("#id_account_l").focus();
				}else if(data.password_l){
					$("#login-form-tips").html(data.password_l).show(500);
					$("#id_password_l").focus();
				}else{
					if(data.status == "success"){
						if(data.onepay_status == 'True'){
							window.location.replace('/');
						}else {
							window.location.replace(data.url);
						}
						if(detect_ie() !== false) {
							window.location.reload();
						}
						//window.location.href = "/user/center";
						return;
					}else if(data.status == "failure"){
						if(data.msg=='no_active'){
							zyemail=$("#id_account_l").val();
							zyUname=zyemail;
							zy_validate_Email(false,zyemail,$("#id_password_l").val());
	
						}
						else
							$("#login-form-tips").html("账号或者密码错误，请重新输入").show(500);
					}
				}
			},
			complete: function(XMLHttpRequest){
				$("#login_btn").html("登录");
				$("#login_btn").removeAttr("disabled");
			}
		});
	
	}
	function detect_ie() {
		var ua = window.navigator.userAgent;
		var msie = ua.indexOf('MSIE ');
		var trident = ua.indexOf('Trident/');
	
		if (msie > 0) {
			// IE 10 or older => return version number
			return parseInt(ua.substring(msie + 5, ua.indexOf('.', msie)), 10);
		}
	
		if (trident > 0) {
			// IE 11 (or newer) => return version number
			var rv = ua.indexOf('rv:');
			return parseInt(ua.substring(rv + 3, ua.indexOf('.', rv)), 10);
		}
	
		// other browser
		return false;
	}
	// 注册提交
	function register_form_submit(type){
		var current_register_form=type||"mobile_register_form";
		if(current_register_form == "mobile_register_form"){
			if($('.active .form-control').val().length > 0){
				$('.active .form-control').next('label').css({'transform': 'translateY(-18px)'});
			}   	
			$.ajax({
				type: "POST",
				url:"/user/register/mobile_verify/",
				data:{
					'type': 'mobile',
					'mobile': $('#id_mobile_code').val(),
					'password_m': $('#id_password_m').val(),
					'geetest_challenge': $('.geetest_challenge').attr('value'),
					'geetest_validate': $('.geetest_validate').attr('value'),
					'geetest_seccode': $('.geetest_seccode').attr('value'),
					"mobile_code": '-11111'
				},
				beforeSend:function(XMLHttpRequest){
					$(".sign_btn").html("注册中...");
					$("sign_btn").attr("disabled","disabled");
				},
				success: function(data) {
					//console.log(data);
					if(data.status == 'success'){
	
						$.ajax({
							type: "POST",
							url:"/user/register/mobile/sendsms_signup/",
							data:{
								'mobile': $('#id_mobile_code').val(),
								'geetest_challenge': $('.geetest_challenge').attr('value'),
								'geetest_validate': $('.geetest_validate').attr('value'),
								'geetest_seccode': $('.geetest_seccode').attr('value'),
							},
							success: function(data){
								//console.log(data)
										
								if(data.mobile){
									$(".verify-tips").removeClass('success').addClass('error').html(data.mobile).show(500);
									//$("#id_mobile").focus();
									$('.tab-pane.active .captcha').siblings('.v_sign_tips').addClass('error').html(data.mobile).show(500);
								}else if(data.captcha){
									$(".verify-tips").removeClass('success').addClass('error').html(data.captcha).show(500);
									
								}else if(data.status == 'failure'){
									$(".verify-tips").removeClass('success').addClass('error').html("短信验证码发送失败").show(500);
								}else{
									$(".verify-tips").removeClass('error').addClass('success').html(data.info).show(500);
									$('#mobile_register_form').hide().siblings('#verify_form').show('fast',function(){
										$('.sign-tabs li').unbind('click');
									});
									show_send_sms(60);
								}
							}
						});
						
						
						$('.user_mobile').html($("#id_mobile_code").val().substring(0,3)+"****"+$("#id_mobile_code").val().substring(8,11));
						
						$('#verify-ok').on('click',function(){
							$.ajax({
								type: "POST",
								url:"/user/register/mobile/",
								data:{
									'type': 'mobile',
									'mobile': $('#id_mobile_code').val(),
									'password_m': $('#id_password_m').val(),
									'geetest_challenge': $('.geetest_challenge').attr('value'),
									'geetest_validate': $('.geetest_validate').attr('value'),
									'geetest_seccode': $('.geetest_seccode').attr('value'),
									'mobile_code': $('#Verify').val(),
									"partner": $('#reg_partner').val(),
									"openid": $('#reg_openid').val(),
									"invitation_code": $('#invitation_code').val()
								},								
								beforeSend:function(XMLHttpRequest){},
								success: function(data) {
	
									if(data.mobile_code){
										$(".verify-tips").removeClass('success').addClass('error').html(data.mobile_code).show(500);
										//$("#Verify").focus();
									}else{
										window.location = '/user/sign_success/';
									}
								}
							});
						})
					}else{
						if(data.mobile){
							$(".m_sign_tips").addClass('error').html(data.mobile).show(500);
							//$("#id_mobile").focus();
						}else if(data.password_m){
							$(".p_sign_tips").addClass('error').html(data.password_m).show(500);
							//$("#id_password_m").focus();
						}else if(data.captcha){
							$('.tab-pane.active .captcha').siblings('.v_sign_tips').addClass('error').html(data.captcha).show(500);
						}
					}
					
				},
				complete: function(XMLHttpRequest){
					$(".sign_btn").html("注册");
					$(".sign_btn").removeAttr("disabled");
				}
			});
		}else if(current_register_form == "email_register_form"){
			
			$.ajax({
				cache: false,
				type: "POST",
				url:"/user/register/email/",
				data:{
					'type': 'email',
					'email': $('#id_email').val(),
					'password': $('#id_password').val(),
					'geetest_challenge': $('#email_register_form .geetest_challenge').attr('value'),
					'geetest_validate': $('#email_register_form .geetest_validate').attr('value'),
					'geetest_seccode': $('#email_register_form .geetest_seccode').attr('value'),
					"partner": $('#reg_partner').val(),
					"openid": $('#reg_openid').val(),
					"invitation_code": $('#invitation_code').val()
				},
				async: true,
				beforeSend:function(XMLHttpRequest){
					$(".sign_btn").html("注册中...");
					$(".sign_btn").attr("disabled","disabled");
				},
				success: function(data) {
					
					//console.log(data)
					if(data.email){
						$("label[for=email]").siblings('.e_sign_tips').addClass('error').html(data.email).show(500);
						//$("#id_email").focus();
					}else if(data.password){
						$("label[for=password]").siblings('.e_sign_tips').addClass('error').html(data.password).show(500);
						//$("#id_password").focus();
					}else if(data.email_ue){
						$('.tab-pane.active .captcha').siblings('.v_sign_tips').addClass('error').html(data.email_ue).show(500);
						//$("#id_password").focus();
					}else if(data.captcha){
						$('.tab-pane.active .captcha').siblings('.v_sign_tips').addClass('error').html(data.captcha).show(500);
					}else{
						$('#email_register_form').hide().siblings('#email_form').show();
						$('.email-tips').addClass('success');
						$('.user_email').html($('#id_email').val());
					}
				},
				complete: function(XMLHttpRequest){
					$(".sign_btn").html("注册");
					$(".sign_btn").removeAttr("disabled");
				}
			});
		}
	}

	// 找回密码表单提交
	function find_password_form_submit(){
	
		$.ajax({
			cache: false,
			type: "POST",
			url:"/user/password/find/",
			data:{
				'account':$('#id_account').val(),
				'geetest_challenge': $('#find_password_form .geetest_challenge').attr('value'),
				'geetest_validate': $('#find_password_form .geetest_validate').attr('value'),
				'geetest_seccode': $('#find_password_form .geetest_seccode').attr('value')
			},
			async: true,
			beforeSend:function(XMLHttpRequest){
				$("#findpassword_btn").html("提交中...");
				$("#findpassword_btn").attr("disabled","disabled");
			},
			success: function(data) {
				if(data.account){
					$("#findpassword-tips").html(data.account).show(500);
					//$("#id_account").focus();
				}else if(data.captcha){
					$("#findpassword-tips").html(data.captcha).show(500);
				}else if(data.email_ue){
					$("#findpassword-tips").html(data.email_ue).show(500);
				}else if(data.mobile){
					$("#findpassword-tips").html(data.mobile).show(500);
				}else{
					if($("#id_account").val().indexOf("@") > 0 ){
						$("#findpassword-tips").html("找回密码邮件已发送").show(500);
					}else{
						if(data.status == 'failure') {
							$('#mobile_code_password_form_message').html("手机短信验证码发送失败！");
						}else{
							$('#mobile_code_password_form_message').html("手机短信验证码已发送，请查收！");
							show_send_sms(60);
						}
						$('#id_mobile' +
							'_f').val($("#id_account").val());
						$('#forgetpswModal').modal('hide');
						$('#forgetpswMobileModal').modal('show');
					}
				}				
			},
			complete: function(XMLHttpRequest){
				$("#findpassword_btn").html("提交");
				$("#findpassword_btn").removeAttr("disabled");
			}
		});
	}
	// 验证邮件
	var zyemail="";
	var zyUname="";
	var hash={
		'qq.com': 'http://mail.qq.com',
		'gmail.com': 'http://mail.google.com',
		'sina.com': 'http://mail.sina.com.cn',
		'163.com': 'http://mail.163.com',
		'126.com': 'http://mail.126.com',
		'yeah.net': 'http://www.yeah.net/',
		'sohu.com': 'http://mail.sohu.com/',
		'tom.com': 'http://mail.tom.com/',
		'sogou.com': 'http://mail.sogou.com/',
		'139.com': 'http://mail.10086.cn/',
		'hotmail.com': 'http://www.hotmail.com',
		'live.com': 'http://login.live.com/',
		'live.cn': 'http://login.live.cn/',
		'live.com.cn': 'http://login.live.com.cn',
		'189.com': 'http://webmail16.189.cn/webmail/',
		'yahoo.com.cn': 'http://mail.cn.yahoo.com/',
		'yahoo.cn': 'http://mail.cn.yahoo.com/',
		'eyou.com': 'http://www.eyou.com/',
		'21cn.com': 'http://mail.21cn.com/',
		'188.com': 'http://www.188.com/',
		'foxmail.coom': 'http://www.foxmail.com'
	};
	function zy_validate_Email(bo,zyem,upwd){
		var zybo1=true;
		if(!bo) {
			$("#emailValidate .close").unbind().click(function(){
				$('#emailValidate').modal('hide');
				//login_form_ajax(zyem,upwd);
			})
			$('#registerModal').modal('hide');
			$('#addemailModal').modal('hide');
			$('#emailValidate').modal('show');
			var zya=$(".zy_email .a>a");
			var url = zyem.split('@')[1];
			zya.attr("href",hash[url]);
			$("#emailValidateEE span").html(zyem);
			if(undefined==hash[url] || hash[url]==null){
				zya.parent().hide();
			}
			zybo1=false;
		}
		else{
			zybo1=true;
		}
		return zybo1;
	}
	// zhouyi:7-30  验证邮件倒计时
	var zy_c_num=60;
	var zy_str="";this.sendECount;
	this.zy_Countdown=function(){
		zy_c_num--;
		$(".sendE2 span").html(zy_c_num+"s");
		$(".zy_success span").html(zy_str);
		(zy_c_num<58)&&$(".zy_success").addClass("upmove");
		if(zy_c_num<=0){
			zy_c_num=60;
			$(".sendE2").hide();
			$(".sendE").show()
			clearInterval(sendECount);
		}
		//setTimeout("zy_Countdown()",1000);
	}
	// 拖拽验证
	var captchaObjF,captchaObjF2,captchaObjF3;
	var captcha = function(obj,ty,callback){
		callback=callback||function(){};
		var setting = {
			obj: obj,
			ty:ty
		};
		if(setting.ty == undefined){
		  setting.ty = '';
		}
		var handler = function (captchaObj) {
			// 将验证码加到id为captcha的元素里
			captchaObj.appendTo(setting.obj);
			captchaObj.onSuccess(function(){
				$('.tab-pane.active .captcha').siblings('.v_sign_tips').removeClass('error').html('').show(500);
			});
			switch(setting.ty){
				case "mobile/":captchaObjF=captchaObj; break;
				case "verifyMobile/":callback.call(this,captchaObj); break;
				case "verifyEmail/":callback.call(this,captchaObj); break;
				case "":captchaObjF3=captchaObj; break;
				default:captchaObjF2=captchaObj;break;
			}
		};
		$.ajax({
			// 获取id，challenge，success（是否启用failback）
			url: "/geetest/getcaptcha/"+setting.ty,
			type: "get",
			dataType: "json", // 使用jsonp格式
			success: function (data) {
				// 使用initGeetest接口
				// 参数1：配置参数，与创建Geetest实例时接受的参数一致
				// 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
				initGeetest({
					gt: data.gt,
					challenge: data.challenge,
					product: "float", // 产品形式
					offline: !data.success,
				}, handler);
			}
		});
	};
	this.captchaMy=captcha;
	this.openVideo = function(url){
		url||(url="http://ocsource.maiziedu.com/lps_intro.mp4");
		$("#microohvideo").children().attr("src",url);
		$('#VideoDemo').modal('show');
	}
	this.openVideo2 = function(url){
		url||(url="http://ocsource.maiziedu.com/lps_intro.mp4");
		$("#microohvideo2").children().attr("src",url);
		$('.teacherVideo').fadeIn();
	}
	// 手机验证码表单验证
	this.mobile_code_password_form_submit=function(){
		$.ajax({
			cache: false,
			type: "POST",
			url:"/user/password/find/mobile/",
			data:$('#mobile_code_password_form').serialize(),
			async: true,
			beforeSend:function(XMLHttpRequest){
				$("#mobile_code_password_btn").html("提交中...")
				$("#mobile_code_password_btn").attr("disabled","disabled")
			},
			success: function(data) {
				if(data.mobile_code_f){
					$("#mobile_code_password-tips").html(data.mobile_code_f).show(500);
					$("#id_mobile_code_f").focus();
				}else if(data.status == "success"){
					//忘记密码跳转到修改密码的界面前的合法性验证
					account = $("#id_account").val();
					code = $("#id_mobile_code_f").val();
					location.href="/user/password/reset/"+account+"/"+code;
				}
			},
			complete: function(XMLHttpRequest){
				$("#mobile_code_password_btn").html("提交");
				$("#mobile_code_password_btn").removeAttr("disabled");
			}
		});
	}
	// 重发送短信验证码计时
	var sendOFF = true;
	this.show_send_sms=function(time){
		$("#forgetpswMobileModal .send-verify,#verify_form .send-verify").html("重发验证码（" + time + "s）").css({'background':'#D6D6D6'}).attr("disabled","disabled");
		if(time<=0){
			$(".verify-tips.success").hide(500);
			$("#forgetpswMobileModal .send-verify,#verify_form .send-verify").html("重发验证码").css({'background':'#5ECFBA'}).removeAttr("disabled");
			sendOFF = true;
			return;
		}
		time--;
		setTimeout("show_send_sms("+time+")", 1000);
	}
	//发送手机验证码
	this.send_sms_code=function(form_id,tips_id){
		show_send_sms(60);
		var mobileVal = $('#id_mobile_code').val();
		var mobile_way = '';
		if(mobileVal == '' || mobileVal == undefined){
			mobileVal = $('#id_mobile_f').val();
			mobile_way = 'change';
		}
		if(sendOFF){
			$.ajax({
				cache: false,
				type: "POST",
				url:"/user/register/mobile/sendsms_signup/",
				data:{
					'mobile': mobileVal,
					'geetest_challenge': $('.geetest_challenge').attr('value'),
					'geetest_validate': $('.geetest_validate').attr('value'),
					'geetest_seccode': $('.geetest_seccode').attr('value'),
					'way': mobile_way
				},
				async: true,
				success: function(data){
					if(data.mobile){
						if(mobile_way != ''){
							$('#mobile_code_password_form_message').css({'background':'#f2dede'}).html(data.mobile);
						}else{
							$(".verify-tips").removeClass('success').addClass('error').html(data.mobile).show(500);
						}
					}else if(data.captcha){
	
						if(mobile_way != ''){
							$('#mobile_code_password_form_message').css({'background':'#f2dede'}).html(data.captcha);
						}else{
							$(".verify-tips").removeClass('success').addClass('error').html(data.captcha).show(500);
						}
					}else if(data.status == 'success'){
						if(mobile_way != ''){
							$('#mobile_code_password_form_message').css({'background':'#f2dede'}).html('');
						}else{
							$(".verify-tips").removeClass('error').addClass('success').html(data.info).show(500);
							show_send_sms(60);
						}
	
					}else if(data.status == 'failure'){
	
						if(mobile_way != ''){
							$('#mobile_code_password_form_message').css({'background':'#f2dede'}).html('请稍后再试');
						}else{
							$(".verify-tips").removeClass('success').addClass('error').html("短信验证码发送失败").show(500);
						}
					}
				},
				complete: function(XMLHttpRequest){
					$("#send-verify").html("重发验证码");
					$("#send-verify").removeAttr("disabled");
				}
			});
	
			sendOFF = false;
		}
		
	}
	//-----------------FUNCTIONEND-------------------------
    var cacheModel=[];
	var init=function(){
		$(".modal").on("show.bs.modal", function(){
			for(var i=0;i<cacheModel.length;i++){
				if(cacheModel[i]){
				cacheModel[i].modal('hide');
				cacheModel[i]=null;
				}
			}
			cacheModel.push($(this));
			var $this = $(this);
			var $modal_dialog = $this.find(".modal-dialog");
			var div=$('<div style="display:table; width:100%; height:100%;"></div>')
			div.html('<div style="vertical-align:middle; display:table-cell;"></div>');
			div.children("div").html($modal_dialog);
			$this.html(div);
		});		
		$(".zy_close").on({"click":function(){
			$(this).parent().parent().parent().parent().parent().modal("hide");
		}
		})
		//返回顶部
		$(".toolbar-item-gotop").click(function(){
			$('html,body').stop().animate({scrollTop: '0px'}, 800);
		});
		//第三方登录弹框验证
		if(login_popupvar) login_popup();
		//弹出登录框
		$(".globalLoginBtn").on("click",topRightLogin);
		//登录信息全局
		$('.top_user .sp').on('click', function (event) {
			event.preventDefault();
			event.stopPropagation();
			$('.show-card-wrap').toggleClass('in');
		});	
		$(document).on('click', function() {
			$('.show-card-wrap').removeClass('in');
		});		
/*		show_card();	
		$(window).resize(function(){
			show_card();
		});
*/		//顶部小喇叭
		$(".top_meg").hover(function(){
			$(this).children(".bubble").show()
		},function(){
			$(this).children(".bubble").hide()
		});
		//顶部搜索
		$(".topSreach").click(function(){
			$(this).parent().parent().toggleClass("sH")
		});
		$(".topSreachTxt,.sreachBBoxTxt").keydown(function(event){
			if(event.keyCode == 13)
				sreachBtn($(this).val());
		});
		$(".sreachBBoxBtn").click(function(){sreachBtn($(".sreachBBoxTxt").val());});
		$(".section1_sreach_txt").keydown(function(event){
			if(event.keyCode == 13)
				sreachBtn($(this).val());
		});
		$(".section1_sreach_btn").click(function(){sreachBtn($(".section1_sreach_txt").val());});
		//绑定53客服
		$(".class53").click(function(){
			$("#KFLOGO .Lelem").eq(0).trigger("click");
		});
		//侧边悬浮框
		$(".toolbar-item-weibo>div").hover(function(){
		},function(){
			$(this).stop().hide("fast");
		});
		$(".toolbar-item-weibo").click(function(){
			$(".lixianB").show();
		});
		$(".toolbar-item-weixin").unbind().click(function(){
			$("#KFLOGO .Lelem").eq(0).trigger("click");
		});

		//忘记密码
		var OFF = true;
		$('#btnForgetpsw').on('click', function () {
		  if(captchaObjF3) captchaObjF3.refresh();
		  if(OFF){
		    captcha(".newcaptcha");
		    OFF = false;
		  }
		  $('#forgetpswModal').modal('show');
		  $('#loginModal').modal('hide');
		  
		});
		$("#forgetpswMobileModal .send-verify").click(function(){
			send_sms_code('verify_form','verify-tips');
		});
		//忘记密码下一步
		$("#mobile_code_password_btn").click(mobile_code_password_form_submit);
		//登录表单键盘事件
		$("#login_form").keydown(function(event){
			if(event.keyCode == 13)
				login_form_submit("login-form-tips");
		});
		//登录事件
		$(".globalLogin").on("click",function(){
			login_form_submit("login-form-tips");
		});		
		//首页-忘记密码表单键盘事件
		//captcha(".newcaptcha");
		$("#find_password_form").keydown(function(event){
			if(event.keyCode == 13)
				find_password_form_submit();
		});
		//zhouyi:7-30 发送验证邮件事件
		$(".sendE a").click(function(){
			sendECount=setInterval(zy_Countdown,1000);
			$(".zy_success").removeClass("upmove");
			$(this).parent().hide();
			$(".sendE2").show().find("span").html("60s");	
			$.ajax({
				 type: "GET",
				 url: "/user/send_again_email",
				 data: {username:$('#id_account_l').val()},
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
		//if($(".top_meg").length>0) notice_message();
		//找回密码提交
		$("#findpassword_btn").click(find_password_form_submit);
	}
	var modular;
	function loadingD(s,option){
		option = option||{};
		switch(s){
			case "index":require.async('./index');break;
			case "signUP":require.async('./signUP',function(e){
					e.init(captcha,captchaObjF,captchaObjF2,register_form_submit,this);
				});break;
			case "newCouse":require.async('./newCouse',function(e){
					e.init(this);
				});break;
			case "studentM":require.async('./studentM',function(e){
					e.init(this,option);
				});break;	
			case "newCouseD":require.async('./newCouseD',function(e){
					e.init(this);
				});break;
			case "statisticsL":require.async('./statisticsL',function(e){
					e.init(this);
				});break;	
			case "statisticsM":require.async('./statisticsM',function(e){
					e.init(this,option);
				});break;	
			case "broadcastM":require.async('./broadcastM',function(e){
					e.init(this);
				});break;
			case "classM":require.async('./classM',function(e){
					e.init(this,option);
				});break;
			case "lessonVideo":require.async('./lessonVideo',function(e){
					e.init(this);
				});break;
			case "lessonVideoLists":require.async('./lessonVideoLists',function(e){
					e.init(this);
				});break;
			case "articleList":require.async('./articleList',function(e){
					e.init(this);
				});break;
			case "articleDetail":require.async('./articleDetail',function(e){
					e.init(this);
				});break;
			case "personalCenterSinfo":require.async('./personalCenterSinfo',function(e){
					e.init(this);
				});break;	
			case "personalCenterStaste":require.async('./personalCenterStaste',function(e){
					e.init(this);
				});break;
			case "personalCenter":require.async('./personalCenter',function(e){
					e.init(this);
				});break;	
			case "personalCenterSbasic":require.async('./personalCenterSbasic',function(e){
					e.init(this,option);
				});break;
			case "educationalCenter":require.async('./educationalCenter',function(e){
					e.init(this,option);
				});break;
			case "teacherCenterING":require.async('./teacherCenterING',function(e){
					e.init(this);
				});break;
			case "personalCenterSjob":require.async('./personalCenterSjob',function(e){
					e.init(this,option);
				});break;
			case "personalCenterResume":require.async('./personalCenterResume',function(e){
					e.init(this,option);
				});break;
			case "personalCenterSsetting":require.async('./personalCenterSsetting',function(e){
					e.init(this);
				});break;	
			case "tutorials_list":require.async('./tutorials_list',function(e){
					e.init(this);
				});break;
			case "tutorials_article":require.async('./tutorials_article',function(e){
					e.init(this);
				});break;
			case "teacherIntroduce":require.async('./teacherIntroduce');break;
			case "courseIntroduce":require.async('./courseIntroduce');break;
			case "teacherRecruit":require.async('./teacherRecruit');break;
			case "teacherRecruitForm":require.async('./teacherRecruitForm',function(e){
					e.init(this);
				});break;
			case "freeLearn":require.async('./free_learn');break;
			case "proAnswer":require.async('./proAnswer');break;
			case "trycourseteacher":require.async('./trycourseteacher');break;
			case "trymanageteacher":require.async('./trymanageteacher');break;
			case "personalCenterStudent":require.async('./personalCenterStudent');break;
			case "studentmyanswerdetail":require.async('./studentmyanswerdetail');break;
			case "studentmyanswer":require.async('./studentmyanswer',function(e){e.init(this);});break;
			case "wikiArticle":require.async('./wikiArticle');break;
			case "feedbackBox":require.async('./feedbackBox');break;
			case "search_result":require.async('./search_result');break;
			case "courseAppointment":require.async('./courseAppointment');break;
			
		}
	}
	module.exports = {
		"init":init,
		"imgpopup": imgPopup,
		"tab":tab,
		'cutTimer':cutTimer,
		"loading":loadingD,
		"login_popup":login_popup,
		"captcha":captcha,
		"jg":$
	};
	init();
	
	//个人中心的资源文件，用不到请屏蔽
	//require('./userCenter');
});