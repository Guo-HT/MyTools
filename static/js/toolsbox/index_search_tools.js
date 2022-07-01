$(function () {
    // 搜索按钮点击
    $("#search-btn").click(function () {
        var search_content = $("#search-input").val();  // 获取表单的内容
        if(search_content===''){  // 如果内容为空，则退出，不响应
            return;
        }
        // 如果内容不为空，直接跳转到对应页面，由对应页面解析信息
        window.location.href = app_root + "search_tool/" + search_content;
    })

    // 焦点再input表单上，按回车直接提交
    $("#search-input").keydown(function(){{
        if (event.keyCode=='13'){
            $("#search-btn").click();
        }
    }})

})