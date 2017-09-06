//get users information
$(document).ready(function() {
	$.getJSON('students.json', function(data) {
		var studentinfo = [];
		$.each(data, function(index, item) {
			studentinfo.push('<tr><td>' + item.studentID + '</td>');
			studentinfo.push('<td>' + item.name + '</td>');
			studentinfo.push('<td>' + item.gender + '</td>');
			studentinfo.push('<td>' + item.age + '</td>');
			studentinfo.push('<td>' + item.majors + '</td>');
			studentinfo.push('<td data-id="' + item.studentID + '" data-name="' + item.name + '">' + '<a href="#" title="查看" id="show_student_info" class="btn btn-default btn-info btn-sm active" style="margin-right:3px;"><i class="glyphicon glyphicon-search" style="margin-right: 3px;"></i>查看</a>' + '<a href="#" title="编辑" id="edit_student_info" class="btn btn-default btn-success btn-sm  active" style="margin-right:3px;"><i class="glyphicon glyphicon-edit" style="margin-right: 3px;"></i>编辑</a>' + '<a href="#" title="删除" id="del_student_info" class="btn btn-default btn-danger btn-sm active" style="margin-right:3px;"><i class="glyphicon glyphicon-trash" style="margin-right: 3px;"></i>删除</a></td></tr>');
		});
		$('#student_info_list').append(studentinfo.toString());
	});
});

//create user information
function createUser(){
	$.ajax({
		type:'post';
//		url:'/users_ajax/createUser',
		url:''
		data:'',
		dataType:'json',
		success:function(result){
			console.log(result.data);
		},
		error:function(){
			console.log('error_message');
		}
	})
}

//updata user information
function updateUser(){
	
}

//delect user information
function delectUser(){
	$.post()
}
