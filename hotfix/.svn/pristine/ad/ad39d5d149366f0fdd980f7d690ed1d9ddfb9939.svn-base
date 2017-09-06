define(function(require, exports, module) {
	require('select')($);require('multiselect')($);require('textFiltered')($);
	var zmap=new Map(),timeArray=new Array(),mysort=true,mypaystate=[],mylearningstate=[],th=this;
	var deanUrl={"ct":"/change/","ls":"/quit/","ds":"/pause/"};
	//-------------FUNTION-----------------.
	//构造函数
	function studentM(th,option){
		init(option);
	}
	//升序
	function ascending (){
		mysort=true;	var j=1;
		$(".sManage_table .people").remove();
		timeArray=timeArray.quickSort();
		for(var i=0;i<timeArray.length;i++){
			var tr=zmap.get(timeArray[i].toString());
			if((mypaystate.length==0||mypaystate.indexOf(tr.find("[pay-state]").attr("pay-state"))>-1)
				&&(mylearningstate.length==0||mylearningstate.indexOf(tr.find("[learning-state]").attr("learning-state"))>-1)
			){
				tr.children().eq(0).html(j);j++;
				$(".sManage_table").append(tr);
			}

		}
	}
	//降序
	function descending (){
		mysort=false;	var j=1;
		$(".sManage_table .people").remove();
		timeArray=timeArray.quickSort();
		for(var i=timeArray.length-1;i>-1;i--){
			var tr=zmap.get(timeArray[i].toString());
			if((mypaystate.length==0||mypaystate.indexOf(tr.find("[pay-state]").attr("pay-state"))>-1)
				&&(mylearningstate.length==0||mylearningstate.indexOf(tr.find("[learning-state]").attr("learning-state"))>-1)
			){
				tr.children().eq(0).html(j);j++;
				$(".sManage_table").append(tr);
			}
		}
	}
	//筛选
	function filterval(e,value){
		mypaystate=value;
		mysort?ascending():descending();
	}
	function filterval2(e,value){
		mylearningstate=value;
		mysort?ascending():descending();
	}
	//------------FUNCTIONEND---------	
	//初始化
	var init=function(op){
		op=op||{};
		$th=this;
		th.userV = new UserVail("vail");
		$(".modal").on({"click":function(){
				$(".modal").modal("hide");
			}
		},".zy_newclose");
		var sid;
		//静态数据
		var csmap=new Map(),ctmap=new Map(),csArray=[],ctArray=[];
		$(".sManage_table .people").each(function(index, element) {
			csmap.put($(this).children('[pay-state]').attr("pay-state"),0);
			ctmap.put($(this).children('[Learning-state]').attr("Learning-state"),0);
		});
		csmap.each(function(k,v,i){
			csArray.push(k);
		});
		ctmap.each(function(k,v,i){
			ctArray.push(k);
		});
		
		//退学等处理
		$(".sManage_table").on({
			"click":function(){
				sid=$(this).attr("sid").split("_");
				var th=$(this);
				$.ajax({
					 type: "GET",
					 url: "/lps3/ea/students/"+sid[1]+"_"+sid[2]+deanUrl[sid[0]]+"",
					 dataType: "html",
					 success: function(data){
						$("#leaveschool").html(data);
						$("#leaveschool").modal("show");
					 },
					error:function(){

					},
					beforeSend:function(XMLHttpRequest){
						th.css({"pointerEvents":"none"});
					},
					complete: function(XMLHttpRequest){
						th.css({"pointerEvents":"auto"});
					}
				 });
			}
		},".operation>a[data-target]");
		$("#leaveschool").on({"click":function(){
			var $th=$(this);
			var thNext=$th.next();
			if((!(th.userV.get("toclass"))||/^[ ]+$/.test(th.userV.get("toclass")))
				&&(!(th.userV.get("remark"))||/^[ ]+$/.test(th.userV.get("remark")))
			){
				thNext.removeClass("megRight").addClass("megError").html("不能为空");
				thNext.width(134);
				return ;
			}
			if(th.userV.get("remark").length>100){
				thNext.removeClass("megRight").addClass("megError").html("不能多余100字");
				thNext.width(134);
				return;
			}
			$.ajax({
				 type: "POST",
				 url: "/lps3/ea/students/"+sid[1]+"_"+sid[2]+deanUrl[sid[0]]+"",
				 data:$("#leaveschoolForm").serialize(),
				 dataType: "json",
				 success: function(data){
					if(data.status){
						thNext.removeClass("megError").addClass("megRight").html(data.message);
						setTimeout(function(){location.reload()},1000);
					}
					else{
						thNext.removeClass("megRight").addClass("megError").html(data.message);
					}
					thNext.width(134);
					setTimeout(function(){thNext.width(0);},4000);
				 },
					error:function(){
						thNext.removeClass("megError").addClass("megRight").html("系统错误");
						setTimeout(function(){location.reload()},1000);
					},
					beforeSend:function(XMLHttpRequest){
						$th.attr("disabled","disabled");
					},
					complete: function(XMLHttpRequest){
						$th.removeAttr("disabled");
					}
			});

			}
		},".deanframebtn");
		//教务班级事件
		$(".sm_select").change(function(){
			//var text=$(this).children("[selected]").html();
			$("#deanClassTxt").val("");
		})

		$(".sm_select").iSimulateSelect({width:148,height:0,selectBoxCls:"sm_info_selectD",optionCls:"sm_info_selectD_Op"});
		$(".sManage_table").on({
			"mouseenter":function(){
				$(this).parent().css("zIndex",3);
				$(this).children(".tstage_child").show();
			},"mouseleave":function(){
				$(this).parent().css("zIndex",2);
				$(this).children(".tstage_child").hide();
			}
		},".tstage>div");

		$(".sManage_table .people").each(function(index, element) {
			zmap.put($(this).children('[ttime]').attr("ttime"),$(element));
			timeArray.push(parseInt($(this).children('[ttime]').attr("ttime"),10));
		});
		var specialtyname=csArray || [],specialtyvalue=csArray.concat() || []
			,tearchername=ctArray || [],tearchervalue=ctArray.concat() || [];
		//多选
		$(".multiselect2").multiselect({
			model:"multiplechoice"
			,"height":350
			,"arrayname":specialtyname
			,"arrayvalue":specialtyvalue
			,"selectvalue":"全部"
			,onSelect:filterval
		});
		$(".multiselect3").multiselect({
			model:"multiplechoice"
			,"height":350
			,"arrayname":tearchername
			,"arrayvalue":tearchervalue
			,"selectvalue":"全部"
			,onSelect:filterval2
		});
		//排序
		$(".multiselect1").multiselect({
			onSelect:function(e,value){
				if(value==1)
					ascending();
				else
					descending();
			}
		});
		//查询筛选框
		$(".sManage_Seltxt").textFiltered({
			"onkeyup":function(){
				var $th=this,bokey=false;
				$.ajax({
					type: "GET",
					url:"/lps3/ea/common/get_classes/",
					data:{"e":$("#lps4dean").val(),"s":$th.val()},
					beforeSend:function(XMLHttpRequest){

					},
					success: function(data1) {
						$th.clear();
						for(var i=0;i<data1.length;i++){
							$th.addNode(data1[i][0],data1[i][1]);
							if(data1[i][1]==$th.val()){$th.data("vv",data1[i][0]);bokey=true;}
						}
					},
					complete: function(XMLHttpRequest){
					}
				});
				if(!bokey) $th.removeData("vv");
			}
			,"height":360
			,"onarrowupdown":function(i){
			}
			,"onVclick":function(v){
				this.data("vv",v);
			}
			,onload:function(){
				(op.newid)&&(this.data("vv",op.newid))
			}
		});
		//第一个搜索
		var errornum=0
		$("#deanClassBtn").click(function(){
			var vv=$("#deanClassTxt").data("vv");
			if(vv&&vv!="-1"){
				location.href=changeURLPar(location.href.split("?")[0],"c",vv);
			}
			else{
				var thN=$(this).next();
				if(errornum>2)
					thN.css({"opacity":1}).html("请到下拉框中选择");
				else
					thN.css({"opacity":1}).html("条件错误，请重新查询");
				setTimeout(function(){thN.css({"opacity":0})},2000);
				errornum++;
			}
		})
		$("#deanClassBtn2").click(function(){
			var val=$("#deanClassTxt2").val().replaceAll(" ","");
			if(val!="") {
				var url = changeURLPar(location.href.split("?")[0], "q", val);
				url = changeURLPar(url, "e", $("#lps4dean").val());
				location.href = url;
			}
		});
	}	
	
	
	module.exports = {
		"init":studentM
	};
	
})