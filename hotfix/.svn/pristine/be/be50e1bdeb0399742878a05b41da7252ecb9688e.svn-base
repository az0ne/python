$(function(){
    //登录全局
    $('.zynewLogin_div_name').unbind().on('click', function (event) {
        event.preventDefault();
        event.stopPropagation();
        $('.show-card-wrap').toggleClass('in');
    });
    $(document).on('click', function() {
        $('.show-card-wrap').removeClass('in');
    });
    function show_card(){
        var _parent_left = $('.zynewLogin_div').offset().left;
        var _parent_outw = $('.zynewLogin_div').outerWidth();
        var _this_outw = $('.show-card').outerWidth();
        var _this_left = Math.abs(_parent_left - (_this_outw - _parent_outw));
        $('.show-card').css({
            'left': _this_left
        })
    }
    show_card();
    var pane,pane2;
    function zzload(){
        $('.playlist2').height($(window).height()-120);
        pane = $('.playlist2').jScrollPane({
            mouseWheelSpeed:10
        });
    }
    zzload();
    $(".d-task-list>li>div").unbind().click(function(){
        if($(this).parent().hasClass("activeH")){
            $(this).parent().removeClass("activeH");
        }else{
            $(this).parent().addClass("activeH");
        }
        zzload();
    });
    //侧边
    $(".zvright a").on("click",function(){
        if(!$(this).hasClass("aH")){
            if($(".zvright a.aH").length==0){
                $(".zvrightSreen").css("right",0);
                $(".zvright").css("right","340px");
            }
            $(this).addClass("aH").siblings().removeClass("aH");
        }
        else{
            $(this).removeClass("aH");
            $(".zvrightSreen").css("right",-340);
            $(".zvright").css("right","0px");
        }
    });

    $(".examinationMain").height($(window).height()-156);
    $(window).resize(function(){
        show_card();
        zzload();
        $(".examinationMain").height($(window).height()-156);
    });
    //$(".zvright a").eq(0).trigger("click");
    $(".modal").on("show.bs.modal", function(){
        var $this = $(this);
        var $modal_dialog = $this.find(".modal-dialog");
        var div=$('<div style="display:table; width:100%; height:100%;"></div>')
        div.html('<div style="vertical-align:middle; display:table-cell;"></div>');
        div.children("div").html($modal_dialog);
        $this.html(div);
    });
    //-----------------未完成---------------
    $(".d-task-list .zyleve1 li a,.d-task-list > li.last a").unbind().live("click",function () {
        if ($(this).attr("href")) {

        }
        else {
            var num = $(".zyunfinish").length;
            if (num > 0) {
                var li = $(".zyunfinish").eq(num - 1).parent().parent();
                if(!li.hasClass("error")) {
                    li.addClass("error").children("a").append('<span class="colorf10 font12 marginR10 wei">未完成</span>');
                }
                if (li.parent().css("display") == "none") {
                    li.parent().prev().trigger("click")
                }

                //$('html,body').stop().animate({scrollTop: li.offset().top - 200}, 800);
            }
        }
    });

})
var ts=0,cb;
function timer(callback){
    (callback)&&(cb=callback)
    var nts=ts;
    var dd = parseInt(nts / 60 / 60 / 24, 10);
    var hh = parseInt(nts / 60 / 60 % 24, 10);
    var mm = parseInt(nts / 60 % 60, 10);
    var ss = parseInt(nts % 60, 10);
    dd = checkTime(dd);
    hh = checkTime(hh);
    mm = checkTime(mm);
    ss = checkTime(ss);
    $(".examinationD_hred .t").html('<span class="bold">'+mm+'</span><span class="font14">分</span><span class="bold">'+ss+'</span><span class="font14">秒</span>');
    ts-=1;
    if(ts<0){
        if (cb) {
            cb.call();
        };
        return;
    }
    setTimeout(timer,1000);
}
function checkTime(i){
   if (i < 10) {
       i = "0" + i;
    }
   return i;
}
function RunOnBeforeUnload() {
    window.onbeforeunload = function(e){
        e = e || window.event;
        if (e) {
            e.returnValue = '确定退出答题吗？/n你的答题记录将不会保存';
        }
        return '确定退出答题吗？/n你的答题记录将不会保存';
    }
}
//下一节
function nextcourse(){
    var goA=$(".zyleve1>li,.zvrightSreen .d-task-list li.last");
    goA.each(function(index,ele){
        if($(ele).hasClass("liH")){
            //goA.eq(index+1).find("a").trigger("click");
            var zyleve1_href=goA.eq(index+1).find("a").attr("hid_href")
            if(zyleve1_href) location.href=zyleve1_href;
        }

        if(goA.length-1==index){
            location.href==$(ele).find("a").attr("hid_href")
        }
    })

}
