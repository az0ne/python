window.onload = function() {
    // var oDiv = document.getElementById("tab");
    // var oLi = oDiv.getElementsByTagName("div")[0].getElementsByTagName("li");
    // var aCon = oDiv.getElementsByTagName("div")[1].getElementsByTagName("div");
    // var timer = null;
    // for (var i = 0; i < oLi.length; i++) {
    //     oLi[i].index = i;
    //     oLi[i].onclick = function() {
    //         show(this.index);
    //     }
    // }

    qun = document.getElementById("qq");
    wx = document.getElementById("wx");
    icos(qun);
    icos(wx);
    // function show(a) {
    //     index = a;
    //     var alpha = 0;
    //     for (var j = 0; j < oLi.length; j++) {
    //         if(j==2){
    //             oLi[j].className = "";
    //         }else{
    //             oLi[j].className = "buttom-border";
    //         }

    //         aCon[j].className = "";
    //         // aCon[j].style.opacity = 0;
    //         // aCon[j].style.filter = "alpha(opacity=0)";
    //         // aCon[index].style.display = 'none';
    //     }
    //     if(index==2){
    //         oLi[index].className = "cur";
    //     }else{
    //         oLi[index].className = "buttom-border cur";
    //     }
    //     clearInterval(timer);
    //     timer = setInterval(function() {
    //         alpha += 2;
    //         alpha > 100 && (alpha = 100);
    //         // aCon[index].style.opacity = alpha / 100;
    //         // aCon[index].style.filter = "alpha(opacity=" + alpha + ")";
    //         aCon[index].className = "cur";
    //         alpha == 100 && clearInterval(timer);
    //     },
    //     5)
    // }

    function icos(b){
        b.onmousemove = function(){
            if(b.id =='qq'){
                document.getElementById("qun").style.display = "block";
            }else if(b.id =='wx'){
                document.getElementById("ewm").style.display = "block";
            }
        }

        b.onmouseout = function(){
            if(b.id =='qq'){
                document.getElementById("qun").style.display = "none";
            }else if(b.id =='wx'){
                document.getElementById("ewm").style.display = "none";
            }
        }
    }
}