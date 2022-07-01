$(function(){
    var online_tools_list = [
        {"name": "长跑配速计算器", "url": "https://guohtgo.asuscomm.com:8002/static/online-tools/paceCal.html",},
        {"name": "Vue计算器", "url": "https://guohtgo.asuscomm.com:8002/static/online-tools/calculator.html",},
        {"name": "出校啦！(失效)", "url": "https://guohtgo.asuscomm.com:8002/static/online-tools/GoOut.html",},
    ];

    for(var element of online_tools_list.reverse()){
        if(element.url=="" || element.name==""){
            continue
        }
        $("#online-list").prepend('<div class="layui-col-lg4 layui-col-md4 layui-col-sm6 layui-col-xs12 online-list-li"><a href="'+  element.url +'" target="_blank">'+element.name+'</a></div>');
    }
    
})