$(function () {
    var $page_nav = $("#page_nav");
    var page_count = 1

    function index_get_resumes(to_page) {
        $.ajax({
            url: app_root + "index_get_resumes",
            type: "get",
            DataType: "json",
            data: {
                group: to_page,
            }
        }).done(function (msg) {
            if (msg.code == 200) {
                var data = msg.data;
                // console.log(data);
                $("#jump_to_page").val("");
                page_count = data.total_page;
                var page_cur = data.cur_page;
                var resume_info_list = data.resume_list;
                var media_url = data.media_url;
                var $resumes_show = $("#resume_list");
                if (to_page > page_count) {
                    alert("页数超出，请检查输入！");
                    return;
                }
                $("#jump_label").text(page_count);
                //清空当前所有元素
                $resumes_show.html('');
                // 将简历数据写入页面
                var cur_num = resume_info_list.length;
                // console.log(cur_num);
                for (var i = 0; i < cur_num; i++) {
                    // resume_info_list[i]
                    // 创建div对象
                    var oDiv = document.createElement('div');
                    // 将html写入
                    oDiv.innerHTML = resume_info_list[i].file_name;
                    // 提取文本
                    var text = oDiv.innerText;
                    var each_content = '<li class="resume_li clearfix"><a href="/resume/show/' +
                        resume_info_list[i].file_name + '" class="resume_a clearfix" target="_blank"><img src="' + media_url + resume_info_list[i].first_img_path + '" alt="简历首页">' +
                        '<div class="resume_user">' + resume_info_list[i].user_belong + '</div></a></li>';
                    $resumes_show.html($resumes_show.html() + each_content)
                }
                var html = "<li id='page_id'>" + "首页" + "</li>";  // 初始化一个html字符串
                var i = 0;
                // 总页数小于 5
                if (page_count <= 5) {
                    for (i = 0; i < page_count; i++) {
                        if (parseInt(page_cur) === (i + 1)) {
                            html += "<li id='page_id' class='cur_page'>" + (i + 1) + "</li>";
                        } else {
                            html += "<li id='page_id'>" + (i + 1) + "</li>";
                        }
                    }
                }
                // 当总数大于5
                else if (page_cur <= 3) {
                    for (i = 0; i < 4; i++) {
                        if (parseInt(page_cur) === (i + 1)) {
                            html += "<li id='page_id' class='cur_page'>" + (i + 1) + "</li>";
                        } else {
                            html += "<li id='page_id'>" + (i + 1) + "</li>";
                        }
                    }
                    html += "<li id='page_none'>" + "..." + "</li>";
                }
                // 当前页面在最后三页，显示最后五个
                else if (page_cur > page_count - 3) {
                    html += "<li id='page_none'>" + "..." + "</li>";
                    for (i = 0; i < 4; i++) {
                        if (parseInt(page_cur) === (page_count - 3 + i)) {
                            html += "<li id='page_id' class='cur_page'>" + (page_count - 3 + i) + "</li>";
                        } else {
                            html += "<li id='page_id'>" + (page_count - 3 + i) + "</li>";
                        }
                    }
                }
                // 在中间的几页
                else {
                    html += "<li id='page_none'>" + "..." + "</li>";
                    for (i = 0; i < 3; i++) {
                        if (i === 1) {
                            html += "<li id='page_id' class='cur_page'>" + page_cur + "</li>";
                        } else {
                            html += "<li id='page_id'>" + (page_cur - 1 + i) + "</li>";
                        }
                    }
                    html += "<li id='page_none'>" + "..." + "</li>";
                }
                html += "<li id='page_id'>" + "尾页" + "</li>";
                $("#page_nav").html(html);
            }else{
                layer.msg(msg.msg)
            }

        }).fail(function (e) {
            console.log(e);
        })
    }

    index_get_resumes(1);

    // 分页导航，点击后转至对应页
    $page_nav.on("click", "#page_id", function () {
        var to_page = $(this).text();
        index_get_resumes(to_page);
    })
    // 直接跳转按键
    $("#jump_go").click(function () {
        var to_page = $("#jump_to_page").val();
        if (to_page <= 0 || to_page > page_count) {
            alert("页数超出，请检查输入！");
            $("#jump_to_page").val('');
            return;
        }
        if (to_page == "首页") {
            to_page = 1
        }
        else if (to_page == "尾页") {
            to_page = "尾页"
        }
        else if (isNaN(to_page)) {
            alert("请检查输入！\n请不要试图注入！！！");
            $("#jump_to_page").val('');
            return;
        }
    })

    // 焦点再input表单上，点击回车，调用按钮点击事件
    $("#jump_to_page").keydown(function () {
        if (event.keyCode == "13") {
            $("#jump_go").click();
            $(this).val('');
        }
    })

})