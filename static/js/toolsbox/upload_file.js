$(function () {
    // 默认不可用
    $("#submit_file").attr("disabled", true);

    // 全部填写后才可以提交
    function check_all_input() {
        var is_input_ok = true;
        for (var i = 1; i < 5; i++) {
            if ($("input").eq(i).val() === "") {
                is_input_ok = false;
            }
        }
        var is_name_ok = false;
        if ($("#tool_name").val().length >= 25) {
            is_name_ok = false;
            $("#tool_name_tip").text("长度不得超过25个字符");
        } else {
            is_name_ok = true;
            $("#tool_name_tip").text("");
        }
        if (is_input_ok && is_name_ok) {
            $("#submit_file").removeAttr("disabled");
        } else {
            $("#submit_file").attr("disabled", true);
        }
    }

    // 定时检查
    setInterval(check_all_input, 30);
})
