$.ajaxSetup({
    data: { csrfmiddlewaretoken: '{{ csrf_token }}' },
});
$(function() {
	$('#courseManange').off('click').on('click', function() {
		// $('#pageMain').load('/course/list/');
		// $.maizi_Course.getCourseList();
	});
	 $('#careerCatagory').off('click').on('click', function() {
	 	$('#pageMain').load("/careerCatagory/list/");
	 	getCareerCatagoryList(null);  //调用careerCatagory.js中的getCareerCatagoryList()函数
	 });

});