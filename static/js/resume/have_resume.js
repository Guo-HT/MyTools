function have_resume(){
    $.ajax({
        url:app_root+"have_resume",
        type:"get",
        Datetype:"json"
    }).done(function(msg){
        if(msg.code==200){
            var data = msg.data
            if (data.state==="none"){
                $("#btn").text("上传你的简历");
                document.cookie="resume_change=false"
            }
            else if(data.state==="have"){
                $("#btn").text("修改/查看你的简历");
                document.cookie="resume_change=true";
                document.cookie="file_name="+data.file_name;
            }
        }
        
    }).fail(function(e){
        console.log(e);
    })
}
have_resume()