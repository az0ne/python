/*二级菜单/小课程页面跳转*/
/*二级菜单/专业方向页面跳转*/
$('#careerCategory').off('click').on('click', function () {
    // $('#pageMain').load("/careerCatagory/list/");
  
});
/*二级菜单/职业广告页面跳转*/
$('#careerAd').off('click').on('click', function () {
    //$('#pageMain').load("/careerAd/list/");

});
/*二级菜单/首页标题页面跳转*/
$('#banner').off('click').on('click', function () {
    var url='/ads/bannermng/list/?action=query&page_index=1';
    window.location.href = url;

});
/*二级菜单/文章分类页面跳转*/
$('#articType').off('click').on('click', function () {
    $('#pageMain').load("/home/articleType/list/");
});


/*二级菜单/个人中心广告页面跳转*/
$('#userCenterAd').off('click').on('click', function () {
    // $('#pageMain').load("/userCenterAd/list/");

});

/*二级菜单/S+EO页面跳转*/
$('#objSEO').off('click').on('click', function () {
    $('#pageMain').load("/objSEO/list/");

});

/*二级菜单/对象标签关系页面跳转*/
$('#objTagRelation').off('click').on('click', function () {
    // $('#pageMain').load("/objTagRelation/list/");

});

/* 二级菜单标签管理菜单跳转 */
$('#managetag').off('click').on('click', function () {
    $('#pageMain').load("/courseCatagory/list/");

});

$("#careertagrelation").off('click').on('click', function () {
    $('#pageMain').load("/careerTagRelation/list/");

});


/*一级菜单点击，展示二级菜单动画设置*/
$('.firstLevelMenu').on('click', function () {
    $(this).children('span').toggleClass('glyphicon-chevron-right glyphicon-chevron-down');
});
/*修改文本时，错误信息*/
function warningPrompt(errorInfo) {
    $('#errorInfo').text(errorInfo);
    $('#errorInfoModal_1').animate({top: "0px"}, 1000);
    setTimeout(function () {
        $('#errorInfoModal_1').stop().animate({top: "-380px"}, 1000)
    }, 3000);
};

/*字符串中变量占位符,使用方式："***{0}****{1}".format(a,b)*/
String.prototype.format=function()
    {
      if(arguments.length==0) return this;
      for(var s=this, i=0; i<arguments.length; i++)
        s=s.replace(new RegExp("\\{"+i+"\\}","g"), arguments[i]);
      return s;
    };
