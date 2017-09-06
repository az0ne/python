/*
 *  maizi trace code
 */


var trace_server_host = "http://hit.maiziedu.com";

/*
 * 通用打点对象
 */
var maizi_trace = {
    _get_cookie: function(c_name) {
        if (document.cookie.length > 0) {
            var c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) {
                    c_end = document.cookie.length;
                }
                return unescape(document.cookie.substring(c_start, c_end));
            }
        }
        return "";
    },

    del_cookie: function (c_name,exdays) {
        var exdate = new Date();
        exdate.setDate(exdate.getDate() + exdays);
        var c_value = escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
        document.cookie = c_name + "=" + c_value + "; path=/";
    },

    /*
     *  打点方法
     */
    trace: function(obj) {
        $.ajax({
            type: "GET",
            url: trace_server_host + "/action/hit/",
            data: obj,
            dataType: "jsonp",
            jsonp: "callback",
            success: function() {
                console.log("maizi trace succeed. trace_action: " + obj["action_id"]);
           }
       });

       console.log("maizi trace started. trace_action: " + obj["action_id"]);

       return true;
    },

    /*
     *  取pay_type
     */
    pay_type: function() {
        return $("#maizi_trace_common_data #trace_pay_type_common_data").attr("value");
    },

    /*
     *  取user_type
     */
    user_type: function() {
        return $("#maizi_trace_common_data #trace_user_type_common_data").attr("value");
    },

    /*
     *  取career_name
     */
    career_name: function() {
        return $("#maizi_trace_common_data #trace_career_name_common_data").attr("value");
    },

    /*
     *  取taskball_name
     */
    taskball_name: function() {
        return $("#maizi_trace_common_data #trace_taskball_name_common_data").attr("value");
    },

    /*
     *  取video_name
     */
    video_name: function() {
        return $("#maizi_trace_common_data #trace_video_name_common_data").attr("value");
    },

   /*
     *  取video_name
     */
    video_name: function() {
        var login_source = this._get_cookie("login_source");

        return this.cookie
    },

    /*
     *  取suid
     */
    suid: function() {
        return this._get_cookie("maiziuid");
    }
}