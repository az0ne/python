define(function(require, exports, module) {
	require('select')($);require('textFiltered')($);require('multiselect')($);
	var myspecialty=[],mytearcher=[],zmap=new Map();;
	//-------------FUNTION-----------------.
	//构造函数
	function statisticsM(th,op){
		var op=op ||{};init(op);
	}
	function filterval2(e,value){
		myspecialty=value;
		filtered();
	}
	function filterval3(e,value){
		mytearcher=value;
		filtered();
	}
	function filtered (){
		var j=1;
		$(".sManage_table .people").remove();
		zmap.each(function(k,d,i){
			var tr=d;
			if((myspecialty.length==0||myspecialty.indexOf(tr.find("[class-specialty]").attr("class-specialty"))>-1)&&
				(mytearcher.length==0||findtype(mytearcher,tr.find("[class-tearcher]"),"class-tearcher"))
			){
				tr.children().eq(0).html(j);j++;
				$(".sManage_table").append(tr);
			}
		});
		function findtype(mytearcher,elem,value){
			for (var i=0;i<elem.length;i++){
				if (mytearcher.indexOf($(elem[i]).attr(value))>-1){
					return true;
				}
			}
			return false;
		}
	}
	function init(op){
		//静态筛选数据
		var csmap=new Map(),ctmap=new Map(),csArray=[],ctArray=[];
		$(".sManage_table .people").each(function(index, element) {
			csmap.put($(this).children('[class-specialty]').attr("class-specialty"),0);
			$(this).children('.teacherName').children('[class-tearcher]').each(function(){
				ctmap.put($(this).attr("class-tearcher"),0);
			})
		});
		csmap.each(function(k,v,i){
			csArray.push(k);
		});
		ctmap.each(function(k,v,i){
			ctArray.push(k);
		});
		
		$(".sManage_table .people").each(function(index, element) {
			zmap.put(index,$(element));
		});
		$(".ssMore").hover(function(){
			var ssMorediv=$(this);
			if(ssMorediv.children(".ssMorediv").length<=0){
				var html='';
				html+='<div class="ssMorediv"><i></i>';
				html+='<p><span>1.授课语言准确，清晰流畅，通俗易懂</span> 5分</p>';
				html+='<p><span>2.授课思路敏捷、逻辑性强、条理清晰</span> 4分</p>';
				html+='<p><span>3.语速控制适当，声音洪亮、富有激情</span> 5分</p>';
				html+='</div>';
				ssMorediv.append(html);
			}
			ssMorediv.children(".ssMorediv").show();
		},function(){
			$(this).children(".ssMorediv").hide();
		});

		//查询筛选框
		$(".sManage_Seltxt").textFiltered({
			"onkeyup":function(){
				var $th=this,bokey=false;
				$.ajax({
					type: "GET",
					url:"/lps3/ea/common/get_eduadmins/",
					data:{"s":$th.val()},
					beforeSend:function(XMLHttpRequest){

					},
					success: function(data1) {
						$th.clear();
						for(var i=0;i<data1.length;i++){
							$th.addNode(data1[i][0],data1[i][1]);
							if($th.val()==data1[i][1]){$th.data("vv",data1[i][0]);bokey=true;}
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
		var specialtyname=csArray || [],specialtyvalue=csArray.concat() || []
			,tearchername=ctArray || [],tearchervalue=ctArray.concat() || [];
		//专业
		$(".multiselect2").multiselect({
			model:"multiplechoice"
			,"height":350
			,"arrayname":specialtyname
			,"arrayvalue":specialtyvalue
			,"selectvalue":["全部","全部"]
			,onSelect:filterval2
		});
		//教师
		$(".multiselect3").multiselect({
			model:"multiplechoice"
			,"height":350
			,"arrayname":tearchername
			,"arrayvalue":tearchervalue
			,"selectvalue":["全部","全部"]
			,onSelect:filterval3
		});
		//搜索
		var errornum=0;
		$("#eduadmin_det").click(function () {
			var vv = $("#deanClassTxt").data("vv");
			var url = changeURLPar(location.href.split("?")[0], "year", $("#year_value").val());
			url = changeURLPar(url, "month", $("#month_value").val());
			url = changeURLPar(url, "eu_id", vv);
			var thN=$(this).next();
			if(vv&&vv!="-1") {
				location.href = url;
			}
			else{
				if(errornum>2)
					thN.css({"opacity":1}).html("请到下拉框中选择");
				else
					thN.css({"opacity":1}).html("条件错误，请重新查询");
				setTimeout(function(){thN.css({"opacity":0})},2000);
				errornum++;
			}

		});
	}
	//-------------FUNTIONEND-----------------	
	module.exports = {
		"init":statisticsM
	};
})