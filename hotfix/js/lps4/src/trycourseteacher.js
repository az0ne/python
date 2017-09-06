define(function (require, exports, module) {
    var $ = require('jquery');
    require('bootstrap');
	require('/static/mz_lps3/js/jquery.datetimepicker');

	openTime();//日期/时间插件
	/*
	 * 点击“新增试学班”
	 */
	$(".tryTeacher .addBtn").click(function(){
		$("#tryTeacherNewClassModal").modal('show');
		$(".tryTeacherNewClassResult").hide();
		$(".tryTeacherNewClassAdd").show();
	});
	/*
	 * 点击“创建”
	 */
	$('.tryTeacherNewClassAdd .create').click(function(){
		var selectVal,tryTeacherNewClassProfess,tryTeacherFirstDate,tryTeacherFirstTime,tryTeacherAnswerTime;
		tryTeacherNewClassProfess = $('#tryTeacherNewClassProfess');//专业选择框
		selectVal = tryTeacherNewClassProfess.find('option:selected').val();//当前选中专业的VALUE值
		tryTeacherFirstDate = $("#tryTeacherFirstDate");//首次班会日期
		tryTeacherFirstTime = $("#tryTeacherFirstTime");//首次班会时间
		tryTeacherAnswerTime = $("#tryTeacherAnswerTime");//答疑班会时间
		console.log(tryTeacherFirstDate.val());
		////所有内容不为空时，切换到结果框
		//if(selectVal > 0 && !tryTeacherFirstDate.val() == "" && !tryTeacherFirstTime.val() == "" && !tryTeacherAnswerTime.val() == ""){
		//	$(this).parent().hide();
		//	$(".tryTeacherNewClassResult").fadeIn(150);
		//}
		//select框未填写内容时，边框变为红色提示
		if(selectVal == 0){
			tryTeacherNewClassProfess.addClass("error");
		};

		//input框未填写内容时，边框变为红色提示
		function nullVal(values,myId){
			if(values == ""){
				myId.addClass("error");
			};
		};
		nullVal(tryTeacherFirstDate.val(),tryTeacherFirstDate);
		nullVal(tryTeacherFirstTime.val(),tryTeacherFirstTime);
		nullVal(tryTeacherAnswerTime.val(),tryTeacherAnswerTime);

		//获取当前选中专业的专业名称，并显示在确认框中
		$(".tryTeacherNewClassResult .title span").html(tryTeacherNewClassProfess.find('option:selected').text());

		//创建试学班结果框“首次班会”及“答疑班会”最终显示结果
		$(".tryTeacherNewClassResult .first em").html($("#tryTeacherFirstTime").val());
		$(".tryTeacherNewClassResult .answer em").html($("#tryTeacherAnswerTime").val());

		$.ajax({
			type: 'POST',
			url: $(this).attr('hrf'),
			data: $('#createFreeClassForms').serialize(),
			dataType: 'json',
			success:function(data){
				if (data['status']){
					$(".tryTeacherNewClassAdd").hide();
					$(".tryTeacherNewClassResult").fadeIn(150);
					$(".tryTeacherNewClassAdd .tips").hide();
				}else{
					$(".tryTeacherNewClassAdd .tips").show();
				}
			}
		});
	});

	//答疑班会的默认时间是当前日期加3天
	var defaultDate = new Date();
		defaultDate.setDate(defaultDate.getDate()+2);
	var defaulty = defaultDate.getFullYear();
	var defaultm = (defaultDate.getMonth()+1)<10?"0"+(defaultDate.getMonth()+1):(defaultDate.getMonth()+1);//获取当前月份的日期，不足10补0
	var defaultd = defaultDate.getDate()<10?"0"+defaultDate.getDate():defaultDate.getDate(); //获取当前几号，不足10补0
	$("#tryTeacherAnswerDate").html(defaulty+"."+defaultm+"."+defaultd);//显示的时间
	$("#tryTeacherAnswerDateHidden").val(defaulty+"/"+defaultm+"/"+defaultd);//input隐藏域的时间

	//获得焦点时，边框颜色变回默认颜色
	$(".tryTeacherNewClassAdd select,.tryTeacherNewClassAdd input").focus(function(){
		$(this).removeClass("error");
	});


	/*
	 * 当“首次班会”日期的input框失去焦点时，获取选择的日期及3天后的时间
	 * 将3天后的日期赋给“答疑班会”日期
	 * 将当前选择的日期赋给“首次班会”日期
	 * 其中“答疑班会”显示的日期与隐藏域的日期一致，方便传输数据到后台
	 */
	$("#tryTeacherFirstDate").blur(function(){
		if(!$(this).val() == ""){
			var answerDate = new Date($(this).val());
				answerDate.setDate(answerDate.getDate()+2);
			var answery = answerDate.getFullYear();
			var answerm = (answerDate.getMonth()+1)<10?"0"+(answerDate.getMonth()+1):(answerDate.getMonth()+1);//获取当前月份的日期，不足10补0
			var answerd = answerDate.getDate()<10?"0"+answerDate.getDate():answerDate.getDate(); //获取当前几号，不足10补0
			var answerweekday = new Array('星期日','星期一','星期二','星期三','星期四','星期五','星期六');
			var  answerTime = answery + "/" + answerm + "/" + answerd;
			$("#tryTeacherAnswerDate").html(answerTime);//“答疑班会”显示的日期
			$("#tryTeacherAnswerDateHidden").val(answerTime);//“答疑班会”隐藏域的日期
		}

		var firstDate = new Date($(this).val());
		var firsty = firstDate.getFullYear();
		var firstm = (firstDate.getMonth()+1)<10?"0"+(firstDate.getMonth()+1):(firstDate.getMonth()+1);//获取当前月份的日期，不足10补0
		var firstd = firstDate.getDate()<10?"0"+firstDate.getDate():firstDate.getDate(); //获取当前几号，不足10补0
		var firstweekday = new Array('星期日','星期一','星期二','星期三','星期四','星期五','星期六');
		$(".tryTeacherNewClassResult .first strong").html(firstweekday[firstDate.getDay()] + "（"+ firstm + "." + firstd +"）<em></em>");//确认框--首次班会日期
		$(".tryTeacherNewClassResult .answer strong").html(answerweekday[answerDate.getDay()] + "（"+ answerm + "." + answerd +"）<em></em>");//确认框--答疑班会日期

		$(".tryTeacherNewClassResult .title strong").html("("+ firstm + "." + firstd + "-" + answerm + "." + answerd +")" + " 3天");//确认框--标题显示日期区间
	});


	///*
	// * 点击“返回修改”
	// */
	//$('.tryTeacherNewClassResult .back').click(function(){
	//	$(this).parent().hide();
	//	$(".tryTeacherNewClassAdd").fadeIn(150);
	//	$(".tryTeacherNewClassResult .first em").html();//移除确认框首次班会时间
	//	$(".tryTeacherNewClassResult .answer em").html();//移除确认框答疑班会时间
	//});
    /*
     * 点击“返回修改”
     */
    $('.tryTeacherNewClassResult .back').click(function () {
        $(this).parent().hide();
        $(".tryTeacherNewClassAdd").fadeIn(150);
    });
	//请重建
	$("#tryTeacherErrorBox .retry").click(function(){
		$("#tryTeacherErrorBox").modal('hide');
		$("#tryTeacherNewClassModal").modal('show');
		$(".tryTeacherNewClassResult").hide();
		$(".tryTeacherNewClassAdd").show();
	});
    //确认创建
    $('.tryTeacherNewClassResult .confirm').click(function () {
        $.ajax({
            type: 'POST',
            url: $('#createFreeClassForms').attr('action'),
            data: $('#createFreeClassForms').serialize(),
            dataType: 'json',
            success:function(data){
                if (data['status']){
                    location.reload();
                }else{
                    $("#tryTeacherNewClassModal").modal('hide');
                    $("#tryTeacherErrorBox").modal('show');
                }
            }
        });
    });

	//日期/时间插件
	function openTime(){
        //弹框时间
        $('.datetimepickerTime').datetimepicker({
            datepicker: false,
            format: 'H:i',
            step: 5,
            onChangeDateTime: function (currentDateTime, $input) {
                var dd2 = new Date();
                var day = $input.parent().parent().prev().find("input").val();
                if (day != "") {
                    currentDateTime = new Date(day + " " + currentDateTime.getHours() + ":" + currentDateTime.getMinutes() + ":" + currentDateTime.getSeconds());
                }
                var dd = Date.parse(currentDateTime);
                if (dd2 > dd) {
                    $input.val("");
                    layer.tips("不能选择过去的时间", $input, {tips: [2, '#68c8b6']});
                }
            }
        });
        $('.datetimepickerDate').datetimepicker({
            lang: 'ch',
            timepicker: false,
            format: 'Y/m/d',
            formatDate: 'Y/m/d',
            onChangeDateTime: function (currentDateTime, $input) {
                currentDateTime.setHours(23);
                currentDateTime.setMinutes(59);
                currentDateTime.setSeconds(59);
                var dd = Date.parse(currentDateTime);
                var dd2 = new Date();
                if (dd2 > dd) {
                    $input.val("");
                    layer.tips("不能选择过去的日期", $input, {tips: [2, '#68c8b6']});
                }
            }
        });
    }
});