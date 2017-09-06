define(function(require, exports, module) {
	require('select')($);
	//-------------FUNTION-----------------.
	//构造函数
	function broadcastM(th){
		init();
	}
	function ajax_living_page(step){
		//异步请求直播分页
		var edu_admin_id=$(".cs_select").val();
		$.ajax({
			type: 'GET',
			url: '/lps3/ea/living/ajax_living_page/?edu_admin_id='+edu_admin_id+'&step='+step+'',
			dataType: "html",
			success: function (data) {
				$('#living_content').html(data);
			},
			error: function (data) {
				console.error("service data error");
			}
		});
	}
	
	function init(op){
		$(".cs_select").iSimulateSelect({width:178,height:0,selectBoxCls:"cs_info_selectD",optionCls:"cs_info_selectD_Op"});
		$(".cs_select").change(function(e){
			var text=$(this).children("[selected]").html();
			$(".selectEND span").html(text);
		});
		//绑定考勤事件
		var meetbo=true;
		$("#living_content").on({"click":function(){
			var class_meeting_id=$(this).attr('class_meeting_id');
			var class_id=$(this).attr('class_id');
            var $th=$(this);
            if(!meetbo){return;}
            meetbo=false;
			$.ajax({
				type: 'GET',
				url: '/lps3/ea/living/ajax_living_attendance/'+class_id+'/'+class_meeting_id+'/',
				dataType: "html",
				success: function (data) {
					$("#attendance").html(data);
					$('#attendance').attr({'class_id':class_id,'class_meeting_id':class_meeting_id});
					$('#attendance').modal('show');
					$(".zy_newclose").unbind().click(function(){
						$(".modal").modal("hide");
					});
                    meetbo=true;
				},
                beforeSend:function(XMLHttpRequest){
                    $th.css({"pointerEvents":"none"});
                },
                complete: function(XMLHttpRequest){
                    $th.css({"pointerEvents":"auto"});
                }

			});
		}
		},".broadcastList>li .hover[class_meeting_id]");

		$('#attendance').on('click','.reload',function(){
			var class_meeting_id=$('#attendance').attr('class_meeting_id');
			var class_id=$('#attendance').attr('class_id');
			$.ajax({
				type: 'GET',
				url: '/lps3/ea/living/ajax_living_attendance/'+class_id+'/'+class_meeting_id+'/'+'?update=true',
				dataType: "html",
				success: function (data) {
					$("#attendance").html(data);
					$(".zy_newclose").unbind().click(function(){
						$(".modal").modal("hide");
					});
				},
                beforeSend:function(XMLHttpRequest){},
                complete: function(XMLHttpRequest){}

			});
		});
		$(".sManage_Sel_sreach_btn").on({"click":function(){
			ajax_living_page(0);
		}
		});
		$("#living_content").on({"click":function(){
			ajax_living_page(parseInt($(this).attr("p"),10));
		}
		},".broadcast_tit a");
	}
	//-------------FUNTIONEND-----------------	
	module.exports = {
		"init":broadcastM
	};
})