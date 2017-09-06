/**
 * Created by Administrator on 2016/6/3.
 */
$(function () {
    captcha(".teacherRecruitForms .captcha");
    $(".submitBtn").click(function () {
        /*
         * 讲师类型、编制类型、工作年限单选按钮提示
         * $lecturerTypeVal讲师类型Value值
         * $formationVal编制类型Value值
         * $workingLifeVal工作年限Value值
         */
        var $lecturerTypeVal, $formationVal, $workingLifeVal, $lecturerTypeTips, $formationTips, $workingLifeTips;
        $lecturerTypeVal = $('.teacherRecruitForms input:radio[name="lecturerType"]:checked').val();
        $formationVal = $('.teacherRecruitForms input:radio[name="formation"]:checked').val();
        $workingLifeVal = $('.teacherRecruitForms input:radio[name="workingLife"]:checked').val();
        $lecturerTypeTips = $(".teacherRecruitFormLecturerTypeTips");
        $formationTips = $(".teacherRecruitFormFormationTips");
        $workingLifeTips = $(".teacherRecruitFormWorkingLifeTips");

        teacherRecruitFormsRadio($lecturerTypeVal, $lecturerTypeTips, $('.teacherRecruitForms input:radio[name="lecturerType"]'));//讲师类型
        teacherRecruitFormsRadio($formationVal, $formationTips, $('.teacherRecruitForms input:radio[name="formation"]'));//编制类型
        teacherRecruitFormsRadio($workingLifeVal, $workingLifeTips, $('.teacherRecruitForms input:radio[name="workingLife"]'));//工作年限
        function teacherRecruitFormsRadio(vals, tips, inputs) {
            if (vals == null) {
                tips.show();
                inputs.click(function () {
                    tips.hide();
                });
            } else {
                tips.hide();
            }
        };

        /*文本框与文本域的提示文字控制*/

        /**
         * 真实名字下的标签定义
         * $teacherRecruitName是input按钮
         * $teacherRecruitNameTips提示文字
         * $teacherRecruitNameTips错误文字
         * teacherRecruitNameVal按钮文字长度
         */
        var $teacherRecruitName, $teacherRecruitNameTips, $teacherRecruitNameTips, teacherRecruitNameVal;
        $teacherRecruitName = $(".teacherRecruitName");
        $teacherRecruitNameTips = $(".teacherRecruitNameTips");
        teacherRecruitNameError = $(".teacherRecruitNameError");
        teacherRecruitNameVal = $teacherRecruitName.val().length;
        if (teacherRecruitNameVal == 0) {
            $teacherRecruitNameTips.show();
            $teacherRecruitName.addClass("error");
            $teacherRecruitName.focus(function () {
                $teacherRecruitNameTips.hide();
                $(this).removeClass("error");
            });
        } else if (teacherRecruitNameVal > 20) {
            teacherRecruitNameError.show();
            $teacherRecruitName.addClass("error");
            $teacherRecruitName.focus(function () {
                teacherRecruitNameError.hide();
                $(this).removeClass("error");
            });
        }

        /**
         * 技术方向下的标签定义
         * $teacherRecruitSkill是input按钮
         * $teacherRecruitSkillTips提示文字
         * $teacherRecruitSkillError错误文字
         * teacherRecruitSkillVal按钮文字长度
         */
        var $teacherRecruitSkill, $teacherRecruitSkillTips, $teacherRecruitSkillError, teacherRecruitSkillVal;
        $teacherRecruitSkill = $(".teacherRecruitSkill");
        $teacherRecruitSkillTips = $(".teacherRecruitSkillTips");
        $teacherRecruitSkillError = $(".teacherRecruitSkillError");
        teacherRecruitSkillVal = $teacherRecruitSkill.val().length;
        if (teacherRecruitSkillVal == 0) {
            $teacherRecruitSkillTips.show();
            $teacherRecruitSkill.addClass("error");
            $teacherRecruitSkill.focus(function () {
                $teacherRecruitSkillTips.hide();
                $(this).removeClass("error");
            });
        } else if (teacherRecruitSkillVal > 30) {
            $teacherRecruitSkillError.show();
            $teacherRecruitSkill.addClass("error")
            $teacherRecruitSkill.focus(function () {
                $teacherRecruitSkillError.hide();
                $(this).removeClass("error");
            });
        }

        /**
         * 个人简介下的标签定义
         * $teacherRecruitTextArea是input按钮
         * $teacherRecruitTextAreaTips提示文字
         * $teacherRecruitTextAreaError1错误文字1
         * $teacherRecruitTextAreaError2错误文字2
         * teacherRecruitTextAreaVal按钮文字长度
         */
        var $teacherRecruitTextArea, $teacherRecruitTextAreaTips, $teacherRecruitTextAreaError1, $teacherRecruitTextAreaError2, teacherRecruitTextAreaVal;
        $teacherRecruitTextArea = $(".teacherRecruitTextArea");
        $teacherRecruitTextAreaTips = $(".teacherRecruitTextAreaTips");
        $teacherRecruitTextAreaError1 = $(".teacherRecruitTextAreaError1");
        $teacherRecruitTextAreaError2 = $(".teacherRecruitTextAreaError2");
        teacherRecruitTextAreaVal = $teacherRecruitTextArea.val().length;
        if (teacherRecruitTextAreaVal == 0) {
            $teacherRecruitTextAreaTips.show();
            $teacherRecruitTextArea.focus(function () {
                $teacherRecruitTextAreaTips.hide();
            });
        } else if (teacherRecruitTextAreaVal < 50) {
            $teacherRecruitTextAreaError1.show();
            $teacherRecruitTextArea.focus(function () {
                $teacherRecruitTextAreaError1.hide();
            });
        } else if (teacherRecruitTextAreaVal > 1000) {
            $teacherRecruitTextAreaError2.show();
            $teacherRecruitTextArea.focus(function () {
                $teacherRecruitTextAreaError2.hide();
            });
        }

        var regPhone, phone_Flag;//手机号码的验证正则定义
        /**
         * 电话号码下的标签定义
         * $teacherRecruitPhone是input按钮
         * $teacherRecruitPhoneTips提示文字
         * $teacherRecruitPhoneError错误文字
         * teacherRecruitPhoneVal按钮文字长度
         */
        var $teacherRecruitPhone, $teacherRecruitPhoneTips, $teacherRecruitPhoneError, teacherRecruitPhoneVal;
        $teacherRecruitPhone = $(".teacherRecruitPhone");
        $teacherRecruitPhoneTips = $(".teacherRecruitPhoneTips");
        $teacherRecruitPhoneError = $(".teacherRecruitPhoneError");
        regPhone = /^0?1[3|4|5|7|8][0-9]\d{8}$/;
        phone_Flag = regPhone.test($teacherRecruitPhone.val());
        teacherRecruitPhoneVal = $teacherRecruitPhone.val().length;
        if (teacherRecruitPhoneVal == 0) {
            $teacherRecruitPhoneTips.show();
            $teacherRecruitPhone.addClass("error")
            $teacherRecruitPhone.focus(function () {
                $teacherRecruitPhoneTips.hide();
                $(this).removeClass("error");
            });
        } else if (!phone_Flag) {
            $teacherRecruitPhoneError.show();
            $teacherRecruitPhone.addClass("error")
            $teacherRecruitPhone.focus(function () {
                $teacherRecruitPhoneError.hide();
                $(this).removeClass("error");
            });
        }

        /**
         * QQ下的标签定义
         * $teacherRecruitQQ是input按钮
         * $teacherRecruitQQTips提示文字
         * $teacherRecruitQQError错误文字
         * teacherRecruitQQVal按钮文字长度
         */
        var $teacherRecruitQQ, $teacherRecruitQQTips, $teacherRecruitQQError, teacherRecruitQQVal;
        $teacherRecruitQQ = $(".teacherRecruitQQ");
        $teacherRecruitQQTips = $(".teacherRecruitQQTips");
        $teacherRecruitQQError = $(".teacherRecruitQQError");
        teacherRecruitQQVal = $teacherRecruitQQ.val().length;
        if (teacherRecruitQQVal == 0) {
            $teacherRecruitQQTips.show();
            $teacherRecruitQQ.addClass("error")
            $teacherRecruitQQ.focus(function () {
                $teacherRecruitQQTips.hide();
                $(this).removeClass("error");
            });
        } else if (teacherRecruitQQVal < 5 || teacherRecruitQQVal > 11 || isNaN($teacherRecruitQQ.val())) {
            $teacherRecruitQQError.show();
            $teacherRecruitQQ.addClass("error")
            $teacherRecruitQQ.focus(function () {
                $teacherRecruitQQError.hide();
                $(this).removeClass("error");
            });
        }

        if (!$(".teacherRecruitForms .gt_ajax_tip").hasClass("success")) {
            $(".teacherRecruitCapchaTips").show();
        } else {
            $(".teacherRecruitCapchaTips").hide();
        }

        //判断表单是否验证通过，通过即提交，不通过无法提交
        var ajax_submit=true;
        $(".teacherRecruitForms li em,.teacherRecruitForms li .error").each(function(){
            switch($(this).css("display")) {
                case "inline":
                    ajax_submit=false;
                    break;
            }
        });
        if(ajax_submit){
           submit_teacher_recruit($("#teacherRecruitForms").serialize());
        }

    });

    /**
     * 提交成功
     */
    //$(".teacherRecruitFormSuccess").show();

    /**
     * 提交失败
     */
    //$(".teacherRecruitFormError").show();


    /*
     * 重新提交
     */
    $(".teacherRecruitFormError .tj").click(function () {
        $(".teacherRecruitFormFlow strong:last-child").removeClass("active");
        $(".teacherRecruitFormSubmit").removeClass("active");
        $(".teacherRecruitFormWrite").addClass("active");
        $(".teacherRecruitForms .captcha").text('');
        captcha(".teacherRecruitForms .captcha");
    });

       /*
     *单选按钮点击；
     * lecturerType讲师类型，formation讲师编制，workingLife工作年限；
     * dkjs带课老师，lkjs录课老师，jzjs兼职老师，qzjs全职老师
     */
    $(".teacherRecruitForms input[name=lecturerType]").click(function(){
        switch($(".teacherRecruitForms input[name=lecturerType]:checked").attr("id")) {
            case "dkjs":
                $(this).parent(".radioBtn").addClass("active").siblings().removeClass("active");
                $(".teacherRecruitForms #qzjs").removeAttr("disabled").parent(".radioBtn").removeClass("disable");
                break;
            case "lkjs":
                $(this).parent(".radioBtn").addClass("active").siblings().removeClass("active");
                $(".teacherRecruitForms #jzjs").attr("checked","checked").parent(".radioBtn").addClass("active");
                $(".teacherRecruitForms #qzjs").attr("disabled","disabled").parent(".radioBtn").addClass("disable");
                $(".teacherRecruitFormFormationTips").hide();
                break;
        }
    });
    $(".teacherRecruitForms input[name=formation]").click(function(){
        switch($(".teacherRecruitForms input[name=formation]:checked").attr("id")) {
            case "jzjs":
                $(this).parent(".radioBtn").addClass("active").siblings().removeClass("active");
                $(".teacherRecruitForms #lkjs").removeAttr("disabled").parent(".radioBtn").removeClass("disable");
                break;
            case "qzjs":
                $(this).parent(".radioBtn").addClass("active").siblings().removeClass("active");
                $(".teacherRecruitForms #lkjs").attr("disabled","disabled").parent(".radioBtn").addClass("disable");
                break;
        }
     });
    $(".teacherRecruitForms input[name=workingLife]").click(function(){
        $(this).parent(".radioBtn").addClass("active").siblings().removeClass("active");
     });
});

function submit_display(ret){
    $(".teacherRecruitFormWrite").removeClass("active");
    $(".teacherRecruitFormSubmit,.teacherRecruitFormFlow strong:last-child").addClass("active");
    if(ret){
        $(".teacherRecruitFormSuccess").show();
        $(".teacherRecruitFormError").hide();
    }
    else{
        $(".teacherRecruitFormSuccess").hide();
        $(".teacherRecruitFormError").show();
    }
}
function submit_teacher_recruit(data) {
    data['geetest_challenge'] = $('#teacherRecruitForms .geetest_challenge').attr('value');
    data['geetest_validate'] = $('#teacherRecruitForms .geetest_challenge').attr('value');
    data['geetest_seccode'] = $('#teacherRecruitForms .geetest_challenge').attr('value');

    $.ajax({
        type: 'POST',
        url: '/common/ajax/teacher_recruit_form/',
        data: data,
        dataType: "json",
        success: function (data_msg) {
            if (data_msg['status']) {
                submit_display(true);

            }
            else {
                $("#error_msg").text(data_msg['msg']);
                submit_display(false);

            }
        }
    });
};
