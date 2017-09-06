/**
 * Created by hidden on 2016/5/17.
 */


/* list */
$(document).ready(function () {
        $("#articTyperow").jqPaginator({
        totalPages: 100,
        visiblePages: 7,
        currentPage: 1,
        onPageChange: function (pageIndex) {
            $.ajax({
                url: "/home/ajax/articleType/list/",//待填写
                type: "get",
                data: {
                    'currentPage': pageIndex,
                    'pageSize': 10
                },
                dataType: "json",
                success: function (data) {
                    courseinfo = [];
                    $.each(data.result.data, function (key, value) {
                        var status = (value.is_homepage) ? '激活' : '未激活';
                        courseinfo.push('<tr><td>' + value.id + '</td>');
                        courseinfo.push('<td>' + value.name + '</td>');
                        courseinfo.push('<td>' + status + '</td>');
                        courseinfo.push('<td data-id="' + value.id + '" data-name="' + value.name + '" data-is_homepage="' + value.is_homepage + '" >' + '<a href="#" title="查看" class="btn btn-default btn-info btn-sm active show_articType" data-toggle="modal" data-target="#confirm" style="margin-right:3px;"><i class="glyphicon glyphicon-search" style="margin-right: 3px;"></i>查看</a>' + '<a href="#" title="编辑" class="btn btn-default btn-success btn-sm  active edit_articType_info" style="margin-right:3px;"><i class="glyphicon glyphicon-edit" style="margin-right: 3px;"></i>编辑</a>' + '<a href="#" title="删除" class="btn btn-default btn-danger btn-sm active del_articType_info" style="margin-right:3px;"><i class="glyphicon glyphicon-trash" style="margin-right: 3px;"></i>删除</a></td></tr>');
                    });
                    $('#articTyperow').children().remove();
                    $('#articTyperow').append(courseinfo.toString());
                    $("#pagerDataInfo").text("共" + data.result.totalPages + "页" + data.result.totalCounts + "条数据");
                    $('#pagination1').jqPaginator('option', {
                        totalPages: data.result.totalPages,
                        currentPage: pageIndex
                    });
                    selectarticname();
                }
            })

        }
    });
    


 /* 删除逻辑 */   
    $(document).off("click", ".del_articType_info").on("click", ".del_articType_info", function () {
        var tableid = $(this).parents().attr("data-id");
        $('#articType_delconfirm').modal('show');
        $(document).off("click", "#update").on("click", "#update", function () {
            del(tableid);
        })

    });
    /* 添加逻辑 */
    $(document).off("click", "#btn_addarticType").on("click", "#btn_addarticType", function () {
        $('#modal_editarticType').modal('show');
        $("#artictype_id").attr("disabled", true);//表ID
        $("#artictype_name").attr("disabled", false);
        $("#articTypeis_homepage").attr("disabled", false);
        $("#artictype_id").val("");
        $("#artictype_name").val("");//清空可能影响下拉框数据待测
        $("#articTypeis_homepage").val("");//清空可能影响下拉框数据待测
        $("#artictype_name").get(0).selectedIndex=0;
        $("#articTypeis_homepage").get(0).selectedIndex=0;
        $(document).off("click", "#update").on("click", "#update", function () {
            var infoname = $("#artictype_name").val();
            var is_hot_active =  $("#articTypeis_homepage").val();
            addinfo(infoname, is_hot_active)
        })

    });
    
    /* 编辑逻辑 */
    $(document).off("click", ".edit_articType_info").on("click", ".edit_articType_info", function () {
        var dataid = $(this).parents().attr("data-id");
        var dataname = $(this).parents().attr("data-name");
        var updateactive = $(this).parents().attr("data-is_homepage");
        $('#modal_editarticType').modal('show');
        $("#artictype_name").attr("disabled", false);
        $("#artictype_id").attr("disabled", true);
        $("#articTypeis_homepage").attr("disabled", false);
        $("#artictype_name").val("");
        $("#artictype_id").val("");
        $("#articTypeis_homepage").val("");
        $("#artictype_name").val(dataname);
        $("#artictype_id").val(dataid);
        $("#articTypeis_homepage").get(0).selectedIndex = 1;
        $(document).off("click", "#update").on("click", "#update", function () {
            var updatename = $("#artictype_name").val();
            var updateid = $("#artictype_id").val();
            var updateactive = $("#articTypeis_homepage").val();
            update(updatename, updateid, updateactive)

        })

    });
    
    /* 查看逻辑 */
    $(document).off("click", ".show_articType").on("click", ".show_articType", function () {
        var dataid = $(this).parents().attr("data-id");
        var dataname = $(this).parents().attr("data-name");
        var dataactive = $(this).parents().attr("data-is_homepage");
        $('#modal_editarticType').modal('show');
        $("#artictype_name").attr("disabled", true);
        $("#artictype_id").attr("disabled", true);
        $("#articTypeis_homepage").attr("disabled", true);
        $("#artictype_name").val("");
        $("#artictype_id").val("");
        $("#articTypeis_homepage").val("");
        $("#artictype_name").val(dataname);
        $("#artictype_id").val(dataid);
        $("#articTypeis_homepage").val(dataactive);

    });

});

//删除方法
function del(tableid) {
    $.ajax({
        url: "/home/ajax/articleType/delete/",//待填写
        type: "post",
        data: {"id": tableid},
        datatype: "json",
        success: function (data) {
            if (data.code == 0) {
                 $('#articType_delconfirm').modal('hide');
                setTimeout(function () {
                    $('#pageMain').load("articleType/list/");
                },300);
            } else {
                alert(data.error);
            }
        }
    });
}

////添加方法
function addinfo(infoname, is_hot_active) {
    $.ajax({
        url: "/home/ajax/articleType/create/",//待填写
        type: "post",
        data: {
            name: infoname,
            is_homepage: is_hot_active
        },
        success: function (data) {
            if (data.code == 0) {
                $('#modal_editarticType').modal('hide');
                setTimeout(function () {
                    $('#pageMain').load("/home/articleType/list/");
                },300);
            } else {
                alert(data.error)
            }
        }
    });
}

//编辑方法
function update(updatename, updateid, updateactive) {
    $.ajax({
        url: "/home/ajax/articleType/update/",//待填写
        type: "post",
        data: {
            id: updateid,
            name: updatename,
            is_homepage: updateactive
        },
        success: function (data) {
            if (data.code == 0) {
               $('#modal_editarticType').modal('hide');
                setTimeout(function () {
                    $('#pageMain').load("/home/articleType/list/");
                },300);
            } else {
                alert(data.error)
            }
        }
    });
}




//动态获取select-tag-id选项
function selectarticname() {
    $.ajax({
        url: "/home/ajax/articleType/get/",//artic表接口
        type: "get",
        async: false,
        success: function (data) {
            var selectinfo = [];
            $.each(data.result, function (id, selectname) {
                selectinfo.push('<option value="' +
                    selectname.id + '">' + selectname.name + '</option>'
                );
            })
            $("#artictype_name").append(selectinfo.toString());
        }
    })
}

//页码输入框
$("#takepaginationarticletype").on("change", function () {
    var pagination = $("#takepaginationarticletype").val();
    $.ajax({
        url: "/home/ajax/articleType/list/",
        type: "get",
        data: {
            'currentPage': pagination,
            'pageSize': 10
        },
        success: function (data) {
            courseinfo = [];
            $.each(data.result.data, function (key, value) {
                var status = (value.is_homepage) ? '显示' : '不显示';
                courseinfo.push('<tr><td>' + value.id + '</td>');
                courseinfo.push('<td>' + value.name + '</td>');
                courseinfo.push('<td>' + status + '</td>');
                courseinfo.push('<td data-id="' + value.id + '" data-name="' + value.name + '" data-is_homepage="' + value.is_homepage + '" >' + '<a href="#" title="查看" class="btn btn-default btn-info btn-sm active show_articType" data-toggle="modal" data-target="#confirm" style="margin-right:3px;"><i class="glyphicon glyphicon-search" style="margin-right: 3px;"></i>查看</a>' + '<a href="#" title="编辑" class="btn btn-default btn-success btn-sm  active edit_articType_info" style="margin-right:3px;"><i class="glyphicon glyphicon-edit" style="margin-right: 3px;"></i>编辑</a>' + '<a href="#" title="删除" class="btn btn-default btn-danger btn-sm active del_articType_info" style="margin-right:3px;"><i class="glyphicon glyphicon-trash" style="margin-right: 3px;"></i>删除</a></td></tr>');
            });
            $('#articTyperow').children().remove();
            $('#articTyperow').append(courseinfo.toString());
            $('#pagination1').children(".page").removeClass("active");
            $('#pagination1').children(".page").eq(pagination - 1).addClass("active");
            if (pagination > data.result.totalPages) {
                alert("error")
            }

        }
    })

});



//刷新
$('#btn_articTyperfh').off('click').on('click', function () {
    $('#pageMain').load("/home/articleType/list/");
    var currtext = $(this).text();
    $("#breadtwo>a").text(currtext);
    $("#breadtwo").show();
});







//验证输入
$(document).ready(function () {
    $('#articType_form').validate({
        rules: {
            articletypename: {
                required: true,
                minlength: 2
            },
            catagoryid: {
                required: true
            }
        },
        messages: {
            articletypename: {
                required: "请键入正确的文章栏目名称",
                minlength: "输入错误"
            },
            catagoryid: {
                required: "至少选择一项"
            }
        }

    });
});