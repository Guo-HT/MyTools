function parse_cookie(){
    var cookie_str = document.cookie;
    var cookie_list = cookie_str.split(";")
    var list_length = cookie_list.length
    var cookie_obj = {};
    for(var i=0;i<list_length;i++){
        var kw = cookie_list[i].split("=");
        cookie_obj[$.trim(kw[0])] = $.trim(kw[1]);
    }
    return cookie_obj;
}
