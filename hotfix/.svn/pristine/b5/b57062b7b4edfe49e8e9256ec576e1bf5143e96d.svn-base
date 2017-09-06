define(function(require, exports, module) { 
	require('radio')($);require('Validform')($);require('Jcrop')($);require('JcropCss');
	require('uiwidget')($);require('fileupload')($);
	var th,xsize=120,ysize=120,boundx,boundy,wScale,hScale,option;
	var captchaPhone,PhoneValue,globlaImg;
	var deferred1 = $.Deferred();
	//-------------FUNTION-----------------.
	function personalCenterSbasic(t,op){
		th=t;option=op;init();
	}
	//从 file 域获取 本地图片 url
	function getFileUrl(sourceId) {
		var url='';
		if (navigator.userAgent.indexOf("MSIE") >= 1) { // IE
			url = document.getElementById(sourceId).value;
		} else if (navigator.userAgent.indexOf("Firefox") > 0) { // Firefox
			url = window.URL.createObjectURL(document.getElementById(sourceId).files.item(0));
		} else if (navigator.userAgent.indexOf("Chrome") > 0) { // Chrome
			url = window.URL.createObjectURL(document.getElementById(sourceId).files.item(0));
		}
		return url;
	}
	function getImageWidth(url,callback){ 
		var img = new Image(); img.src = url; 
		if(img.complete){ 
			callback(img.width, img.height);
		}else{ 
			img.onload = function(){ 
				callback(img.width, img.height); 
			} 
		} 
		return img;
	}
	function updatePreview(c){
		if (parseInt(c.w) > 0){
			var rx = xsize / c.w;
			var ry = ysize / c.h;	
			$(".cuttPictureBoxR img").css({
				width: Math.round(rx * boundx) + 'px',
				height: Math.round(ry * boundy) + 'px',
				marginLeft: '-' + Math.round(rx * c.x) + 'px',
				marginTop: '-' + Math.round(ry * c.y) + 'px'
			});
		}
    };
	function updateCoords(c){
		$('#x').val(c.x);
		$('#y').val(c.y);
		$('#w').val(c.w);
		$('#h').val(c.h);
	};
	function sendsms($th){
		return $.ajax({
			type: "POST",
			url:"/home/settings/bind_mobile/sendsms/",
			data:{"mobile":$("#newPhone .pcsBasicTableTxt").val(),
				"type":"verifyMobile",
				'geetest_challenge': $('#newPhone .geetest_challenge').attr('value'),
				'geetest_validate': $('#newPhone .geetest_validate').attr('value'),
				'geetest_seccode': $('#newPhone .geetest_seccode').attr('value')
			},
			dataType:"json",
			beforeSend:function(XMLHttpRequest){
				$th.css("pointer-events","none");
			},
			success: function(data) {
				if(data.success){
					$("#newPhone2").modal("show");
					PhoneValue=$("#newPhone .pcsBasicTableTxt").val();
				}
				else{
					$("#newPhone .megError").html(data.message).slideDown();
					captchaPhone.refresh();
				}
			},
			complete: function(XMLHttpRequest){
				$th.css("pointer-events","auto");
			}
		});
	}
	var setInObj,setIn_num=60;
	function setIn(dom,time,callback){
		setIn_num--;
		dom.html(setIn_num);
		if(setIn_num<=0){
			setIn_num=time||setIn_num;
			callback.call(this);			
			clearInterval(setInObj);
		}
	}
	//再次发送
	function onceSend(){
		var $th=$(this);
		$th.html("重发验证码(<span>60</span>s)").css("pointer-events","none");
		$.ajax({
			type: "POST",
			url:"/home/settings/bind_mobile/sendsms/",
			data:{"mobile":PhoneValue,"retry":true},
			dataType:"json",
			beforeSend:function(XMLHttpRequest){
			},
			success: function(data) {
				if(data.success){
					var npa=$("#newPhone2 .fg > a");
					$("#newPhone2 .pm").html("手机短信验证码已发送，请查收！").slideDown();
					$th.removeAttr("style").addClass("smsend");
					setInObj=setInterval(_foo($("#newPhone2 .fg > a>span"),60,function(){
						npa.html("重发验证码").removeClass("smsend");
						npa.unbind().click(onceSend);
						$th.css("pointer-events","auto");
					}),1000);
				}
				else{$("#newPhone2 .pm").html(data.message).slideDown();}
			},
			complete: function(XMLHttpRequest){
				
			}
		});
	}
	function _foo(dom,time,callback){		
		setIn_num=time||setIn_num;
		clearInterval(setInObj);
		return function(){		
			setIn(dom,time,callback);		
		}		
	}
	//头像上传
	function upImg(img_url,picwidth,picheight,width,height,left,top){
		var $th=$(this);
		$.ajax({
			type: "POST",
			url:"/home/settings/avatar/save/",
			data:{"img_url":img_url,"picwidth":picwidth,"picheight":picheight,"width":width,"height":height,"left":left,"top":top},
			dataType:"json",
			beforeSend:function(XMLHttpRequest){
				$th.css("pointer-events","none");
			},
			success: function(data) {
				if(data.success){
					//$(".pcsBasicTableOne .img img,.personalCTop .img img,.top_user .ai img,.zy_userDiv .d1 img").attr("src",globlaImg);
					location.reload();
				}
				else{alert(data.message);}				
			},
			complete: function(XMLHttpRequest){
				$th.css("pointer-events","auto");
			}
		})
	}
	//切换头像
    function change_photo0(){
        $.ajax({
            type: "POST",
            url: "/home/settings/avatar/random/",
            dataType: "json",
            success: function(data) {
                if(data.success){
					$(".pcsBasicTableOne .img img,.personalCTop .img img,.top_user .ai img,.zy_userDiv .d1 img").attr("src",data.data.avatar);
				}
				else{alert(data.message);}		
            }
        })
    }
	//城市切换ajax
	function selectCity(){
		var $th=$(this);
		$.ajax({
            type: "POST",
            url: "/home/base/citylist/"+$th.val()+"/",
            dataType: "json",
            success: function(data) {
                if(data.success){
					var dom=$(".pcsBasicTable .pccity");
					dom.html("");
					var list=data.data.list;
					for(var i=0;i<list.length;i++){						
						dom.append('<option value="'+list[i].city_id+'">'+list[i].city_name+'</option>')
					}
				}
				else{alert(data.message);}		
            }
        })
	}
	//------------FUNCTIONEND---------	
	//初始化
	var init=function(){
		$(".pcsRadio").statisticsRadio();		
		
		//选择头像
		$(".cuttPictureBoxL .pb > a.a2").click(function(){
			$("#cuttPictureFile").trigger("click");
		});
		//保存头像
		$(".cuttPictureBoxL .pb > a.a1").click(function(){
			var img=$(".cuttPictureBoxL .picY");
			var width=img.width()>250?250:img.width();
			var height=img.height()>250?250:img.height();
			upImg.call(this,img.attr("src"),width,height,$("#w").val(),$("#h").val(),$("#x").val(),$("#y").val());			
			
		});
		$(".pcsBasicTableOne .imgSelect").click(change_photo0);
		//城市切换
		$(".pcsBasicTable .pcprovince").change(selectCity);
		var jcropImg;//setImage		
		//deferred1.done(upImg);
		$('#cuttPictureFile').fileupload({
			url: '/home/settings/avatar/upload/',
			dataType: 'json',
			autoUpload: true,
			done: function (e, data) {
				data=data.result;
				if(data.success){
					var imgURL=data.data.img_url;
					globlaImg=imgURL;
					getImageWidth(imgURL,function(w,h){
						$(".cuttPictureBoxR img").attr("src",imgURL);
						var img=$("<img/>").addClass("picY");
						img.attr("src",imgURL).attr("id","cuttPictureImg");
						$(".cuttPictureBoxR img").removeAttr("style");
						$(".cuttPictureBoxL .img").html(img);
						$('#cuttPictureImg').Jcrop({
						  onChange: updatePreview,
						  onSelect: updateCoords,
						  aspectRatio: 1
						},function(){
						  jcropImg=this;
						  jcropImg.animateTo([0,0,100,100]);
						  // Use the API to get the real image size
						  var bounds = this.getBounds();
						  boundx = bounds[0];
						  boundy = bounds[1];
						  wScale=w;
						  hScale=h;
						});						
					});	
				}
				else{alert(data.message);}
			},
			progressall: function (e, data) {}
		})

		
		//提交表单
		var qisValid=$("#pcBasicForm").Validform({
			btnSubmit:".personalCbtn",
			ajaxPost:true,
			datatype:{
				"carded":function(gets,obj,curform,regxp){
					if (option.is_join_job_class!="True"){
						if(gets=="") return true;
					}
					var reg = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/;  
				   	if(reg.test(gets) === false){return  "身份证输入不合法";}else{return true;}
				}
			},
			tiptype:function(msg,o,cssctl){
				//msg：提示信息;
				//o:{obj:*,type:*,curform:*},
				//obj指向的是当前验证的表单元素（或表单对象，验证全部验证通过，提交表单时o.obj为该表单对象），
				//type指示提示的状态，值为1、2、3、4， 1：正在检测/提交数据，2：通过验证，3：验证失败，4：提示ignore状态, 
				//curform为当前form对象;
				//cssctl:内置的提示信息样式控制函数，该函数需传入两个参数：显示提示信息的对象 和 当前提示的状态（既形参o中的type）;
				var typeCss="error";
				if(o.obj.attr("type")=="radio"){
					o.obj.parent().parent().find(".error").remove();
					o.obj.parent().parent().parent().removeClass("er");
					if(o.type!=2){
						o.obj.parent().parent().parent().addClass("er");
						o.obj.parent().parent().append("<span class='"+typeCss+"'>"+msg+"</span>");
					}
				}
				else if(o.obj.attr("type")=="hidden"){
					o.obj.parent().parent().removeClass("er");
					o.obj.parent().find(".error").remove();
					if(o.type!=2){
						o.obj.parent().parent().addClass("er");
						o.obj.parent().append("<span class='"+typeCss+"'>请绑定手机</span>");
					}
				}
				else if(o.obj.attr("type")=="text"){
					o.obj.removeClass("er");
					o.obj.parent().find(".error").remove();					
					if(o.type!=2){
						o.obj.addClass("er");
						o.obj.parent().append("<span class='validform "+typeCss+"'>"+msg+"</span>");
					}
				}
				else{
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
					if(data.next==""){
						location.href=location.href;
					}
					else{
						location.href=data.next;
					}
				}
				else{
					layer.tips(data.message, $("#pcBasicForm .personalCbtn"), {
					  tips: [2, '#e95050'] //还可配置颜色
					});
				}
			}
		});
		qisValid.resetForm();
		var myTimer=option.time||"1990-01-01";
		new GySetDate({"targets":'#year1,#month2,#day3',"range":"1900-01-01,2030-09-21","value":myTimer});

		getTime();

		function getTime(){
			$(".pcsBasicTable .bir").val($("#year1").val()+"-"+$("#month2").val()+"-"+$("#day3").val());
		}
		
		$(".pcsBasicTable .birTD select").change(getTime);

		//关闭消息
		$("#newMeg .cl").click(function(){
			$("#newMeg").modal("hide");
		});
		//新增手机
		$(".pcsBasicTable td.ph a").click(function(){
			if($(this).hasClass("addphone")){
				$("#newPhone .pt span").html("新增手机号");
			}
			else{
				$("#newPhone .pt span").html("修改手机号");
			}
			$(".captchaMy").children().remove();
			th.captchaMy(".captchaMy","verifyMobile/",function(cap){
				captchaPhone=cap;
			});
			$("#newPhone").modal("show");
		});
		$("#newPhone .personalCbtn").click(function(){			
			var $th=$(this);	
			$.when(sendsms($th)).then(function(a){
				$("#newPhone2 .pm").slideUp();
				var npa=$("#newPhone2 .fg > a");
				npa.addClass("smsend").html("重发验证码(<span>5</span>s)");
				setInObj=setInterval(_foo($("#newPhone2 .fg > a>span"),60,function(){
					npa.html("重发验证码").removeClass("smsend");
					npa.unbind().click(onceSend);
				}),1000);
			});
		});
		$("#newPhone2 .personalCbtn").click(function(){
			var $th=$(this);
			$.ajax({
				type: "POST",
				url:"/home/settings/bind_mobile/",
				data:{"mobile":PhoneValue,"mobile_code":$("#newPhone2 .pcsBasicTableTxt").val()},
				dataType:"json",
				beforeSend:function(XMLHttpRequest){
					$th.css("pointer-events","none");
				},
				success: function(data) {						
					if(data.success){
						$(".pcsBasicTable td.ph").html("");
						$(".pcsBasicTable td.ph").prepend(PhoneValue+' <span>(已验证)</span><a class="editphone">修改手机</a>');
						$(".pcsBasicTable td.ph input").val(PhoneValue);
						$("#newMeg").modal("show");	
						setInObj=setInterval(_foo($("#newMeg .p2>span"),5,function(){
							$("#newMeg").modal("hide");
						}),1000);
					}
					else{
						$("#newPhone2 .pm").html(data.message).slideDown();
					}			
				},
				complete: function(XMLHttpRequest){
					$th.css("pointer-events","auto");
				}
			});
		});

		var isRegist = $('#user_center_course_record').val();// $('#');
		//模块弹出
		if(isRegist == 'true'){
			$("#interestCourse").modal('show');
		}

		var index = 0,oLis,oSpan;
			oLis = $("#interestCourse .modal-body li");
			oSpan = $("#interestCourse .modal-footer span");
		oSpan.click(function(){
			pages = parseInt((oLis.length-1)/6);//获取页数
			if(index < pages){
				index++;
			}else{
				index = 0;
			}
			//隐藏所以li,再显示需要显示的li
			oLis.hide().slice(6*index,6*(index+1)).fadeIn();
		});

		if(oLis.length<=6){
			oSpan.unbind("click");//当li个数小于等于6个时，取消点击事件
		};
		
	}	

	module.exports = {
		"init":personalCenterSbasic
	};
	
})