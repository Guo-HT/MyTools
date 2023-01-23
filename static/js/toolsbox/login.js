$(function () {

    var slider;
    //一般直接写在一个js文件中
    layui.config({
        base: '/static/js/'
    }).extend({
        sliderVerify:"sliderVerify"
    }).use(['sliderVerify', 'jquery', 'form'], function() {
        var sliderVerify = layui.sliderVerify,
            form = layui.form;
        slider = sliderVerify.render({
            elem: '#slider',
            // onOk: function(){//当验证通过回调
            // 	// layer.msg("滑块验证通过");
            // },
            isAutoVerify: false,
            bg: "layui-bg-red",
            text: "滑 动 验 证"
        })
    })

    function get_verify_img_func(){
        $.ajax({
            url: app_root + "get_verify_img",
            type: "get",
            dataType: "json",
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        }).done(function(msg){
            console.log(msg)
            if(msg.code==200){
                var data = "data:image/png;base64,"+msg.data
                $("#login_verify_img").attr("src", data)
            }
        }).fail(function(e){
            console.log(e)
        })
    }
    get_verify_img_func()

    $("#login_verify_img_div").click(get_verify_img_func)

    // 提交登录信息
    $("#submit").click(function () {
        layui.use("layer", function(){
            var layer = layui.layer;
        })
        var user_name = $("#user-name").val();
        var user_password = $("#user-password").val();
        var verify_img_input = $("#verify_img_input").val();
        var is_remember = $("#is-remember").is(":checked");

        if (user_name == "" && user_password!="") {
            layer.msg('请填写用户名或邮箱');
            return;
        }
        else if(user_name!="" && user_password==""){
            layer.msg("请填写密码");
            return;
        }
        else if(user_name == "" && user_password == ""){
            layer.msg("请填写信息");
            return;
        }
        else if(verify_img_input == ""){
            layer.msg("请填写验证码")
        }
        // else if(!slider.isOk()){
        //     layer.msg("请完成滑动验证");
        //     return;
        // }
        console.log(user_name, user_password, is_remember, verify_img_input);

        $.ajax({
            type: "post",
            url: app_root + "login_ajax",
            data: {
                "name": user_name,  // 用户名/密码
                "password": user_password,  // 用户密码（暂时未加密）
                "is_remember": is_remember,  // 是否选中“记住我”
                "verify_img_input": verify_img_input.toUpperCase(),  // 是否选中“记住我”
            },
            dataType: 'json',
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        })
            .done(function (msg) {
                // var data = eval(msg);
                if (msg.code === 200) {
                    $("#dragContainer").css({"display": "inherit"});
                    if (document.referrer === app_root + 'register') {
                        // 注册后登录的，直接返回index主页
                        window.location.href = app_root + 'index';
                    } else if (document.referrer === app_root + 'login') {
                        // 从登录界面来登录界面的，直接跳转回主页
                        window.location.href = app_root + 'index';
                    } else if (document.referrer === app_root + 'forget') {
                        // 从登录界面来登录界面的，直接跳转回主页
                        window.location.href = app_root + 'index';
                    } else {
                        // 除注册后登录的，从哪来的到哪去
                        window.location.href = document.referrer;
                    }

                }else {
                    layer.msg(msg.msg);
                    if (msg.msg=="验证码错误"){
                        $("#verify_img_input").val();
                        get_verify_img_func()
                    }
                } 
            })
            .fail(function () {
                layer.msg("请求错误！");
            })
    })


})