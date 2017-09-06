var initGeetest = (function (window, document) {
	var random = function () {
		return parseInt(Math.random() * 10000) + (new Date()).valueOf();
	};
	var callbacks = [];
	var status = "loading";
	// 加载Geetest库
	var cb = "geetest_" + random();
	window[cb] = function () {
		status = "loaded";
		window[cb] = undefined;
		try {
			delete window[cb];
			} catch (e) {
		}
		for (var i = 0, len = callbacks.length; i < len; i = i + 1) {
			callbacks[i]();
		}
	};
	var s = document.createElement("script");
	s.onerror = function () {
		status = "fail";
		for (var i = 0, len = callbacks.length; i < len; i = i + 1) {
			callbacks[i]();
		}
	};
	s.src = (location.protocol === "https:" ? "https:" : "http:") + "//api.geetest.com/get.php?callback=" + cb;
	document.getElementsByTagName("head")[0].appendChild(s);
	return function (config, callback) {
		var protocol = config.https ? "https://" : "http://";
		var initGeetest = function () {
			callback(new window.Geetest(config));
		};
		var backendDown = function () {
			var s = document.createElement("script");
			s.id = "gt_lib";
			s.src = protocol + "static.geetest.com/js/geetest.0.0.0.js";
			s.charset = "UTF-8";
			s.type = "text/javascript";
			head.appendChild(s);
			s.onload = s.onreadystatechange = function () {
				if (!this.readyState || this.readyState === "loaded" || this.readyState === "complete") {
					initGeetest();
					s.onload = s.onreadystatechange = null;
				}
			};
		};
		//alert(status);
		if (status === "loaded") {
			// Geetest对象已经存在，则直接初始化
			initGeetest();
		} else if (status === "fail") {
			// 无法动态获取Geetest库，则去获取geetest.0.0.0.js
			backendDown();
		} else if (status === "loading") {
			// 之前已经去加载Geetest库了，将回调加入callbacks，等Geetest库好后去回调
			callbacks.push(function () {
				if (status === "fail") {
					backendDown();
				} else {
					initGeetest();
				}
			});
		} else {
		}
	};
}(window, document));


window.init = function (config) {
	console.log(config);
	initGeetest({
		gt: config.gt,
		challenge: config.challenge,
		product: "embed",
		width: "556px",
		offline: !config.success
	}, function (obj) {
		// alert(obj)
		window.o = obj;
		// alert('append before')
		o.appendTo($("#captcha"));
		 //alert('append end')
		o.onReady(function () {
			//$("#captcha").firstChild.addEventListener("click", function (e) {
			//	e.stopPropagation();
			//});
		});
        o.onFail(function(){
            o.refresh
        });
		o.onSuccess(function () {
		    alert("onSuccess");
			validate(o, function (result) {
			    console.log(result);
				if (result === "success") {
					console.log("成功")
				} else {
					o.refresh();
				}
			});
		});
	});
};
var validate = function (captcha, cb) {
	var values = captcha.getValidate();
//	var query = "geetest_challenge=" + values.geetest_challenge + "&geetest_validate=" + values.geetest_validate + "&geetest_seccode=" + values.geetest_seccode;
	var query = "geetest_challenge=" + values.geetest_challenge + "&geetest_validate=" + values.geetest_validate + "&geetest_seccode=" + values.geetest_seccode + "&callback=handlerResult";
        var script = document.createElement("script");
        script.src = "http://webapi.geetest.com/apis/mobile-server-validate/?" + query;
        script.charset = "utf-8";
        document.body.appendChild(script);
	var data={
	            geetest_challenge:values.geetest_challenge,
	            geetest_validate:values.geetest_validate,
	            geetest_seccode:values.geetest_seccode,

				};
	$.ajax({
		url:'/geetest/validate/',
		data:data,
		type:'post',
		dataType:'json',
		success:function(msg){
		    var data = eval('(' + msg + ')');
		    alert(data.status);
			if(data.status=='success'){
				console.log("成功~");
			}else{
				o.refresh();
			}
		}
	})
	window.handlerResult = cb;
};
var script = document.createElement("script");
    script.src = "http://webapi.geetest.com/apis/start-mobile-captcha/?callback=init";
    script.charset = "utf-8";
    document.body.appendChild(script);
