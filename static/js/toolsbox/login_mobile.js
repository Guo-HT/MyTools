$(function () {
    // var app_root = 'https://' + location.host +'/tools/';

    // 获取用户状态
    function get_user_status() {
        $.ajax({
            url: app_root + "get_name_status",
            type: "get",
            dataType: "json",
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        })
            .done(function (msg) {
                var data = JSON.parse(msg);
                // 将cookie中存储的名称显示在login界面表单上
                $("#login_name").val(data.user_name_cook);
            })
    }
    get_user_status();

    // 提交登录信息
    $("#login_btn").click(function () {
        // alert("提交登录信息");
        if ($("#login_name").val() === "" || $("#login_password").val() === "") {
            alert("请完整填写信息");
            return;
        }
        $.ajax({
            type: "post",
            url: app_root + "login_ajax",
            data: {
                "name": $("#login_name").val(),  // 用户名/密码
                "password": $('#login_password').val(),  // 用户密码（暂时未加密）
                "is_remember": $("#remember_me").is(":checked"),  // 是否选中“记住我”
            },
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
            dataType: 'json',
        })
            .done(function (msg) {
                var data = eval(msg);
                if (data.state === "OK") {
                    $("#dragContainer").css({"display": "inherit"});
                    if (document.referrer === app_root + 'register') {
                        // 注册后登录的，直接返回index主页
                        window.location.href = app_root + 'index';
                    } else if (document.referrer === app_root + 'login') {
                        // 从登录界面来登录界面的，直接跳转回主页
                        window.location.href = app_root + 'index';
                    } else {
                        // 除注册后登录的，从哪来的到哪去
                        window.location.href = document.referrer;
                    }

                } else if (data.state === "password_error") {
                    $("#name_tip").text("");
                    $("#password_tip").text("  密码错误！");
                    $("#login_password").val("");
                } else if (data.state === "user_not_exist") {
                    $("#name_tip").text("  该用户不存在");
                    $("#login_name").val("");
                    $("#login_password").val("");
                }
            })
            .fail(function () {
                alert("失败");
            })
    })
})