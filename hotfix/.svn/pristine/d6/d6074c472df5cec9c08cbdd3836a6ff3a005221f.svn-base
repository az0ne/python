var _BIG_WIDTH = 384; //大div
var _SMALL_WIDTH = 256; //小图
var _BIG_HEIGHT = 480; //大div
var _SMALL_HEIGHT = 320;//小
var _IMG_BIG_WIDTH = 384;//大图
var _IMG_SMALL_WIDTH = 256;
var _IMG_BIG_HEIGHT = 288;//大图
var _IMG_SMALL_HEIGHT = 159;
var _TEXT_BIG_WIDTH = 384;//大文字
var _TEXT_SMALL_WIDTH = 256;
var _TEXT_BIG_HEIGHT = 241;//大文字
var _TEXT_SMALL_HEIGHT = 161;
var _SPAN_SIZE = 60;
var _SPEED = 500;
var _pos_list_src = new Array();
var _path_list = new Array();
var _num = 0;
var _timer = null;
var _step = 0;
var _finish_count = 0;
function creat_img_list(num) {
    pos = new Array();
    $("#ulContainer").html("");
    var style = "";
    var img_style = "";
    var text_style = "";
    for (var i = 0; i < num; ++i) {
        if (i == 0) {
            pos["index" + 0] = -90;
            style = "small first";
            img_style = "img_small";
            text_style = "text_small"
        } else {
            if (i == 2) {
                pos["index" + i] = 390;
                style = "big other";
                img_style = "img_big";
                text_style = "text_big"
            } else {
                if (i == 3) {
                    pos["index" + i] = 690
                } else {
                    pos["index" + i] = pos["index" + (i - 1)] + _BIG_WIDTH
                }
                style = "small other";
                img_style = "img_small";
                text_style = "text_small"
            }
        }
        $("#ulContainer").append("<li style='left:" + pos["index" + i] + "px;' index='" + i + "' class='item " + style + "'>"
            + "<img src='/static/images/mz_new_ad/web-images/slide-img1.png' class='" + img_style + " ' />"
            + '<div class=" ' + text_style + '"> '
            + ' <h6 class="slide-name "> ' + "周伟安" + "</h6>"
            + ' <p class="slide-salary "> ' + "月薪12K,入职腾讯" + "</p>"
            + ' <p class="slide-text-p "> ' + "团队是一个整体，讲究的是合作，有事没事多沟通，往往自己苦思冥想做出的结果却不适合。" + "</p>" + "</div> " + "</li>")
    }
    return pos
}
function count_img_num(container_width) {
    var num = 14;
    // container_width = container_width - _BIG_WIDTH - _SPAN_SIZE;
    // num = parseInt(container_width / (_SMALL_WIDTH + _SPAN_SIZE)) + 5;
    return num
}
function move(item) {
    var path = $(item).attr("path").split(",");
    var next = parseInt($(item).attr("next"));
    if (next == path.length - 1) {
        _finish_count = _finish_count - 1;
        return
    }
    next = next + 1;
    $(item).attr("next", next);
    var img = $(item).children()[0];
    var text = $(item).children()[1];
    if (path[next] == _num - 1 && path[next - 1] == 0) {
        $(item).animate({"left": -350, "width": _SMALL_WIDTH, "height": _SMALL_HEIGHT}, _SPEED, function () {
            var path = $(this).attr("path").split(",");
            var next = parseInt($(this).attr("next"));
            $(this).css("left", _pos_list_src["index" + path[next]] + "px");
            move(this)
        })
    } else {
        if (path[next] == 0 && path[next - 1] == _num - 1) {
            $(item).css("left", -350 + "px");
            $(item).animate({"left": -90, "width": _SMALL_WIDTH, "height": _SMALL_HEIGHT}, _SPEED, function () {
                var path = $(this).attr("path").split(",");
                var next = parseInt($(this).attr("next"));
                move(this)
            })
        } else {
            var width = _SMALL_WIDTH;
            var height = _SMALL_HEIGHT;
            var img_width = _IMG_SMALL_WIDTH;
            var img_height = _IMG_SMALL_HEIGHT;
            var text_width = _TEXT_SMALL_WIDTH;
            var text_height = _TEXT_SMALL_HEIGHT;
            if (path[parseInt($(item).attr("next"))] == 2) {
                width = _BIG_WIDTH;
                height = _BIG_HEIGHT;
                img_width = _IMG_BIG_WIDTH;
                img_height = _IMG_BIG_HEIGHT;
                text_width = _TEXT_BIG_WIDTH;
                text_height = _TEXT_BIG_HEIGHT
            }
            $(img).animate({"width": img_width, "height": img_height}, _SPEED);
            $(text).animate({"width": text_width, "height": text_height}, _SPEED);
            $(item).animate({
                "left": _pos_list_src["index" + path[next]],
                "width": width,
                "height": height
            }, _SPEED, function () {
                move(this)
            })
        }
    }
}
function init_img() {
    var container_width = document.body.clientWidth;
    $("#divContainer").width(container_width);
    _num = count_img_num(container_width);
    $("#ulContainer").width(_num * _SMALL_WIDTH + _BIG_WIDTH + _num * _SPAN_SIZE);
    _pos_list_src = creat_img_list(_num);
    $(".item").click(function () {
        if (_finish_count != 0) {
            return
        }
        _finish_count = _num;
        var current_click_index = parseInt($(this).attr("index"));
        _step = current_click_index - 2;
        for (var i = 0; i < $("#ulContainer li").length; ++i) {
            var pos_des = 0;
            var item = $("#ulContainer li")[i];
            var index = parseInt($(item).attr("index"));
            if (_step == 0) {
                _finish_count = 0;
                return
            }
            if (index == current_click_index) {
                pos_des = 2
            } else {
                if (_step < 0) {
                    if (index - _step < _num) {
                        pos_des = index - _step
                    } else {
                        pos_des = -_num + index - _step
                    }
                } else {
                    if (index - _step < 0) {
                        pos_des = _num + (index - _step)
                    } else {
                        pos_des = index - _step
                    }
                }
            }
            $(item).attr("index", pos_des);
            var path = [];
            if (_step < 0) {
                if (index > pos_des) {
                    for (var cell = index + 1; cell <= _num - 1; ++cell) {
                        path.push(cell)
                    }
                    for (var cell = 0; cell <= pos_des; ++cell) {
                        path.push(cell)
                    }
                } else {
                    for (var cell = index + 1; cell <= pos_des; ++cell) {
                        path.push(cell)
                    }
                }
            } else {
                if (index > pos_des) {
                    for (var cell = index - 1; cell >= pos_des; --cell) {
                        path.push(cell)
                    }
                } else {
                    for (var cell = index - 1; cell >= 0; --cell) {
                        path.push(cell)
                    }
                    for (var cell = _num - 1; cell >= pos_des; --cell) {
                        path.push(cell)
                    }
                }
            }
            _path_list["index" + pos_des] = path
        }
        for (var i = 0; i < $("#ulContainer li").length; ++i) {
            var item = $("#ulContainer li")[i];
            var index = $(item).attr("index");
            var path = _path_list["index" + index];
            $(item).attr("next", 0);
            $(item).attr("path", path);
            var img = $(item).children()[0];
            var text = $(item).children()[1];
            if (_step > 0) {
                if (path[parseInt($(item).attr("next"))] == _num - 1) {
                    $(item).animate({
                        "left": -350,
                        "width": _SMALL_WIDTH,
                        "height": _SMALL_HEIGHT
                    }, _SPEED, function () {
                        var path = $(this).attr("path").split(",");
                        var next = parseInt($(this).attr("next"));
                        $(this).css("left", _pos_list_src["index" + path[next]] + "px");
                        move(this)
                    })
                } else {
                    var path = $(item).attr("path").split(",");
                    var next = parseInt($(item).attr("next"));
                    var width = _SMALL_WIDTH;
                    var height = _SMALL_HEIGHT;
                    var img_width = _IMG_SMALL_WIDTH;
                    var img_height = _IMG_SMALL_HEIGHT;
                    var text_height = _TEXT_SMALL_HEIGHT;
                    var text_width = _TEXT_SMALL_WIDTH;
                    if (path[parseInt($(item).attr("next"))] == 2) {
                        width = _BIG_WIDTH;
                        height = _BIG_HEIGHT;
                        img_width = _IMG_BIG_WIDTH;
                        img_height = _IMG_BIG_HEIGHT;
                        text_width = _TEXT_BIG_WIDTH;
                        text_height = _TEXT_BIG_HEIGHT
                    }
                    $(img).animate({"width": img_width, "height": img_height}, _SPEED);
                    $(text).animate({"width": text_width, "height": text_height}, _SPEED);
                    $(item).animate({
                        "left": _pos_list_src["index" + path[next]],
                        "width": width,
                        "height": height
                    }, _SPEED, function () {
                        move(this)
                    })
                }
            } else {
                if (path[parseInt($(item).attr("next"))] == 0) {
                    $(item).css("left", -350 + "px");
                    $(item).animate({"left": -90, "width": _SMALL_WIDTH, "height": _SMALL_HEIGHT}, _SPEED, function () {
                        var path = $(this).attr("path").split(",");
                        var next = parseInt($(this).attr("next"));
                        move(this)
                    })
                } else {
                    var path = $(item).attr("path").split(",");
                    var next = parseInt($(item).attr("next"));
                    var img_width = _IMG_SMALL_WIDTH;
                    var img_height = _IMG_SMALL_HEIGHT;
                    var text_height = _TEXT_SMALL_HEIGHT;
                    var text_width = _TEXT_SMALL_WIDTH;
                    var width = _SMALL_WIDTH;
                    var height = _SMALL_HEIGHT;
                    if (path[parseInt($(item).attr("next"))] == 2) {
                        width = _BIG_WIDTH;
                        height = _BIG_HEIGHT;
                        img_width = _IMG_BIG_WIDTH;
                        img_height = _IMG_BIG_HEIGHT;
                        text_height = _TEXT_BIG_HEIGHT;
                        text_width = _TEXT_BIG_WIDTH
                    }
                    $(img).animate({"width": img_width, "height": img_height}, _SPEED);
                    $(text).animate({"width": text_width, "height": text_height}, _SPEED);
                    $(item).animate({
                        "left": _pos_list_src["index" + path[next]],
                        "width": width,
                        "height": height
                    }, _SPEED, function () {
                        move(this)
                    })
                }
            }
        }
    })
}
$(document).ready(function () {
    init_img()
});
$(window).resize(function () {
    init_img()
});