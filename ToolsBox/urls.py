from django.urls import path, re_path
from ToolsBox import views

# /tools/.*/
urlpatterns = [
    re_path(r'^$', views.index, name="index"),  # 主页√
    re_path(r'^index$', views.index, name="index"),  # 主页√
    re_path(r'^login$', views.login, name="login"),  # 登录页√
    re_path(r'^register$', views.register, name="register"),  # 注册页√
    re_path(r'^reg_ajax$', views.reg_ajax, name="reg_ajax"),  # 注册功能√
    re_path(r'^login_ajax$', views.login_ajax, name="login_ajax"),  # 登录功能√
    re_path(r'^logout$', views.logout, name="logout"),  # 登出功能√
    re_path(r'^upload$', views.upload, name="upload"),  # 上传页√
    re_path(r'^upload_ajax$', views.upload_ajax, name="upload_ajax"),  # 上传功能√
    re_path(r'^tool_detail/(\d+)$', views.tool_detail, name="tool_detail"),  # 工具详情页√
    re_path(r'^get_tool_info$', views.get_tool_info, name="get_tool_info"),  # 工具详细信息√
    re_path(r'^search_tool/(.+)$', views.search_tool, name="search_tool"),  # 工具搜索页√
    re_path(r'^get_search_tool$', views.get_search_tool, name="get_search_tool"),  # 工具搜索√
    re_path(r'^email_check$', views.email_check, name="email_check"),  # 邮箱验证功能√
    re_path(r'^get_personal_info$', views.get_personal_info, name="get_personal_info"),  # 获取个人数据√
    re_path(r'^personal/(\w+)$', views.personal, name="personal"),  # 个人页√
    re_path(r'^get_browser_history$', views.get_browser_history, name="get_browser_history"),  # ajax获取个人浏览记录√
    re_path(r'^get_upload_history$', views.get_upload_history, name="get_upload_history"),  # ajax获取个人上传记录√
    re_path(r'^get_download_history$', views.get_download_history, name="get_download_history"),  # ajax获取个人下载记录√
    re_path(r'^download$', views.download, name="download"),  # ajax进行下载量记录√
    re_path(r'^get_tools$', views.get_tools, name="get_tools"),  # 主页ajax获取工具信息√
    re_path(r'^get_top_ten$', views.get_top_ten, name="get_top_ten"),  # 主页ajax获取下载量、浏览量前十√
    re_path(r'^submit_comment$', views.submit_comment, name="submit_comment"),  # 获取评论内容并存储√
    re_path(r'^get_comments$', views.get_comments, name="get_comments"),  # 请求评论内容√
    re_path(r'^comments_good$', views.comments_good, name="comments_good"),  # 点赞√
    re_path(r"^get_name_status$", views.get_name_status, name="get_name_status"),  # 获取用户登录状态和用户名√
    re_path(r"^forget$", views.forget_pwd, name="forget_pwd"),  # 用户忘记密码 页面√
    re_path(r"^change_pwd$", views.change_pwd, name="change_pwd"),  # 接收数据，修改密码√
    re_path(r"^email_check_change_pwd$", views.email_check_change_pwd, name="email_check_change_pwd"),  # 修改密码验证邮件发送√
    re_path(r'^ckeditor_upload', views.ckeditor_img, name="ckeditor_img"),  # 获取富文本编辑器上传的图片√
    re_path(r"^status$", views.status, name="status"),  # 服务器设备信息页面√
    re_path(r"^get_status$", views.get_status, name="get_status"),  # 获取服务器设备信息√
    re_path(r'^get_csrf_token$', views.get_csrf_token),  # 获取csrf token
    re_path(r"^put_order$", views.put_order),  # 获取订单√
    re_path(r"^notify$", views.notify), # 支付校验
    re_path(r"^ban$", views.ban, name="ban"),  # 拦截IP√
    re_path(r"^ban_ip$", views.ban_ip, name="ban_ip"),  # 获取拦截ip信息列表√

    re_path(r'^test_resp', views.stream_video),  # 视频播放
    re_path(r'^video$', views.video_show),  # 视频播放

    re_path(r"^get_verify_img$", views.verify_img),  # 获取登录验证码√
]
