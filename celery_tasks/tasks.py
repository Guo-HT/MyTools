from celery import Celery
from MyTools import settings
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyTools.settings')
django.setup()

from Resume.models import *
# 创建一个Celery类的对象
#app = Celery("celery_tasks.tasks", broker="redis://:guoht990520_2_redis@127.0.0.1:6379/1")
from celery_tasks import app

# 定义任务函数
@app.task
def send_mail_register(to_email, verify_code):
    from django.core.mail import send_mail

    email_title = '来自 工具人的工具箱 的验证信息'
    email_body = f'''Email 地址验证

            尊敬的用户：

                这封信是由 工具人的工具箱 发送的。

                您收到这封邮件，是由于在 工具人的工具箱 进行了·~新用户注册~·，使用了这个邮箱地址。如果您并没有访问过 工具人的工具箱，或没有进行上述操作，请忽略这封邮件。您不需要退订或进行其他进一步的操作。

                注册验证码：  {verify_code}

                请谨慎操作。

                最后，祝您学业有成、工作顺利。

                *注：
                    站内所有工具均为注册用户上传，涉及版权问题的内容与本站开发者无关。

                '''
    email_dest = to_email  # 对方的邮箱

    send_status = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email_dest])
    if send_status:
        print("send_to:", email_dest, "   verify_code:", verify_code, "邮件发送成功，数据保存完成！")
    else:
        print("出现问题，邮件状态码：", send_status)


# 用户修改密码
@app.task
def send_mail_change_pwd(to_email, verify_code):
    from django.core.mail import send_mail
    email_title = '来自 工具人的工具箱 的验证信息'
    email_body = f'''Email 地址验证

            尊敬的用户：

                这封信是由 工具人的工具箱 发送的。

                您收到这封邮件，是由于在 工具人的工具箱 进行·~密码修改~·，使用了这个邮箱地址。如果您并没有访问过 工具人的工具箱，或没有进行上述操作，请忽略这封邮件。您不需要退订或进行其他进一步的操作。

                注册验证码：  {verify_code}

                请谨慎操作。

                最后，祝您学业有成、工作顺利。

                *注：
                    站内所有工具均为注册用户上传，涉及版权问题的内容与本站开发者无关。

                '''
    email_dest = to_email  # 对方的邮箱

    send_status = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email_dest])
    if send_status:
        print("send_to:", email_dest, "   verify_code:", verify_code, "邮件发送成功，数据保存完成！")
    else:
        print("出现问题，邮件状态码：", send_status)


# pdf转png
@app.task
def pdf2png(user_id, pdf_path, img_name):
    import time
    
    from pdf2image import convert_from_bytes
    from pdf2image.exceptions import (
        PDFInfoNotInstalledError,
        PDFPageCountError,
        PDFSyntaxError
    )

    images = convert_from_bytes(open(pdf_path, 'rb').read())
    for image in images:
        image.save(f'{settings.MEDIA_ROOT}/Resume/{img_name}.png', 'PNG')
        break
    resume = UserResume.objects.get(user_belong=user_id)

    resume.first_page_img = "Resume/"+img_name+".png"
    resume.save()
    print("pdf -> png 转换完成！！！")
