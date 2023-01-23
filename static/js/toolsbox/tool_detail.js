$(function () {
    window.onblur = function(){
        $("title").text("快回来！| 工具箱");
    }
    window.onfocus = function(){
        $("title").text(tool_name + " | 详情");
    }
    // var app_root = 'https://' + location.host + '/tools/';
    var tool_id = window.location.pathname.slice(19);
    var tool_name = "工具详情";
    // 获取工具信息
    function get_tool_info() {
        var $content_ul = $("#content_ul");
        $.ajax({
            url: app_root + "get_tool_info",
            type: "get",
            dataType: "json",
            data: {
                "from_url": tool_id,
            },
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        }).done(function (msg) {
            // console.log(data);
            if (msg.code==200){
                data = msg.data;
                tool_name = data.tool_name;
                $("title").text(data.tool_name+" | 详情");
                $("#img_icon").attr("src",  data.media_url + data.tool_icon);  // 图标链接
                $("h1").text(data.tool_name);  // 工具名称
                $("#tool_detail_content").html(data.tool_describe);  // 工具简介
                $("#tool_watch").text(data.tool_watch);  // 浏览量
                $("#upload_time").text(data.upload_time);
                if (data.is_login === true) {
                    // 如果登录，则可以下载，可以评论
                    $("#download_btn").html("<a href=\"" + data.media_url  + data.tool_file + "\" id=\"file_download\">文件下载</a>");
                    $("#submit_btn").removeAttr("disabled").val("发表评论");
                } else {
                    // 未登录，下载按钮跳转到登陆界面，评论按钮不可用
                    $("#download_btn").html("<a href=\"/tools/login\">登陆后下载</a>");
                    $("#submit_btn").attr("disabled", "disabled").val("登陆后评论");
                }
            }else{
                layer.msg(msg.msg);
                // location.href=document.referrer;
            }
        })
    }

    get_tool_info();

    //统计下载量
    $("#download_btn").on("click", "#file_download", function () {
        $.ajax({
            url: app_root + "download",
            type: "get",
            dataType: 'json',
            data: {
                // 'csrfmiddlewaretoken': get_csrf_token(),
                "url": tool_id,
            },
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        })
            .done(function (msg) {
                // alert("成功");
            })
            .fail(function () {
                // alert('失败');
            })
    })


    layui.use("layer", function(){
        var layer = layui.layer;
    })
    
    $("#tool_detail_content").on("click", "img", function(){
        var img_src = $(this).attr("src");
        var img_layer_json = {
            "title": "", //相册标题
            "id": 0, //相册id
            "start": 0, //初始显示的图片序号，默认0
            "data": [   //相册包含的图片，数组格式
              {
                "alt": img_src,
                "pid": 0, //图片id
                "src": img_src, //原图地址
                "thumb": "" //缩略图地址
              }
            ]
          }

          layer.photos({
            photos: img_layer_json
            ,anim: 5 //0-6的选择，指定弹出图片动画类型，默认随机（请注意，3.0之前的版本用shift参数）
          });
    })

})
