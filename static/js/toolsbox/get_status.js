$(function () {
    // var app_root = 'https://' + location.host + '/tools/';
    function get_device_status() {
        $.ajax({
            url: app_root + 'get_status',
            type: "get",
            dataType: "json",
            headers: {
                "X-CSRFToken": get_csrf_token(),
            },
        }).done(function (msg) {
            if (msg.code == 200) {
                var data = msg.data
                var cpu_info = eval(data.cpu_info);
                var mem_info = eval(data.mem_info);
                var disk_info = eval(data.disk_info);
                var open_info = eval(data.open_info);
                var cpu_core_percent = eval(cpu_info.cpu_core_percent);

                $("#cpu_total_percent").text(cpu_info.cpu_total_percent);
                var li_content = "";
                for (var i = 0; i < cpu_core_percent.length; i++) {
                    li_content += "<li class='cpu_core'>逻辑处理器" + (i + 1) + ":&nbsp;&nbsp;&nbsp;&nbsp;" + cpu_core_percent[i] + "</li>";
                }
                // $("#cpu_core_percent_div").css({'height': cpu_core_percent.length * 30})
                $("#cpu_core_percent").html(li_content);
                $("#cpu_temp").text(cpu_info.cpu_temp);
                $("#mem_total").text(mem_info.mem_total);
                $("#mem_available").text(mem_info.mem_available);
                $("#mem_percent").text(mem_info.mem_percent);
                $("#disk_total").text(disk_info.disk_total);
                $("#disk_percent").text(disk_info.disk_percent);
                $("#open_date").text(open_info.open_date);
                $("#open_time").text(open_info.open_time.slice(0, -7));

                if (cpu_info.cpu_temp === "无法获取") {
                    $("#cpu_temp").css({ "color": "rgb(204,204,204)" });
                }

                if (cpu_info.cpu_total_percent >= "80.0%" || cpu_info.cpu_total_percent === "100.0%") {
                    $(".cpu_inner_box").css({ "width": cpu_info.cpu_total_percent, "background-color": "red" });
                } else {
                    $(".cpu_inner_box").css({ "width": cpu_info.cpu_total_percent, "background-color": "rgb(122,194,60)" });
                }

                if (mem_info.mem_percent >= "80.0%" || mem_info.mem_percent === "100.0%") {
                    $(".mem_inner_box").css({ "width": mem_info.mem_percent, "background-color": "red" });
                } else {
                    $(".mem_inner_box").css({ "width": mem_info.mem_percent, "background-color": "rgb(122,194,60)" });
                }

                if (disk_info.disk_percent >= "80.0%" || disk_info.disk_percent === "100.0%") {
                    $(".disk_inner_box").css({ "width": disk_info.disk_percent, "background-color": "red" });
                } else {
                    $(".disk_inner_box").css({ "width": disk_info.disk_percent, "background-color": "rgb(122,194,60)" });
                }
            }else{
                layer.msg(msg.msg)
            }


        })
            .fail(function (e) {
                console.log(e);
            })
    }

    get_device_status();
    setInterval(get_device_status, 1000);

    $("#cpu_core_percent").slideUp();
    $("#cpu_info").click(function () {
        $("#cpu_core_percent").slideToggle();
    })
})