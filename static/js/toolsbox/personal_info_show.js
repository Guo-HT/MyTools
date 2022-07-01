$(function () {
    var user_name = window.location.pathname.slice(16);

    // 获取个人信息
    function get_per_info() {
        $.ajax({
            url: app_root + "get_personal_info",
            dataType: "json",
            type: 'get',
            data: {
                "from_url": user_name,
            },
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        }).done(function (data) {
            console.log(data);
            // 写入表单
            $("#user-id").val(data.id);
            $("title").text(data.user_name + "的个人主页");
            $("#user-name").val(data.user_name);
            // $("#user-passwd").val(data.user_password);  // 此处密码会在源码处外泄
            $("#user-email").val(data.user_email);
            $("#user-real-name").val(data.user_real_name);
            $("#user-reg-time").val(data.user_reg_time);
        })
    }
    get_per_info();


    //点击浏览记录 start
    $("#tab-title").children().eq(1).click(function () {
        get_browser_history(1);
    })
    //点击浏览记录 end

    function get_browser_history(page) {
        // 请求浏览历史
        $.ajax({
            url: app_root + 'get_browser_history',
            type: 'get',
            dataType: 'json',  // JsonResponse这垃圾玩意发不出来json数组
            data: {
                "from": user_name,
                "page":page,
            },
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        })
            .done(function (data) {  // 请求成功
                
                var html_content = "";
                $.each(data.history_list, function (index, object) {
                    html_content += '<li class="layui-col-lg6 layui-col-md6 layui-col-sm12 layui-col-xs12 history-li"><a href="/tools/tool_detail/' + object.tool_id + '" target="_blank">' +
                        '<img src="/upload_files/' + object.tool_icon + '" alt="图片" class="tool-img" title="' + object.tool_name + '"/>' +
                        '<span class="tool-name">' + object.tool_name + '</span><span class="tool-time">' + object.history_time + '</span></a></li>';
                })

                // 写入
                $("#tab-item-watch").html(html_content);

                layui.use("laypage", function () {
                    var laypage = layui.laypage;
                    laypage.render({
                        elem: 'watch-page-nav' //注意，这里的 test1 是 ID，不用加 # 号
                        , count: data.total_count //数据总数，从服务端得到
                        , limit: data.limit
                        , curr: parseInt(data.cur_page)
                        , jump: function (obj, first) {

                            //首次不执行
                            if (!first) {
                                get_browser_history(obj.curr);
                            }
                        },
                        layout: ['prev', 'page', 'next', 'count'],
                    });
                })
                
            })
            .fail(function () {  // 请求失败
                alert("浏览历史请求错误！");
            })
    }


    //点击上传记录 start
    $("#tab-title").children().eq(2).click(function () {
        get_upload_history(1);
    })
    //点击上传记录 end

    function get_upload_history(page) {
        // 请求上传记录
        $.ajax({
            url: app_root + 'get_upload_history',
            type: 'get',
            dataType: 'json',  // JsonResponse这垃圾玩意发不出来json数组
            data: {
                "from": user_name,
                "page": page,
            },
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        })
            .done(function (data) {  // 请求成功

                var html_content = "";
                $.each(data.upload_list, function (index, object) {
                    html_content += '<li class="layui-col-lg6 layui-col-md6 layui-col-sm12 layui-col-xs12 history-li"><a href="/tools/tool_detail/' + object.tool_id + '" target="_blank">' +
                        '<img src="/upload_files/' + object.tool_icon + '" alt="图片" class="tool-img" title="' + object.tool_name + '"/>' +
                        '<span class="tool-name">' + object.tool_name + '</span><span class="tool-time">' + object.upload_time + '</span></a></li>';
                })

                // 写入
                $("#tab-item-upload").html(html_content);

                layui.use("laypage", function () {
                    var laypage = layui.laypage;
                    laypage.render({
                        elem: 'upload-page-nav' //注意，这里的 test1 是 ID，不用加 # 号
                        , count: data.total_count //数据总数，从服务端得到
                        , limit: data.limit
                        , curr: parseInt(data.cur_page)
                        , jump: function (obj, first) {

                            //首次不执行
                            if (!first) {
                                get_upload_history(obj.curr);
                            }
                        },
                        layout: ['prev', 'page', 'next', 'count'],
                    });
                })

            })
            .fail(function () {  // 请求失败
                alert("上传历史请求错误");
            })
    }


    //点击下载记录 start
    $("#tab-title").children().eq(3).click(function () {
        get_download_history(1);
    })
    //点击下载记录 end

    function get_download_history(page) {
        // 请求下载记录
        $.ajax({
            url: app_root + 'get_download_history',
            type: 'get',
            dataType: 'json',  // JsonResponse这垃圾玩意发不出来json数组
            data: {
                "from": user_name,
                "page": page,
            },
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        })
            .done(function (data) {  // 请求成功

                var html_content = "";
                $.each(data.download_list, function (index, object) {
                    html_content += '<li class="layui-col-lg6 layui-col-md6 layui-col-sm12 layui-col-xs12 history-li"><a href="/tools/tool_detail/' + object.tool_id + '" target="_blank">' +
                        '<img src="/upload_files/' + object.tool_icon + '" alt="图片" class="tool-img" title="' + object.tool_name + '"/>' +
                        '<span class="tool-name">' + object.tool_name + '</span><span class="tool-time">' + object.download_time + '</span></a></li>';
                })

                // 写入
                $("#tab-item-download").html(html_content);

                layui.use("laypage", function () {
                    var laypage = layui.laypage;
                    laypage.render({
                        elem: 'download-page-nav' //注意，这里的 test1 是 ID，不用加 # 号
                        , count: data.total_count //数据总数，从服务端得到
                        , limit: data.limit
                        , curr: parseInt(data.cur_page)
                        , jump: function (obj, first) {

                            //首次不执行
                            if (!first) {
                                get_download_history(obj.curr);
                            }
                        },
                        layout: ['prev', 'page', 'next', 'count'],
                    });
                })
            })
            .fail(function () {  // 请求失败
                alert("下载历史请求错误");
            })
    }


})
