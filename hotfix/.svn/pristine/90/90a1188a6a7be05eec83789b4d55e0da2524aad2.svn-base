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
        quizId = $currTr.data("quiz_id");

    switch(action) {
        case "delete":
            $.post(window.mz.url.paper_quiz_delete,
            {

                quiz_id: quizId

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


// toggle active
var $paperInfoForm = $("#course_info_form");
$paperInfoForm.on("change", "input[name='is_active']", function(event) {
    var $currTarget = $(event.currentTarget),
        paperId = $paperInfoForm.data("paper_id");

    $.post(window.mz.url.paper_toggle_active,
    {
        is_active: $currTarget.is(":checked"),
        paper_id: paperId

    }).done(function(res) {
        
    }).error(function(xhr) {
        
    });

});

});



