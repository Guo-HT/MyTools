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
        }).done(function(data){
            window.location.href = data.pay_url;

        }).fail(function(){

        })
    })
})