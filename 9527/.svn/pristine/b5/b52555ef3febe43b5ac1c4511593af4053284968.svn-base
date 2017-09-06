$(document).ready(function() {
	//页面加载DOM后，调用getCourseList函数
	//绑定createCourse()函数到#btn_addCourse单击事件上
	//	$(document).unbind('click').on('click','#btn_addNewCourse',function(){
	//		createCourse();
	//	});
	//绑定updateCourse#btn_addCourse单击事件上
	//	$(document).unbind('click').on('click','#btn_editCourse', function updateCourse() {
	//		updateCourse();
	//	});
	$(document).off('click', '.btn_showCourse').on('click', '.btn_showCourse', function() {
		$('#madalTitle_course').text('查看专业方向信息');
		//		careerCatagoryId = getOneCareerCatagory($(this).parents().data('id'));
		$('#modal_course').modal('show');
		$('#txt_courseName').val($(this).parents().data('name')); //***临时数据***
		$('#txt_courseName').attr('disabled', true); //设置文本框不可编辑
		$('#btn_courseName').hide();
		$('#errorMessage').text($(this).parents().data('id'));
	});

});

jQuery.maizi_Course = {  //使用命名空间
	//获取课程信息列表
	getCourseList: function() {
		//	var pageSize=8;
		//	var currentPage=$('.pagination').val();
		$.getJSON('../../static/json/mz_course/course.json', function(data) {
			//	$.getJSON('/mz_cousre/getCourseList?pageSize="'+pagesize+'",currentPage="'+currentPage+'"',function(){
			var courseinfo = [];
			$.each(data.RECORDS, function(index, item) {
				courseinfo.push('<tr><td>' + item.name + '</td>');
				courseinfo.push('<td>' + item.image + '</td>');
				courseinfo.push('<td>' + item.description + '</td>');
				courseinfo.push('<td>' + item.date_publish + '</td>');
				courseinfo.push('<td>' + item.student_count + '</td>');
				courseinfo.push('<td data-id="' + item.id + '" data-name="' + item.name + '">' + '<a href="#" title="查看" class="btn btn-default btn-info btn-sm active btn_showCourse" style="margin-right:3px;"><i class="glyphicon glyphicon-search" style="margin-right: 3px;"></i>查看</a>' + '<a href="#" title="编辑" class="btn btn-default btn-success btn-sm  active btn_editCourse" style="margin-right:3px;"><i class="glyphicon glyphicon-edit" style="margin-right: 3px;"></i>编辑</a>' + '<a href="#" title="删除" class="btn btn-default btn-danger btn-sm active btn_delCourse" style="margin-right:3px;"><i class="glyphicon glyphicon-trash" style="margin-right: 3px;"></i>删除</a></td></tr>');
			});
			$('#courseTableRow').append(courseinfo.toString());
			//分页
			$(".pagination").jPages({
				containerID: "courseTableRow",
				perPage: 5,
				delay: 20
			});
		});
	},
	//创建新课程
	createCourse: function() {
		$.ajax({
			type: 'post',
			//		url: '/course/createCourse/',  //请求后台API接口
			url: '../../static/json/mz_course_course.json',
			data: {
				name: $('#name').val(),
				image: $('#image').val(),
				description: $('#description').val(),
				date_publish: $('#date_pulish').val(),
				student_count: $('#student_count').val()
			},
			dataType: 'json',
			success: function(data) {
				if (data.code < 0) {
					$('#errorMessage').html(data.message);
				} else {
					console.log('OK');
				}
			},
			error: function() {
				console.log('error.message');
			}
		});
	},

	//更新课件信息
	updateCourse: function() {
		//	$.post('/course/updateCourse/',{
		//				name:$('#name').val(),
		//				image:$('#image').val(),
		//				description:$('#description').val(),
		//				date_publish:$('#date_pulish').val(),
		//				student_count:$('#student_count').val()},function(data){
		//		
		//	});
	},
	//删除课件信息
	delectCareerCatagory: function(careerCatagory) {
		//	$.post('/course/delectCourse/', {
		//		id: careerCatagory.id
		//	}, function(data) {
		//		if (data.code == 0) {
		//			$('#modal_delCareerCatagory').modal('hide');
		//			getCourseCatagoryList(careerCatagory.currentPage);
		//		};
		//		else {
		//			$('errorMessage').text(data.error);
		//		};
		//	});
	},
};