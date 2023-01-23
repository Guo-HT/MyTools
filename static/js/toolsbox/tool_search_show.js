$(function () {
    var key_words = window.location.pathname.slice(19);
    // 搜索
    function get_search_tools(page) {
        $("#search-content").css({"display": "none"});
        $.ajax({
            type: 'get',
            url: app_root + 'get_search_tool',
            dataType: 'json',
            data: {
                'from_url': key_words,
                'to_page': page,
            },
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        }).done(function (msg) {
            $("#search-content").css({"display": "block"});
            $(".loading-div").css({"display":"none"});
            console.log(msg);
            if (msg.code==200){
                data = msg.data
                // 获取解析数据
                var key_str = data.key_str;
                var html_content = '';
                var i = 0;
                $("#search-key").text(key_str);
                // 构造内容
                $.each(data.tool_data, function (index, object) {
                    // 创建div对象
                    var oDiv = document.createElement('div');
                    // 将html写入
                    oDiv.innerHTML = object.tool_describe;
                    // 提取文本
                    var text = oDiv.innerText;
                    text = text.replace(/ /ig, "");
                    text = text.replace(/&nbsp;/ig, "8");
                    html_content+='<li class="search-result-li"><a href="/tools/tool_detail/'+ object.tool_id +'">'+
                    '<img src="/upload_files/'+ object.tool_icon +'" alt="图片" class="tool-img" title="'+object.tool_name+'"/>'+
                    '<span class="tool-name">'+object.tool_name+'</span><span class="tool-describe">' + text +'</span></a></li>';
                })
                
                // 写入
                $(".search-result-ul").html(html_content);
                layui.use("laypage", function(){
                    var laypage = layui.laypage;
                    laypage.render({
                        elem: 'search-page-nav' //注意，这里的 test1 是 ID，不用加 # 号
                        , count: data.total_count //数据总数，从服务端得到
                        , limit: data.limit
                        , curr: data.to_page
                        , jump: function (obj, first) {
                            //obj包含了当前分页的所有参数，比如：
                            // console.log(obj.curr); //得到当前页，以便向服务端请求对应页的数据。
                            // console.log(obj.limit); //得到每页显示的条数
                            //首次不执行
                            if (!first) {
                                //do something
                                // history.pushState({}, null, location.origin + location.pathname +"?p=" +obj.curr);
                                get_search_tools(obj.curr);
                            }
                        },
                        layout: ['prev', 'page', 'next', 'count'],
                    });
                })
            }else{
                layer.msg("请求失败！");
            }
        })
    }
    // 默认获取第一页搜索结果
    get_search_tools(1);
})
