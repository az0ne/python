define(function(require, exports, module) {
	var th, option, nowtimes, nowtimeselect, is_click_experedit = false, is_click_educedit = false,experliId,educliId;
	nowtimes = new Date();
	nowtimeselect = nowtimes.getFullYear() + '-' + (nowtimes.getMonth() + 1) + '-' + nowtimes.getDate();
	//-------------FUNTION-----------------.
	function personalCenterSjob(t,op){
		th=t;option=op;init();
	}
	//------------FUNCTIONEND---------	
	//初始化
	var init=function(){
		/*
		 * @个人信息
		 */
		$(".resume .tabTit li").on('click',function(){
			$(this).addClass('cur').siblings().removeClass('cur');
			$('.resume .tabBox>div').eq($(this).index()).addClass('cur').siblings().removeClass('cur');
		});
		$(".resume .radio-inline").on('click',function(){
			$(this).addClass('active').siblings().removeClass('active');
		});
		//个人信息的出生日期及开始工作时间下拉列表
		personalInfoSelect();

		//判断个人信息姓名是否为空且弹出提示
		var name = $(".resume .info .username");
		var work_date = $('.resume .info #workDate');
		name.on('keyup',function(){
			if(name.val().length > 0){
				name.removeClass('err');
				name.siblings('.error').text('');
			}else{
				name.addClass('err');
				name.siblings('.error').text('请输入您的姓名');
			}
		});
		work_date.change(function(){
			$(this).siblings('.error').text('');
		});
		//个人信息表单提交
		$('.resume .info .submitBtn input').on('click',function(){
			var tips = $('.resume .info .tips');
			if(name.val().length == 0){
				name.siblings('.error').text('请输入您的姓名');
				return;
			}else if(work_date.val() == '0'){
				work_date.siblings('.error').text('请选择开始工作时间');
				return;
			}
			$.ajax({
				type: "POST",
				url:"/home/s/ajax_save_resume_user_info/",
				data:$("#resumeForm").serialize(),
				dataType: "json",
				success: function(data1) {
					if(data1.success){
						tips.removeClass('err').addClass('succ').text('保存成功').fadeIn(200);
						setTimeout(function(){
							tips.removeClass('succ').text('').fadeOut(200);
						},5000);
						$('.personalTab').find('em').remove();
					}else{
						tips.removeClass('succ').addClass('err').text('保存失败').fadeIn(200);
						setTimeout(function(){
							tips.removeClass('err').text('').fadeOut(200);
						},5000);
					}
				}
			});
		});

		/*
		 * @工作经历
		 */
		var experAddForm = '<div class="create">'+
							'	<form id="workExperForm">'+
							'		<input type="hidden" id="workLastInsert" value="">'+
							'		<div class="form-group">'+
							'			<label for="company" class="control-label">公司名称：</label>'+
							'			<div class="form-right"><input type="text" name="company" id="company" class="form-control"/><em class="error"></em></div>'+
							'		</div>'+
							'		<div class="form-group">'+
							'			<label for="worlPast" class="control-label">工作岗位：</label>'+
							'			<div class="form-right"><input type="text" name="worlPast" id="worlPast" class="form-control"/><em class="error"></em></div>'+
							'		</div>'+
							'		<div class="form-group">'+
							'			<label class="control-label">任职时间：</label>'+
							'			<div class="form-right selectTime">'+
							'				<span class="starttime"><select class="form-control" id="experStartTimeYear"></select><select class="form-control" id="experStartTimeMonth"></select><select class="hiddenSelect" id="experStartTimeDay"></select></span> —— <span class="endtime"><select class="form-control" id="experEndTimeYear"></select><select class="form-control" id="experEndTimeMonth"></select><select class="hiddenSelect" id="experEndTimeDay"></select></span>'+
							'				<span class="nowtime">至今</span>'+
							'				<input type="hidden" name="experStartTime" value="" id="experStartTime"/>'+
							'				<input type="hidden" name="experEndTime" value="" id="experEndTime"/>'+
							'				<em class="error"></em>'+
							'			</div>'+
							'		</div>'+
							'		<div class="form-group jobDesc">'+
							'			<label for="jobDesc" class="control-label">工作描述：</label>'+
							'			<textarea class="form-control" id="jobDesc" name="jobDesc" placeholder="请输入工作描述"></textarea>'+
							'			<em class="error"></em>'+
							'		</div>'+
							'		<div class="btns">'+
							'			<span class="keep">保存</span>'+
							'			<span class="cancel">取消</span>'+
							'		</div>'+
							'	</form>'+
							'</div>';

		var experlist = $('.resume .exper');
		//删除
		experlist.on({'click':function(){
			var th = $(this).parent().parent().parent();
			$.ajax({
				type: "POST",
				url:"/home/s/ajax_del_resume_work/",
				data:{last_insert_id: th.attr('id')},
				dataType: "json",
				success: function(data1) {
					if(data1.success){
						if (!th.siblings().length) {
							$('.workTab').append('<em>[未完善]</em>');
						}
						th.remove();
					}else{
						console.log(data1.message)
					}
				}
			});
		}},'.del');
		/*
		 * @点击“编辑”
		 * is_click_experedit是否点击工作经历下的编辑
		 */
		experlist.on({'click':function(){
			var th, exper,exper_company,exper_work_title,exper_start_time,exper_work_content,exper_end_time;
			exper = $('.resume .exper');
			th = $(this).parent().parent().parent();
			exper_company = th.find('.exper_company').text();
			exper_work_title = th.find('.exper_work_title').text();
			exper_start_time = th.find('.exper_start_time').text()+'-01';
			exper_work_content = th.find('.exper_work_content').text();
			if(th.find('.exper_end_time').text() == '至今'){
				exper_end_time = th.find('.exper_end_time').text();
			}else{
				exper_end_time = th.find('.exper_end_time').text()+'-01';
			}

			if(_exper_create_block == true){
				exper.children('.create').remove();
			}
			experliId = th.attr('id');
			th.children().fadeOut(1);
			th.children('.boxTop').before(experAddForm);
			exper.find('#company').val(exper_company);
			exper.find('#worlPast').val(exper_work_title);
			exper.find('#experStartTime').val(exper_start_time);
			exper.find('#jobDesc').val(exper_work_content);
			exper.find('#experEndTime').val(exper_end_time);
			$('#workLastInsert').val(th.attr('id'));

			option.experEndTime = exper.find('#experEndTime').val();
			option.experStartTime = exper.find('#experStartTime').val();

			experSelect();
			exper_worktime_endval();

			exper.find('.add').fadeOut(200);
			_exper_create_block = true;

			is_click_experedit = true;
		}},'.edit');

		//判断公司名称、工作岗位、工作描述所填值是否合法并弹出提示
		exper_val_legal();
		//工作经历工作时间结束值切换当前时间并获取值
		exper_worktime_endvalnowtime();

		var _exper_create_block = false;
		//点击创建工作经历的“保存”
		$('.resume .exper').on({'click':function(){
			var company,wordpast,jobDesc,startTimeVal,endTimeVal,selectTime,timeDiffer;
				company = $('.resume #company');
				wordpast = $('.resume #worlPast');
				jobDesc = $('.resume #jobDesc');
				selectTime = $('.resume #experEndTime');
				startTimeVal = $('#experStartTime').val();
				endTimeVal = $('#experEndTime').val();
			if(endTimeVal == '至今'){
				endTimeVal = nowtimes.getFullYear() + '-'+ (nowtimes.getMonth() + 1);
			};
			timeDiffer = Date.parse(new Date(endTimeVal))-Date.parse(new Date(startTimeVal));
			if(company.val().length == 0){
				company.siblings('.error').text('请输入公司名称');
				return;
			}else if(company.val().length > 50){
				company.siblings('.error').text('字数不能超过50个');
				return;
			}else if(wordpast.val().length == 0){
				wordpast.siblings('.error').text('请输入工作岗位');
				return;
			}else if(timeDiffer <= 0){
				selectTime.siblings('.error').text("任职时间格式不对，截止时间不能小于等于开始时间");
				return;
			}else if(jobDesc.val().length == 0){
				jobDesc.siblings('.error').text('请输入工作描述');
				return;
			}else if(jobDesc.val().length > 500){
				jobDesc.siblings('.error').text('字数不能超过500个');
				return;
			}
			$.ajax({
				type: "POST",
				url:"/home/s/ajax_save_resume_work/",
				data:$("#workExperForm").serialize() + '&resume_work_id=' + $('#workLastInsert').attr('value'),
				dataType: "json",
				success: function(data1) {
					if(data1.success){
						save_work_success(data1.data['last_insert_id']);
						$('.workTab').find('em').remove();
					}else{
						console.log(data1.message)
					}
				}
			});
		}},'.keep');

		//点击创建工作经历的“取消”
		$('.resume .exper').on({'click':function(){
			_exper_create_block = false;
			$(this).parent().siblings().find('.error').text('');
			$('.resume .exper .create').remove();
			$('.resume .exper #'+experliId).children('.create').remove();
			$('.resume .exper #'+experliId).children().fadeIn(300);
			$('.resume .exper .add').fadeIn(300);
		}},'.cancel');

		//点击添加工作经历
		$('.resume .exper .add').on('click',function(){
			$('.resume .exper .add').before(experAddForm);
			//清除id
			$('#workLastInsert').val('');
			//清除工作经历所填值
			clearExperVal();
			//工作经历任职时间的下拉列表
			experSelect();
			//判断任职时间结束值是否为“至今”并做处理
			exper_worktime_endval();
			if(_exper_create_block == false){
				_exper_create_block = true;
				$(this).fadeOut();
			};
			if(is_click_experedit == true) is_click_experedit = false;
		});


		/*
		 * 教育背景
		 */
		var educAddForm = '<div class="create">'+
							'<form id="eudcForm">'+
							'	<input type="hidden" id="eduLastInsert">'+
							'	<div class="form-group">'+
							'		<label for="school" class="control-label">学校名称：</label>'+
							'		<div class="form-right"><input type="text" name="school" id="school" class="form-control"/><em class="error"></em></div>'+
							'	</div>'+
							'	<div class="form-group">'+
							'		<label for="major" class="control-label">专业名称：</label>'+
							'		<div class="form-right"><input type="text" name="major" id="major" class="form-control"/><em class="error"></em></div>'+
							'	</div>'+
							'	<div class="form-group">'+
							'		<label class="control-label">就读时间：</label>'+
							'		<div class="form-right selectTime">'+
							'			<span class="starttime"><select class="form-control" id="educStartTimeYear"></select><select class="form-control" id="educStartTimeMonth"></select><select class="hiddenSelect" id="educStartTimeDay"></select></span> —— <span class="endtime"><select class="form-control" id="educEndTimeYear"></select><select class="form-control" id="educEndTimeMonth"></select><select class="hiddenSelect" id="educEndTimeDay"></select></span>'+
							'			<span class="nowtime">至今</span>'+
							'			<input type="hidden" name="educStartTime" value="" id="educStartTime"/>'+
							'			<input type="hidden" name="educEndTime" value="" id="educEndTime"/>'+
							'			<em class="error"></em>'+
							'		</div>'+
							'	</div>'+
							'	<div class="form-group">'+
							'		<label for="education" class="control-label">学历：</label>'+
							'		<div class="form-right"><select class="form-control" name="education" id="education">'+
							'			<option value="硕士">硕士</option>'+
							'			<option value="本科">本科</option>'+
							'			<option value="大专">大专</option>'+
							'			<option value="高中及以下">高中及以下</option>'+
							'		</select></div>'+
							'	</div>'+
							'	<div class="btns">'+
							'		<span class="keep">保存</span>'+
							'		<span class="cancel">取消</span>'+
							'	</div>'+
							'</form>'+
						'</div>';

		var educlist = $('.resume .educ');
		//删除
		educlist.on({'click':function(){
			var th = $(this).parent().parent().parent();
			$.ajax({
				type: "POST",
				url:"/home/s/ajax_del_resume_edu/",
				data:{last_insert_id: th.attr('id')},
				dataType: "json",
				success: function(data1) {
					if(data1.success){
						if (!th.siblings().length) {
							$('.eduTab').append('<em>[未完善]</em>');
						}
						th.remove();
					}else{
						console.log(data1.message)
					}
				}
			});
		}},'.del');
		/*
		 * @点击“编辑”
		 * is_click_educedit是否点击教育背景下的编辑
		 */
		educlist.on({'click':function(){
			var th, educ, educ_school, educ_major, educ_start_time, educ_title, educ_end_time;
			educ = $('.resume .educ');
			th = $(this).parent().parent().parent();
			educ_school = th.find('.educ_school').text();
			educ_major = th.find('.educ_major').text();
			educ_start_time = th.find('.educ_start_time').text()+'-01';
			educ_title = th.find('.educ_title').text();
			if(th.find('.educ_end_time').text() == '至今'){
				educ_end_time = th.find('.educ_end_time').text();
			}else{
				educ_end_time = th.find('.educ_end_time').text()+'-01';
			}

			if(_educ_create_block == true){
				educ.children('.create').remove();
			}
			educliId = th.attr('id');
			th.children().fadeOut(1);
			th.children('.boxTop').before(educAddForm);
			educ.find('#school').val(educ_school);
			educ.find('#major').val(educ_major);
			educ.find('#educStartTime').val(educ_start_time);
			educ.find('#education').val(educ_title);
			educ.find('#educEndTime').val(educ_end_time);
			$('#eduLastInsert').val(th.attr('id'));

			option.educStartTime = educ.find('#educStartTime').val();
			option.educEndTime = educ.find('#educEndTime').val();
			educSelect();
			educ_readtime_endval();

			educ.find('.add').fadeOut(200);
			_educ_create_block = true;
			is_click_educedit = true;
		}},'.edit');

		//判断学校名称、专业名称所填值是否合法并弹出提示
		educ_val_legal();
		//教育背景就读时间结束值切换当前时间并获取值
		educ_readtime_endvalnowtime();

		var _educ_create_block = false;
		//点击创建教育背景的“保存”
		$('.resume .educ').on({'click':function(){
			var school,major,selectTime,startTimeVal,endTimeVal,timeDiffer;
				school = $('.resume #school');
				major = $('.resume #major');
				selectTime = $('.resume #educEndTime');
				startTimeVal = $('#educStartTime').val();
				endTimeVal = $('#educEndTime').val();
			if(endTimeVal == '至今'){
				endTimeVal = nowtimes.getFullYear() + '-'+ (nowtimes.getMonth() + 1);
			};
			timeDiffer = Date.parse(new Date(endTimeVal))-Date.parse(new Date(startTimeVal));
			if(school.val().length == 0){
				school.siblings('.error').text('请输入学校名称');
				return;
			}else if(major.val().length == 0){
				major.siblings('.error').text('请输入专业名称');
				return;
			}else if(timeDiffer <= 0){
				selectTime.siblings('.error').text("任职时间格式不对，截止时间不能小于等于开始时间");
				return;
			}
			$.ajax({
				type: "POST",
				url:"/home/s/ajax_save_resume_edu/",
				data:$("#eudcForm").serialize() + '&resume_edu_id=' + $('#eduLastInsert').attr('value'),
				dataType: "json",
				success: function(data1) {
					if(data1.success){
						save_educ_success(data1.data['last_insert_id']);
						$('.eduTab').find('em').remove();
					}else{
						console.log(data1.message)
					}
				}
			});
		}},'.keep');

		//点击创建教育背景的“取消”
		$('.resume .educ').on({'click':function(){
			_educ_create_block = false;
			$(this).parent().siblings().find('.error').text('');
			$('.resume .educ .create').remove();
			$('.resume .educ #'+educliId).children('.create').remove();
			$('.resume .educ #'+educliId).children().fadeIn(300);
			$('.resume .educ .add').fadeIn(300);
		}},'.cancel');

		//点击添加教育背景
		$('.resume .educ .add').on('click',function(){
			$('.resume .educ .add').before(educAddForm);
			//清除id
			$('#eduLastInsert').val( '');
			//清除工作经历所填值
			cleareducVal();
			//教育背景就读时间的下拉列表
			educSelect();
			//判断就读时间结束值是否为“至今”并做处理
			educ_readtime_endval();
			if(_educ_create_block == false){
				_educ_create_block = true;
				$(this).fadeOut();
			};
			if(is_click_educedit == true) is_click_educedit = false;
		});

	}

	/*
	 * @个人信息
	 * @个人信息下拉列表
	 * birthtime出生日期
	 * worktime开始工作时间
	 */
	function personalInfoSelect(){
		//出生日期
		var myTimer=option.birthtime||"1970-01-01";
		new GySetDate({"targets":'#year1,#month2,#day3',"range":"1970-01-01,"+nowtimeselect,"value":myTimer});
		getTime();
		function getTime(){
			$(".resume .births").val($("#year1").val()+"-"+$("#month2").val()+"-"+$("#day3").val());
		}
		$(".resume .birSelect select").change(getTime);

		//工作时间
		var nowYear = nowtimes.getFullYear();
		var str = "";
		var workDate = $(".resume .info #workDate");
		for(var i=0;i<=30;i++){
			if((nowYear - i) == option.worktime){
				str = "<option value=" + (nowYear - i) + " selected=true>" + (nowYear - i) + "年</option>";
			}else{
				str = "<option value=" + (nowYear - i) + ">" + (nowYear - i) + "年</option>";
			}
			workDate.append(str);
		}
		str = "<option value=" + "0" + ">请选择</option>";
		workDate.append(str);
		if (option.worktime == 0){
			workDate.val("0")
		}
	}

	/*
	 * @工作经历
	 * @工作经历下拉列表
	 * experStartTime开始时间
	 * experEndTime结束时间
	 */
	function experSelect(){
		//任职时间
		var myexperStartTimer=option.experStartTime||"1990-01-01";
		new GySetDate({"targets":'#experStartTimeYear,#experStartTimeMonth,#experStartTimeDay',"range":"1990-01-01,"+nowtimeselect,"value":myexperStartTimer});
		var myexperEndTimer=option.experEndTime||"1990-01-03";
		new GySetDate({"targets":'#experEndTimeYear,#experEndTimeMonth,#experEndTimeDay',"range":"1990-01-01,"+nowtimeselect,"value":myexperEndTimer});
		getexperStartTime();
		getexperEndTime();
		function getexperStartTime(){
			$(".resume #experStartTime").val($("#experStartTimeYear").val()+"-"+$("#experStartTimeMonth").val());
		}
		function getexperEndTime(){
			$(this).parent().siblings('.error').text('');
			$(".resume #experEndTime").val($("#experEndTimeYear").val()+"-"+$("#experEndTimeMonth").val());
		}
		$(".resume .exper .starttime select").change(getexperStartTime);
		$(".resume .exper .endtime select").change(getexperEndTime);
	}

	/*
	 * @教育背景
	 * @教育背景下拉列表
	 * educStartTime开始时间
	 * educEndTime结束时间
	 */
	function educSelect(){
		var myeducStartTimer=option.educStartTime||"1990-01-01";
		new GySetDate({"targets":'#educStartTimeYear,#educStartTimeMonth,#educStartTimeDay',"range":"1990-01-01,"+nowtimeselect,"value":myeducStartTimer});
		var myeducEndTimer=option.educEndTime||"1990-01-03";
		new GySetDate({"targets":'#educEndTimeYear,#educEndTimeMonth,#educEndTimeDay',"range":"1990-01-01,"+nowtimeselect,"value":myeducEndTimer});
		geteducStartTime();
		geteducEndTime();
		function geteducStartTime(){
			$(".resume #educStartTime").val($("#educStartTimeYear").val()+"-"+$("#educStartTimeMonth").val());
		}
		function geteducEndTime(){
			$(this).parent().siblings('.error').text('');
			$(".resume #educEndTime").val($("#educEndTimeYear").val()+"-"+$("#educEndTimeMonth").val());
		}
		$(".resume .educ .starttime select").change(geteducStartTime);
		$(".resume .educ .endtime select").change(geteducEndTime);
	}

	/*
	 * @工作经历
	 * @保存工作经历成功
	 */
	function save_work_success(last_insert_id){
		var experBox,experBoxList,company,worlpast,start_time,end_time,jobdesc,str;
			experBox = $('.resume .exper');
		    experBoxList = $('.resume .exper .experList');
			company = experBox.find('#company').val();
			worlpast = experBox.find('#worlPast').val();
			start_time = experBox.find('#experStartTime').val();
			end_time = experBox.find('#experEndTime').val();
			jobdesc = experBox.find('#jobDesc').val();
		str = "";
		str +='<li id="' + last_insert_id + '">';
		str +='<div class="boxTop">';
		str +='	<span class="title"><span class="exper_start_time">'+ start_time +'</span>—<span class="exper_end_time">'+ end_time +'</span> | <span class="exper_company">'+ company +'</span></span>';
		str +='<span class="handle"><em class="del">删除</em><em class="edit">编辑</em></span>';
		str +='</div>';
		str +='<div class="boxCon">';
		str +='<p><strong>工作岗位：</strong><span class="exper_work_title">'+ worlpast +'</span></p>';
		str +='<p><strong>工作描述：</strong><span class="exper_work_content">'+ jobdesc +'</span></p>';
		str +='</div>';
		str +='</li>';
		if(is_click_experedit){
			experBoxList.find('#' + last_insert_id).replaceWith(str);
		} else {
			experBoxList.append(str);
		}

		_exper_create_block = false;
		$('.resume .exper .create').remove();
		$('.resume .exper #'+experliId).children('.create').remove();
		$('.resume .exper #'+experliId).children().fadeIn(300);
		$('.resume .exper .add').fadeIn(300);
	};

	/*
	 * @教育背景
	 * @保存教育背景成功
	 */
	function save_educ_success(last_insert_id){
		var educBox,educBoxList,school,major,start_time,end_time,education,str;
			educBox = $('.resume .educ');
		    educBoxList = $('.resume .educ .experList');
			school = educBox.find('#school').val();
			major = educBox.find('#major').val();
			start_time = educBox.find('#educStartTime').val();
			end_time = educBox.find('#educEndTime').val();
			education = educBox.find('#education').val();
		str = "";
		str +='<li id="' + last_insert_id + '">';
		str +='<div class="boxTop">';
		str +='	<span class="title"><span class="educ_start_time">'+ start_time +'</span> — <span class="educ_end_time">'+ end_time +'</span> | <span class="educ_school">'+ school +'</span></span>';
		str +='<span class="handle"><em class="del">删除</em><em class="edit">编辑</em></span>';
		str +='</div>';
		str +='<div class="boxCon">';
		str +='<span><em>专业名称：</em><span class="educ_major">'+ major +'</span></span>';
		str +='<span><em>学历：</em><span class="educ_title">'+ education +'</span></span>';
		str +='</div>';
		str +='</li>';
		if(is_click_educedit){
			educBoxList.find('#' + last_insert_id).replaceWith(str);
		} else {
			educBoxList.append(str);
		}

		_educ_create_block = false;
		$('.resume .educ .create').remove();
		$('.resume .educ #'+educliId).children('.create').remove();
		$('.resume .educ #'+educliId).children().fadeIn(300);
		$('.resume .educ .add').fadeIn(300);
	};

	/*
	 * @工作经历
	 * @清除工作经历所填值
	 */
	function clearExperVal(){
		var experBox = $('.resume .exper');
		experBox.find('#company').val('');
		experBox.find('#worlPast').val('');
		experBox.find('#experStartTime').val('');
		experBox.find('#experEndTime').val('');
		experBox.find('#jobDesc').val('');
	};

	/*
	 * @教育背景
	 * @清除教育背景所填值
	 */
	function cleareducVal(){
		var educBox = $('.resume .educ');
		educBox.find('#school').val('');
		educBox.find('#major').val('');
		educBox.find('#educStartTime').val('');
		educBox.find('#educEndTime').val('');
	};

	/*
	 * @工作经历
	 * @判断公司名称、工作岗位、工作描述所填值是否合法并弹出提示
	 */
	function exper_val_legal(){
		//输入公司名称不超过50字提示
		$('.resume').on({'keyup':function(){
			var companyVal = $(this).val();
			if(companyVal.length > 50){
				$(this).siblings('.error').text('字数不超过50个');
			}else if(companyVal.length == 0){
				$(this).siblings('.error').text('请输入公司名称');
			}else{
				$(this).siblings('.error').text('');
			}
		}},'#company');
		//判断工作岗位是否输入值
		$('.resume').on({'keyup':function(){
			if($(this).val().length > 50){
				$(this).siblings('.error').text('字数不超过50个');
			}else if($(this).val().length == 0){
				$(this).siblings('.error').text('请输入工作岗位');
			}else{
				$(this).siblings('.error').text('');
			}
		}},'#worlPast');
		//输入工作描述不超过500字提示
		$('.resume').on({'keyup':function(){
			var companyVal = $(this).val();
			if(companyVal.length>500){
				$(this).siblings('.error').text('字数不超过500个');
			}else if(companyVal.length == 0){
				$(this).siblings('.error').text('请输入工作描述');
			}else{
				$(this).siblings('.error').text('');
			}
		}},'#jobDesc');
	}

	/*
	 * @教育背景
	 * @判断校名称、专业名称所填值是否合法并弹出提示
	 */
	function educ_val_legal(){
		//判断学校名称是否输入值
		$('.resume').on({'keyup':function(){
			if($(this).val().length > 50){
				$(this).siblings('.error').text('字数不超过50个');
			}else if($(this).val().length == 0){
				$(this).siblings('.error').text('请输入学校名称');
			}else{
				$(this).siblings('.error').text('');
			}
		}},'#school');
		//判断专业名称是否输入值
		$('.resume').on({'keyup':function(){
			if($(this).val().length > 50){
				$(this).siblings('.error').text('字数不超过50个');
			}else if($(this).val().length == 0){
				$(this).siblings('.error').text('请输入专业名称');
			}else{
				$(this).siblings('.error').text('');
			}
		}},'#major');
	}

	/*
	 * @工作经历
	 * @判断任职时间结束值是否为“至今”并做处理
	 */
	function exper_worktime_endval(){
		//判断后台值是否为“至今”
		var oExpernowtime = $(".resume .exper .nowtime");
		if(option.experEndTime == '至今'){
			oExpernowtime.addClass('active');
			$(".resume .exper .endtime select").attr('disabled','disabled').css('background',"#f4f3f3");
			$(".resume #experEndTime").val('至今');
		}else{
			oExpernowtime.removeClass('active');
			$(".resume .exper .endtime select").removeAttr('disabled').css('background',"#fff");
		}
	}

	/*
	 * @教育背景
	 * @判断就读时间结束值是否为“至今”并做处理
	 */
	function educ_readtime_endval(){
		//判断后台值是否为“至今”
		var oEducnowtime = $(".resume .educ .nowtime");
		if(option.educEndTime == '至今'){
			oEducnowtime.addClass('active');
			$(".resume .educ .endtime select").attr('disabled','disabled').css('background',"#f4f3f3");
			$(".resume #educEndTime").val('至今');
		}else{
			oEducnowtime.removeClass('active');
			$(".resume .educ .endtime select").removeAttr('disabled').css('background',"#fff");
		}
	}

	/*
	 * @工作经历
	 * @点击任职时间结束值“至今”并切换获取值
	 */
	function exper_worktime_endvalnowtime(){
		//点击“至今”
		var oExper = $(".resume .exper");
		oExper.on({'click':function(){
			$(this).siblings('.error').text('');
			if($(this).hasClass('active')){
				$(this).removeClass('active');
				$(".resume .exper .endtime select").removeAttr('disabled').css('background',"#fff");
				$(".resume #experEndTime").val($('.resume #experEndTimeYear').val() + '-' + $('.resume #experEndTimeMonth').val());
			}else{
				$(this).addClass('active');
				$(".resume .exper .endtime select").attr('disabled','disabled').css('background',"#f4f3f3");
				$(".resume #experEndTime").val('至今');
			}
		}},'.nowtime');
	}

	/*
	 * @教育背景
	 * @点击就读时间结束值“至今”并切换获取值
	 */
	function educ_readtime_endvalnowtime(){
		//点击“至今”
		var oEduc = $(".resume .educ");
		oEduc.on({'click':function(){
			$(this).siblings('.error').text('');
			if($(this).hasClass('active')){
				$(this).removeClass('active');
				$(".resume .educ .endtime select").removeAttr('disabled').css('background',"#fff");
				$(".resume #educEndTime").val($('.resume #educEndTimeYear').val() + '-' + $('.resume #educEndTimeMonth').val());
			}else{
				$(this).addClass('active');
				$(".resume .educ .endtime select").attr('disabled','disabled').css('background',"#f4f3f3");
				$(".resume #educEndTime").val('至今');
			}
		}},'.nowtime');
	}

	module.exports = {
		"init":personalCenterSjob
	};
	
})