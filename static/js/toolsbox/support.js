$(function(){
    // var app_root = 'https://' + location.host +'/tools/';
    
    $("#support").click(function(){
        
        $.ajax({
            url:app_root+"put_order",
            type:"post",
            dataType:"json",
            data: {
                "support_id": "0",
            },
            headers:{
                "X-CSRFToken": get_csrf_token(),
            }
        }).done(function(msg){
            if(msg.code==200){
                var data = msg.data
                window.location.href = data.pay_url;
            }else{
                layer.msg(msg.msg)
            }

        }).fail(function(){

        })
    })
})