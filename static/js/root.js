$(function(){

    $(".box a").mousedown(function(){
        $(this).css({"transform": "translate(2px, 2px)", "box-shadow":"none"})
    })

    $(".box a").mouseup(function(){
        $(this).css({"transform": "none", "box-shadow": "1px 1px 5px rgb(200 200 200)"});
    })

    $(".box a").mouseout(function(){
        $(this).css({"transform": "none", "box-shadow": "1px 1px 5px rgb(200 200 200)"});
    })
        

})
