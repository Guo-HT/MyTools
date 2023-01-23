$(function () {

    layui.use("layer", function () {
        var layer = layui.layer;
    })

    var paramsStr = window.location.search
    var params = new URLSearchParams(paramsStr)
    var page = params.get('p') ? params.get('p') : 1; // list

    // 获取页面信息并显示
    function ajax_get_tools_in_page(to_page, page_size) {
        $.ajax({
            type: "get",
            url: app_root + 'get_tools',
            dataType: "json",
            data: {
                // "csrfmiddlewaretoken": get_csrf_token(),
                "group": to_page,
                "page_size": page_size,
            },
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        })
            .success(function (msg) {
                if (msg.code == 200) {
                    var data = msg.data;
                    page_count = data.total_page;
                    var total_count = data.total_count;
                    var page_cur = data.cur_page;
                    var tool_info_json = data.tool_list;
                    var media_url = data.media_url;
                    var $tools_show = $("#tool-list");
                    if (to_page > page_count) {
                        alert("页数超出，请检查输入！");
                        return;
                    }
                    $("#jump_label").text(page_count);
                    //清空当前所有元素
                    $tools_show.html('');
                    // 将工具数据写入页面
                    $.each(tool_info_json, function (index, object) {
                        // 创建div对象
                        var oDiv = document.createElement('div');
                        // 将html写入
                        oDiv.innerHTML = object.tool_intro;
                        // 提取文本
                        var text = oDiv.innerText;
                        text = text.replace(/ /ig, "");
                        text = text.replace(/&nbsp;/ig, "8");
                        // 写入
                        var each_content = '<div class="layui-col-lg4 layui-col-md6 layui-col-sm6 layui-col-xs12 each-card">' +
                            '<a href="' + app_root + "tool_detail/" + object.tool_id + '" title="' + object.tool_name + '" target="_blank"><div class="card-img"><img src="' + media_url + object.tool_img_path + '" alt="图片" />' +
                            '</div><div class="info"><h3>' + object.tool_name + '</h3><p class="summary">' + text + '</p></div></a></div>';
                        $tools_show.html($tools_show.html() + each_content);
                    })
                    layui.use("laypage", function () {
                        var laypage = layui.laypage;
                        laypage.render({
                            elem: 'page-nav' //注意，这里的 test1 是 ID，不用加 # 号
                            , count: total_count //数据总数，从服务端得到
                            , limit: data.limit
                            , limits: [12, 24, 36, 48]
                            , curr: page_cur
                            , jump: function (obj, first) {
                                //obj包含了当前分页的所有参数，比如：
                                // console.log(obj.curr); //得到当前页，以便向服务端请求对应页的数据。
                                // console.log(obj.limit); //得到每页显示的条数
                                //首次不执行
                                if (!first) {
                                    //do something
                                    history.pushState({}, null, location.origin + location.pathname + "?p=" + obj.curr);
                                    ajax_get_tools_in_page(obj.curr, obj.limit);
                                }
                            },
                            layout: ['prev', 'page', 'next', 'count', "limit"],
                        });
                    })
                }else{
                    layer.msg(msg.msg)
                }
            })
            .fail(function () {
                layer.msg("获取数据失败");
                // window.location.reload();
            })
    }

    // 调用后，直接获取第一页
    ajax_get_tools_in_page(page, 12);


})
