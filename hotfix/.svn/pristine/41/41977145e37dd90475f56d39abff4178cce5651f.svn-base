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
        //enableContextMenu: false, // 关闭右键
        wordCount: false, //关闭字数统计
        autoHeightEnabled: false, // 关闭窗口自增长
        initialStyle:'p{color: #7a7a7a;font-size: 14px;line-height:1em;font-family: Microsoft Yahei;}img{max-width:100%;}'
    });
};

/*创建页提交*/
$("#bdeditor .submit-problem").on("click", function(){
    var strContentcreate = ue.getContent(),
        problemContainer = $('#problem-container');
    if(strContentcreate == "" || ue.getContentTxt() == '请输入你的问题'){
        layer.alert('内容不能为空', {
            skin: 'layui-layer-molv',
            closeBtn: 0
        });
    }else{
        $.ajax({
            url: '/lps4/student_coach/' + careerId + '/',
            type: 'POST',
            data: {'content': strContentcreate},
            success: function(data){
                htmlTemp = $('<div class="item new"><div class="fl"><img src="' + data.data.head + '" alt=""/><p class="font14 textC bold">' + data.data.name + '</p></div><a href="" class="right"><p class="problem-desc font14">' + data.data.content + '</p></a><p class="problem-time font14">' + data.data.create_date + '提问于' + data.data.source + '</p></div>');
                if(data.success){
                    problemContainer.prepend(htmlTemp);
                }else{
                    layer.alert(data.message, {
                        skin: 'layui-layer-molv',
                        closeBtn: 0
                    });
                };
                setTimeout(function(){
                    $('.item').removeClass('new');
                }, 3000);
                ue.ready(function() {
                    ue.setContent('<p style="color: #7a7a7a;font-size: 14px;font-family: "Microsoft Yahei";">请输入你的问题</p>');
                });
            }
        });
    }
});


