define(function(require, exports, module) {
	require('multiselect')($);require('textFiltered')($);require('uiwidget')($);require('fileupload')($);
	var nowdate=new Date();
	var zmap=new Map();
	var classMegStr={"ce":"确认关闭报名?","oe":"确认开启报名?","graduation":"确认毕业？"};
	var myclassstate=[],myspecialty=[],mytearcher=[];
	//-------------FUNTION-----------------.
	//构造函数
	function classM(th,op){
		op=op||{},init(op);
	}	
	
	function filterval1(e,value){
		myclassstate=value;
		filtered();
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
			if((myclassstate.length==0||myclassstate.indexOf(tr.find("[class-state]").attr("class-state"))>-1) &&
				(myspecialty.length==0||myspecialty.indexOf(tr.find("[class-specialty]").attr("class-specialty"))>-1)&&
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
		//静态数据
		var cnmap=new Map(),csmap=new Map(),ctmap=new Map(),cnArray=[],csArray=[],ctArray=[];
		$(".sManage_table .people").each(function(index, element) {
			cnmap.put($(this).children('[class-state]').attr("class-state"),0);
			csmap.put($(this).children('[class-specialty]').attr("class-specialty"),0);
			$(this).children('.teacherName').children('[class-tearcher]').each(function(){
				ctmap.put($(this).attr("class-tearcher"),0);
			})
		});
		cnmap.each(function(k,v,i){
			cnArray.push(k);
		});
		csmap.each(function(k,v,i){
			csArray.push(k);
		});
		ctmap.each(function(k,v,i){
			ctArray.push(k);
		});
		
		$(".zy_newclose,.zy_classMeg_btn>.a2").click(function(){
			$(".modal").modal("hide");
		});
		$(".zy_classMeg_btn>.a1").click(function(){
			var classid=$(this).attr("classid").split("_");
			$.ajax({
				type: "GET",
				url:"/lps3/ea/classes/update_state/",
				data:{"e":classid[1],"i":classid[2]},
				beforeSend:function(XMLHttpRequest){

				},
				success: function(data1) {
					location.reload();
				},
				complete: function(XMLHttpRequest){
				}
			});
		});
		//时间限制
		new GySetDate({"targets":'#year1,#month2,#day3',"range":nowdate.getFullYear()+"-"+(nowdate.getMonth()+1)+"-"+nowdate.getDate()+",2030-09-21","value":""})

		$(".sManage_table .people").each(function(index, element) {
			zmap.put(index,$(element));
		});

		$(".modal").on("show.bs.modal", function(e){
			var datameg=e.relatedTarget.getAttribute("data-meg");
			if(datameg){
				var datamegA=datameg.split("_"),zcM=$(".zy_classMeg>p");
				zcM.eq(0).html("班级编号 "+datamegA[0]);
				zcM.eq(1).html(classMegStr[datamegA[1]]);
				zcM.eq(2).children().eq(0).attr("classid",datameg);
			}
		});

		$(".deanframecreatebtn").click(function(){
			var $th=$(this),
				career_courseV=$("#createClassForm input[name=career_course]").val(),
				teacherV1,
				teacherV2,
				teacherNum,
				teacherRep,
				teacherNary,
				teacherArry = new Array(),
				edu_adminV=$("#createClassForm input[name=edu_admin]").val(),
				qq_groupV=$("#createClassForm input[name=qq_group]").val(),
				key_groupV=$("#createClassForm input[name=key_group]").val(),
				imageV=$("#createClassForm input[name=image]").val(),
				teacherL = $("#createClassForm .teachInfo .teacher").length;
			for(var i = 0;i<teacherL;i++){
				teacherArry[i] = $("#createClassForm .teachInfo .teacher").eq(i).find(".tpl input").val();
			}
			for (x in teacherArry){
				if(teacherArry[x]==""||teacherArry[x]=="-1"){
					teacherV1 = false;
					teacherNum = parseInt(x)+1;
				}
			}
			teacherNary=teacherArry.sort();
			for(var i=0;i<teacherArry.length;i++){
				if (teacherNary[i]==teacherNary[i+1]){
					teacherV2 = false;
				}
			}
			if(career_courseV.replaceAll(" ","")==""||career_courseV.replaceAll(" ","")=="-1"){
				$th.next().height(30).html("*请选择专业"); return;
			}
			else if(teacherV1 == false){
				$th.next().height(30).html("*请选择教师"+teacherNum); return;
			}
			else if(teacherV2 == false){
				$th.next().height(30).html("*教师重复，请重新选择"); return;
			}
			else if(edu_adminV.replaceAll(" ","")==""||edu_adminV.replaceAll(" ","")=="-1"){
				$th.next().height(30).html("*请选择教务"); return;
			}
			else if(qq_groupV.replaceAll(" ","")==""){
				$th.next().height(30).html("*请输入班级群号"); return;
			}
			else if(key_groupV.replaceAll(" ","")==""){
				$th.next().height(30).html("*请输入群Key值"); return;
			}
			else if(imageV.replaceAll(" ","")==""){
				$th.next().height(30).html("*请上传班级群二维码"); return;
			}
			else{
				$th.next().height(0).html("");
			}

			$.ajax({
				type: "POST",
				url:"/lps3/ea/classes/create_class/",
				data:$("#createClassForm").serialize(),
				dataType: "json",
				beforeSend:function(XMLHttpRequest){
					$th.attr("disabled","disabled");
				},
				success: function(data1) {
					if(data1.status){
						location.reload();
					}
					else{
						$th.next().height(30).html(data1.message);
					}
				},
				complete: function(XMLHttpRequest){
					$th.removeAttr("disabled");
				}
			});

		});
		var cStatename=cnArray || [],cStatevalue=cnArray.concat() || []
			,specialtyname=csArray || [],specialtyvalue=csArray.concat() || []
			,tearchername=ctArray || [],tearchervalue=ctArray.concat() || [];
		//班级状态
		$(".multiselect1").multiselect({
			model:"multiplechoice"
			,"height":350
			,"arrayname":cStatename
			,"arrayvalue":cStatevalue
			,"selectvalue":"全部"
			,onSelect:filterval1
		});
		//专业
		$(".multiselect2").multiselect({
			model:"multiplechoice"
			,"height":350
			,"arrayname":specialtyname
			,"arrayvalue":specialtyvalue
			,"selectvalue":"全部"
			,onSelect:filterval2
		});
		//教师
		$(".multiselect3").multiselect({
			model:"multiplechoice"
			,"height":350
			,"arrayname":tearchername
			,"arrayvalue":tearchervalue
			,"selectvalue":"全部"
			,onSelect:filterval3
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
							$th.addNode(data1[i][0],data1[i][1],data1[i][2]);
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
		//----添加班级下拉框---
		$(".csSreach").textFiltered({
			"onkeyup":function(){
				var $th=this,bokey=false;
				var career_courseObj=$("#createClassForm input[name=career_course]");
				$.ajax({
					type: "GET",
					url:"/lps3/ea/common/get_career_courses/",
					data:{"s":$th.val()},
					beforeSend:function(XMLHttpRequest){

					},
					success: function(data1) {
						$th.clear();
						for(var i=0;i<data1.length;i++){
							$th.addNode(data1[i][0],data1[i][1],data1[i][2]);
							if(data1[i][1]==$th.val()){career_courseObj.val(data1[i][0]);bokey=true;}
						}
					},
					complete: function(XMLHttpRequest){
					}
				});
				if(!bokey) career_courseObj.val("");
			}
			,"height":180
			,"onarrowupdown":function(i){
			}
			,"onVclick":function(v,v2){
				this.data("vv",v);
				//var d=new Date();
				var no=v2.toUpperCase()+ $("#createClassForm #year1").val()+ $("#createClassForm #month2").val()+ $("#createClassForm #day3").val();
				$("#numberS").html(no);
				$("#createClassForm input[name=class_no]").val(no).data("v2",v2);
				$("#createClassForm input[name=career_course]").val(v);
			}
		});
		$(".selectTime select").change(function(){
			var v2=$("#createClassForm input[name=class_no]").data("v2");
			if(v2){
			var no=v2.toUpperCase()+ $("#createClassForm #year1").val()+ $("#createClassForm #month2").val()+ $("#createClassForm #day3").val();
			$("#createClassForm input[name=class_no]").val(no);
			$("#numberS").html(no);
			}
		});
		tearcherSreach($(".tearcherSreach"));
		function tearcherSreach(node,inputNode){
			node.textFiltered({
				"onkeyup":function(){
					var $th=this,bokey=false;
					$.ajax({
						type: "GET",
						url:"/lps3/ea/common/get_teachers/",
						data:{"s":$th.val()},
						beforeSend:function(XMLHttpRequest){

						},
						success: function(data1) {
							$th.clear();
							for(var i=0;i<data1.length;i++){
								$th.addNode(data1[i][0],data1[i][1]);
								if(data1[i][1]==$th.val()){
									node.parents(".teacher").find(".tpl input").val(data1[i][0]);
									$("#teacherManage input[name=addteacher]").val(data1[i][0]);
									bokey=true;
								}
							}
						},
						complete: function(XMLHttpRequest){
						}
					});
					if(!bokey) node.parents(".teacher").find(".tpl input").val("");$("#teacherManage input[name=addteacher]").val("");
				}
				,"height":180
				,"onarrowupdown":function(i){
				}
				,"onVclick":function(v){
					this.data("vv",v);
					node.parents(".teacher").find(".tpl input").val(v);
					$("#teacherManage input[name=addteacher]").val(v);
				}
			});
		}

		$(".deanSreach").textFiltered({
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
							if(data1[i][1]==$th.val()){$("#createClassForm input[name=edu_admin]").val(data1[i][0]);bokey=true;}
						}
					},
					complete: function(XMLHttpRequest){
					}
				});
				if(!bokey) $("#createClassForm input[name=edu_admin]").val("");
			}
			,"height":180
			,"onarrowupdown":function(i){
			}
			,"onVclick":function(v){
				this.data("vv",v);
				$("#createClassForm input[name=edu_admin]").val(v);
			}
		});
		var errornum=0
		//教务查询
		$(".sManage_Sel_sreach_btn").click(function(){
			var vv=$("#deanClassTxt").data("vv");
			if(vv&&vv!="-1"){
				location.href=changeURLPar(location.href.split("?")[0],"b",vv);
			}
			else{
				var thN=$(this).next();
				if(errornum>2)
					thN.css({"opacity":1}).html("请到下拉框中选择");
				else
					thN.css({"opacity":1}).html("条件错误，请重新查询");
				setTimeout(function(){thN.css({"opacity":0})},2000);
				errornum++
			}
		});

		//创建班级滚动条
		require('mousewheel');
    	require('jscrollpane');

		var liNum = 0,
			html = "";

		$('#createClass,#teacherManage').jScrollPane({
			mouseWheelSpeed:100
		});
		$("#createClass .teachInfo").on({"click": function(){
			$('#createClass').jScrollPane({
				mouseWheelSpeed:100
			});
		}}, 'em');
		$("#createClass .teachInfo").on({"click": function(){
			var liIndex = $(this).parent(".teacher").index();
			var liLength = $(".teachInfo .teacher").length - 2;
			$(this).parent("li").remove();
			for(var i=liIndex;i<=liLength;i++){
				$(".teachInfo .teacher").eq(i).find(".tpl span").html('教师'+(i+1));
				$(".teachInfo .teacher").eq(i).find(".tpl input").attr("name",'teacher'+(i+1));
			}
		}}, '.del');
		$("#createClass .add").on("click",function(){
			liNum = $("#educational").index() + 1;
			var teaVlaue = $("#createClassForm .teachInfo .teacher").eq(liNum-2).find(".tpl input").val();
			if(liNum>10){
				console.log("对不起，最多只能添加10个老师");
				return;
			}

			if(teaVlaue.replaceAll(" ","")==""||teaVlaue.replaceAll(" ","")=="-1"){
				$("#createClassForm .teachInfo .teacher").eq(liNum-2).find(".showmoew input").focus();
				return;
			}

			html = '<li class="teacher">' +
			'<label class="tpl"><span>教师'+liNum+'</span><input type="hidden" name="teacher'+liNum+'"></label>' +
			'<span class="showmoew" style="margin-left:4px;"><input type="text" class="deanframetxt createClassTxt tearcherSreach" placeholder="输入教师姓名搜索" ></span>' +
			'<em class="del" style="margin-left:8px;">删除</em>' +
			'</li>';
			$("#educational").before(html);
			tearcherSreach($("#createClassForm .teachInfo li").eq(liNum-1).find(".tearcherSreach"));
		});

		/*创建班级*/
		$(".createClass").on("click",function(){
			$(".eduadminBoxBg").fadeIn();
			$("#createClass").stop().animate({
				right:"0"
			});
		});
		$("#createClass .zy_newclose").on("click",function(){
			$(".eduadminBoxBg").fadeOut();
			$("#createClass").stop().animate({
				right:"-450px"
			});
		});
		//图片上传
		$('#QRupload').fileupload({
			url:"/home/settings/avatar/upload/",
			dataType: 'json',
			autoUpload: true,
			add: function (e, data) {
				var uploadErrors = [];
				var acceptFileTypes = /^(png|jpg|jpeg)$/i;
				Ntype = data.originalFiles[0]['name'].split('.')[1];

				if (acceptFileTypes.test(Ntype)) {
					$(".file>span").html('更改');
				}else{
					$("#createClass .showFile img").attr("src","/images/createClassQRImg.png");
					uploadErrors.push('Not an accepted file type');
				}

				 if(uploadErrors.length==0){
					data.submit();
				  }

			},
			done: function (e, data) {
				data=data.result;
				if(data.success){
					var img_url = data.data.img_url;
					$("#QRurl").val(img_url);
					$("#createClass .showFile img").attr("src",img_url);
				}
			}
		});

		/*教师管理*/
		var class_id;
		$(".sManage_table").on({"click":function(){
			class_id=$(this).attr('class_id')
			$("#teacherManage table .list").remove();
			initManageTeachers(class_id);
			$(".eduadminBoxBg").fadeIn();
			$("#teacherManage").stop().animate({
				right:"0"
			});
		}},'.teacherManage');

		$("#teacherManage .zy_newclose").on("click",function(){
			$(".eduadminBoxBg").fadeOut();
			$("#teacherManage").stop().animate({
				right:"-450px"
			});
		});

		evenLine();
		function evenLine(){
			$("#teacherManage tr:even td").css("background-color","#eee");
		}
		function oddLine(){
			$("#teacherManage tr:odd td").css("background-color","#fff");
		}

		$("#teacherManage .table").on({"click": function(){
			var trIndex = $(this).parents("tr").index();
			var trLength = $("#teacherManage .table .list").length - 1;
			$(this).parents("tr").remove();
			for(var i=trIndex;i<=trLength;i++){
				$("#teacherManage .table .list").eq(i-1).find(".teacherNum span").html('教师'+i);
				$("#teacherManage .table .list").eq(i-1).find(".teacherNum input").attr("name",'addTeacherv'+i);
			}
			evenLine();
			oddLine();
			$('#teacherManage').jScrollPane({
				mouseWheelSpeed:100
			});
		}}, '.del');
		function manageClear(){
			$("#teacherManage .tearcherSreach ").val("");
			$("#teacherManage input[name=addteacher]").val("");
		}
		$("#teacherManage .addBox").on({"click": function(){
			var trLength = $("#teacherManage .table .list").length + 1,
				manageAddDate = $("#teacherManage .tearcherSreach ").val(),
				manageAddV = $("#teacherManage input[name=addteacher]").val(),
				error = $("#teacherManage .errorFF"),
				manageV = true,
				manageArry = new Array(),
				teacherManageL = $("#teacherManage .table .list").length;
			if(trLength>10){
				console.log("对不起，最多只能添加10个老师");
				manageClear();
				return;
			}
			if(manageAddV == ""||manageAddV=="-1"){
				error.height(30).html("*教师选择错误或不存在！");
				manageClear();
				return;
			}
			for(var j=0;j<teacherManageL;j++){
				manageArry[j] = $("#teacherManage .table .list").eq(j).find("input").val();
				if(manageAddV == manageArry[j]){
					manageV = false;
				}
			}
			if(manageV==false){
				error.height(30).html("*教师重复，请重新选择");
				manageClear();
				return;
			}else{
				error.height(0).html("");
			}
			html =	'<tr class="list">'+
					'<td class="teacherNum"><span>教师'+ trLength +'</span><input type="hidden" name="addTeacherv'+trLength+'" value="'+ manageAddV +'"></td>'+
					'<td class="teacherName">'+ manageAddDate +'</td>'+
					'<td><span class="del">删除</span></td>'+
					'</tr>';
			$("#teacherManage table").append(html);
			evenLine();
			oddLine();
			manageClear();
			$('#teacherManage').jScrollPane({
				mouseWheelSpeed:100
			});
		}}, '.add');

		function initManageTeachers(class_id){
			$.ajax({
					type: "GET",
					url:"/lps3/ea/classes/get_class_teachers/",
					data:{"s":class_id},
					beforeSend:function(XMLHttpRequest){
					},
					success: function(data) {
						if (data.status){
							var data1=data.message;
							for(var i=0;i<data1.length;i++){
								html =	'<tr class="list">'+
										'<td class="teacherNum"><span>教师'+ (i+1) +'</span><input type="hidden" name="addTeacherv'+(i+1)+'" value="'+ data1[i][0] +'"></td>'+
										'<td class="teacherName">'+ data1[i][1] +'</td>'+
										'<td><span class="del">删除</span></td>'+
										'</tr>';
								$("#teacherManage table").append(html);
							}
							evenLine();
							oddLine();
						}
					},
					complete: function(XMLHttpRequest){
					}
					});
		};
		$(".deanframemanagebtn").click(function(){
			var $th= $(this);
			$.ajax({
				type: "POST",
				url:"/lps3/ea/classes/update_class_teachers/"+class_id+"/",
				data:$("#manageForm").serialize(),
				beforeSend:function(XMLHttpRequest){
					$th.attr("disabled","disabled");
				},
				success: function(data) {
					if (data.status){
						location.reload();
					}else{
						$th.next().height(30).html(data.message);
					}
				},
				complete: function(XMLHttpRequest){
					$th.removeAttr("disabled");
				}
				});
		});
	}
	//-------------FUNTIONEND-----------------	
	module.exports = {
		"init":classM
	};
})