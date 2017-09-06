define(function (require, exports, module) {
    var $ = require('jquery');
    // require('textFiltered')($);


    if ($('.search_result_bg').length > 0) {
        var app = $('.search_app').val() ? $('.search_app').val() : 'course';
        $('.hot-words a').attr('target', '_self');
        $("#fLayerdl dd a").attr('target', '_self');
        $('.hot-words a').attr('href', '/search/' + app + '/web前端-1/');
        $('.hot-words a:first-child').attr('href', '/search/' + app + '/产品经理-1/');
        $('.hot-words a:last-child').attr('href', '/search/' + app + '/ui-1/');
    }

    function Search() {
        $(".search-btn").click(function () {
            sreachBtn($("#data-search").val());
            zhuge.track('搜索次数', {'搜索关键词': $("#data-search").val()});
        });

        function sreachBtn(str) {
            var str = str.replace('#', 'u0023').replace('?', 'u0022');
            if ($('.search_result_bg').length > 0) {
                var app = $('.search_app').val() ? $('.search_app').val() : 'course';
                window.location.href = "/search/" + app + "/" + str + "-1/";
            } else {
                window.open("/search/course/" + str + "-1/");
            }

        }

        $("#data-search").keyup(function (event) {
            var e = event || window.event || arguments.callee.caller.arguments[0];
            if (e && e.keyCode == 13) {
                sreachBtn($(this).val());
                return;
            }
        });

        //     $("#data-search").textFiltered({
        //         "boEnter": true,
        //         "onkeyup": function (boolean) {
        //             var $th = this, bokey = false;
        //             if (boolean) {
        //                 sreachBtn($th.val());
        //                 return;
        //             }
        //             $.ajax({
        //                 type: "GET",
        //                 url: "/homepage/get_course_category/",
        //                 data: {"s": $th.val()},
        //                 beforeSend: function (XMLHttpRequest) {
        //                 },
        //                 success: function (data1) {
        //                     $th.clear();
        //                     for (var i = 0; i < data1.length; i++) {
        //                         $th.addNode(data1[i], data1[i]);
        //                         if (data1[i] == $th.val()) {
        //                             $th.data("vv", data1[i]);
        //                             bokey = true;
        //                         }
        //                     }
        //                 },
        //                 complete: function (XMLHttpRequest) {
        //                 }
        //             });
        //             if (!bokey) $th.removeData("vv");
        //         }
        //         , "height": 180
        //         , "onarrowupdown": function (i) {
        //         }
        //         , "onVclick": function (v) {
        //             this.data("vv", v);
        //             if (v != "暂无数据") {
        //                 $("#data-search").val(v);
        //             }
        //         }
        //     });
    }


    module.exports = {
        'Search': Search
    };

});
