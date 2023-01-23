layui.use("layer", function(){
    var layer = layui.layer;
    layer.photos({
        photos: {
            "title": "", //相册标题
            "id": 0, //相册id
            "start": 0, //初始显示的图片序号，默认0
            "data": [   //相册包含的图片，数组格式
              {
                "alt": "",
                "pid": 666, //图片id
                "src": "/static/img/happyNewYear.jpg", //原图地址
                "thumb": "" //缩略图地址
              }
            ]
        }
        , amin: 5
        ,time : 3000
    })
    // var imgHtml = "<img src='/static/img/happyNewYear.jpg' width='800px' height='500px' />"
    // var happyNewYearLayer = layer.open({
    //     type: 1,
    //     shade:0.8,
    //     offset: 'auto',
    //     area: ['800px', '500px'],
    //     shadeClose: true,
    //     scrollbar: false,
    //     title: "",
    //     content: imgHtml,
    //     time: 5000,
    //     closeBtn: 0,
    // })

})