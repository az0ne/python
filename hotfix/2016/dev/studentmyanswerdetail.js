$(".personalCTop .font .personalCico").hover(function(){
	layer.tips($(this).attr("title"), $(this), {
	  tips: [1, '#333333'] //还可配置颜色
	});
},function(){
	
});	
function is_login() {
    return $('.topRight').attr('login') == 'True';
}

var detailAnswerTextarea,
    detailAnswerUl, 
    replylinks, 
    replyname, 
    reply_id, 
    parent_id, 
    problem_id, 
    $personalInterlocutionDetailInfo = $('.personalInterlocutionDetailInfo');

	detailAnswerTextarea = $(".personalInterlocutionDetailAnswer .commentBody textarea");
	detailAnswerUl = $(".personalInterlocutionDetailAnswer ul");

//点赞
$personalInterlocutionDetailInfo.find('.infos dt').click(function(){
	if (is_login()) {
		var ths = $(this);
		var problem_id = ths.attr('data-discuss-id');
		$.ajax({
			url: '/home/s/ajax_praise/',
			method: 'POST',
			dataType: 'json',
			data: {'problem_id': problem_id},
			success:function(result){
				if (result['success']) {
					var action = result['data']['action'];
					var praise_count = result['data']['praise_count'];
					if (action == 'mark') {
						ths.html(praise_count);
						ths.addClass("parised");
					} else if (action == 'cancel') {
						ths.html(praise_count);
						ths.removeClass("parised");
					}
				} else {
					if (result['code'] == 401) {
						login_popup('登录状态已过期！');
						return false;
					}
				}
			}
		});
	} else {
		login_popup();
		return false;
	}
});

//初始化回复的内容
problem_id = $personalInterlocutionDetailInfo.attr('discuss_id');
parent_id  = problem_id;
replyname  = $personalInterlocutionDetailInfo.find('.infos .user strong').html();
reply_id   = $personalInterlocutionDetailInfo.find('.infos .user strong').attr('answer_user_id');

detailAnswerUl.on({"click": function(){
	var placeholdername = $(this).parents(".infos").find(".user strong").html();//回复名字
	detailAnswerUl.find('.reply').removeClass("click");
	$(this).addClass("click");
	replylinks = $(this).parents(".infos").find(".user>a").attr('href');
	detailAnswerTextarea.focus().attr('placeholder',"回复 "+placeholdername+"：");
	replyname  = $(this).parent().siblings('.user').find('strong').html();//回复名字
	reply_id   = $(this).parent().siblings('.user').find('strong').attr('answer_user_id');//回复ID
	parent_id  = $(this).parents('li').attr('discuss_id'); //回复的父ID
}}, '.reply');

$personalInterlocutionDetailInfo.on({'click':function(){
	problem_id = $personalInterlocutionDetailInfo.attr('discuss_id');
	parent_id  = problem_id;
	replyname  = $personalInterlocutionDetailInfo.find('.infos .user strong').html();
	reply_id   = $personalInterlocutionDetailInfo.find('.infos .user strong').attr('answer_user_id');
	detailAnswerTextarea.focus();
	//清除所有“click”类
	detailAnswerUl.find('.reply').removeClass("click");
	//
	detailAnswerTextarea.attr('placeholder','');
}}, '.reply');

//如果是回复的话
var replycontent;
$(".personalInterlocutionDetailAnswer .btn").on("click",function(){

	replycontent = detailAnswerTextarea.val();//获取回复内容
	var ajaxUrl = $(this).attr('ajaxUrl'),$btnBottm = $('.btnBottm'),html;
	//如果内容为空，不予以提交
	if(replycontent == ""){
		html = $('<span>请输入回复内容</span>');
		$btnBottm.prepend(html);
		return;
	}else{
		$btnBottm.find('span').remove();
	};

	//如果有“click”类，就说明是“回复”，则执行第一条；否则是直接回答
	if(detailAnswerUl.find('.click').hasClass("click")){
		ajax_add_answer(true,ajaxUrl);
	}else{
		ajax_add_answer(false,ajaxUrl);
	};
});
//提交回复
function ajax_add_answer(answerFlags,ajaxUrl){
	var data = {
		problem_id: problem_id,
		parent_id: parent_id,
		answer_user_id: reply_id,
		answer_nick_name: replyname,
		comment: replycontent
	}
	//提交回复
	$.ajax({
		url:ajaxUrl,
		dataType:'json',
		method: 'POST',
		data: data,
		success:function(result){
			if (result['success']){
				var resultData = result['data'];
				if (answerFlags){
					//回复的回复
					replyhtml = '<div class="item" discuss_id='+resultData['new_discuss_id']+'>'+
									'<a class="img" href="'+resultData['user_url']+'" target="_blank">' +
										'<img src="'+resultData['head']+'"/>' +
									'</a>' +
									'<div class="infos">'+
										'<div class="user">'+
											'<a href="'+resultData['user_url']+'" class="font14"><strong answer_user_id='+resultData['user_id']+'>'+resultData['nick_name']+'</strong></a>'+
											'<span class="replyTxt">回复<a target="_blank" href="'+replylinks+'">'+replyname+'</a></span>'+
										'</div>'+
										'<p>'+$('<div/>').text(replycontent).html()+'</p>'+
										'<div class="timeReply font14">'+
											'<span class="time">刚刚</span>'+
											'<span class="reply">回复</span>'+
										'</div>'+
									'</div>'+
								'</div>';
					detailAnswerUl.find('.click').parents("li").children(".infos").after(replyhtml);						
					
				}else{
					//直接回答
					var html = '<li discuss_id='+resultData['new_discuss_id']+'>'+
								'	<a class="img" href="'+resultData['user_url']+'" target="_blank">'+
								'		<img src="'+resultData['head']+'">'+
								'	</a>'+
								'	<div class="infos">'+
								'		<div class="user">'+
								'			<a href="'+resultData['user_url']+'" class="font14"><strong answer_user_id='+resultData['user_id']+'>'+resultData['nick_name']+'</strong></a>'+
								'		</div>'+
								'		<p>'+ $('<div/>').text(replycontent).html()+'</p>'+
								'		<div class="timeReply font14">'+
								'			<span class="time">刚刚</span>'+
								'			<span class="reply">回复</span>'+
								'		</div>'+
								'	</div>'+
								'</li>';
					detailAnswerUl.prepend(html);
				}
			//文本框置空
			detailAnswerTextarea.val("");
			//清除所有“click”类
			detailAnswerUl.find('.reply').removeClass("click");
			//回答数+1
			$(".discuss_count").text(parseInt($(".discuss_count").text())+1+' 回答')
			}
			else{
				html = $('<span>'+result['message']+'</span>');
				$('.btnBottm').prepend(html);
				setTimeout(function(){
					$('.btnBottm span').remove();
				}, 5000);
			}
		}
	});
}

// 加载更多评论
$('.load-more').on('click', function(){
	ajax_html();
});
//加载评论
function ajax_html(){
	//这里就是AJAX载入回复
	var ajaxUrl, param, end_id;

		ajaxUrl = $personalInterlocutionDetailInfo.attr("url");
		param   = "";
		end_id  = $('.personalInterlocutionDetailAnswer>ul>li:last').attr("discuss_id");

	if (end_id){
		param += '?end_id='+ end_id;
	}

	$.ajax({
		url:ajaxUrl + param,
		dataType:"html",
		success:function(html){
			//把新数据追加到对象中
			if(html==''){
				$('.load-more').text('没有更多');
				$('.load-more').off('click');
			}else{
				detailAnswerUl.append(html);
			}				
	   }
   });
}