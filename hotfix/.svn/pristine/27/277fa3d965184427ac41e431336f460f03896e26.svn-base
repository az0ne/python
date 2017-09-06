/**
 * Created by Administrator on 2017/6/14.
 */
$(function() {

	var tit = $('title').html();
	var pro = (tit.split('-'))[0].trim();
	var addr = window.location.href;

	$('#yz-form').append($('<input type="hidden" name="qq" value="' + pro + '">'));
	$('#yz-form').append($('<input type="hidden" name="source" value="' + addr + '">'));

	$('.yz-submit').click(function() {
		var self = $(this);
		var $name = $('.yz-name input').val().trim();
		var $phone = $('.yz-phone input').val().trim();
		var isphone = /^1[34578]\d{9}$/.test($phone);
		var data;

		if($name === "") {
			$('.yz-name').addClass('yz-error');
		} else if(!isphone) {
			$('.yz-phone').addClass('yz-error');
		} else {

			data = $("#yz-form").serialize();
			$.ajax({
				type: "POST",
				url: "/common/app_consult_info_stream/add/?op=web",
				data: data,
				beforeSend: function() {
					self.text('提交中...')
						.attr('disabled', 'true');
				},
				success: function(data) {
					if(data.status == "success") {

						alert("提交成功！专业老师稍后会与您电话联系，为您申请试学体验！");
					} else {
						alert("提交失败！请重新提交");
					}
					self.text('提交').removeAttr('disabled');
				},
				error: function() {
					alert('提交失败，请重新提交');
					self.text('提交')
						.removeAttr('disabled');
				}
			});
		}
		return false;
	});
	$(document).keyup(function(key) {
		if(key.keyCode == 8) {
			if($(':focus').length !== 0) {
				$('.yz-error').removeClass('yz-error');
			}
		}
	});
});