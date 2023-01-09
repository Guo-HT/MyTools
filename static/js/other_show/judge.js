layui.use("layer", function(){
    var layer = layui.layer;
})

window.onload = function(){

    setTimeout(function(){
        if (typeof(killads)=='undefined'){
            // 广告被过滤
            layer.msg("很棒！检测到您安装了广告过滤软件！", {
                icon: 1,
                time: 5000,
            })
        }else{
            layer.msg("检测到您未安装广告过滤软件，建议安装哦！", {
                icon:2,
                time: 5000,
            })
        }
    }, 100)

}

