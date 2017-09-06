seajs.config({
    base:"/js/lib/",
    alias:{
        "jquery"      :"jquery/jquery/1.11.3/jquery.js",
        "bootstrap"   :"jquery/bootstrap/js/bootstrap.min.js",
        "bootstrapCss":"jquery/bootstrap/css/bootstrap.min.css",
        "textFiltered":"jquery/textFiltered.js",
        "function"    :"../../common/function.js",
        'superSlide'  :"jquery/jquery.SuperSlide.2.1.1.js"
    },
    map: [
        [ /^(.*\.(?:css|js|tpl))(.*)$/i, '$1?'+seajsTimestamp ]
    ],
    preload: ['jquery', 'superSlide']
});