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
  })
  
  //登陆
  $('#btnLogin').on('click', function () {
    $('#registerModal').modal('hide');
  })
  $('.show-card').on('click', function (event) {
    event.stopPropagation();
  })
  $('.dt-username').on('click', function (event) {
    event.preventDefault();
    event.stopPropagation();
    $('.show-card-wrap').toggleClass('in');
  })

  //忘记密码
  $('#btnForgetpsw').on('click', function () {
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
              html += "<a style=background-color:"+course.course_color+" href=/course/"+ course.id +"/recent/play/ >" + course.name + "</a>";
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
        var _parent_left = $('.v5-topbar-login').offset().left;
        var _parent_outw = $('.v5-topbar-login').outerWidth();
        var _this_outw = $('.show-card').outerWidth();
        var _this_left = Math.abs(_parent_left - (_this_outw - _parent_outw));
        $('.show-card').css({
            'left': _this_left
        })
    }
    show_card();
    $(window).resize(function(){
        show_card();
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