$(function(){
    ratyRemark();
});
function ratyRemark(){
    var ratingStar1 = $('.star-1'),
        ratingStar2 = $('.star-2'),
        oScore = $("#score"),
        textRemark = $('#remark'),
        rated = $('.submitBtn');

    oScore.val('');

    ratingStar1.raty({
        hints: ['1', '2', '3', '4', '5'],
        showHalf:false,
        path: 'http://' + window.location.host + '/images/lps4',
        "click": function (score, evt) {
            oScore.val(score);
        }
    });
    if(serviceScore != 'None'){
        ratingStar2.raty({
            path: 'http://' + window.location.host + '/images/lps4',
            readOnly: true,
            score: serviceScore
        });
    }
    
    
    // textRemark.keyup(function(){
    //     if($(this).val().length > 14){
    //         rated.removeClass('disabled').removeAttr('disabled');
    //     }else{
    //         rated.addClass('disabled').attr('disabled','disabled');
    //     }
    // });
    rated.on('click', function(){
        var ratingBox = $('.rating-box h2'), ratingError;
        if(oScore.val() != ''){
            $.ajax({
                type: "POST",
                url: "/lps4/student_score_meeting/",
                data: {
                    "score": oScore.val(),
                    "comment":textRemark.val(),
                    "meeting_id":service_id
                },
                success: function(data){
                    var ratingBox = $('.rating-box'),
                        html = '<div class="rating-info"><div class="rating-star star-2 textC"></div><div class="remark-box font14">'+textRemark.val()+'</div></div>';
                    if(data.success){
                        $('.rating-error').remove();
                        ratingBox.html(html);
                        $('.star-2').raty({
                            path: 'http://' + window.location.host + '/images/lps4',
                            readOnly: true,
                            score: oScore.val()
                        });
                    }else {
                        ratingError = $('<div class="rating-error font12 textC red" style="margin-top: 20px;">' + data.message + '</div>');
                        $('.rating-error').remove();
                        $('.rating').append(ratingError);
                    }                
                },
                error: function(data){
                    layer.alert(data.success, {
                        skin: 'layui-layer-molv',
                        closeBtn: 0
                    });
                }
            });
            ratingBox.removeAttr('style');
        }else{
            ratingBox.css('color', 'red');
        }        
    });
}