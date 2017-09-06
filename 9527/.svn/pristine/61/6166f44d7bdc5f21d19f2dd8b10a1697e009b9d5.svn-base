/**
 * Created by hidden on 2016/5/17.
 */


/* list */
$(document).ready(function () {
    $("#CareerTagRelationrow").jqPaginator({
        totalPages: 100,
        visiblePages: 7,
        currentPage: 1,
        onPageChange: function (pageIndex) {
            $.ajax({
                url: "/ajax/careerTagRelation/list/",
                type: "get",
                data: {
                    'currentPage': pageIndex,
                    'pageSize': 10
                },
                dataType: "json",
                success: function (data) {
                    courseinfo = [];
                    $.each(data.result.data, function (key, value) {
                        courseinfo.push('<tr><td>' + value.id + '</td>');
                        courseinfo.push('<td>' + value.tag_id + '</td>');
                        courseinfo.push('<td>' + value.careercatagory_id + '</td>');
                        courseinfo.push('<td data-id="' + value.id + '" data-tag-id="' + value.tag_id + '" data-careercatagory_id="' + value.careercatagory_id + '" >' + '<a href="#" title="查看" class="btn btn-default btn-info btn-sm active show_careertagrelation" data-toggle="modal" data-target="#confirm" style="margin-right:3px;"><i class="glyphicon glyphicon-search" style="margin-right: 3px;"></i>查看</a>' + '<a href="#" title="删除" class="btn btn-default btn-danger btn-sm active del_careertagrelation_info" style="margin-right:3px;"><i class="glyphicon glyphicon-trash" style="margin-right: 3px;"></i>删除</a></td></tr>');
                    });
                    $('#CareerTagRelationrow').children().remove();
                    $('#CareerTagRelationrow').append(courseinfo.toString());
                    $("#pagerDataInfo").text("共" + data.result.totalPages + "页" + data.result.totalCounts + "条数据");
                    $('#pagination1').jqPaginator('option', {
                        totalPages: data.result.totalPages,
                        currentPage: pageIndex,
                    });
                    TAGID();
                    careercatagoryid();
                }
            })

        }
    });



 /* 删除逻辑 */   
    $(document).off("click", ".del_careertagrelation_info").on("click", ".del_careertagrelation_info", function () {
        var tableid = $(this).parents().attr("data-id");
        $('#CareerTagRelation_delconfirm').modal('show');
        $(document).off("click", "#update").on("click", "#update", function () {
            del(tableid);
        })

    });
    /* 添加逻辑 */
    $(document).off("click", "#btn_addCareerTagRelation").on("click", "#btn_addCareerTagRelation", function () {
        $('#modal_editCareerTagRelation').modal('show');
        $("#tagID").attr("disabled", false);
        $("#course_tag_id").attr("disabled", true);
        $("#careertagrelationID").attr("disabled", false);
        $("#update").attr("disabled", false);
        $("#course_tag_id").val("");
        $("#careertagrelationID").val("");
/*        $.ajax({
            url: "careerCourse/list/ajax/", 
            type: "get",
            
        });*/
        $("#tagID").val("");
        $("#tagID").get(0).selectedIndex=0;
        $("#careertagrelationID").get(0).selectedIndex=0;
        $(document).off("click", "#update").on("click", "#update", function () {
            var infotagid = $("#tagID").val();
            var infocareertagrelationid =  $("#careertagrelationID").val();
            addinfo(infotagid, infocareertagrelationid)
        })

    });
    
    /* 编辑逻辑 */
    $(document).off("click", ".edit_careertagrelation_info").on("click", ".edit_careertagrelation_info", function () {
        var dataid = $(this).parents().attr("data-id");
        var datatagid = $(this).parents().attr("data-tag-id");
        var datacareercatagoryid = $(this).parents().attr("data-careercatagory_id");
        $('#modal_editCareerTagRelation').modal('show');
        $("#tagID").attr("disabled", false);
        $("#careertagrelationID").attr("disabled", false);
        $("#course_tag_id").attr("disabled", true);
        $("#update").attr("disabled", false);
        $("#tagID").val("");
        $("#careertagrelationID").val("");
        $("#course_tag_id").val("");
        $("#tagID").val(datatagid);
        $("#course_tag_id").val(dataid);
        $("#careertagrelationID").val(datacareercatagoryid);
        $(document).off("click", "#update").on("click", "#update", function () {
            var updatetagid = $("#tagID").val();
            var updateid = $("#course_tag_id").val();
            var updatecareercatagoryid = $("#careertagrelationID").val();
            update(updatetagid, updateid, updatecareercatagoryid)

        })

    });
    
    /* 查看逻辑 */
    $(document).off("click", ".show_careertagrelation").on("click", ".show_careertagrelation", function () {
        var dataid = $(this).parents().attr("data-id");
        var datatagid = $(this).parents().attr("data-tag-id");
        var datacareercatagoryid = $(this).parents().attr("data-careercatagory_id");
        $('#modal_editCareerTagRelation').modal('show');
        $("#tagID").val("");
        $("#careertagrelationID").val("");
        $("#course_tag_id").val("");
        $("#tagID").val(datatagid);
        $("#course_tag_id").val(dataid);
        $("#careertagrelationID").val(datacareercatagoryid);
        $("#careertagrelationID").attr("disabled", true);
        $("#tagID").attr("disabled", true);
        $("#course_tag_id").attr("disabled", true);
        $("#update").attr("disabled", true);

    });

    
});

//删除方法
function del(tableid) {
    $.ajax({
        url: "/ajax/careerTagRelation/delete/",//待填写
        type: "post",
        data: {"id": tableid},
        datatype: "json",
        success: function (data) {
            if (data.code == 0) {
                $('#CareerTagRelation_delconfirm').modal('hide');
                setTimeout(function () {
                    $('#pageMain').load("/careerTagRelation/list/");
                },300);
            } else {
                alert(data.error);
            }

        },
    });
}

////添加方法
function addinfo(infotagid, infocareertagrelationid) {
    $.ajax({
        url: "/ajax/careerTagRelation/create/",
        type: "post",
        data: {
            tag_id: infotagid,
            careercatagory_id: infocareertagrelationid
        },
        success: function (data) {
            if (data.code == 0) {
                $('#modal_editCareerTagRelation').modal('hide');
                setTimeout(function () {
                    $('#pageMain').load("/careerTagRelation/list/");//待填写职业方向标签load接口
                }, 300);
            } else {
                alert(data.error)
            }
        }
    });
}

//编辑方法
function update(updatetagid, updateid, updatecareercatagoryid) {
    $.ajax({
        url: "/ajax/careerTagRelation/update/",//待填写careertagrelation编辑接口
        type: "post",
        data: {
            id: updateid,
            tag_id: updatetagid,
            careercatagory_id: updatecareercatagoryid
        },
        success: function (data) {
            if (data.code == 0) {
                $('#modal_editCareerTagRelation').modal('hide');
                setTimeout(function () {
                    $('#pageMain').load("/careerTagRelation/list/");//待填写职业方向标签load接口
                }, 300);
            } else {
                alert(data.error)
            }
        }
    });
}



//动态获取select-tag-id选项
function TAGID() {
    $.ajax({
        url: "/ajax/tag/get/",//tag表id接口
        type: "get",
        async: false,
        success: function (data) {
            var selectinfo = [];
            $.each(data.result, function (id, selectname) {
                selectinfo.push('<option value="' +
                    selectname.id + '">' + selectname.id + ':' + selectname.name + ':' + selectname.is_hot_tag + '</option>'
                );
            })
            $("#tagID").append(selectinfo.toString());
        }
    })
}

//动态获取select-careercatagoryid选项
function careercatagoryid() {
    $.ajax({
        url: "/ajax/careerCatagory/get/",//careercatagory表id接口
        type: "get",
        async: false,
        success: function (data) {
            var selectinfo = [];
            $.each(data.result, function (id, selectname) {
                selectinfo.push('<option value="' +
                    selectname.id + '">' + selectname.id + ':' + selectname.name + '</option>'
                );
            })
            $("#careertagrelationID").append(selectinfo.toString());
        }
    })
}

//页码输入框
$("#takepaginationcareerrelation").on("change", function () {
    var pagination = $("#takepaginationcareerrelation").val();
    $.ajax({
        url: "/ajax/careerTagRelation/list/",
        type: "get",
        data: {
            'currentPage': pagination,
            'pageSize': 10
        },
        success: function (data) {
            courseinfo = [];
            $.each(data.result.data, function (key, value) {
                var status = (value.is_hot_tag) ? '激活' : '未激活';
                courseinfo.push('<tr><td>' + value.id + '</td>');
                courseinfo.push('<td>' + value.tag_id + '</td>');
                courseinfo.push('<td>' + value.careercatagory_id + '</td>');
                courseinfo.push('<td data-id="' + value.id + '" data-tag-id="' + value.tag_id + '" data-careercatagory_id="' + value.careercatagory_id + '" >' + '<a href="#" title="查看" class="btn btn-default btn-info btn-sm active show_careertagrelation" data-toggle="modal" data-target="#confirm" style="margin-right:3px;"><i class="glyphicon glyphicon-search" style="margin-right: 3px;"></i>查看</a>' + '<a href="#" title="删除" class="btn btn-default btn-danger btn-sm active del_careertagrelation_info" style="margin-right:3px;"><i class="glyphicon glyphicon-trash" style="margin-right: 3px;"></i>删除</a></td></tr>');
            });
            $('#CareerTagRelationrow').children().remove();
            $('#CareerTagRelationrow').append(courseinfo.toString());
            $('#pagination1').children(".page").removeClass("active");
            $('#pagination1').children(".page").eq(pagination - 1).addClass("active");
            if (pagination > data.result.totalPages) {
                alert("error")
            }

        }
    })

});


//刷新
$("#btn_articTyperfh").off('click').on('click', function () {
    $('#pageMain').load("/careerTagRelation/list/");
    var currtext = $(this).text();
    $("#breadtwo>a").text(currtext);
    $("#breadtwo").show();
});







//验证输入
$(document).ready(function () {
    $('#careertagrelation_form').validate({
        rules: {
            tagidvalidate: {
                required: true,
            },
            careervalidate: {
                required: true
            },
        },
        messages: {
            tagidvalidate: {
                required: "至少选择一项"
            },
            careervalidate: {
                required: "至少选择一项"
            }
        }

    });
});