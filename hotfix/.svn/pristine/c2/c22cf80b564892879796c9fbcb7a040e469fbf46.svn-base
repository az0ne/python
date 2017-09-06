"use strict";
require.config({
    baseUrl: "/static/",

    paths: {
        "lodash": "script/lib/lodash",
        "autogrow": "script/lib/autogrow",

        "ls": "libs/ls",

        // 页面相关
        "page": "script/page",

        "helper": "script/helper"
    },

    shim: {
        livescript: {
            exports: "LiveScript"
        },

        prelude: {
            exports: "prelude"
        },

        "lodash": {
            exports: "_"
        },
    },

    urlArgs: "bust=" +  (new Date()).getTime()
});


// main module
require([
    "lodash",
    "autogrow"
],
function(_) {
"use strict";

// bootstrap 控件初始化
$("[data-toggle='tooltip']").tooltip();
$("[data-toggle='popover']").popover();
$('[data-toggle="checkbox"]').radiocheck();

// 存在相应页面脚本的 page.name 列表
var _SCRIPT_LIST = [
    "lesson_resources",
    "user_teachers_info",
    "lesson_paper",
    "lesson_discusses",
    "course_paper",
    "teacher_messages",
    "student_messages"
];

// 在所有设置了 autogrow 的 元素上初始化 autogrow
$(".autogrow").autogrow({onInitialize: true});

// require 根据 page 名称加载相应的 page 脚本
if ("page" in window) {
    if (_.indexOf(_SCRIPT_LIST, window.page.name) > -1) {
        require(["page/" + window.page.name]);

    } else {

        console.log(window.page.name + " not in _SCRIPT_LIST");
    }
}

});


