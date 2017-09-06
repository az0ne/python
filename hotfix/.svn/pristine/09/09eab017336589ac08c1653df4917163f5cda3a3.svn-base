/**
 * Created by Administrator on 2016/5/19.
 */

var player;

player = videojs("microohvideo", {
    controls: true,
    playbackRates: [1, 1.25, 1.5, 2]
});


var _isLogin = false;//是否登录
var _isPay = false;//学员是否付费
var _isRemind = false;//是否提醒
var _isFree = false;//课程是否免费
var _isStop = true;//视频是否停止
var _freeTime = 5;//付费视频免费播放时间

var _video_current_time = 0;

function stopPlayer()
{
    player.pause();
    _isStop = true;
}

$(function(){
    //_video_current_time = 来自cookie

    player.ready(function () {
        player.currentTime(_video_current_time);
        player.pause();

        player.on("play", function () {
            _isStop = false;

            if(_isLogin == false && GLOBA_SHOWDIALOG == false)
            {
                stopPlayer();
                login_pop();
                return;
            }

            if(player.currentTime() > _freeTime && _isFree == false && _isPay == false && GLOBA_SHOWDIALOG == false){
                stopPlayer();
                pay_pop();
                return;
            }

            if(_isRemind == true && GLOBA_SHOWDIALOG == false)
            {
                stopPlayer();
                console.log("tixing");
                GLOBA_SHOWDIALOG = true;
                return;
            }

        });

        player.on('timeupdate', function () {

            if(_isLogin==false && GLOBA_SHOWDIALOG == false) {
                stopPlayer();
                login_pop();
                return;
            }
        });


        setInterval(function(){
            if(player.currentTime() > _freeTime && _isStop==false && _isFree == false && _isPay == false && GLOBA_SHOWDIALOG == false){
                stopPlayer();
                pay_pop();
            }
        },1000);

        //全屏
        $(player.L).on('dblclick', function () {
				if (player.isFullscreen()) {
					player.exitFullscreen();
				} else {
					player.requestFullscreen();
				}
        });

    });
});





