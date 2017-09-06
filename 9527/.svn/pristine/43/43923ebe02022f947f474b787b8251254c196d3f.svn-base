/**
 * Created by hidden on 2016/5/17.
 */


/* list */
$(document).ready(function () {
    $("#courseTableRow").jqPaginator({
        totalPages: 100,
        visiblePages: 7,
        currentPage: 1,
        onPageChange: function (pageIndex) {
            $.ajax({
                url: "/ajax/courseCatagory/list/",
                type: "get",
                data: {
                    'currentPage': pageIndex,
                    'pageSize': 10
                },
                dataType: "json",
                success: function (data) {
                    courseinfo = [];
                    $.each(data.result.data, function (key, value) {
                        var status = (value.is_hot_tag) ? '激活' : '未激活';
                        courseinfo.push('<tr><td>' + value.id + '</td>');
                        courseinfo.push('<td>' + value.career_catagory_id + '</td>');
                        courseinfo.push('<td>' + value.name + '</td>');
                        courseinfo.push('<td>' + status + '</td>');
                        courseinfo.push('<td data-id="' + value.id + '" data-name="' + value.name + '" data-active="' + value.is_hot_tag + '" data-career="' + value.career_catagory_id + '">' + '<a href="#" title="查看" class="btn btn-default btn-info btn-sm active show_coursecatagory" data-toggle="modal" data-target="#confirm" style="margin-right:3px;"><i class="glyphicon glyphicon-search" style="margin-right: 3px;"></i>查看</a>' + '<a href="#" title="编辑" class="btn btn-default btn-success btn-sm  active edit_coursetag_info" style="margin-right:3px;"><i class="glyphicon glyphicon-edit" style="margin-right: 3px;"></i>编辑</a>' + '<a href="#" title="删除" class="btn btn-default btn-danger btn-sm active del_this_info" style="margin-right:3px;"><i class="glyphicon glyphicon-trash" style="margin-right: 3px;"></i>删除</a></td></tr>');
                    });
                    $('#courseTableRow').children().remove();
                    $('#courseTableRow').append(courseinfo.toString());
                    $("#pagerDataInfo").text("共" + data.result.totalPages + "页" + data.result.totalCounts + "条数据");
                    $('#pagination1').jqPaginator('option', {
                        totalPages: data.result.totalPages,
                        currentPage: pageIndex
                    });
                    dafa();
                }
            })
            
        }
    });
    


    /* 删除逻辑 */
    $(document).off("click", ".del_this_info").on("click", ".del_this_info", function () {
        var tableid = $(this).parents().attr("data-id");
        $('#coursecatagory_delconfirm').modal('show');
        $(document).off("click", "#update").on("click", "#update", function () {
            del(tableid);
        })

    });
    /* 添加逻辑 */
    $(document).off("click", "#btn_addcoursecatagory").on("click", "#btn_addcoursecatagory", function () {
        $('#modal_editcoursecatagory').modal('show');
        $("#update").attr("disabled", false);
        $("#course_tag_name").attr("disabled", false);
        $("#selectcourseinfo").attr("disabled", false);
        $("#course_tag_active").attr("disabled", false);
        $("#course_tag_active").val("");
        $("#course_tag_name").val("");
        // $.ajax({
        //     url: "careerCourse/list/ajax/",
        //     type: "get",
        //
        // });
        // $("#course_tag_id").val("");
        $("#course_tag_active").get(0).selectedIndex = 0;
        $("#selectcourseinfo").get(0).selectedIndex = 0;
        $(document).off("click", "#update").on("click", "#update", function () {
            var infotext = $("#course_tag_name").val();
            var is_hot_active = $("#course_tag_active").val();
            var infoid = $("#selectcourseinfo").val();
            addinfo(infotext, is_hot_active, infoid)
    })

});


        /* 编辑逻辑 */
        $(document).off("click", ".edit_coursetag_info").on("click", ".edit_coursetag_info", function () {
            var dataid = $(this).parents().attr("data-id");//ID
            var dataname = $(this).parents().attr("data-name");//類目
            var career = $(this).parents().attr("data-career");//序列
            $('#modal_editcoursecatagory').modal('show');
            $("#update").attr("disabled", false);
            $("#course_tag_name").attr("disabled", false);
            $("#course_tag_active").attr("disabled", false);
            $("#selectcourseinfo").attr("disabled", false);
            $("#course_tag_name").val("");
            $("#course_tag_active").val("");
            $("#selectcourseinfo").val("");
            $("#course_tag_name").val(dataname);
            $("#selectcourseinfo").val(career);
            $("#course_tag_active").get(0).selectedIndex = 1;
            $(document).off("click", "#update").on("click", "#update", function () {
                var updatename = $("#course_tag_name").val();
                var hotactive = $("#course_tag_active").val();
                var updateactive = $("#selectcourseinfo").val();
                update(updatename, dataid, updateactive, hotactive)

            });
            return false;

        });

        /* 查看逻辑 */
        $(document).off("click", ".show_coursecatagory").on("click", ".show_coursecatagory", function () {
            var dataid = $(this).parents().attr("data-id");
            var dataname = $(this).parents().attr("data-name");
            $('#modal_editcoursecatagory').modal('show');
            $("#course_tag_name").val("");
            $("#course_tag_id").val("");
            $("#course_tag_name").val(dataname);
            $("#course_tag_id").val(dataid);
            $("#course_tag_name").attr("disabled", true);
            $("#selectcourseinfo").attr("disabled", true);
            $("#course_tag_active").attr("disabled", true);
            $("#update").attr("disabled", true);

        });
        /*    //jquery合法验证
         $("#coursecatagory_form").validate({
         rules: {
         course_tag_name: "required",
         course_tag_id: {
         required:true,
         digits:true
         }
         }
         })

         */
    });

//删除方法
    function del(tableid) {
        $.ajax({
            url: "/ajax/courseCatagory/delete/",
            type: "post",
            data: {"id": tableid},
            datatype: "json",
            success: function (data) {
                if (data.code == 0) {
                    $('#coursecatagory_delconfirm').modal('hide');
                    setTimeout(function () {
                        $('#pageMain').load("/courseCatagory/list/");
                    }, 300);
                } else {
                    alert(data.error);
                }

            }
        });
    }

////添加方法
    function addinfo(infotext, is_hot_active, infoid) {
        $.ajax({
            url: "/ajax/courseCatagory/create/",
            type: "post",
            data: {
                name: infotext,
                careercatagory_id: infoid,
                is_hot_tag: is_hot_active
            },
            success: function (data) {
                if (data.code == 0) {
                    $('#modal_editcoursecatagory').modal('hide');
                    setTimeout(function () {
                        $('#pageMain').load("/courseCatagory/list/");
                    }, 300);
                } else {
                    alert(data.error)
                }
            }
        });
    }

//编辑方法
    function update(updatename, dataid, updateactive, hotactive) {
        $.ajax({
            url: "/ajax/courseCatagory/update/",
            type: "post",
            data: {
                id: dataid,
                name: updatename,
                is_hot_tag: hotactive,
                career_catagory_id: updateactive
            },
            success: function (data) {
                if (data.code == 0) {
                    $('#modal_editcoursecatagory').modal('hide');
                    setTimeout(function () {
                        $('#pageMain').load("/courseCatagory/list/");
                    }, 300);
                } else {
                    alert(data.error)
                }
            }
        });
    }


//动态获取select选项
function dafa() {
    $.ajax({
        url: "/ajax/careerCatagory/get/",
        type: "get",
        async: false,
        success: function (data) {
            var selectinfo = [];
            $.each(data.result, function (id, selectname) {
                selectinfo.push('<option value="' +
                    selectname.id + '">' + selectname.id + ':' + selectname.name + '</option>'
                );
            })
            $("#selectcourseinfo").append(selectinfo.toString());
        }
    })
}

//页码输入框
$("#takepagination").on("change", function () {
    var pagination = $("#takepagination").val();
    $.ajax({
        url: "/ajax/courseCatagory/list/",
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
                courseinfo.push('<td>' + value.career_catagory_id + '</td>');
                courseinfo.push('<td>' + value.name + '</td>');
                courseinfo.push('<td>' + value.is_hot_tag + '</td>');
                courseinfo.push('<td data-id="' + value.id + '" data-name="' + value.name + '" data-active="' + value.is_hot_tag + '" data-career="' + value.career_catagory_id + '">' + '<a href="#" title="查看" class="btn btn-default btn-info btn-sm active show_coursecatagory" data-toggle="modal" data-target="#confirm" style="margin-right:3px;"><i class="glyphicon glyphicon-search" style="margin-right: 3px;"></i>查看</a>' + '<a href="#" title="编辑" class="btn btn-default btn-success btn-sm  active edit_coursetag_info" style="margin-right:3px;"><i class="glyphicon glyphicon-edit" style="margin-right: 3px;"></i>编辑</a>' + '<a href="#" title="删除" class="btn btn-default btn-danger btn-sm active del_this_info" style="margin-right:3px;"><i class="glyphicon glyphicon-trash" style="margin-right: 3px;"></i>删除</a></td></tr>');
            });
            $('#courseTableRow').children().remove();
            $('#courseTableRow').append(courseinfo.toString());
            $('#pagination1').children(".page").removeClass("active");
            $('#pagination1').children(".page").eq(pagination-1).addClass("active");
            if (pagination>data.result.totalPages){
                alert("error")
            }

        }
    })

});


//刷新
$('#btn_articTyperfh').off('click').on('click', function () {
    $('#pageMain').load("/courseCatagory/list/");
    var currtext = $(this).text();
    $("#breadtwo>a").text(currtext);
    $("#breadtwo").show();
});








//验证输入
$(document).ready(function () {
    $('#coursecatagory_form').validate({
        rules: {
            catagoryname: {
                required: true,
                minlength: 2
            },
            catagoryid: {
                required: true
            },
            catagoryactive: {
                required: true
            },
        },
        messages: {
            catagoryname: {
                required: "请键入正确的类目名称",
                minlength: "输入错误"
            },
            catagoryid: {
                required: "至少选择一项"
            },
            catagoryactive: {
                required: "至少选择一项"
            }
        }

    });
});