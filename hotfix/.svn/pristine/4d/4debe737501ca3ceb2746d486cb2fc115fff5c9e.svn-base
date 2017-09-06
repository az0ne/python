$(function(){
    var ue = createUE("onevone_ueditor");
    ue.ready(function() {
		ue.setContent('<p style="color: #7a7a7a;font-size: 14px;font-family: "Microsoft Yahei";"></p>');
	});
	//(ue).addListener('focus',function(){
	//	if(ue.getContentTxt() == '继续向老师提问'){
	//		ue.setContent('');
	//	}
	//});
    function createUE(name){
		return UE.getEditor(name,{
			toolbars:[['simpleupload']],
			autoClearinitialContent: true,
			autoFloatEnabled: false,
			wordCount: false,
			elementPathEnabled: false,
			initialFrameHeight: 128,
			initialFrameWidth:718,
			initialStyle:'p{color: #7a7a7a;font-size: 14px;line-height:1em;font-family: Microsoft Yahei;}img{max-width:100%;}'
		});
	}

	/*创建页提交*/
	$(".oneVoneServiceList .submit_reviews_create").on("click",function(){
		var strContentcreate = UE.getEditor('onevone_ueditor').getContent();
		var post_url = $('#onevone_service_sub_url').val();
		var jump_url = $('#onevone_service_list_url').val();
		if(strContentcreate == ""){
			layer.alert('内容不能为空', {
                skin: 'layui-layer-molv',
                closeBtn: 0
            });
		}else{
			$.ajax({
				url: post_url,
				type: 'POST',
				data: {'content': strContentcreate},
				success: function(data){
					if(data.success){
						window.location.href = jump_url;
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



	/*详情页提交*/
	$("#sub_service_reply").on("click",function(){
		var strContentadd = UE.getEditor('onevone_ueditor').getContent();
		var post_url = $('#onevone_service_add_url').val();
		if(strContentadd == ""){
			layer.alert('内容不能为空', {
                skin: 'layui-layer-molv',
                closeBtn: 0
            });
		}else{
			$.ajax({
				url: post_url,
				type: 'POST',
				data: {'content': strContentadd},
				success: function(data){
					if(data.success){
						layer.alert('发送成功', {
                            skin: 'layer-ext-moon',
                            closeBtn: 0
                        });
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
});
