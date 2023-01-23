// var app_root = 'https://' + location.host +'/tools/';
$(function(){
    $.ajax({
        url:app_root+"ban_ip",
        type:"get",
        dataType:"json",
     }).done(function(msg){
        //console.log(data);
        if(msg.code==200){
            var data = msg.data.ban_ip_list
            var ip_count = data.length;
            var $content = $("#content");
            var html_content = "";
            for(var i=0; i<ip_count;i++){
                var ip = data[i].ip
                var time = data[i].time;
                var loc = data[i].loc;
                //console.log(time, loc);
                html_content+="<li><span class='ip'>"+ip+"</span><span class='time'>"+time+"</span><span class='loc'>"+loc+"</span></li>"
            }
            $content.html(html_content);
        }else{
            layer.msg(msg.msg)
        }
        
     })
      .fail(function(e){
        })
})
