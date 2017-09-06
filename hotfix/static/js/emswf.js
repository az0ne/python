var FlashPlayer=function(outid,config,flashvars){
    var T=this,
        Dom=document;
    T.id="swf"+new Date().getTime();
    T.outContetid=outid;
    T.flashvars=flashvars;
    var dconfig = {
        bgcolor:"#000000",
        allowscriptaccess:"always",
        wmode:"Opaque",
        width:"100%",
        height:"100%"
    }
    for(var key in config){
        dconfig[key] = config[key];
    }
    T.config  = dconfig;
    dconfig = null;
}
FlashPlayer.prototype = {
    hasFlash:false,
    isIE:navigator.appName.indexOf("Microsoft") != -1,
    playerPlugin:null,
    $E:function(id){
        return  document.getElementById(id);
    },
    playerObject:function(){
        if(this.playerPlugin==null){
            this.playerPlugin=(this.isIE)?this.$E(this.id):document[this.id];
        };
        return this.playerPlugin;
    },
    setPlayer:function(){
        var flashvars="",
            html="";
        for(var k in this.flashvars){
            flashvars+=k+"="+encodeURIComponent(this.flashvars[k])+"&";
        };
        if(this.isIE){
            html="<object id='"+this.id+"' classid='clsid:D27CDB6E-AE6D-11cf-96B8-444553540000'codebase='http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=10' type='application/x-shockwave-flash' width='"+this.config.width+"' height='"+this.config.height+"'><param name='allowFullScreen' value='true'/><param name='movie' value='"+this.config.url+"'/><param name='quality' value='high'/><param name='allowscriptaccess' value='"+ this.config.allowscriptaccess+"'/><param name='bgcolor' value='"+ this.config.bgcolor+"' /><param name='wmode' value='"+ this.config.wmode+"'/><param name='flashvars' value='"+flashvars+"'/></object>";
        }else{
            html="<embed name='"+this.id+"'src='"+this.config.url+"' bgcolor='"+ this.config.bgcolor+"' quality='high' flashvars='"+flashvars+"' pluginspage='http://www.macromedia.com/go/getflashplayer' type='application/x-shockwave-flash' allowscriptaccess='"+ this.config.allowscriptaccess+"' wmode='"+ this.config.wmode+"' width='"+this.config.width+"' height='"+this.config.height+"' allowFullScreen='true'/>";
        }
        return 	html;
    },
    checkFlash:function(){
        if(this.isIE){
            try{
                var swf = new ActiveXObject('ShockwaveFlash.ShockwaveFlash');
                if(swf) {
                    this.hasFlash=true;
                    var  VSwf=swf.GetVariable("$version");
                    this.verison=parseInt(VSwf.split(" ")[1].split(",")[0]);;
                }
            }catch(e){}
        }else{
            try{
                if (navigator.plugins && navigator.plugins.length > 0)
                {
                    var swf=navigator.plugins["Shockwave Flash"];
                    if (swf)
                    {
                        this.hasFlash=true;;
                        var words = swf.description.split(" ");
                        for (var i = 0; i < words.length; ++i)
                        {
                            if (isNaN(parseInt(words[i]))) continue;
                            this.verison=parseInt(words[i]);;
                        }
                    }
                }
            }catch(e){ }
        }
    },
    initialize:function(){
        this.checkFlash();
        if(this.hasFlash){
            this.$E(this.outContetid).innerHTML=this.setPlayer();
            this.playerPlugin=(this.isIE)?this.$E(this.id):document[this.id];
        }else{
            this.$E(this.outContetid).innerHTML="<div style='color:#FFF;padding-top:20px'><a href=' http://www.macromedia.com/go/getflashplayer' target='_blank'>没有发现flashplayer插件，请下载,下载后可以正常观看影片</a></div>"
        }
    }
};