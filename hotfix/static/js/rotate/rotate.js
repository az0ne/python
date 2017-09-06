var _rotate_deg = 0;//回正 回到0度
var _rotate_angle = 30;//旋转度数 30度
var _rotate_deg_step = 5; //每次旋转角度，能够被_angle整除
var _rotate_duration = 1;//每次旋转时间
var _rotate_count = 0; //初始旋转次数
var _rotate_count_max = 6;//最大旋转次数
var _rotate_timer = null;
var _rotate_stop_time = 0;
var _rotate_stop_max_time = 500; //停止时间3秒

function _rotate_rotate(item) {
	if (_rotate_count == _rotate_count_max) {
		if (_rotate_deg == 0) {
			_rotate_stop_time = _rotate_stop_time + _rotate_duration;
			if (_rotate_stop_time == _rotate_stop_max_time) {
				_rotate_stop_time = 0;
				_rotate_count = 0;
			}
			return;
		}
		_rotate_deg = _rotate_deg + _rotate_deg_step;
		$("#" + item).css("transform", "rotate(" + _rotate_deg + "deg)");
		return;
	}

	_rotate_deg = _rotate_deg + _rotate_deg_step;
	if (_rotate_deg == _rotate_angle || _rotate_deg == -_rotate_angle) {
		_rotate_count = _rotate_count + 1;
		_rotate_deg_step = -_rotate_deg_step;
	}
	$("#" + item).css("transform", "rotate(" + _rotate_deg + "deg)");
}

function _rotate_start(item) {
	_rotate_timer = setInterval("_rotate_rotate('" + item + "')", _rotate_duration);
}

function _rotate_stop() {
	clearInterval(_rotate_timer);
}