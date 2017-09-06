define(function(require, exports, module) {
	require('layerjs');
	$(".personalCTop .font .personalCico").hover(function(){console.log($(this).attr("title"))
		layer.tips($(this).attr("title"), $(this), {
		  tips: [1, '#333333'] //还可配置颜色
		});
	},function(){
		
	});
	var zhugeZ=window.zhuge||false;
	if(zhugeZ){
		var otherPageTxt="";
		if(window.otherPage){otherPageTxt="第三方访问";
			zhugeZ.track("第三方进入该个人中心的次数", {"事件位置": document.title,"热点关键词": "第三方"});
		}
		$(".personalCmainLmenu li a").click(function(e){
			var txt=$(e.target.parentNode).text();
			zhugeZ.track(otherPageTxt+"个人中心侧边菜单点击次数", {"事件位置": "个人中心侧边菜单","热点关键词": txt,"页面标题":document.title});
		});
		$(".pCcourseList li .describe .pbtn").click(function(){
			if($(this)=="继续学习"){zhugeZ.track("已报名课程中点击继续学习的点击数", {"事件位置": "已报名课程","热点关键词": "继续学习"});}
		});
		$(".personalCenterStasteList li .font .pcbtnP > a").click(function(){
			zhugeZ.track("体验课程中点击的点击数", {"事件位置": "体验课程","热点关键词": $(this).text()});
		});
		$(".teacherCenterList li > a").click(function(){
			zhugeZ.track("老师个人中心小课程的次数", {"事件位置": "老师个人中心","热点关键词": $(this).find(".font").children(".bold").text()});
		});
		$(".teacherCenterENDbox > .a").click(function(){
			zhugeZ.track("已毕业中点击班级历史数据的次数", {"事件位置": "老师已毕业班级","热点关键词": "班级历史数据"});
		});
		$(".eCother .personalCbtn").click(function(){
			zhugeZ.track("第三方点击查看职业课程的次数", {"事件位置": "教务面板","热点关键词": "去看看麦子职业课程"});
		});
	}
})