$(function () {

    layui.use('layer', function () {
        var layer = layui.layer;
    });

    $("#user-name").blur(function () {
        var reg = /^\w+$/;
        if ((!reg.test($("#user-name").val()))||($("#user-name").val().length < 8)) {
            $("#user-name").val("");
            $("#tip-user-name").text("请使用数字、字母、下划线，且长度不小于8位。");
        }else{
            $("#tip-user-name").text("");
        }
    })
    $("#user-password").blur(function () {
        var reg = /^(?![a-zA-Z]+$)(?![A-Z0-9]+$)(?![A-Z._~!@#$^&*]+$)(?![a-z0-9]+$)(?![a-z._~!@#$^&*]+$)(?![0-9._~!@#$^&*]+$)[a-zA-Z0-9._~!@#$^&*]{8,}$/;
        if (!reg.test($("#user-password").val())) {
            $("#user-password").val("");
            $("#tip-password").text("要求包含大、小写字母，数字，特殊字符(_!@#$%^&*()+.)的组合（至少三种），不能低于8位");
        }else{
            $("#tip-password").text("");
        }
    })
    $("#user-password-check").blur(function () {
        var reg = /^(?![a-zA-Z]+$)(?![A-Z0-9]+$)(?![A-Z._~!@#$^&*]+$)(?![a-z0-9]+$)(?![a-z._~!@#$^&*]+$)(?![0-9._~!@#$^&*]+$)[a-zA-Z0-9._~!@#$^&*]{8,}$/;
        if (!reg.test($("#user-password-check").val())) {
            $("#user-password-check").val("");
            $("#tip-password-check").text("要求包含大、小写字母，数字，特殊字符(_!@#$%^&*()+.)的组合（至少三种），不能低于8位");
        }else{
            $("#tip-password-check").text("");
        }
    })


    //注册提交
    $("#register-submit").click(function () {
        // alert("点击上传");
        var name = $("#user-name").val();
        var passwd = $("#user-password").val();
        var passwd_check = $("#user-password-check").val();
        var email = $("#user-email").val();
        var verify = $("#user-verify").val();
        var real_name = $("#user-real-name").val();

        if(name=="" || passwd=="" || passwd_check=="" || email=="" || verify=="" || real_name==""){
            layer.msg("请完整填写信息！");
            return;
        }
        
        else if(passwd!=passwd_check){
            $("#user-password").val("");
            $("#user-password-check").val("");
            layer.msg("请重新确认密码！");
            return;
        }
        console.log(name+" | "+real_name+" | "+passwd+" | "+email+" | "+verify)
        $.ajax({
            url: app_root + 'reg_ajax',
            type: 'post',
            dataType: 'json',
            data: {
                "user_name": name,
                "user_real_name": real_name,
                "user_password": passwd,
                "user_email": email,
                "verify_code": verify,
            },
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        }).done(function (msg) {
            console.log(msg);
            var data = eval(msg);
            if (data.state === "OK") {
                window.location.href = app_root + 'login';
            } else if (data.state === "name_exist") {
                layer.msg("用户名已存在！");
            } else if (data.state === "wrong or timeout") {
                layer.msg("验证码超时或错误！");
                window.location.reload();
            }
        })
            .error(function () {
                layer.msg("失败");
            });
    })


    //提交邮箱验证请求
    $("#get-verify").click(function () {
        // 判断邮箱是否填写
        var email = $("#user-email").val();
        if(email==""){
            layer.msg("输入邮箱后验证");
            return;
        }
        //点击后按钮不可用
        var $e_check_btn = $("#get-verify");
        $e_check_btn.attr("disabled", true);
        // 六十秒后按钮可用
        var rest_time = 60;
        var timer_60s = setInterval(function () {
            $e_check_btn.val(rest_time + "秒后重试");
            rest_time--;
            if (rest_time < 0) {
                $e_check_btn.val("获取验证码")
                $e_check_btn.removeAttr("disabled");
                clearInterval(timer_60s);
            }
        }, 1000);
        $.ajax({
            type: 'get',
            url: app_root + 'email_check',
            dataType: 'text',
            data: {
                "user_email": $("#user-email").val(),
            },
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        }).done(function (msg) {
            // console.log('验证中......');
            if (msg === 'email_exist') {
                rest_time = 60;
                $e_check_btn.val("获取验证码")
                $e_check_btn.removeAttr("disabled");
                clearInterval(timer_60s);
                layer.msg("邮箱已被使用，请重新验证。");
                $("#email").val("");
            } else if (msg === "error") {
                rest_time = 60;
                $e_check_btn.val("获取验证码")
                $e_check_btn.removeAttr("disabled");
                clearInterval(timer_60s);
                layer.msg("邮件发送出现问题");
            }
        })
            .fail(function () {
                rest_time = 60;
                $e_check_btn.val("获取验证码")
                $e_check_btn.removeAttr("disabled");
                clearInterval(timer_60s);
                layer.msg("失败！请确认网络状态后重试");
            })
    })
})

