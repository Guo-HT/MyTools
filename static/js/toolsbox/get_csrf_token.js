//获取csrftoken start
function get_csrf_token() {
    // 获取cookie
    var cookies = document.cookie;
    // 将cookie字符串切分成单个cookie数组
    var cookies_list = cookies.split(';')
    //cookie数量
    var cookie_num = cookies_list.length;
    //遍历
    for (var i = 0; i < cookie_num; i++) {
        var kw = cookies_list[i].split('=');
        //如果cookie的key为csrftoken
        if (kw[0] === 'csrftoken') {
            // alert(csrf_token);
            return kw[1];  //返回
        }
    }
}
//获取csrftoken end