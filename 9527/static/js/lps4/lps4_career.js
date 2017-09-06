/**
 * Created by Administrator on 2016/9/21 0021.
 */


        $(document).ready(function () {
            var ad_url = $("#ad_url").val();
            if(ad_url==""){
                $(".image_show").css("display", "none")
            }
            $("#upload").click(function () {
                $("#upload").on("change", function () {
                    var objUrl = getObjectURL(this.files[0]);  //获取图片的路径，该路径不是图片在本地的路径
                    if (objUrl) {
                        $("#pic").attr("src", objUrl);      //将图片路径存入src中，显示出图片
                        getBackImgSize();
                        $(".image_show").css("display", "inline");
                    }
                });
            });
            getBackImgSize();  // 获取图片尺寸
            select_ad_type();  // 更改广告类型时的样式操作
            form_validate()
        })


// *********************以下为各个功能函数******************************
        var form_validate=function () {
            $("#careerForm").validate({   // 表单验证
                rules: {
                    careerId: {
                        required: true,
                        digits: true
                    },
                    careerName: {
                        required: true
                    },
                    short_name: {
                        required: true
                    },
                    careerType: {
                        required: true
                    },
                    adType: {
                        required: true
                    },
                    url: {
                        required: true
                    },
                    video_url: {
                        required: true
                    },
                    old_price: {
                        required:true,
                        min:0.1
                    },
                    price: {
                        required:true,
                        min:0.1
                    },
                    description:{
                        required:true
                    },
                    jobless_price:{
                        required:true,
                        min:0.1
                    },
                },
                messages: {
                    careerId: {
                        required: "请输入课程ID"
                    },
                    careerName: {
                        required: "请输入课程名称"
                    },
                     short_name: {
                        required: "请输入课程简称"
                    },
                    careerType: {
                        required: "请选择课程类型"
                    },
                    adType: {
                        required: "请选择广告类型"
                    },
                    url: {
                        required: "请输入图片广告跳转链接"
                    },
                    video_url: {
                        required: "请输入视频地址"
                    },
                    old_price: {
                        required: "请输入市场价格",
                        min:"价格必须大于0"
                    },
                    price: {
                        required: "请输入麦子价格",
                        min:"价格必须大于0"
                    },
                    description:{
                        required:"请输入课程描述"
                    },
                    jobless_price:{
                        required:"请输入非就业价格",
                        min:"价格必须大于0"
                    },
                }
            })
        }


        var select_ad_type = function () {
            var type = $("#select_ad_type").val();
            if (type == "IMAGE") {
                $(".video_url").css("display", "none");
                $("#video_url").prop("disabled", true);
                $(".image_ad").css("display", "block")
            }
            else {
                $(".video_url").css("display", "block");
                $("#video_url").prop("disabled", false);
                $(".image_ad").css("display", "none")
            }
            $("#select_ad_type").change(function () {
                select_ad_type();
            });
        }


        function getObjectURL(file) {  //建立一個可存取到該file的url
            var url = null;
            if (window.createObjectURL != undefined) { // basic
                url = window.createObjectURL(file);
            } else if (window.URL != undefined) { // mozilla(firefox)
                url = window.URL.createObjectURL(file);
            } else if (window.webkitURL != undefined) { // webkit or chrome
                url = window.webkitURL.createObjectURL(file);
            }
            return url;
        }

        //获取上传列表图片的尺寸
        function getBackImgSize() {
            var img = new Image();
            img.src = $('#pic').attr('src');
            img.onload = function () {  // 等待图片加载完后，才能获取到图片的信息
                $('#img_width').text(img.width);
                $('#img_height').text(img.height);
            }

        }

        function check_submit(req_width, req_height) {
            var width = $("#img_width").text();
            var height = $("#img_height").text();
            if ((width == req_width && height == req_height) || (width == 0 && height == 0)) {
                check_short_name();
            }
            else {
                layer.msg("图片尺寸必须为{0}*{1}！".format(req_width, req_height));
            }
        }

        var check_short_name = function () {  // 检查课程简称是否已存在
            var short_name = $("#careerShortName").val()
            var career_id = $("#careerId").val()
            var action = $("#lps4_career_action").val()
            $.ajax({
                type: 'GET',
                url: "/lps4/career/sn_check/",
                data: {short_name: short_name,id:career_id, action:action},
                dateType: "json",
                success: function (data) {
                    if (data.status == "success") {
                        if(data.is_had){
                            layer.alert("该简称已存在！");
                        }
                        else{
                            $("#careerForm").submit(); // 提交表单
                        }
                    }
                    else{
                        layer.alert(data.msg);
                    }
                },
            });
        }

        function goback() {  //返回
            history.go(-1)
        }