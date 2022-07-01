$(function () {

    layui.use("layer", function(){
        var layer = layui.layer;
    })

    $("#user-password").blur(function () {
        var reg = /^(?![a-zA-Z]+$)(?![A-Z0-9]+$)(?![A-Z._~!@#$^&*]+$)(?![a-z0-9]+$)(?![a-z._~!@#$^&*]+$)(?![0-9._~!@#$^&*]+$)[a-zA-Z0-9._~!@#$^&*]{8,}$/;
        if ((!reg.test($("#user-password").val()))||($("#user-password").val().length < 6)) {
            $("#user-password").val("");
            $("#tip-password").text("要求包含大、小写字母，数字，特殊字符(_!@#$%^&*()+.)的组合，不能低于8位");
        }else{
            $("#tip-password").text("");
        }
    })
    $("#user-password-check").blur(function () {
        var reg = /^(?![a-zA-Z]+$)(?![A-Z0-9]+$)(?![A-Z._~!@#$^&*]+$)(?![a-z0-9]+$)(?![a-z._~!@#$^&*]+$)(?![0-9._~!@#$^&*]+$)[a-zA-Z0-9._~!@#$^&*]{8,}$/;
        if ((!reg.test($("#user-password-check").val()))||($("#user-password-check").val().length < 6)) {
            $("#user-password-check").val("");
            $("#tip-password-check").text("要求包含大、小写字母，数字，特殊字符(_!@#$%^&*()+.)的组合，不能低于8位");
        }else{
            $("#tip-password-check").text("");
        }
    })

    $("#user-email").blur(function () {
        var reg = /^[a-z0-9._%-]+@([a-z0-9-]+\.)+[a-z]{2,4}$|^1[3|4|5|7|8]\d{9}$/;
        if (!reg.test($("#user-email").val())) {
            $("#user-email").val("");
            $("#tip-user-email").text("邮件格式错误。");
        }else{
            $("#tip-user-email").text("");
        }
    })

    //提交邮箱验证请求 start
    $("#get-verify").click(function () {
        // 判断邮箱是否填写
        if ($("#user-email").val() === '') {
            layer.msg('请输入邮箱地址!');
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
            url: app_root + 'email_check_change_pwd',
            dataType: 'text',
            data: {
                // 'csrfmiddlewaretoken': csrf_token,
                "user_email": $("#user-email").val(),
            },
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        }).done(function (msg) {
            console.log('验证中......');
            if (msg === 'email_not_exist') {
                layer.msg("邮箱未绑定，请确认重试。");
                $("#user-email").val("");
            } else if (msg === "error") {
                layer.msg("邮件发送出现问题");
            }
        })
            .fail(function () {
                layer.msg("失败");
            })
    })
    //提交邮箱验证请求 end

    // 提交修改密码数据 start
    $("#forget-submit").click(function () {
        $.ajax({
            url: app_root + "change_pwd",
            type: "post",
            dataType: "text",
            data: {
                'email': $("#user-email").val(),
                'verify': $("#user-verify").val(),
                'new_password': $("#user-password").val(),
            },
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        }).done(function (msg) {
            if (msg === 'not_exist') {
                layer.msg("邮箱没有绑定！");
            } else if (msg === "failed") {
                layer.msg("修改失败");
            } else if (msg === "error") {
                layer.msg("验证码错误！");
            } else if (msg === "ok") {
                layer.msg("修改成功，即将跳转");
                window.location.href = "/tools/login";
            }
        })
            .fail(function () {
                layer.msg("失败");
            })
    })
    // 提交修改密码数据 end
})