$(function(){

    function popupMsg(obj){
        obj.modal({show:true, keyboard:false,backdrop: 'static'});
        $('.close, .know').on('click', function(){
            obj.modal('hide');
        });
    }

	$(".d-task-list,.d-task-list ").unbind().on({
		"click": function () {
			if ($(this).attr("href")) {

			}
			else  if ($(this).attr("desc") == "task_is_lock") {
				popupMsg($('#popup-1'))
			}
			else{
				var num = $(".zyunfinish").length;
				if (num > 0) {
					var li = $(".zyunfinish").eq(num - 1).parent().parent();
					if (!li.hasClass("error")) {
						li.addClass("error").children("a").append('<span class="colorf10 font12 marginR10 wei">未完成</span>');
					}
					if (li.parent().css("display") == "none") {
						li.parent().prev().trigger("click")
					}

					//$('html,body').stop().animate({scrollTop: li.offset().top - 200}, 800);
				}
			}
		}
	}, ".zyleve1 li a, > li.last a");
});
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
			var goAindex=goA.eq(index+1);
			if(goAindex.find("a").attr("href")){
				var zyleve1_href=goAindex.find("a").attr("hid_href");
				if(zyleve1_href) location.href=zyleve1_href;
			}
			else{
				goAindex.find("a").trigger("click");
			}
		}
		if(goA.length-1==index){
			location.href==$(ele).find("a").attr("hid_href")
		}
	})

}