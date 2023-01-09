$(function(){

    const page_limit = 12
    var online_tools_list = [
        {"name": "EQP人格测试", "url": "https://guohtgo.asuscomm.com:8002/static/online-tools/EPQ_test.html",},
        {"name": "长跑配速计算器", "url": "https://guohtgo.asuscomm.com:8002/static/online-tools/paceCal.html",},
        {"name": "Vue计算器", "url": "https://guohtgo.asuscomm.com:8002/static/online-tools/calculator.html",},
        {"name": "出校啦！(失效)", "url": "https://guohtgo.asuscomm.com:8002/static/online-tools/GoOut.html",},
        {"name": "Shodan Search Engine", "url":"https://www.shodan.io/"},
        {"name": "国家信息安全漏洞库", "url":"http://www.cnnvd.org.cn/"},
//        {"name": "红黑联盟论坛", "url":"https://bbs.2cto.com/"},
        {"name": "世界中文黑客论坛", "url":"https://www.cnhackteam.org/"},
        {"name": "i春秋【专注网络安全】", "url":"https://www.ichunqiu.com/"},
        {"name": "强大的多功能在线工具库", "url":"http://tools.bugscaner.com/"},
        {"name": "强大的多功能在线工具", "url":"http://tools.bugscaner.com/"},
        {"name": "多地区ping", "url":"https://ping.chinaz.com/"},
        {"name": "DNS-info", "url":"https://viewdns.info/"},
        {"name": "小迪渗透吧", "url":"http://www.xiaodi8.com/"},
        {"name": "🔰雨苁ℒ🔰", "url":"https://www.ddosi.org/"},
        {"name": "蚂蚁安全", "url":"https://www.mayisafe.cn/"},
        {"name": "ASCII TOOL", "url":"https://www.wishingstarmoye.com/tools/ascii"},
        {"name": "知道创宇Seebug漏洞平台", "url":"https://www.seebug.org/"},
        {"name": "DNS-Log", "url":"http://www.dnslog.cn/"},
        {"name": "WooYun公开漏洞查询", "url":"https://wooyun.website/"},
        {"name": "照片转签名", "url":"https://www.fococlipping.com/"},
        {"name": "随机数据生成", "url":"https://www.mockaroo.com/#tab_all"},
        {"name": "Z-Library数字图书馆", "url":"https://zh.libsolutions.net/"},
        {"name": "arXiv - 论文预印本", "url":"https://arxiv.org/"},
        {"name": "", "url":""},
        {"name": "", "url":""},
        {"name": "", "url":""},
        {"name": "", "url":""},
        {"name": "", "url":""},
        {"name": "", "url":""},
        {"name": "", "url":""},
        {"name": "", "url":""},
    ];

    slice_show_tools_in_page(1)

    function slice_show_tools_in_page(cur_page){
        // console.log((cur_page-1)*page_limit, cur_page*page_limit-1)
        var content_ok_count = 0
        var html = ""
        for(var element of online_tools_list.slice((cur_page-1)*page_limit, cur_page*page_limit)){
            if(element.url=="" || element.name==""){
                continue
            }
            html+=('<div class="layui-col-lg4 layui-col-md4 layui-col-sm6 layui-col-xs12 online-list-li"><a href="'+  element.url +'" target="_blank">'+element.name+'</a></div>');
        }
        $("#online-list").html(html);

        for(var element of online_tools_list){
            if(element.url=="" || element.name==""){
                continue
            }
            content_ok_count+=1
        }

        layui.use("laypage", function () {
            console.log(content_ok_count)
            var laypage = layui.laypage;
            laypage.render({
                elem: 'page-nav' //注意，这里的 test1 是 ID，不用加 # 号
                , count: content_ok_count //有效数据总数
                , limit: page_limit
                , curr: cur_page
                , jump: function (obj, first) {
                    //首次不执行
                    if (!first) {
                        slice_show_tools_in_page(obj.curr);
                    }
                },
                layout: ['prev', 'page', 'next', 'count'],
            });
        })
    }
    

    

})
