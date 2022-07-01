from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from MyTools import settings
from ToolsBox.models import User, Tool, EmailVerify, History, ToolComment, DownloadHistory, SupportMe
from django.db.models import Q
from pc_or_mobile import judge_pc_or_mobile
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.middleware.csrf import get_token
from django.views import View
from alipay import AliPay
import time
import re
import os
import mimetypes
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
from django.contrib.auth.hashers import check_password


# Create your views here.
# 每页显示的工具量
tool_count_each_page = 12

# 每个详情页几个评论
comments_each_page = 3

# 每个搜索页几个结果
tool_count_each_search_page = 12

# 允许上传的用户名列表
allowed_upload = ['superuser', 'lovelyq', 'bewind']


def root_index(request):
    return render(request, "index.html")


# 获取ip地址
def get_ip(request):
    # 获取ip地址
    if 'HTTP_X_FORWARDED_FOR' in  request.META:
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip


# 装饰器：判断是否登录，未登录则不允许访问
def login_required(view_func):
    def wrapper(requests, *view_args, **kwargs):
        # 判断用户是否登录        
        if requests.session.has_key('is_login'):
            # 已登录，调用对应视图
            return view_func(requests, *view_args, **kwargs)
        else:
            # 未登录，调转到登录页
            return redirect('/tools/login')

    return wrapper


# 装饰器，查看每个view的逻辑处理时间
def timer(func):
    def wrapper(*view_args, **kwargs):
        start = time.time()
        ret = func(*view_args, **kwargs)
        end = time.time()
        request = view_args[0]
        ip = "暂无IP地址"
        try:
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
        except Exception as e:
            print(e)
        ua = request.META["HTTP_USER_AGENT"]
        mobile = judge_pc_or_mobile(ua)
        try:    
            print(f"[* {func.__name__}, {ip}, {'移动端' if mobile else 'PC端'}, 用时{end - start}秒 *]")
        except Exception as e:
            print(e)
        return ret

    return wrapper


# 主页
@timer
@ensure_csrf_cookie
def index(requests):
    # 提取工具列表
    return render(requests, "ToolsBox/index.html")


# 前后端分离，获取csrf_token
@timer
def get_csrf_token(request):
    import addIpBan
    ip = get_ip(request)
    referer = request.META.get('HTTP_REFERER')  # 需要判断来路。否则会早上csrf_token任意申请
    server_host = request.META.get('HTTP_HOST')  # 判断服务器主机
    try:
        # 尝试获取get参数，以判断是否为本站的移动端程序
        mobile_csrf_password = request.GET.get("get_csrf_password")
    except Exception as e:
        mobile_csrf_password = ""
    # print(referer,type(referer) , server_host, type(server_host), mobile_csrf_password, type(mobile_csrf_password))
    
    if mobile_csrf_password != settings.get_csrf_password:
        # 不包括此参数，一律认为是攻击
        print(f"<< 攻击!!! {ip} 申请csrf_token，但并未成功!!! >>")
        addIpBan.main([ip])
        return JsonResponse({'token':'would i give you my token???'})
    elif referer.find(server_host) == -1 :
        #  包含guohtgo，但无referer，没想到可能会有这种情况
        pass
    else:
        token = get_token(request)
        return JsonResponse({'token': token})


# 获取用户名和登录状态
@timer
def get_name_status(requests):
    import json
    try:
        user_name_cookie = requests.COOKIES['user_name']
    except KeyError:
        user_name_cookie = ""
    if requests.session.has_key('is_login'):
        is_login = True
        user_name = requests.session["user_name"]
    else:
        is_login = False
        user_name = ''
    return JsonResponse(
        {"islogin": is_login, "user_name_sess": user_name, "user_name_cook": user_name_cookie}, safe=False)


# 登录页面
@timer
@ensure_csrf_cookie
def login(requests):
    ua = requests.META.get("HTTP_USER_AGENT")
    mobile = judge_pc_or_mobile(ua)
    try:
        # 查看是否有user_name的cookie 
        user_name = requests.COOKIES['user_name']
    except KeyError as e:
        # 没有记住的用户，设置为空
        user_name = ''
    # if mobile:
    #     #print("手机访问：", "cookie中记住的用户：", user_name)
    #     return render(requests, "ToolsBox/login_mobile.html")
    # else:
    #     #print("pc访问", "cookie中记住的用户：", user_name)
    #     return render(requests, "ToolsBox/login.html")
    return render(requests, "ToolsBox/login.html")


# 注册界面
@timer
@ensure_csrf_cookie
def register(requests):
    return render(requests, "ToolsBox/register.html")


# 注册功能实现
@timer
def reg_ajax(requests):
    from datetime import datetime, timedelta
    import pytz
    user_name = requests.POST.get("user_name")  # 提取上传用户名
    user_real_name = requests.POST.get("user_real_name")  # 提取上传年龄
    user_password = requests.POST.get("user_password")  # 提取上传密码
    user_email = requests.POST.get("user_email")  # 提取上传邮箱地址
    verify_code = requests.POST.get('verify_code')  # 提取上传验证码
    print("提交信息：" + user_name + '\t' + user_real_name + '\t' + user_password + '\t' + user_email + '\t' + verify_code)

    # 判断提交信息是否存在冲突
    same_name = User.objects.filter(Q(user_name=user_name) | Q(user_email=user_email))
    if len(same_name) == 0:
        # 检查验证码与邮箱是否匹配
        deadline = datetime.now() - timedelta(0, 60 * 5)

        # 查看5分钟内给该邮箱发送的验证码邮件
        verify_code_list = EmailVerify.objects.filter(email_addr=user_email, verify_code=verify_code, send_time__gt=deadline)
        if len(verify_code_list) != 0:
            # 如果发送成功，保存发送消息
            user_reg = User()
            user_reg.user_name = user_name
            user_reg.user_real_name = user_real_name
            user_reg.user_password = user_password
            # user_reg.user_reg_time = datetime.now(pytz.timezone('Asia/Shanghai'))
            user_reg.user_email = user_email
            user_reg.save()
            #print("数据保存成功！")
            return JsonResponse({"state": "OK"})
        else:
            return JsonResponse({"state": "wrong or timeout"})
    else:
        #print("数据未保存")
        return JsonResponse({"state": "name_exist"})



# 注册时的邮箱验证
@timer
def email_check(requests):
    from celery_tasks import tasks
    email_dest = requests.GET.get("user_email")
    verify_code = create_verify_code()
    email_exist = User.objects.filter(user_email=email_dest)
    if len(email_exist) == 0:
        # 存入Redis交给celery异步处理
        tasks.send_mail_register.delay(email_dest, verify_code)
        send_status=1
        if send_status:
            # 发送成功
            verify = EmailVerify()
            verify.email_addr = email_dest
            verify.verify_code = verify_code
            # verify.send_time = datetime.now(pytz.timezone('Asia/Shanghai'))  #这条字段设置为自动 
            try:
                verify.save()
            except Exception as e:
                print(e)
            print("send_to:", email_dest, "   verify_code:", verify_code, "邮件发送成功，数据保存完成！")
            return HttpResponse("ok")
        else:
            print("出现问题，邮件状态码：", send_status)
            return HttpResponse("error")
    else:
        print('邮箱被使用，退回！')
        return HttpResponse("email_exist")


# 修改密码
@timer
def change_pwd(requests):
    from datetime import datetime, timedelta
    import pytz

    email_addr = requests.POST.get('email')
    verify_code = requests.POST.get('verify')
    new_password = requests.POST.get('new_password')
    print("修改密码：", email_addr, verify_code, new_password)
    try:
        cur_user = User.objects.get(user_email=email_addr)
    except Exception as e:
        return HttpResponse("not_exist")
    else:
        deadline = datetime.now() - timedelta(0, 60 * 5)
        verify_check = EmailVerify.objects.filter(email_addr=email_addr, verify_code=verify_code,
                                                  send_time__gt=deadline)
        if len(verify_check):
            cur_user.user_password = new_password
            try:
                cur_user.save()
            except Exception as e:
                print("密码更改失败", e)
                return HttpResponse("failed")
        else:
            return HttpResponse("error")
    return HttpResponse("ok")


# 修改密码邮箱验证
@timer
def email_check_change_pwd(requests):
    from celery_tasks import tasks
    verify_code = create_verify_code()
    email_dest = requests.GET.get('user_email')  # 对方的邮箱
    print(verify_code, email_dest)
    email_exist = User.objects.filter(user_email=email_dest)
    print("更改密码验证消息发送:\t", email_dest, "\t", email_exist)
    if len(email_exist) != 0:
        # 如果该邮箱已绑定 
        tasks.send_mail_change_pwd.delay(email_dest, verify_code)
        # 发送成功
        verify = EmailVerify()
        verify.email_addr = email_dest
        verify.verify_code = verify_code
        # verify.send_time = datetime.now(pytz.timezone('Asia/Shanghai')) # 发送成功
        try:
            verify.save()
        except Exception as e:
            print(e)
        print("send_to:", email_dest, "   verify_code:", verify_code, "邮件发送成功，数据保存完成！")
        return HttpResponse("ok")
    else:
        print("邮箱未绑定")
        return HttpResponse("email_not_exist")


# 生成6位数字验证码
# @timer
def create_verify_code():
    from random import randint
    verify_list = []
    for i in range(6):
        verify_list.append(str(randint(0, 9)))
    verify_code = ''.join(verify_list)
    print(verify_code)
    # 返回值为str类型
    return verify_code


# 登录功能实现
@timer
def login_ajax(requests):
    name = requests.POST.get("name")
    pwd = requests.POST.get("password")
    remember_me = requests.POST.get("is_remember")
    print("用户提交：", name, '\t', pwd, '\t', remember_me)
    try:
        user_exist = User.objects.get(Q(user_name=name) | Q(user_email=name))  # 判断用户名是否存在
        try:
            # 用户确认存在，判断密码是否正确
            user_ok = User.objects.get(Q(user_name=name) | Q(user_email=name))  # 判断用户名密码是否匹配
            assert check_password(pwd, user_ok.user_password)
            # 没有抛出异常，则用户名、密码匹配
            #print("登录")
            requests.session['is_login'] = True
            requests.session['user_id'] = user_ok.id
            requests.session['user_name'] = user_ok.user_name
            requests.session['password'] = pwd
            requests.session.set_expiry(value=2*7*24*3600)  # session的过期时间为2周
            if remember_me.find("false") != -1:
                # 如果remember_me中有false字符串
                print("登录成功")
                try:
                    return JsonResponse({"state": "OK"})
                except Exception as e:
                    print(e)
                    return JsonResponse({"state": "OK"})
                    
            else:
                # 设置cookie
                response = JsonResponse({"state": "OK"})
                response.set_cookie("user_name", name)
                print("登录成功！")
                return response
        except Exception as e:
            print("密码错误！")
            return JsonResponse({"state": "password_error"})
    except Exception as e:
        print("没有该用户，登陆失败!")
        return JsonResponse({"state": "user_not_exist"})


# 登出功能实现
@timer
def logout(requests):
    if requests.GET.get('logout') == 'true':
        requests.session.clear()  # 删除session
        response = HttpResponse("logout_ok")
        response.delete_cookie("sessionid")  # 删除对应sessionid
        #print('登出')
        return response
    else:
        return HttpResponse("Nothing Done")


# 登陆后可实现文件上传
@timer
@login_required
def upload(requests):
    global allowed_upload

    user_name = requests.session['user_name']
    if user_name in allowed_upload:
        return render(requests, "ToolsBox/upload_file.html")
    else:
        return render(requests, "ToolsBox/refuse_upload.html")


# 上传文件，暂时为表单提交
@timer
def upload_ajax(requests):
    from datetime import datetime
    import pytz
    from pypinyin import lazy_pinyin

    # 获取上传文件的处理对象
    file = requests.FILES["tool_file"]
    file_icon = requests.FILES["tool_ico"]

    # 如果文件名包含中文
    if is_Chinese(file.name):
        pinyin_list = lazy_pinyin(file.name)
        file_name = "".join([char[0] for char in pinyin_list[:-1]])
        file_name += pinyin_list[-1]
    else:
        file_name = file.name
    file_name = file_name.lower()

    # 如果图标名包含中文
    if is_Chinese(file_icon.name):
        pinyin_list = lazy_pinyin(file_icon.name)
        file_icon_name = "".join([char[0] for char in pinyin_list[:-1]])
        file_icon_name += pinyin_list[-1]
    else:
        file_icon_name = file_icon.name
    file_icon_name = file_icon_name.lower()

    # 提取其他信息
    user_name = requests.session["user_name"]
    tool_name = requests.POST.get('tool_name')
    tool_intro = requests.POST.get('liasionContent')
    user_id = User.objects.filter(user_name=user_name)

    # 写入数据库
    Tool.objects.create(tool_name=tool_name, tool_describe=tool_intro, tool_file=f'Files/{file_name}',
                        tool_icon=f'Icons/{file_icon_name}',
                        # tool_upload_time=datetime.now(),
                        tool_upload_user_id=user_id[0].id)

    # 保存文件
    save_file(file, file_name)
    save_icon(file_icon, file_icon_name)
    del file
    del file_icon
    return redirect('/tools/index')


# 保存上传的文件
def save_file(file_object, file_name):
    # 创建文件
    file_path = f"{settings.MEDIA_ROOT}/Files/{file_name}"
    #print(file_path)
    with open(file_path, 'wb') as f:
        # 获取文件上传内容，写入文件
        for content in file_object.chunks():
            f.write(content)


# 保存上传的图标
def save_icon(file_object, file_name):
    file_path = f"{settings.MEDIA_ROOT}/Icons/{file_name}"
    #print(file_path)
    with open(file_path, 'wb') as f:
        for content in file_object.chunks():
            f.write(content)


# 判断字符串有无中文
def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


# 显示工具详情
@timer
@ensure_csrf_cookie
def tool_detail(requests, tool_id):
    try:
        # 检测工具id号是否存在，如果不存在，渲染500页面
        Tool.objects.get(id=tool_id)
    except:
        return render(requests, "500.html")
    return render(requests, "ToolsBox/tool_detail.html")


# 获取工具数据
@timer
def get_tool_info(requests):
    import json
    import re

    ip = get_ip(requests)

    tool_id = requests.GET.get("from_url")
    # 提取对应工具的对象
    try:
        tool_info = Tool.objects.get(id=tool_id, tool_is_checked=True)
    except Exception as e:
        return JsonResponse({"state":"is_not_checked"}, safe=False)
    # 浏览量+1
    tool_info.tool_watch += 1
    tool_info.save()

    # 检查用户登录状态
    if requests.session.has_key('is_login'):
        is_login = True
        user_name = requests.session["user_name"]
        user_id = requests.session['user_id']
        # 创建浏览历史记录
        watcher = User.objects.get(id=user_id)
        try:
            pre_history = History.objects.filter(user__id=watcher.id).order_by("-browse_time")[0]  # 获取上一个浏览记录
            if int(tool_id) == pre_history.browse_history.id:
                # 如果和当前浏览项一致，则不做浏览记录
                pass
            else:
                history = History()
                history.browse_history = tool_info
                history.user = watcher
                # history.browse_time = datetime.now(pytz.timezone('Asia/Shanghai'))
                history.ip_addr=ip
                # 保存浏览历史
                history.save()
                print(watcher, " 浏览了 ", tool_info)
        except Exception as e:
            # 如果新用户之前没有浏览记录，则抛异常，并做浏览记录
            history = History()
            history.browse_history = tool_info
            history.user = watcher
            # history.browse_time = datetime.now(pytz.timezone('Asia/Shanghai'))
            history.ip_addr=ip
            # 保存浏览历史
            history.save()
            print(watcher, " 浏览了 ",  tool_info)
    else:
        history = History()
        history.browse_history = tool_info
        # history.user = None
        # history.browse_time = datetime.now(pytz.timezone('Asia/Shanghai'))
        history.ip_addr=ip
        # 保存浏览历史
        history.save()
        print(f"某游客{ip}浏览了：", tool_info)
        is_login = False
        user_name = ''

    # 构造返回数据
    data = dict()
    data["tool_icon"] = str(tool_info.tool_icon) 
    data["tool_name"] = str(tool_info.tool_name) 
    data["tool_describe"] = str(tool_info.tool_describe)
    data["tool_watch"] = str(tool_info.tool_watch)
    data["tool_file"] = str(tool_info.tool_file)
    data["media_url"] = settings.MEDIA_URL
    data["is_login"] = is_login
    data["upload_time"] = tool_info.tool_create_time.strftime('%Y-%m-%d %H:%M:%S')
    return JsonResponse(data, safe=False)



# 显示搜索工具页
@timer
@ensure_csrf_cookie
def search_tool(requests, key):
    #print("请求页面:", key)
    return render(requests, "ToolsBox/tools_search.html")


# 搜索结果
@timer
def get_search_tool(requests):
    from django.core.paginator import Paginator
    from urllib.parse import urlparse
    import urllib
    import jieba
    import json
    import re

    # 每页几个
    global tool_count_each_search_page

    page = requests.GET.get("to_page")
    key_str = requests.GET.get("from_url")
    key_str = urllib.parse.unquote(key_str)
    # print("搜索关键词str：", key_str)

    # 处理搜索关键字
    # key_list = jieba.cut_for_search(key_str, HMM=True)  # 使用jieba的搜索引擎模式
    key_list = key_str.split(" ")
    q = Q()
    for key in key_list:
        q.add(("tool_name__icontains", key), Q.OR)
        q.add(("tool_describe__icontains", key), Q.OR)

    # 分词后搜索
    search_result = Tool.objects.filter(q, tool_is_checked=True).order_by("-tool_upload_time")

    paginator = Paginator(search_result, tool_count_each_search_page)
    page_num = paginator.num_pages  # 总页数 
    page_list = paginator.page_range  # 页码列表

    page = int(page)

    #print("搜索：", key_str, f"  共有 {len(search_result)} 条搜索记录")
    #print(f"请求：第{page}页， 共{page_num}页")
    data_list = paginator.page(page).object_list # 获取分页数据 
    data_dict = dict()
    i = 0
    for each in data_list:
        data_each = dict()
        data_each['tool_id'] = each.id
        data_each['tool_name'] = each.tool_name
        data_each['tool_describe'] = each.tool_describe
        data_each['tool_icon'] = str(each.tool_icon)
        data_dict[f'tool{i}'] = data_each
        i += 1

    data = {'total_count': len(search_result), "limit":tool_count_each_search_page,'key_str': key_str, 'page_num': page_num, "to_page": page, "tool_data": data_dict}
    return JsonResponse(data, safe=False)


# 访问当前用户的个人数据
@timer
@login_required
def get_personal_info(requests):
    import json
    import re

    from_url = requests.GET.get("from_url")
    user_name = from_url
    if requests.session['user_name'] != user_name:
        #print("用户请求了别人的主页")
        return JsonResponse({"state":"option denied"}, safe=False)

    user = User.objects.filter(user_name=user_name)[0]
    user_id = user.id
    #print("id为", user_id, '访问了个人主页')
    user_dict = dict()
    user_dict['user_name'] = user.user_name
    user_dict['user_real_name'] = user.user_real_name
    user_dict['user_email'] = user.user_email
    # user_dict['user_password'] = user.user_password
    user_dict['user_reg_time'] = user.user_reg_time.strftime('%Y-%m-%d %H:%M:%S')
    user_dict['id'] = user.id

    return JsonResponse(user_dict, safe=False)


# 获取个人主页
@timer
@ensure_csrf_cookie
@login_required
def personal(requests, user_name):
    if requests.session['user_name'] != user_name:
        print("用户请求了别人的主页")
        return render(requests, "ToolsBox/refuse_others_page.html")
    else:
        return render(requests, "ToolsBox/personal_detail.html")


# 获取用户浏览记录 ajax
@timer
@login_required
def get_browser_history(requests):
    import re
    from django.core.paginator import Paginator

    global tool_count_each_page

    from_url = requests.GET.get('from')
    page = requests.GET.get("page")
    user_name = from_url
    #print(user_name, '请求了浏览记录')
    history_list = History.objects.filter(user__user_name=user_name).order_by('-browse_time')
    total_count = len(history_list)
    paginator = Paginator(history_list, tool_count_each_page)
    page_num = paginator.num_pages

    history_list_page = paginator.page(page).object_list

    histories_list_ = []
    for history in history_list_page:
        history_dict = dict()
        history_dict['tool_id'] = history.browse_history.id
        history_dict['tool_name'] = history.browse_history.tool_name
        history_dict['history_time'] = history.browse_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        history_dict['tool_icon'] = str(history.browse_history.tool_icon)
        histories_list_.append(history_dict)
    data = {"history_list": histories_list_, "limit":tool_count_each_page,"total_count":total_count, "total_page":page_num, "cur_page":page}

    return JsonResponse(data, safe=False)


# 获取用户上传记录 ajax
@timer
@login_required
def get_upload_history(requests):
    import re
    from django.core.paginator import Paginator

    global tool_count_each_page
    from_url = requests.GET.get('from')
    page = requests.GET.get("page")
    user_name = from_url
    #print(user_name, '请求了上传记录')
    upload_list = Tool.objects.filter(tool_upload_user__user_name=user_name, tool_is_checked=True).order_by("-tool_create_time")
    total_count = len(upload_list)
    paginator = Paginator(upload_list, tool_count_each_page)
    page_num = paginator.num_pages
    
    upload_list_page = paginator.page(page).object_list
    
    # 获取json数据
    upload_list_ = []
    for upload_file in upload_list_page:
        upload_dict = dict()
        upload_dict['tool_id'] = upload_file.id
        upload_dict['tool_name'] = upload_file.tool_name
        upload_dict['upload_time'] = upload_file.tool_create_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        upload_dict["tool_icon"] = str(upload_file.tool_icon)
        upload_list_.append(upload_dict)
    data = {"upload_list": upload_list_, "limit":tool_count_each_page,"total_count":total_count, "total_page":page_num, "cur_page":page}

    return JsonResponse(data, safe=False)



# 获取用户下载记录 ajax
@timer
@login_required
def get_download_history(requests):
    import re
    from django.core.paginator import Paginator

    global tool_count_each_page

    from_url = requests.GET.get('from')
    page = requests.GET.get("page")
    user_name = from_url
    #print(user_name, '请求了下载记录')
    download_list = DownloadHistory.objects.filter(user__user_name=user_name).order_by("-download_time")
    total_count = len(download_list)
    paginator = Paginator(download_list, tool_count_each_page)
    page_num = paginator.num_pages

    download_list_page = paginator.page(page).object_list

    download_list_ = []
    for download_file in download_list_page:
        download_dict = dict()
        download_dict['tool_id'] = download_file.download_history.id
        download_dict['tool_name'] = download_file.download_history.tool_name
        download_dict['download_time'] = download_file.download_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        download_dict["tool_icon"] = str(download_file.download_history.tool_icon)
        download_list_.append(download_dict)
    data = {"download_list": download_list_, "limit":tool_count_each_page,"total_count":total_count, "total_page":page_num, "cur_page":page}
    return JsonResponse(data, safe=False)



# 下载量统计
@timer
@login_required
def download(requests):
    import re
    download_id = requests.GET.get('url')
    #print("下载：", download_id)
    tool = Tool.objects.get(id=download_id, tool_is_checked=True)
    tool.tool_download += 1
    tool.save()
    
    user_id = requests.session['user_id']

    down_his = DownloadHistory()
    down_his.user = User.objects.get(id=user_id)
    down_his.download_history = tool
    down_his.save()
    return JsonResponse({"state": "ok"})


# 主页获取工具信息
@timer
def get_tools(requests):
    from django.core.paginator import Paginator
    import json
    import urllib.parse

    global tool_count_each_page
    tools_all = Tool.objects.filter(tool_is_checked=True).order_by('-tool_upload_time')   # 搜索所有
    total_count = len(tools_all)
    paginator = Paginator(tools_all, tool_count_each_page)  # 每页几个
    cur_page = requests.GET.get('group', default='1')  # 获得跳转页参数
    page_num = paginator.num_pages  # 获得总页数

    #print(f"请求：第{cur_page}页，共{page_num}页")
    if cur_page == "首页":
        cur_page = 1
    elif cur_page == "尾页":
        cur_page = page_num
    elif not cur_page.isdigit():
        try:
            user_input_page = urllib.parse.unquote(cur_page)
            print(f"<< WARNING!!! {get_ip(requests)} 试图跳转内容：{user_input_page} >>")
        except Exception as e:
            print(e)
        cur_page = 1
    try:
        data_list = paginator.page(cur_page).object_list  # 获取分页数据
    except:
        #print("超出页数")
        return JsonResponse({'state': 'over_pages'})
    tool_list = {}
    i = 1
    for tool in data_list:
        # id + 名称 + 图标链接 + 名字 + 介绍
        tool_data = dict()  # 构造单个工具的数据字典
        tool_data["tool_id"] = tool.id
        tool_data["tool_name"] = tool.tool_name
        tool_data["tool_img_path"] = str(tool.tool_icon)
        tool_data["tool_intro"] = tool.tool_describe
        tool_list[f'tool_{i}'] = tool_data  # 加入总数据中
        i += 1
    data_send = {"limit": tool_count_each_page,'total_count': total_count, 'total_page': page_num, 'cur_page': cur_page, 'tool_list': tool_list, 'media_url': settings.MEDIA_URL}
    # 返回：总页数，页码，数据
    return JsonResponse(data_send, safe=False)


# 获取浏览和下载量前10的
@timer
def get_top_ten(requests):
    try:
        import json
        watch_top_ten = Tool.objects.filter(tool_is_checked=True).order_by('-tool_watch')[:10]
        download_top_ten = Tool.objects.filter(tool_is_checked=True).order_by('-tool_download')[:10]
        i = 0
        watch_dict = dict()
        for watch in watch_top_ten:
            each_dict = dict()
            each_dict['id'] = str(watch.id)
            each_dict['name'] = watch.tool_name
            each_dict['count'] = str(watch.tool_watch)
            watch_dict[f'{i}'] = each_dict
            i += 1
        i = 0
        download_dict = dict()
        for download_ in download_top_ten:
            each_dict = dict()
            each_dict['id'] = str(download_.id)
            each_dict['name'] = download_.tool_name
            each_dict['count'] = str(download_.tool_download)
            download_dict[f'{i}'] = each_dict
            i += 1

        dict_result = dict()
        dict_result["watch"] = watch_dict
        dict_result["download"] = download_dict

        return JsonResponse(dict_result, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({"state":e}, safe=False)

# 获取评论内容并存储
@timer
@login_required
def submit_comment(requests):
    import re
    user_id = requests.session['user_id']
    comment_content = requests.GET.get("text")
    from_tool_id = requests.GET.get("from")
    #print(f"用户{user_id} 对 工具{from_tool_id} 发表了评论")
    comment = ToolComment()
    comment.comment_content = comment_content
    comment.user = User.objects.get(id=user_id)
    comment.tool = Tool.objects.get(id=from_tool_id)
    comment.save()
    return HttpResponse("ok")


# 提取评论信息，并在工具详情页面显示
@timer
def get_comments(requests):
    from django.core.paginator import Paginator
    import re
    import json

    global comments_each_page

    from_tool_id = requests.GET.get("from")
    to_page = requests.GET.get("to_page")
    comments_all = ToolComment.objects.filter(tool=from_tool_id).order_by('-comment_time')
    paginator = Paginator(comments_all, comments_each_page)  # 每页几个
    page_num = paginator.num_pages  # 总共有几页
    data_list = paginator.page(to_page).object_list  # 获取当页数据
    comment_count = len(comments_all)
    comment_data = dict()
    i = 0
    for each in data_list:
        comment_each = dict()
        comment_each['user_name'] = User.objects.get(id=each.user.id).user_name
        comment_each['content'] = each.comment_content
        comment_each['time'] = each.comment_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        comment_each['good'] = str(each.good)
        comment_data[f'comment{i}'] = comment_each
        i += 1

    data_send = {'limit':comments_each_page, 'total_page': page_num, 'comment_count': comment_count, 'cur_page': to_page,
                 'comment_list': comment_data}
    # 返回：总页数，页码，数据
    return JsonResponse(data_send, safe=False)


# 统计点赞个数
@timer
def comments_good(requests):
    import re

    from_tool_id = requests.GET.get("from")
    user_name = requests.GET.get("user")
    comment_time = requests.GET.get("time")
    #print('点赞', from_tool_id, user_name, comment_time)
    result = ToolComment.objects.get(user__user_name=user_name, tool_id=from_tool_id, comment_time=comment_time)
    print(result)
    result.good += 1
    result.save()
    return HttpResponse('ok')


# 忘记密码页面
@timer
@ensure_csrf_cookie
def forget_pwd(requests):
    return render(requests, "ToolsBox/forget_pwd.html")


# 接受富文本编辑器的图片
@csrf_exempt
@timer
def ckeditor_img(request):
    import time
    if request.method == 'POST':
        callback = request.POST.get('CKEditorFuncNum')
        file_name = ''
        file_time = ''
        f = request.FILES["upload"]
        try:
            file_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
            path = settings.MEDIA_ROOT + 'ckeditor/' + file_time

            file_name = path + "_" + f.name
            with open(file_name, "wb+") as des_origin_f:
                for chunk in f.chunks():
                    des_origin_f.write(chunk)
        except Exception as e:
            print(e)
        try:
            response_data = {
                "uploaded": 1,
                "fileName": f"{file_time}_{f.name}",
                "url": f"{settings.MEDIA_URL}ckeditor/{file_time}_{f.name}"
            }
            #print(response_data)
            return JsonResponse(response_data, safe=False)
        except Exception as e:
            print("图片上传错误:", e)
            return JsonResponse({"uploaded": 0, "error": {"message": e}})
    else:
        raise Http404()



# 查看设备信息
@timer
@ensure_csrf_cookie
def status(requests):
    return render(requests, "ToolsBox/status.html")


# 获取设备信息
@timer
def get_status(requests):
    import json
    import psutil
    import datetime
    try:
        # 逻辑处理器占用率
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", 'r') as temp_file:
                cpu_temp = int(temp_file.read()) / 1000
        except Exception as e:
            cpu_temp = '无法获取'
        cpu_total_percent = psutil.cpu_percent(interval=0.1)
        cpu_percent = psutil.cpu_percent(interval=0.1, percpu=True)
        for i in range(len(cpu_percent)):
            cpu_percent[i] = str(cpu_percent[i]) + "%"
        cpu_info = dict()
        cpu_info["cpu_total_percent"] = str(cpu_total_percent) + '%'
        cpu_info["cpu_core_percent"] = str(cpu_percent)
        cpu_info['cpu_temp'] = str(cpu_temp)

        # 内存信息
        mem = psutil.virtual_memory()
        # 总内存
        mem_total = round(mem.total / (1024 * 1024 * 1024), 2)
        # 内存使用率
        mem_percent = mem.percent
        # 内存可用
        mem_available = round(mem.available / (1024 * 1024 * 1024), 2)
        mem_info = {"mem_total": str(mem_total) + "G", "mem_available": str(mem_available) + "G",
                    "mem_percent": str(mem_percent) + "%"}

        # 磁盘信息
        disk_usage = psutil.disk_usage('/') 
        # 磁盘总空间
        disk_total = round(disk_usage.total / (1024 * 1024 * 1024), 2)
        # 磁盘使用率
        disk_percent = disk_usage.percent
        disk_info = {"disk_total": str(disk_total) + "G", "disk_percent": str(disk_percent) + "%"}

        # 开机时间信息
        open_date = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d,%H:%M:%S")
        open_time = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
        open_info = {"open_date": open_date, "open_time": str(open_time)}

        pc_status = {"cpu_info": cpu_info, "mem_info": mem_info, "disk_info": disk_info, "open_info": open_info}
        return JsonResponse(pc_status)
    except Exception as e:
        print("设备信息错误:", e)
        return JsonResponse({"state":"error 500"})


# 渲染命令行窗口
@timer
@ensure_csrf_cookie
def cmd(requests):
    return render(requests, "ToolsBox/cmd.html")


# 获得、执行命令
@timer
def cmd_run(requests):
    import subprocess

    cmd = requests.POST.get("cmd")
    print(cmd.split(" "))
    if cmd.find("shutdown")!=-1 or cmd.find("halt")!=-1:
        return HttpResponse("['想peach']")
    command = cmd.split(" ")
    content = subprocess.Popen(command, stdout=subprocess.PIPE)
    content.wait()
    lines = content.stdout.readlines()
    list_cmd = [line.decode('utf8') for line in lines]
    #print(list_cmd)
    return HttpResponse(str(list_cmd))


# 企业微信出门页面
@timer
def go_out(requests):
	return render(requests, "others/GoOut.html")


# vue.js计算器
@timer
def cal(requests):
    return render(requests, "others/calculator.html")


# 读取项目私钥
#@timer
def open_my_private_key():
    with open("./alipay_keys/app_private_key.pem", "r") as my_private_key:
        return my_private_key.read()


# 读取支付宝公钥
#@timer
def open_alipay_public_key():
    with open("./alipay_keys/alipay_public_key.pem", "r") as alipay_public_key:
        return alipay_public_key.read()
    

# 获取订单，返回支付地址
#@timer
def put_order(request):
    import time
    try:
        ip = get_ip(request)
        # 生成订单、订单状态、带付款、已付款、付款失败等
        order_id = f"{str(time.time())}"
        amount = 5
        my_alipay = MyAliPay()
    
        # 身份识别+信息存储
        if request.session.has_key("is_login"):
            user_name = request.session["user_name"]
            user_fk = User.objects.filter(user_name=user_name)[0]
            print(user_fk)
            print(f"{user_name}来掏钱了")
            SupportMe.objects.create(user=user_fk, pay_amount=amount, order_id=order_id,pay_finish=False, ip_addr=ip)
        else:
            user_name = "游客"
            #print("游客来掏钱")
            SupportMe.objects.create(pay_amount=amount, order_id=order_id,pay_finish=False, ip_addr=ip)
        # print(f"order_id:{order_id}")
        pay_url = my_alipay.get_trade_url(order_id, amount)
        return JsonResponse({"pay_url": pay_url}, safe=False)
    except Exception as e:
        print(e)
        print(e.__traceback__.tb_lineno)


class MyAliPay(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.alipay = AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_private_key_string=open_my_private_key(),
            alipay_public_key_string=open_alipay_public_key(),
            app_notify_url=None,
            sign_type="RSA2",
            debug=True,
        )
        #except Exception as e:
        #    print(e)
        #    print(e.__traceback__.tb_lineno)
    
    def get_trade_url(self, order_id, amount):
        order_string = self.alipay.api_alipay_trade_page_pay(
            subject="支持一下“工具人的工具箱”",
            out_trade_no = order_id,  # 订单号
            total_amount=amount,  # 订单金额
            return_url=settings.ALIPAY_RETURN_URL,
            notify_url=settings.ALIPAY_NOTIFY_URL
        )
        return "https://openapi.alipaydev.com/gateway.do?"+order_string


# 回调验证
@timer
@csrf_exempt
def notify(requests):
    import datetime
    notify_dict = dict()
    for key, value in requests.POST.items():
        notify_dict[key] = value
        #print(key + "~~~" + value)
    try:
        order_detail = SupportMe.objects.get(order_id=notify_dict["out_trade_no"])
        # print("查询出结果")
        order_detail.pay_time=datetime.datetime.strptime(notify_dict["gmt_payment"],"%Y-%m-%d %H:%M:%S")
        order_detail.pay_finish=True
        order_detail.save()
        #print("notify成功")
        return HttpResponse("success")
    except Exception as e:
        """
            gmt_create~~~2021-06-26 00:17:39
            charset~~~utf-8
            gmt_payment~~~2021-06-26 00:17:48
            notify_time~~~2021-06-26 00:17:49
            subject~~~支持一下“工具人的工具箱”
            sign~~~w8+LymyWkAjgj0n+2oGSzgeH+OoVm1zQUZCcz2zwYHDcQ6WYCVBzpoxOMNmC5Jpb9jnhwgqWBh/U/nSfc/G6nJGqq7bGn2PfO5woHA+zZaGgscY1EqmIEpCWVxOcsq7XBdop+2JclPQySH/sClPWcO6eSThITfbzLGoc6YL/66rv4Kx9wBixoMtU6nxSXCcS0SyP0lz1FBZqS6zdeahHpo4dHrtzOpIb6WoAzCCPAjNOlinrc5STENAiMaJnrVe3lBoH2CuR01rpg63Xy/3gIhb1oyFRxpqVWKJ4d+6uN4Mmq4wU8cITKd/A0cLwOpvISKnG8+n+Vwt5TPoCG9I7mg==
            buyer_id~~~2088622956137821
            invoice_amount~~~5.00
            version~~~1.0
            notify_id~~~2021062600222001749037820513031614
            fund_bill_list~~~[{"amount":"5.00","fundChannel":"ALIPAYACCOUNT"}]
            notify_type~~~trade_status_sync
            out_trade_no~~~1624637844.1788201
            total_amount~~~5.00
            trade_status~~~TRADE_SUCCESS
            trade_no~~~2021062622001437820501386287
            auth_app_id~~~2021000117676739
            receipt_amount~~~5.00
            point_amount~~~0.00
            app_id~~~2021000117676739
            buyer_pay_amount~~~5.00
            sign_type~~~RSA2
            seller_id~~~2088621955964500
        """
        #print("notify失败", e)
        return HttpResponse("fail")        


def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data


# 视频流媒体
@timer
def stream_video(request):
    """将视频文件以流媒体的方式响应"""
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    path = request.GET.get('path')
    print(path)
    try:
        path = settings.MEDIA_ROOT + path  # path就是template ？后面的参数的值
        size = os.path.getsize(path)
        content_type, encoding = mimetypes.guess_type(path)
        content_type = content_type or 'application/octet-stream'
        if range_match:
            first_byte, last_byte = range_match.groups()
            first_byte = int(first_byte) if first_byte else 0
            last_byte = first_byte + 1024 * 1024 * 10
            if last_byte >= size:
                last_byte = size - 1
            length = last_byte - first_byte + 1
            resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206,
                                         content_type=content_type)
            resp['Content-Length'] = str(length)
            resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
        else:
            resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
            resp['Content-Length'] = str(size)
        resp['Accept-Ranges'] = 'bytes'
        return resp
    except Exception as e:
        print(e)
        return HttpResponse(status=404)


# 视频播放页面
@timer
@ensure_csrf_cookie
def video_show(requests):
    return render(requests, "ToolsBox/video.html")


# 获取屏蔽ip地址
@timer
def ban_ip(request):
    try:
        from getBanIp import get_ban_ip
        ban_ips = get_ban_ip()
        data = {"data":ban_ips} 
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return HttpResponse("something error!")

@timer
def ban(request):
   return render(request, "ToolsBox/ban_ip.html")

@timer
def love(request):
    return render(request, "ToolsBox/heart_jump.html")


@timer
def paceCal(request):
    return render(request, "ToolsBox/paceCal.html")

@timer
def resume(request, name):
    print(name,"的简历")
    return render(request, "ToolsBox/resume.html", {
        "name": name,
    })


@timer
def resume2(request, name):
    print(name,"的简历")
    return render(request, "ToolsBox/resume2.html", {
        "name": name,
    })
