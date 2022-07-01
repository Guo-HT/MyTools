$(function(){
    var isFileInput=false;
    $("#resume_pdf").change(function(){
        try{
            var oFile = this.files[0];
            var file_name = oFile.name;
            var name_list = file_name.split(".");
            var file_type = name_list[name_list.length-1];
            file_type = file_type.toLowerCase();
            if (file_type !== "pdf"){
                document.getElementById("resume_pdf").value="";
                $("#tip_file").attr({"color":"red"}).text("只允许上传pdf文件！")
            }
            isFileInput=true;
        }
        catch(e){
            isFileInput=false;
        }
    });
    
    $("#url_input").on("input", function(){
        if($(this).val().indexOf("#")==-1 && $(this).val().indexOf("?")==-1 && $(this).val().indexOf("？")==-1){
            $("#url_show").text($(this).val());
        }
        else{
            var str_now = $(this).val();
            var str_length = str_now.length;
            $(this).val(str_now.slice(0,str_length-1));
        }
        
    })

    if (parse_cookie()["resume_change"]=="true"){
        $("#current_resume_url1").html("<a href='"+location.origin+"/resume/show/"+parse_cookie()['file_name'] + "' target='_blank'>你的简历1(兼容手机、平板)</a>");
        $("#current_resume_url2").html("<a href='"+location.origin+"/resume/show2/"+parse_cookie()['file_name'] + "' target='_blank'>你的简历2(仅PC端)</a>");
    }
    else{
        $("#current_resume_url1").text("暂无");
    }

    $url_input = $("#url_input") //表单输入
    $resume_pdf = $("#resume_pdf")// 文件选择
    setInterval(function(){
        // console.log($resume_pdf);
        if($url_input.val()==="" || !isFileInput){
            // console.log("有空")
            $("#submit").attr({"disabled":true});
        }
        else{
            // console.log("都填了");

            $("#submit").attr({"disabled":false});
        }
    }, 300);



    
})
