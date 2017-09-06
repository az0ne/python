var ue = createUE("bdeditor");
ue.ready(function() {
    ue.setContent('<p style="color: #7a7a7a;font-size: 14px;font-family: "Microsoft Yahei";">请输入你的问题</p>');
});

ue.addListener('focus',function(){
    if(ue.getContentTxt() == '请输入你的问题'){
        ue.setContent('');
    }
});
function createUE(name){
    return UE.getEditor(name,{
        toolbars:[['simpleupload']],
        autoClearinitialContent: true,
        autoFloatEnabled: false,
        wordCount: false,
        elementPathEnabled: false,
        initialFrameHeight: 200,
        initialFrameWidth:1028,
        initialContent: '请输入你的问题',
        autoClearEmptyNode: true, // 清除空标签
        enableContextMenu: false, // 关闭右键
        wordCount: false, //关闭字数统计
        autoHeightEnabled: false, // 关闭窗口自增长
        initialStyle:'p{color: #7a7a7a;font-size: 14px;line-height:1em;font-family: Microsoft Yahei;}img{max-width:100%;}'
    });
};


/*详情页提交*/
$(".submit-problem").on("click",function(){
    var strContentadd = ue.getContent();
    if(strContentadd == "" || ue.getContentTxt() == '请输入你的问题'){
        layer.alert('内容不能为空', {
            skin: 'layui-layer-molv',
            closeBtn: 0
        });
    }else{
        $.ajax({
            url: '/lps4/coach/' + $('.detailes-container').attr('data-coach-id') + '/',
            type: 'POST',
            data: {'content': strContentadd},
            success: function(data){
                if(data.success){
                    window.location.reload();
                }else{
                    layer.alert(data.message, {
                        skin: 'layui-layer-molv',
                        closeBtn: 0
                    });
                }
            }
        });
    }
});