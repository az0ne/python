// 获取需要显示大图的图片列表
var getShowBigImgList = function() {
	var img_list = [];
	var img = $('img');
	for(var i = 0; i < img.length; ++i) {
		if($(img[i]).attr('data-tag') == 'showBigImg') {
			img_list.push($(img[i]).attr('_src'));
		}
	}
	return img_list;
};

// 图片放大或缩小
function resizeImg(isSmall) {
	var big_img = $('.big_img');
	var client_height = $('.show_big_image').height();
	if(!isSmall) {
		big_img.height(big_img.height() * 1.1);
		big_img.css({'margin-top':(client_height-big_img.height())/2});
	} else {
		big_img.height(big_img.height() * 0.9);
		big_img.css({'margin-top':(client_height-big_img.height())/2});
	}
};
// 显示需要查看大图的图片
function showBigImg() {
	var show_position, html, current_img;
	img_arr = arguments[0] ? arguments[0] : null;
	show_position = arguments[1] ? arguments[1] : null;
	current_img = arguments[2] ? arguments[2] : null;
	html = '<img class="big_img" src="' + current_img + '" />'
	for(var i = 0; i < img_arr.length - 1; ++i) {
		if(img_arr[i] == current_img) {
			current_index = i;
		}
	}
	show_position.html(html);

	var img = new Image();
	img.src = current_img;
	var img_height = img.height;
	var client_height = $('.show_big_image').height();
	$('.big_img').css({'transform':'rotate(0deg) scale(1, 1)','height':client_height-40,'margin-top':'20px'});
};

var showBigImgMain = function(){
	var rotate_deg = 0, current_index = 0;
	// 获取所有需放大查看图片列表
	$(window).resize(function(){
		var client_height = $('.show_big_image').height();
		$('.big_img').css({'margin-top':(client_height-$('.big_img').height())/2});
	});

	// 查看大图
	$(".ckdt").off('click').on('click',function() {
		var img_arr = getShowBigImgList();
		$('.show_big_image').show();
		showBigImg(img_arr, $('.show_big_image .images'), $(this).siblings('img').attr('_src'));
	});
	// 关闭放大图片
	$('.viewer-close').off('click').on('click',function() {
		$('.show_big_image').hide();
	});
	$(window).keyup(function(e) {　　　
		if(e.keyCode == 27) { //此处代表按的是键盘的Esc键
			　　　　　
			$('.show_big_image').hide();　　　　
		}　　　
	});
	// 监听鼠标滚轮事件
	$(".images").each(function() {
		if(/firefox/.test(navigator.userAgent.toLowerCase())) { // 判断浏览器是否是火狐浏览器
			$('.show_big_image').off().on("DOMMouseScroll", function(event) {
				if(event.originalEvent.detail < 0) {
					resizeImg(false);
				} else {
					resizeImg(true);
				}
				event.originalEvent.preventDefault(); //去掉浏览器默认滚动事件
				event.stopPropagation();
			});
		} else {
			$('.show_big_image').off().on("mousewheel", function(event) {
				var e = e || event,
					v = e.originalEvent.wheelDelta || e.originalEvent.detail;
				if(v > 0) {
					resizeImg(false); //放大图片呗
				} else {
					resizeImg(true); //缩小图片喽
				}
				window.event.returnValue = false; //去掉浏览器默认滚动事件
				e.stopPropagation();
				return false;
			});
		}
	});

	// 显示下一张图
	$('.viewer-next').off('click').on('click', function() {
		++current_index;
		if(current_index >= img_arr.length) {
			current_index = 0;
		}

		$('.big_img').attr('src', img_arr[current_index]);
	});
	// 显示上一张图
	$('.viewer-prev').off('click').on('click', function() {
		--current_index;
		if(current_index < 0) {
			current_index = img_arr.length - 1;
		}
		$('.big_img').attr('src', img_arr[current_index]);
	});
	// 图片向左旋转90度
	$('.viewer-rotate-left').off('click').on('click', function(){
		rotate_deg -= 90;
		$(this).parents('.viewer-footer').siblings('.images').children('.big_img').css({'transform': 'rotate('+rotate_deg+'deg)'});
	});
	// 图片向右旋转90度
	$('.viewer-rotate-right').off('click').on('click', function(){
		rotate_deg += 90;
		$(this).parents('.viewer-footer').siblings('.images').children('.big_img').css({'transform': 'rotate('+rotate_deg+'deg)'});
	});
	// 放大图片按钮
	$('.viewer-zoom-in').off('click').on('click', function(){
		resizeImg(false);
	});
	// 缩小图片按钮
	$('.viewer-zoom-out').off('click').on('click', function(){
		resizeImg(true);
	});
}
$(showBigImgMain());