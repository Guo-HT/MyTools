$(function () {
    layui.use("layer", function () {
        var layer = layui.layer;
    })

    // 获取头栏信息
    function get_head_data() {
        // var $head_nav = $("#my-head-nav");
        $.ajax({
            url: app_root + "get_name_status",
            type: "get",
            dataType: "json",
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        })
            .done(function (data) {
                console.log(data);
                var html_head = "";  // 初始化变量
                if (data.islogin === true) {
                    // 如果用户处于登录状态
                    // $("#my-head-nav").children().eq(0).html('<a href="/">门户</a>');
                    // $("#my-head-nav").children().eq(1).html('<a href="/tools/index">工具箱</a>');
                    $("#my-head-nav").children().eq(2).html('<a href="/tools/personal/' + data.user_name_sess + '" title="'+data.user_name_sess+'的主页"><span class="user-name-head">' + data.user_name_sess + '</span>的主页</a>');
                    $("#my-head-nav").children().eq(3).html('<a href="javascript:void(0);" id="logout-1">登出</a>');
                    $("#my-head-nav").children().eq(4).html('<a href="/tools/upload">上传</a>');
                    // $("#my-head-nav").children().eq(5).children().find("dd").eq(0).html('<a href="/">门户</a>');
                    // $("#my-head-nav").children().eq(5).children().find("dd").eq(1).html('<a href="/tools/index">工具箱</a>');
                    $("#my-head-nav").children().eq(5).children().find("dd").eq(2).html('<a href="/tools/personal/' + data.user_name_sess + '" title="'+data.user_name_sess+'的主页"><span class="user-name-head">' + data.user_name_sess + '</span>的主页</a>');
                    $("#my-head-nav").children().eq(5).children().find("dd").eq(3).html('<a href="javascript:void(0);" id="logout-2">登出</a>');
                    $("#my-head-nav").children().eq(5).children().find("dd").eq(4).html('<a href="/tools/upload">上传</a>');

                } else {
                    // 如果处于游客状态
                    // $("#my-head-nav").children().eq(0).html('<a href="/">门户</a>');
                    // $("#my-head-nav").children().eq(1).html('<a href="/tools/index">工具箱</a>');
                    $("#my-head-nav").children().eq(2).html('<a href="/tools/login">登录</a>');
                    $("#my-head-nav").children().eq(3).html('<a href="/tools/register">注册</a>');
                    $("#my-head-nav").children().eq(4).html('<a href="/tools/login">上传</a>');
                    // $("#my-head-nav").children().eq(5).children().find("dd").eq(0).html('<a href="/">门户</a>');
                    // $("#my-head-nav").children().eq(5).children().find("dd").eq(1).html('<a href="/tools/index">工具箱</a>');
                    $("#my-head-nav").children().eq(5).children().find("dd").eq(2).html('<a href="/tools/login">登录</a>');
                    $("#my-head-nav").children().eq(5).children().find("dd").eq(3).html('<a href="/tools/register">注册</a>');
                    $("#my-head-nav").children().eq(5).children().find("dd").eq(4).html('<a href="/tools/login">上传</a>');
                }
            })
            .fail(function (error) {
                console.log(error);
            })
    }
    get_head_data();

    // 按下登出按钮
    $("#my-head-nav").on("click", "#logout-1", function () {
        logout();
    })

    $("#my-head-nav").on("click", "#logout-2", function () {
        logout();
    })

    function logout() {
        // 发送数据
        $.ajax({
            url: app_root + 'logout',
            type: 'get',
            dataType: 'text',
            data: {
                "logout": 'true',
            },
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        }).done(function (msg) {
            if (msg === "logout_ok") {
                // 如果登出成功，跳转到主页
                window.location.href = app_root + 'index';
                // 弹框提醒
                layer.msg('成功退出登录！');
            }
        })
            .fail(function () {
                layer.msg('失败');
            })
    }
})
