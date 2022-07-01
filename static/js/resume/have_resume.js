function have_resume(){
    $.ajax({
        url:app_root+"have_resume",
        type:"get",
        Datetype:"json"
    }).done(function(msg){
        if (msg.state==="none"){
            $("#btn").text("上传你的简历");
            document.cookie="resume_change=false"
        }
        else if(msg.state==="have"){
            $("#btn").text("修改/查看你的简历");
            document.cookie="resume_change=true";
            document.cookie="file_name="+msg.file_name;
        }
    }).fail(function(e){
        console.log(e);
    })
}
have_resume()