$(function () {
    var is_fold = 0;

    setInterval(function(){
        var innerHeight = window.innerHeight;
        var css_top = (innerHeight-350)/2;
        $(".download_top_div").css({"top": css_top});
        $(".watch_top_div").css({"top":css_top});
    }, 100);

    function sidebar_toggle() {
        if (is_fold === 1) {
            // 隐藏->展开
            $(".download_top_div").animate({
                right: "5px"
            });
            $(".show_sidebar_download").toggle(500)
            setTimeout(function () {
                $("#download_top_ten").slideToggle(500);
            }, 500);
        } else {
            // 展开->隐藏
            $("#download_top_ten").slideToggle(500);
            setTimeout(function () {
                $(".show_sidebar_download").toggle(500);
                $(".download_top_div").animate({
                    right: "-190px"
                });
            }, 500);
        }

        if (is_fold === 1) {
            // 隐藏->展开
            $(".watch_top_div").animate({
                left: "5px"
            });
            $(".show_sidebar_watch").toggle(500);
            setTimeout(function () {
                $("#watch_top_ten").slideToggle(500);
            }, 500);
        } else {
            // 展开->隐藏
            $("#watch_top_ten").slideToggle(500);
            setTimeout(function () {
                $(".show_sidebar_watch").toggle(500);

                $(".watch_top_div").animate({
                    left: "-190px"
                });
            }, 500);

        }


        if (is_fold === 0) {
            is_fold = 1;
        } else {
            is_fold = 0;
        }
    }

    $("#hidden_btn_watch").click(sidebar_toggle)
    $("#hidden_btn_download").click(sidebar_toggle)
    $("#show_sidebar_download").click(sidebar_toggle)
    $("#show_sidebar_watch").click(sidebar_toggle)

})