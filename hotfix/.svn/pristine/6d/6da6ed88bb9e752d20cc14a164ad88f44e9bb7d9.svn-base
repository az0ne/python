define([
    "lodash",
    "helper"
],
function(_, helper) {
"use strict";

var $table = $(".table");

$table.on("click", ".action_list", function(event) {
    var $currTarget = $(event.currentTarget),
        $currTr = $currTarget.parents("tr"),
        $target = $(event.target);

    var action = $target.data("action"),
        messageId = $currTr.data("message_id");

    switch(action) {
        case "delete":
            $.post(window.mz.url.messages_delete,
            {
                message_id: messageId
            }, "json").done(function(res) {
                if (res.msg === "ok") {
                    $currTr.addClass("deleted_tr");
                    $target.addClass("disabled");

                    helper.showErrorIn($table.parent(), "删除成功", "success");
                } else {

                    showErrorIn($table.parent(), "操作失败", "danger");
                }
            }).error(function(xhr) {
                helper.showErrorIn($table.parent(), "操作失败", "danger");
            });
            break;
    }
});

});




