
define(["lodash"], function(_) {
"use strict";

var helper = {},
    alertTpl = $("#alert_tpl").html();

var showErrorIn = function($where, errorMsg, level) {
    var LEVELS = ["danger", "warning", "success"];

    // 删除 $where 中的第一个 alert
    $($where.find(".alert")[0]).remove();

    $where.prepend(alertTpl);
    $($where.find(".alert")[0]).addClass("alert-" + level).find(".text").text(errorMsg);
};


helper.showErrorIn = showErrorIn;

return helper;

});



