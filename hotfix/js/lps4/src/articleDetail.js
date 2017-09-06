define(function(require, exports, module) {
	var login_popup = require('./main').login_popup;

	function articleDetail(t){
		init();
	}
	//初始化
	var init = function(){
		var ue, ueSmall;

		ue = createUE("reviews_ueditor");
		ueSmall = createUE("reviews_ueditor_small");
		ue.ready(function() {
			ue.setContent('<p style="color: #999999;font-size: 14px;">说点什么吧...</p>');
		});
		ueSmall.ready(function() {
			ueSmall.setContent('<p style="color: #999999;font-size: 14px;">说点什么吧...</p>');
		});

		(ue).addListener('focus',function(){
			if(ue.getContentTxt() == '说点什么吧...'){
				ue.setContent('');
			}
		});

		(ueSmall).addListener('focus',function(){
			if(ueSmall.getContentTxt() == '说点什么吧...'){
				ueSmall.setContent('');
			}
		});

		// 点赞
		onPraise();
		function onPraise(){
			var praise = $('.praise-btn'),
				articleID = get_article_id(),
				off = true;

			praise.on('click',function(){
				if(is_login()) {
					$(this).addClass('good');
					if(off){
						$.ajax({
							type: 'POST',
							url: '/common/ajax/like/article',
							data: {article_id: articleID},
							success: praiseSuccess,
							complete: function(){
								praise.addClass('disabled_praise');
							}
						});
						off = false;
					}
				}else{
					login_popup();
				}
			});
		}

		$('.not_sign a').on('click',function(){
			login_popup();
		});

		function createUE(name){
			return UE.getEditor(name,{
				toolbars:[['insertcode', 'simpleupload','emotion']],
				autoClearinitialContent: true,
				autoFloatEnabled: false,
				wordCount: true,
				maximumWords: 1000,
				elementPathEnabled: false,
				initialFrameHeight: 94
			});
		}

		// 加载评论
		$.ajax({
			type: 'GET',
			url: '/common/ajax/get/discuss',
			data: {'object_type': 'ARTICLE', 'object_id': get_article_id()},
			success: loadSuccess
		});

		// 用户是否登录
		function is_login() {
			var l = $('#this_user').val();
			return l == 'True';
		}
		// 获取文章id
		function get_article_id() {
			return $('#article_id').val();
		}
		// 获取获取媒体文件url头路径
		function get_media_url() {
			return $('#MEDIA_URL').val();
		}

		// 获取回复按钮的最上层div
		function get_button_parent_div(obj) {
			var parent_div = $(obj).parent().parent().parent().parent();
			return parent_div;
		}
		// 获取回复的父级的id跟parent_id
		function get_comment_id_parent_id(obj) {
			var c_id = $(obj).attr('data-id'),
				p_id = $(obj).attr('data-parent-id');
			return {'id': c_id, 'parent_id': p_id};
		}
		// 获取回复的父级div
		function get_parent_div(obj) {
			var parent_div = $(obj).parent().parent();
			return parent_div;
		}
		// 获取回复按钮的最高层父级div
		function get_button_real_parent_div(obj) {
			var parent_div = get_button_parent_div(obj);
			var p_i_d = get_comment_id_parent_id(parent_div);
			if (parseInt(p_i_d.parent_id) != 0) {
				return get_parent_div(parent_div);
			} else {
				return parent_div;
			}
		}

		// 给回复标签绑定点击事件，检查是否登录
		function bound_reply_event() {
			$('.reviews_answer').on({'click':function(){
				if (is_login()) {
					var div = $(this).parent().siblings(".divUEContent");
					if ($(div).html() == "") {
						$(".reviews_answer a").text("回复");
						$(".divUEContent").html("");
						var divUE = $("#divUE").html();
						$(div).html(divUE);
						$(this).text("收起");
					}else{
						$(div).html("");
						$(this).text("回复");
					}
				} else {
					login_popup();
				}

				$('.submit_reviews').on({'click':function(){
					onReplay(this);
				}},'button');

			}},'a')
		}

		// 回复成功后插入html
		function insert_html_dom(obj, html) {
			var insert_dom = $(obj).children('.col_r').children('.divUEContent');
			insert_dom.after(html);
		}

		// 回复评论

		function onReplay(obj){
			var str = ueSmall.getContent(),
				content = ueSmall.body.innerHTML.replace(/<[^>]+>/g, "").replace(/&nbsp;/g, "").replace(/​/, "").trim(),
				parent_div = get_button_real_parent_div(obj);
			var parent_id = get_comment_id_parent_id(parent_div).id;
			var oBtn = $('.divUEContent .submit_reviews');
			if(str != '' && ueSmall.getContentTxt() == '说点什么吧...'){
				oBtn.find('span').css('left',0).text('至少15个字符');
				ueSmall.setContent('');
			}else if(content.length < 15){
				oBtn.find('span').css('left',0).text('至少15个字符');
			}else{
				$.ajax({
					type: 'POST',
					url: '/common/ajax/add/discuss',
					data: {'object_type': 'ARTICLE', 'object_id': get_article_id(), 'parent_id': parent_id, 'comment': str},
					success: function(data) {
						if (data.success) {
							var html = '';
							html += '<div parent="parent_0" class="item child" data-id="' + data.id + '" data-parent-id="' + data.parent_id + '">';
							html += '<div class="col_l"><a href="'+ $('.sign_reviews a').attr('href') +'" target="_blank"><img src="' + $('.sign_reviews img').attr('src') + '" alt="' + $('.sign_reviews .nike_name').text() + '"></a></div>';
							html += '<div class="col_r" style="width: 710px;">';
							html += '<p><span class="nike_name">' + $('.sign_reviews .nike_name').text() + '</span><span class="date_time">刚刚</span></p>';
							html += '<p>' + str + '</p>';
							html += '<p class="reviews_answer"><a href="javascript:void(0);">回复</a></p>';
							html += '<div class="divUEContent"></div>';
							html += '</div>';
							html += '</div>';

							insert_html_dom(parent_div, html);
							bound_reply_event();
							$(".reviews_answer a").text("回复");
							$(".divUEContent").html("");
						} else {
							oBtn.find('span').css('left',0).text('提交失败');
						}
					}
				});
			}

		};

		function commentSuccess(data){
			var oBtn = $('.submit_reviews');
			if (data.success) {
				var html = '',
					content = ue.getContent();

				ue.setContent('');
				oBtn.find('span').css('left',0).text('提交成功');

				html += '<div parent="parent_0" class="item" data-id="' + data.id + '" data-parent-id="' + data.parent_id + '">';
				html += '<div class="col_l"><a href="'+ $('.sign_reviews a').attr('href') +'" target="_blank"><img src="'+ $('.sign_reviews img').attr('src') +'" alt="'+ $('.sign_reviews .nike_name').text() +'"></a></div>';
				html += '<div class="col_r" style="width: 710px;">';
				html += '<p><span class="nike_name">'+ $('.sign_reviews .nike_name').text() +'</span><span class="date_time">刚刚</span></p>';
				html += '<p>'+ content +'</p>';
				html += '<p class="reviews_answer"><a href="javascript:void(0);">回复</a></p>';
				html += '<div class="divUEContent"></div>';
				html += '</div>';
				html += '</div>';

				$('.reviews_lists').prepend(html);
				bound_reply_event();
			} else {
				oBtn.find('span').css('left',0).text('提交失败');
			}
		}

		// 评论
		$('.submit_reviews').on({'click':function(){
			var str = ue.getContent(),
				oBtn = $('.submit_reviews'),
				content = ue.body.innerHTML.replace(/<[^>]+>/g, "").replace(/&nbsp;/g, "").replace(/​/, "").trim(),
				num = 0;
			//判断字符长度
			if(str != '' && ue.getContentTxt() == '说点什么吧...'){
				oBtn.find('span').css('left',0).text('至少15个字符');
				ue.setContent('');

			}else if(content.length < 15){
				oBtn.find('span').css('left',0).text('至少15个字符');

			}else{
				$.ajax({
					type: 'POST',
					url: '/common/ajax/add/discuss',
					data: {'object_type': 'ARTICLE', 'object_id': get_article_id(), 'parent_id': 0, 'comment': str} ,
					success: commentSuccess
				});
			}

			$(".reviews_answer a").text("回复");
			$(".divUEContent").html("");

		}},'button');

		var onComment = function(){
		}

		// 点赞返回函数
		function praiseSuccess(data) {
			var praiseTotal = $('.praise-btn span i');
			praiseTotal.text(data.like_num);
		}

		// 加载更多评论返回函数
		function loadSuccess(data){
			var html = '',
				parent_id,
				oList = $('.reviews_lists');
			$('.reviews_num').text(data.discuss_total + '条评论');
			data = data.discuss;

			if(data.length > 0){
				for(var i =0; i < data.length; ++i){
					parent_id = data[i].id;
					if(data[i].parent_id == 0){
						//添加父评论html
						html += '<div id = "' + data[i].id + '" class="item" data-id="' + data[i].id + '" data-parent-id="0">';
						html += '<div class="col_l"><a href="/u/' + data[i].user_id + '" target="_blank"><img src="'+ get_media_url() + data[i].head +'" alt="'+ data[i].nick_name +'"></a></div>';
						html += '<div class="col_r" style="width: 710px;">';
						html += '<p><span class="nike_name">'+ data[i].nick_name +'</span><span class="date_time">'+ data[i].date +'</span></p>';
						html += '<p>'+ data[i].content +'</p>';
						html += '<p class="reviews_answer"><a href="javascript:void(0);">回复</a></p>';
						html += '<div class="divUEContent"></div>';

						for(var j =0; j < data.length; ++j){
							if(data[j].parent_id == parent_id){
								//添加子评论html
								html += '<div class="item child" data-id="' + data[j].id + '" data-parent-id="' + parent_id + '">';
								html += '<div class="col_l"><a href="/u/' + data[j].user_id + '" target="_blank"><img src="'+ get_media_url() + data[j].head +'" alt="'+ data[j].nick_name +'"></a></div>';
								html += '<div class="col_r" style="width: 640px;">';
								html += '<p><span class="nike_name">'+ data[j].nick_name +'</span><span class="date_time">'+ data[j].date +'</span></p>';
								html += '<p>' + data[j].content + '</p>';
								html += '<p class="reviews_answer"><a href="javascript:void(0);">回复</a></p>';
								html += '<div class="divUEContent"></div>';
								html += '</div>';
								html += '</div>';
							}
						}
						html += '</div>';
						html += '</div>';
					}
				}
				oList.append(html);
				bound_reply_event();
			}
		}
	};

	module.exports = {
		"init":articleDetail
	};
});