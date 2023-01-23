$(function () {
    // var app_root = 'https://' + location.host +'/tools/';

    var tool_id = window.location.pathname.slice(19);
    // 点赞功能
    $("#comment_ul").on("click", "li #good", function () {
        // 获取父类元素
        var $this_li = $(this).parent();
        // alert($this_li.find("#user").text());
        // alert($this_li.find("#comment_date").text());
        $.ajax({
            type: "post",
            url: app_root + 'comments_good',
            dataType: "json",
            data: {
                "user": $this_li.find("#user").text(),  // 点击元素统计的用户名
                "from": tool_id,
                "time": $this_li.find("#comment_date").text(),  // 点击元素统计的点赞时间
            },
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        }).done(function (msg) {
            // console.log("点赞成功!");
            if(msg.code==200){
                $this_li.find('#good_num').text(msg.data.good_num);  // 页面上的点赞数实时+1
            }
            // alert("评论成功")
        })
            .fail(function () {
                console.log("点赞失败");
            })
    })
})