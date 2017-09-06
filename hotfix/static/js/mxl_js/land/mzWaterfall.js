$(window).on("load", function() {
	mzWaterfal();
	//加载更多评论
	$(".load-more-comment").click(function() {
		var _this = $(this);
		var html = '<li>' +
			'										<div class="review-bcontainer-t-pic">' +
			'											<img src="images/review-bcontainer-t-pic.jpg" alt="" />' +
			'										</div>' +
			'										<div class="clear review-bcontainer-t">' +
			'											<div class="fl review-bcontainer-t-l">' +
			'												<b>后期添加的数据</b>' +
			'												<div class="mzedu-student-review-score dib">' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'												</div>' +
			'											</div>' +
			'											<span class="fr">' +
			'											45分钟前' +
			'										</span>' +
			'										</div>' +
			'										<div class="review-bcontainer-contxt">' +
			'											<div class="review-bcontainer-txt-sdu">' +
			'												作为一个刚入门的前端工程师，用这个视频教程作为学习 Vue 真是太好了，主要之前没怎么接触过模块化设计，网上对将这些方面的又不是很多。这个教程很 nice。1 天半看了 1/3 了，毫无难度，通俗易懂。唯一的一点不足就是这不是 Vue 2.0 的，有些不一样的地方我还得翻官方文档去改。但总的来说很好。点赞！' +
			'											</div>' +
			'											<div class="review-bcontainer-txt-tec">' +
			'												<b>老师回复：</b>感谢支持~ 能学会使用 Vue 开发实战项目就是本门课的宗旨~由于课程录制时间比较早选择的是 1.0 的。' +
			'											</div>' +
			'										</div>' +
			'									</li>' +
			'									<li>' +
			'										<div class="review-bcontainer-t-pic">' +
			'											<img src="images/review-bcontainer-t-pic.jpg" alt="" />' +
			'										</div>' +
			'										<div class="clear review-bcontainer-t">' +
			'											<div class="fl review-bcontainer-t-l">' +
			'												<b>周安伟</b>' +
			'												<div class="mzedu-student-review-score dib">' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'												</div>' +
			'											</div>' +
			'											<span class="fr">' +
			'											45分钟前' +
			'										</span>' +
			'										</div>' +
			'										<div class="review-bcontainer-contxt">' +
			'											<div class="review-bcontainer-txt-sdu">' +
			'												作为一个刚入门的前端工程师，用这个视频教程作为学习 Vue 真是太好了，主要之前没怎么接触过模块化设计，网上对将这些方面的又不是很多。这个教程很 nice。1 天半看了 1/3 了，毫无难度，通俗易懂。唯一的一点不足就是这不是 Vue 2.0 的，有些不一样的地方我还得翻官方文档去改。但总的来说很好。点赞！' +
			'											</div>' +
			'										</div>' +
			'									</li>' +
			'									<li>' +
			'										<div class="review-bcontainer-t-pic">' +
			'											<img src="images/review-bcontainer-t-pic.jpg" alt="" />' +
			'										</div>' +
			'										<div class="clear review-bcontainer-t">' +
			'											<div class="fl review-bcontainer-t-l">' +
			'												<b>周安伟</b>' +
			'												<div class="mzedu-student-review-score dib">' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'												</div>' +
			'											</div>' +
			'											<span class="fr">' +
			'											45分钟前' +
			'										</span>' +
			'										</div>' +
			'										<div class="review-bcontainer-contxt">' +
			'											<div class="review-bcontainer-txt-sdu">' +
			'												作为一个刚入门的前端工程师</div>' +
			'										</div>' +
			'									</li>' +
			'									<li>' +
			'										<div class="review-bcontainer-t-pic">' +
			'											<img src="images/review-bcontainer-t-pic.jpg" alt="" />' +
			'										</div>' +
			'										<div class="clear review-bcontainer-t">' +
			'											<div class="fl review-bcontainer-t-l">' +
			'												<b>周安伟</b>' +
			'												<div class="mzedu-student-review-score dib">' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'												</div>' +
			'											</div>' +
			'											<span class="fr">' +
			'											45分钟前' +
			'										</span>' +
			'										</div>' +
			'										<div class="review-bcontainer-contxt">' +
			'											<div class="review-bcontainer-txt-sdu">' +
			'												作为一个刚入门的前端工程师，用这个视频教程作为学习 Vue 真是太好了，主要之前没怎么接触过模块化设计，网上对将这些方面的又不是很多。这个教程很 nice。1 天半看了 1/3 了，毫无难度，通俗易懂。唯一的一点不足就是这不是 Vue 2.0 的，有些不一样的地方我还得翻官方文档去改。但总的来说很好。点赞！' +
			'											</div>' +
			'											<div class="review-bcontainer-txt-tec">' +
			'												<b>老师回复：</b>感谢支持~ 能学会使用 Vue 开发实战项目就是本门课的宗旨~由于课程录制时间比较早选择的是 1.0 的。' +
			'											</div>' +
			'										</div>' +
			'									</li>' +
			'									<li>' +
			'										<div class="review-bcontainer-t-pic">' +
			'											<img src="images/review-bcontainer-t-pic.jpg" alt="" />' +
			'										</div>' +
			'										<div class="clear review-bcontainer-t">' +
			'											<div class="fl review-bcontainer-t-l">' +
			'												<b>周安伟</b>' +
			'												<div class="mzedu-student-review-score dib">' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'													<i class="mzicon mzicon-star"></i>' +
			'												</div>' +
			'											</div>' +
			'											<span class="fr">' +
			'											45分钟前' +
			'										</span>' +
			'										</div>' +
			'										<div class="review-bcontainer-contxt">' +
			'											<div class="review-bcontainer-txt-sdu">' +
			'												作为一个刚入门的前端工程师，用这个视频教程作为学习 Vue 真是太好了，主要之前没怎么接触过模块化设计，网上对将这些方面的又不是很多。这个教程很 nice。1 天半看了 1/3 了，毫无难度，通俗易懂。唯一的一点不足就是这不是 Vue 2.0 的，有些不一样的地方我还得翻官方文档去改。但总的来说很好。点赞！' +
			'											</div>' +
			'											<div class="review-bcontainer-txt-tec">' +
			'												<b>老师回复：</b>感谢支持~ 能学会使用 Vue 开发实战项目就是本门课的宗旨~由于课程录制时间比较早选择的是 1.0 的。' +
			'											</div>' +
			'										</div>' +
			'									</li>';
		$(".review-load-more-item").before(html);
		mzWaterfal();
	});
});

function mzWaterfal() {
	var $aPin = $(".mzedu-student-review-bcontainer").find("li");
	var iPinW = $aPin.eq(0).outerWidth();
	var num = 2;
	var pinHArr = [];
	var topArr = [];
	$aPin.each(function(index, value) {
		var pinH = $aPin.eq(index).height();
		if(index < num) {
			pinHArr[index] = pinH;
		} else {
			var minH = Math.min.apply(null, pinHArr);
			var minHIndex = $.inArray(minH, pinHArr);
			$(value).css({
				'position': 'absolute',
				'top': minH + 40,
				'left': $aPin.eq(minHIndex).position().left
			});
			pinHArr[minHIndex] += $aPin.eq(index).height() + 40;
		}
		topArr.push($(value).position().top)
	});
	var topArrLen = topArr.length - 1;
	$(".mzedu-student-review-bcontainer ul").height(topArr[topArrLen] + $aPin.eq(topArrLen).outerHeight())
}