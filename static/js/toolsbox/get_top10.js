$(function () {
    $.ajax({
        type: "get",
        url: app_root + 'get_top_ten',
        dataType: "json",
        data: {
            // "csrfmiddlewaretoken": get_csrf_token(),
        },
        headers: {
            "X-CSRFToken": get_csrf_token(),
        },
    }).done(function (data) {
        // console.log(data);
        var watch_data = data.watch;
        var download_data = data.download;
        var html_watch = "";
        var html_download = "";
        var i = 0;
        $.each(watch_data, function (index, object) {
            var id = object.id;
            var name = object.name;
            var count = object.count;
            html_watch += '<li><a href="' + app_root + "tool_detail/" + id + '"><span>'+name+'</span>&nbsp;<i class="layui-icon layui-icon-heart-fill"></i>&nbsp;<span>'+count+'</span></a></li>'
        })
        var i = 0;
        $.each(download_data, function (index, object) {
            var id = object.id;
            var name = object.name;
            var count = object.count;
            html_download += '<li><a href="' + app_root + "tool_detail/" + id + '"><span>'+name+'</span>&nbsp;<i class="layui-icon layui-icon-heart-fill"></i>&nbsp;<span>'+count+'</span></a></li>'

        })

        $("#browser-top-ten").html(html_watch);
        $("#download-top-ten").html(html_download);

    })
        .fail(function () {
            alert("失败");
        })
})
