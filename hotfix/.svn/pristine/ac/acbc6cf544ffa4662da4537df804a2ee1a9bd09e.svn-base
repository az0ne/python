$(function(){

    //////  随机热门头像功能及函数:

    var total_images = 30;
    var need_images = 7;

    // 头像太多, hardcode is stupid, so generate the head image url dynamically.
    var generate_head_image_url = function(index){
        return "/static/images/mz_wap/head_images/" + index + "_small.png";
    }

    // 记录视频下方的参与用户的头像
    var hot_head_images = {};

    var generate_hot_images = function(){
          for (var i = 0; i < need_images; i++){  // 从头像中随机生成需要的hot_head_image
          while (true){
              var index = Math.floor(Math.random() * total_images);
              if (!hot_head_images[index]){ //不存在, 添加, 并跳出循环
                  hot_head_images[index] = true;
                  break;
              }
          }
       }
        var html = '';
        for (key in hot_head_images){	// 渲染到页面
            html += '<li><img class="ui-imglazyload" src="' + generate_head_image_url(key) + '" alt=""/></li>'
        }
        $(".course-count ul").html(html);
    };

    generate_hot_images();

    //////  随机热门头像功能及函数结束


    // 此用户是否已付费
    function is_paid() {
        return $('#is_paid').val() == 'True';
    };

    // 此课程是否需要付费观看
    function need_pay() {
        return $('#need_pay').val() == 'True';
    };

    // 获取当前播放的是第几章
    function get_current_lesson_index() {
        return $('ol li').index('li.active') + 1;
    };

    // 弹出支付弹窗
    function pop_pay() {
        $(".bg").fadeIn();
        $(".tips-box").fadeIn();
        $(".tips h4").html($(".course-banner h2").html());
    };

    //播放提示弹窗
//    $(".course-chapter ol li").each(function(){
//        $(".course-chapter li:nth-child(n+3) a").attr("href","javascript:void(0)");
//        $(this).bind("click",function(){
//            if($(this).index() > 1){
//                $(".bg").fadeIn();
//                $(".tips-box").fadeIn();
//            }
//            $(".tips h4").html($(".course-banner h2").html());
//        })
//    })

    //　关闭弹出窗口
    $(".close-box").bind("click",function(){
        $(".bg").fadeOut();
        $(this).parent().fadeOut();
    });


    var playerWrap = $('video');
    var player = playerWrap[0];

    playerWrap.ready(video_ready);

    // 视频播放控制函数

    function video_ready() {
        playerWrap.on("play", video_play);
        playerWrap.on("ended", video_ended);
    };

    // 相应视频播放的函数

    function video_play() {
        // 如果课程需要付费而用户为付费（或未登录）,则只运行看前两节;
        // 第三节只允许看前1分钟
        var play_flag = true;
        if (get_current_lesson_index() == 3 && need_pay() && !is_paid()) { // 判断当前播放的是第几章
            if (player.currentTime > 60) {
                player.pause();
                pop_pay();
                play_flag = false;
            }
            setInterval(function () {
                if (player.currentTime > 60 && play_flag) {
                    player.pause();
                    pop_pay();
                    play_flag = false;
                }
            }, 1000);
            return false;
        } else if (get_current_lesson_index() > 3 && need_pay() && !is_paid()) {
            player.pause();
            pop_pay();
            return false;
        }
    };

    // 播放完毕，弹出引导咨询框
    function video_ended() {
        pop_pay();
    };
})