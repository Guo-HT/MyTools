from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from Resume.models import *
from ToolsBox.models import *
from MyTools import settings
import time
from utils.pc_or_mobile import judge_pc_or_mobile


# Create your views here.
resume_count_each_page = 10

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

@timer
def index(request):
    return render(request, "resume/index.html")

@timer
@ensure_csrf_cookie
@login_required
def upload(request):
    return render(request, "resume/upload_resume.html")


# 保存上传的文件
def save_file(file_object, file_name):
    # 创建文件
    file_path = f"{settings.MEDIA_ROOT}/pdf/{file_name}.pdf"
    #print(file_path)
    with open(file_path, 'wb') as f:
        # 获取文件上传内容，写入文件
        for content in file_object.chunks():
            f.write(content)


@timer
@ensure_csrf_cookie
@login_required
def upload_file(request):
    import os
    from celery_tasks import tasks
    
    file_pdf = request.FILES["resume_pdf"]  # 文件
    file_name = request.POST.get("url_input")  # 文件名
    is_public = request.POST.get("is_public") # on || None 是否公开
    is_modify = request.COOKIES.get("resume_change") # 是否为更改
    user_id = request.session["user_id"]  # 用户id
    user_name = request.session["user_name"]  # 用户名

    user = User.objects.get(id=user_id)  # 用户存储对象
    is_public = True if is_public!=None else False
    if is_modify == "false":  # 新建简历  
        # 数据库！！！
        UserResume.objects.create(user_belong=user, is_public=is_public, file_name=file_name)
    
    elif is_modify=="true":  # 修改简历
        resume = UserResume.objects.get(user_belong=user_id)
        old_file_name = resume.file_name
        # print(settings.MEDIA_ROOT+"/pdf/"+old_file_name+".pdf")
        try:
            os.remove(settings.MEDIA_ROOT+"/pdf/"+old_file_name+".pdf")
        except Exception as e:
            print(e)
        resume.file_name = file_name
        resume.is_public = is_public
        resume.watch_num = 0
        resume.save()
    
    save_file(file_pdf, file_name)  # 保存文件
    tasks.pdf2png.delay(user_id, f"{settings.STATIC_ROOT}/pdf/{file_name}.pdf", file_name)

    myRedirect = HttpResponseRedirect("/resume/index")
    myRedirect.delete_cookie("resume_change")

    return myRedirect


@timer
@ensure_csrf_cookie
def have_resume(request):
    if request.session.has_key("user_id"):
        user_id = request.session["user_id"]
    else:
        return JsonResponse({"code": 200, "msg": "", "data":{"state":"none"}}, safe=False)
    resume_list = UserResume.objects.filter(user_belong=user_id)
    if len(resume_list):
        return JsonResponse({"code": 200, "msg": "", "data":{"state":"have", "file_name":resume_list[0].file_name}}, safe=False)
    else:
        return JsonResponse({"code": 200, "msg": "", "data":{"state":"none"}}, safe=False)

@timer
@ensure_csrf_cookie
def index_get_resumes(request):
    from django.core.paginator import Paginator
    import json
    import urllib.parse

    global resume_count_each_page

    resume_all = UserResume.objects.filter(is_public=True).order_by('-watch_num')   # 搜索所有
    paginator = Paginator(resume_all, resume_count_each_page)  # 每页几个
    cur_page = request.GET.get('group', default='1')  # 获得跳转页参数
    page_num = paginator.num_pages  # 获得总页数

    #print(f"请求：第{cur_page}页，共{page_num}页")
    if cur_page == "首页":
        cur_page = 1
    elif cur_page == "尾页":
        cur_page = page_num
    elif not cur_page.isdigit():
        try:
            user_input_page = urllib.parse.unquote(cur_page)
        except Exception as e:
            print(e)
        cur_page = 1
    try:
        data_list = paginator.page(cur_page).object_list  # 获取分页数据
    except:
        #print("超出页数")
        return JsonResponse({"code": 500, "msg": "分页错误", "data": {}}, safe=False)
    resume_list = []
    for resume in data_list:
        # id + 名称 + 图标链接 + 名字 + 介绍
        resume_data = dict()  # 构造单个工具的数据字典
        resume_data["user_belong"] = resume.user_belong.user_name
        resume_data["file_name"] = resume.file_name
        resume_data["first_img_path"] = str(resume.first_page_img)
        resume_list.append(resume_data)  # 加入总数据中
    
    data_send = {'total_page': page_num, 'cur_page': cur_page, 'resume_list': resume_list, 'media_url': settings.MEDIA_URL}
    # 返回：总页数，页码，数据
    return JsonResponse({"code": 200, "msg": "", "data": data_send}, safe=False)


@timer
@ensure_csrf_cookie
def show(request):
    return render(request, "resume/resume.html")

@timer
@ensure_csrf_cookie
def show2(request):
    return render(request, "resume/resume2.html")

@timer
def watch_num(request):
    file_name = request.GET.get("file_name")
    try:
        watching = UserResume.objects.get(file_name=file_name)
        # print(watching, watching.watch_num)
        watching.watch_num = watching.watch_num + 1
        watching.save()
    except Exception as e:
        print(e)
    return JsonResponse({"code": 200, "msg": "", "data": {"watch_num": watching.watch_num}}, safe=False)
