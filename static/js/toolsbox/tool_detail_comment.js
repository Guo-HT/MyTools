$(function () {

    // var app_root = 'https://' + location.host + '/tools/';

    var tool_id = window.location.pathname.slice(19);

    // 发表评论
    $("#submit_btn").click(function () {
        // /tools/tool_detail/
        var comment_text = $("#up_comment_text").val();  // 获取评论表单
        if (comment_text === '') {  // 如果评论栏为空
            alert("评论为空！");
            return;
        }
        $.ajax({
            type: "post",
            url: app_root + 'submit_comment',
            dataType: "json",
            data: {
                "text": $("#up_comment_text").val(),
                "from": tool_id,
            },
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        }).done(function (msg) {
            if (msg.code == 200) {
                $("#up_comment_text").val("");  // 评论表单清空
                get_comment_data(1);  // 跳转到评论第一页
                // window.location.href = window.location.href+"#comment";
                // alert("评论成功")
            }
        })
            .fail(function () {
                alert("失败");
            })
    })

    //获取评论 参数为页码
    function get_comment_data(to_page) {
        $.ajax({
            type: "get",
            url: app_root + 'get_comments',
            dataType: "json",
            data: {
                // "text": $("#up_comment_text").val(),
                "to_page": to_page,
                "from": tool_id,
            },
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        }).done(function (msg) {
            if (msg.code == 200) {
                var data = msg.data

                var page_count = data.total_page;
                var page_cur = data.cur_page;
                var comment_count = data.comment_count;
                var comment_info_json = data.comment_list;
                $("#comment_count").text(comment_count);

                var $com_ul = $("#comment_ul")
                $com_ul.html("");
                var data_length = 0;
                $.each(comment_info_json, function (index, object) {
                    // console.log(index, object);
                    // xss防护
                    var content_raw = object.content;
                    var new_div = document.createElement("div");
                    new_div.innerHTML = content_raw;
                    var content = new_div.innerText;

                    var each_content = "<li class=\"comment_content\" id=\"comment_content\">" +
                        "<div class=\"clearfix\"><span class=\"user\" id=\"user\">" + object.user_name + "</span>" +
                        "<span class=\"comment_date\" id=\"comment_date\">" + object.time + "</span></div>" +
                        "<div class=\"content\" id=\"content\">" + content +
                        " </div>" +
                        "<div class=\"good\" id=\"good\">" +
                        "<svg t=\"1617427273444\" class=\"icon\" viewBox=\"0 0 1024 1024\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" p-id=\"2058\" width=\"16\" height=\"16\"><path d=\"M569.6 121.6a19.2 19.2 0 0 1 22.08-18.9824c16.384 2.048 51.5584 25.3056 68.8832 43.392 21.376 19.776 27.0464 52.3712 11.872 78.656l-35.1808 60.9408 0.192-0.0064C614.2784 334.1312 625.7984 358.4 672 358.4h150.0672c42.4128 0 76.8 34.3872 76.8 76.8a76.8 76.8 0 0 1-0.5696 9.2992l-45.2672 371.2A76.8 76.8 0 0 1 776.8 883.2H422.4c-42.4128 0-76.8-34.3872-76.8-76.8V435.2c0-40.2944 31.0336-73.344 70.5024-76.544L416 358.4c21.3632-4.9408 41.1072-20.6912 59.2384-47.2384l86.752-150.2528c0.352-0.608 0.704-1.2096 1.0752-1.792C569.6 144.8512 569.6 139.9488 569.6 121.6zM192 358.4h38.4c35.3472 0 64 28.6528 64 64v396.8c0 35.3472-28.6528 64-64 64h-38.4c-35.3472 0-64-28.6528-64-64V422.4c0-35.3472 28.6528-64 64-64z\" fill=\"#59AAFF\" p-id=\"2059\"></path></svg>" +
                        "<span class=\"good_num\" id=\"good_num\">" + object.good + "</span></div>" +
                        "<hr>" +
                        "</li>";
                    // console.log(each_content);
                    $com_ul.html($com_ul.html() + each_content);
                })

                layui.use("laypage", function () {
                    var laypage = layui.laypage;
                    laypage.render({
                        elem: 'comment-page-nav' //注意，这里的 test1 是 ID，不用加 # 号
                        , count: data.comment_count //数据总数，从服务端得到
                        , limit: data.limit
                        , curr: parseInt(data.cur_page)
                        , jump: function (obj, first) {

                            //首次不执行
                            if (!first) {
                                get_comment_data(obj.curr);
                            }
                        },
                        layout: ['prev', 'page', 'next', 'count'],
                    });
                })
            }else{
                layer.msg(msg.msg);
            }
        })
            .fail(function () {
                alert("失败");
                return 0;
            })
    }

    // 初始状态，自动获取第一页评论
    get_comment_data(1);

    // 点击分页导航后
    $("#page_nav").on("click", "#page_id", function () {
        var to_page = $(this).text();
        get_comment_data(parseInt(to_page));
    })


})
