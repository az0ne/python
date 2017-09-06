$(function(){
  $(document).on('click', function() {
    $('#hotkeyword').slideUp();
    $('#keyword-group').slideUp();
    $('.show-card-wrap').removeClass('in');
  });
  $(document).mousewheel(function(event, delta, deltaX, deltaY) {
      $('#hotkeyword').slideUp();
      $('#keyword-group').slideUp();
      $('.show-card-wrap').removeClass('in');
  });
  //弹出框显示后的一些操作
  $('.modal').on({
    'show.bs.modal': function (e) {
      $(this).children('.modal-dialog')
      .css('margin','0 auto')
      .wrap('<div class="wrap-modal-main"></div>')
      .wrap('<div class="wrap-modal-con"></div>');
      $('.wrap-modal-main').css({
        'display': 'table',
        'width': '100%',
        'height': '100%'
      });
      $('.wrap-modal-con').css({
        'display': 'table-cell',
        'width': '100%',
        'vertical-align': 'middle'
      });

    },
    'shown.bs.modal': function (e) {
      $(this).find('.form-control').first().focus();
    }
  });
    $(".top_meg").hover(function(){
			$(this).children(".bubble").show()
		},function(){
			$(this).children(".bubble").hide()
		});

    //顶部搜索
    $(".topSreach").click(function(){
        $(this).parent().parent().toggleClass("sH")
    })

  //登陆
  $('#btnLogin').on('click', function () {
    $('#registerModal').modal('hide');
  })
  $('.show-card').on('click', function (event) {
    event.stopPropagation();
  })
  $('.top_user .sp').on('click', function (event) {
    event.preventDefault();
    event.stopPropagation();
    $('.show-card-wrap').toggleClass('in');
  })

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
    
  })

  //注册
  $('#btnRegister').on('click', function () {
    $('#loginModal').modal('hide');
  })

  //search
    var $keywordGroup = $("#keyword-group"),
        $careerCourses = $keywordGroup.find(".careercourses"),
        $courses = $keywordGroup.find(".courses"),
        isSearching = false,
        SEARCHING_PLACEHOLDER = "<div><a href='javascript:void(0);'>搜索中...</a></div>",
        EMPTY_PLACEHOLDER = "<div><a href='javascript:void(0);'>无</a></div>",
        FAIL_PLACEHOLDER = "<div><a href='javascript:void(0);'>搜索中...</a></div>";

    var creatCoursesHtml = function(courses, linkBaseUrl) {
        var html = "";
        if(linkBaseUrl == 'recent'){
            courses.forEach(function(course) {
              html += "<a style=background-color:"+course.course_color+" href=/course/"+ course.id +"/recent/play/"+ "?stageid=" + course.stage_id + " >" + course.name + "</a>";
            });
        }else{
          courses.forEach(function(course) {
              html += "<a style=background-color:"+course.course_color+" href=/"+ linkBaseUrl + course.id +
                  ">" + course.name + "</a>";
          });
        }

        return html;
    };

    $('#search').on({
        click: function(event) {
            event.stopPropagation();
        },
        focus: function() {
            if($(this).val() == '') {
                $('#hotkeyword').show();
            } else {
                $('#keyword-group').show();
            }
        },
        keyup: function(event) {
            // var keycode = (event.keyCode ? event.keyCode : event.which);
            //   if(keycode == '13'){
            //     alert('wwwwww');
            //   }
            var $currTarget = $(event.currentTarget),
                keyword = $currTarget.val();
                def_search(keyword);



        },
        paste:function(event){
        	    $currTarget = $(event.currentTarget);
        		setTimeout(function(){
        			keyword = $currTarget.val();
        			def_search(keyword);
        		}, 100);


        }
    });



    $('.search-dp').click(function(event) {
        event.stopPropagation();
    });

    $('#hotkeyword').on("click", "a", function(event) {
        event.preventDefault();
        $('#search').val($(this).text());
        $('#search').trigger("keyup");
        $('#hotkeyword').hide();
        $('#keyword-group').show();
    });

    $('.keyword-group').jScrollPane({
      autoReinitialise: true
    });
  //点击收藏
  $('.house').on('click', function (event) {
    event.preventDefault();
    var _thisI = $(this).children('i');
    var _thisIclass = _thisI.hasClass('v5-icon-saved');
    _thisI.toggleClass('v5-icon-saved');
    var _text = (_thisIclass == true) ? '收藏' : '已收藏';
    $(this).children('span').text(_text);
  });

  $('.plan-tip').hover(function() {
    $('.plan-tip-box').addClass('show');
  }, function() {
    $('.plan-tip-box').removeClass('show');
  });

  $('.feedback-switch').click(function(){
    $(this).toggleClass('active');
    var _has_active = $(this).hasClass('active');
    if(_has_active){
      $(this).parent('.feedback').animate({
        bottom:0
      },500);
    }
    else{
      $(this).parent('.feedback').animate({
        bottom:'-300px'
      },500);
    }
  });

  $('img#viptips').hover(function(){
    $(this).tooltip({
      template: '<div class="tooltip tooltip-vip" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>'
    });
    $(this).tooltip('show');
  },function(){
    $(this).tooltip('hide');
  });

  $('[data-toggle="tooltip"]').hover(function(){
    $(this).tooltip('show');
  },function(){
    $(this).tooltip('hide');
  });

//搜索函数
 function def_search(keyword){


  	        if(typeof keyword === "undefined" || keyword.length < 1) {
            	$('#hotkeyword').show();
            	$('#keyword-group').hide();
                return;
            }
            if (isSearching === true) {
                return;
            }
            isSearching = true;

            $('#hotkeyword').hide();

            if (keyword === "") {
                $('#hotkeyword').show();
                $('#keyword-group').hide();
                isSearching = false;
                return;
            }

            $courses.html(SEARCHING_PLACEHOLDER);
            $careerCourses.html(SEARCHING_PLACEHOLDER);

            $.get("/common/course/search/", {keyword: keyword})
                .done(function(res) {
                    // refresh courses
                    if ("courses" in res && res["courses"].length > 0) {
                        $courses.html(creatCoursesHtml(res["courses"], "recent"));
                    } else {
                        $courses.html(EMPTY_PLACEHOLDER);
                    }

                    // refresh career courses
                    if ("career_courses" in res && res["career_courses"].length > 0) {
                        $careerCourses.html(creatCoursesHtml(res["career_courses"], "course/"));
                    } else {
                        $careerCourses.html(EMPTY_PLACEHOLDER);
                    }
                })
                .error(function(error) {
                    $courses.html(FAIL_PLACEHOLDER);
                    $careerCourses.html(FAIL_PLACEHOLDER);
                }).
                always(function() {
                    isSearching = false;
                    $('#keyword-group').show();
                });
  }

  //登录后
    function show_card(){
        if($('.top_user').length>0) {
            var _parent_left = $('.top_user').offset().left;
            var _parent_outw = $('.top_user').outerWidth();
            var _this_outw = $('.show-card').outerWidth();
            var _this_left = Math.abs(_parent_left - (_this_outw - _parent_outw));
            $('.show-card').css({
                'left': _this_left
            })
        }
    }
    show_card();
    $(window).resize(function(){
        show_card();
    });

    $(".zy_menu_D").hover(function(){
        $(".zy_menu_div2").html($("#zy_menu_div2_txt").val());
        $(this).children(".zy_menu_div2_arr").show();
        $(this).children(".zy_menu_div2").stop().slideDown();

    },function(){
         $(this).children(".zy_menu_div2_arr").hide();
        $(this).children(".zy_menu_div2").stop().slideUp();
    })
});


function v5_popover_tpl(tpl_class,elem,popover_container,popover_placement,popover_trigger){
  var elem_popover = document.getElementById(elem);
  var popover_c = $('.' + popover_container);
  popover_c.popover({
    content:elem_popover,
    container:'body',
    template:'<div class="popover ' + tpl_class + '" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>',
    placement:popover_placement,
    trigger:popover_trigger,
    html: true
  });
}

function v5_addplan(){
  var plan_len = $('.add-task').siblings('section').find('.plan-block').length;
  if(plan_len==0){
    $('.add-task').css('margin-left',0);
  }
  else{
    $('.add-task').css('margin-left','40px');
  }
}
v5_addplan();
//Damon: 喇叭气泡
function notice_message(){
  function notice_info(data){
    var Txt = '';
    Txt += '<li><a href="'+_fps_site_url+'chat/?type=system">系统消息&nbsp;<span>'+ (data.sys_msg_count == 0 ? '' : data.sys_msg_count) + '</sapn></a></li>';
    //var uu=_fps_site_url +"common/dynmsg/";
    //if(data.dyn_msg_count > 0){uu=_fps_site_url+"common/dynmsg/?unread=1&page=1";}
    //Txt += '<li><a href="'+uu+'">动态&nbsp;<span>'+ (data.dyn_msg_count == 0 ? '' : data.dyn_msg_count) + '</sapn></a></li>';
    //Txt += '<li><a href="'+_fps_site_url+'common/social/?list_type=fans">粉丝&nbsp;'+ (data.fan_msg_count == 0 ? '' : data.fan_msg_count) + '</sapn></a></li>';
    //Txt += '<li><a href="'+_fps_site_url+'chat/?type=praise">赞&nbsp;'+ (data.praise_msg_count == 0 ? '' : data.praise_msg_count) + '</sapn></a></li>';
    //Txt += '<li><a href="'+_fps_site_url+'chat/?type=at">@我&nbsp;'+ (data.at_msg_count == 0 ? '' : data.at_msg_count) + '</sapn></a></li>';
    return Txt;
  }

  var oUl = $('.bubble');
  $.ajax({
     url: _fps_site_url+'chat/',
     xhrFields: {withCredentials: true},
     type: 'POST',
     dataType: 'json',
     success: function (data) {
        if(data.status == 'success') {
            var num = data.sys_msg_count; //+ data.dyn_msg_count + data.fan_msg_count + data.praise_msg_count + data.at_msg_count;
            var html = notice_info(data);
            if(num){
              $('.top_meg').addClass('top_megH');
              $('.top_megH i.Arial').css('display','block').html(num);
            }
            oUl.html(html).removeClass('loading');
        }
     }
  });

    $.ajax({
		 url: _fps_site_url+'common/user_fans_zan/',
		 type: 'POST',
		 dataType: 'json',
		 xhrFields: {
              withCredentials: true
           },
		 success: function (data) {
			if(data.status == 'success') {
				$(".zy_userDiv .d2 .s1").html(data.fans);
				$(".zy_userDiv .d2 .s2").html(data.praise);
			}
		 }
	  });
}

//拖拽验证
var captchaObjF,captchaObjF2,captchaObjF3;
var captcha = function(obj,ty){
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
        if(setting.ty=="mobile/"){
          captchaObjF=captchaObj;
        }else if(setting.ty==""){
          captchaObjF3=captchaObj;
        }else{
          captchaObjF2=captchaObj;
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