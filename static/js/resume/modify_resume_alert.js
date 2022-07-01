$(function(){
    if(parse_cookie()['resume_change']==="true"){
        alert("修改后，原来的文件将会被删除，请谨慎操作！");
    }
})