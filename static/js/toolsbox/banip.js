// var app_root = 'https://' + location.host +'/tools/';
$(function(){
    $.ajax({
        url:app_root+"ban_ip",
        type:"get",
        dataType:"json",
     }).done(function(data){
        //console.log(data);
        var ip = data["data"];
        var ip_count = ip.length;
        //console.log(ip);
        var $content = $("#content");
        var html_content = "";
        for(var i=0; i<ip_count;i++){
            //console.log(ip[i])
            var time = ip[i][1].split("\t")[0];
            var loc = ip[i][1].split("\t")[1];
            //console.log(time, loc);
            html_content+="<li><span class='ip'>"+ip[i][0]+"</span><span class='time'>"+time+"</span><span class='loc'>"+loc+"</span></li>"
        }
        $content.html(html_content);
     })
      .fail(function(e){
        })
})
