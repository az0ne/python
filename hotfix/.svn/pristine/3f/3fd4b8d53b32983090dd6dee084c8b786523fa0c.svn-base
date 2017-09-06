//初始化
function init(){
    var $footerAd = $('.footer-ad'), $div_li = $('.tab_menu li span');
    
    $div_li.on('click',function(){
        $(this).parent().addClass('active').siblings().removeClass('active');
        var index = $div_li.index(this);
        $('.tab_box > div').eq(index).show().siblings().hide();
    });
    $footerAd.find('i').on('click',function(){
        $footerAd.hide();
    });
}
init();