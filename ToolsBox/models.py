from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import format_html
from MyTools import settings
#from fernet_fields import EncryptedCharField, EncryptedEmailField
from django.contrib.auth.hashers import make_password


# Create your models here.
class User(models.Model):
    # user_id = models.AutoField()  # 自动添加
    user_name = models.CharField(max_length=20, verbose_name="用户名")  # 用户名
    user_real_name = models.CharField(max_length=10, default="", verbose_name="真实姓名")  # 真实姓名
    user_password = models.CharField(max_length=255, verbose_name="密码")  # 密码
    user_email = models.EmailField(unique=True, default='', verbose_name="邮箱")
    user_reg_time = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")  # 注册时间

    class Meta:
        db_table = "user_info"  # 表名
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.user_name

    def save(self, *args, **kwargs):
        self.user_password = make_password(self.user_password, None, 'pbkdf2_sha256')
        super(User, self).save(*args, **kwargs)


class Tool(models.Model):
    # tool_id = models.AutoField()
    tool_name = models.CharField(max_length=30, verbose_name="工具名称")  # 工具名称
    # tool_describe = RichTextField(verbose_name="介绍")  # 工具介绍，富文本编辑器(不能传图)
    tool_describe = RichTextUploadingField(config_name="default", verbose_name="介绍")  # 工具介绍，富文本编辑器(可以上传图片)，有bug
    tool_file = models.FileField(upload_to="Files/", verbose_name="文件路径")  # 工具图标
    tool_icon = models.ImageField(upload_to="Icons/", verbose_name="图标路径")  # 文件
    tool_watch = models.IntegerField(default=0, verbose_name="浏览量")  # 浏览量
    tool_download = models.IntegerField(default=0, verbose_name="下载量")  # 下载量
    tool_upload_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")  # 更改时间
    tool_upload_user = models.ForeignKey("User", blank=True, null=True, on_delete=models.SET_NULL,
                                         verbose_name="上传用户")  # 上传用户
    tool_create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")  # 创建时间
    tool_is_checked = models.BooleanField(default=False, verbose_name="是否通过审核")  # 管理员是否审核

    class Meta:
        db_table = "tool_info"
        verbose_name = '工具'
        verbose_name_plural = '工具'

    def __str__(self):
        return self.tool_name

    def is_checked(self):
        if self.tool_is_checked:
            return "√"
        else:
            return "X"

    is_checked.admin_order_field = "tool_is_checked"  # 通过tool_is_checked排序
    is_checked.short_description = "是否通过审核"

    def tool_img(self):
        return format_html('<img src="{}{}" alt="" width="24"/>', settings.MEDIA_URL, self.tool_icon)  # 在后台管理列表显示图标
    tool_img.short_description = "图标"

    def summary(self):
        if len(self.tool_describe) > 10:
            return self.tool_describe[:10] + '...'
        else:
            return self.tool_describe

    summary.short_description = "简介"


class EmailVerify(models.Model):
    email_addr = models.EmailField(default='', verbose_name="邮箱地址")  # 邮箱目的地址
    verify_code = models.CharField(max_length=6, verbose_name="验证码")  # 发送的验证码
    send_time = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")  # 发送的时间

    class Meta:
        db_table = "email_verify"
        verbose_name = '邮箱验证'
        verbose_name_plural = '邮箱验证'

    def __str__(self):
        return self.email_addr


class History(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="浏览用户", null=True, blank=True)
    browse_history = models.ForeignKey("Tool", on_delete=models.CASCADE, verbose_name="浏览内容")
    browse_time = models.DateTimeField(auto_now_add=True, verbose_name="浏览时间")
    ip_addr = models.CharField(max_length=25, verbose_name="IP地址")

    class Meta:
        db_table = "browse_history"
        verbose_name = '浏览历史'
        verbose_name_plural = '浏览历史'

    def __str__(self):
        return self.browse_history.tool_name


class ToolComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="评论用户")
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, verbose_name="评论工具")
    comment_content = models.CharField(max_length=255, verbose_name="评论内容")
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name="发表时间")
    good = models.IntegerField(default=0, verbose_name="点赞量")

    class Meta:
        db_table = "tool_comment"
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        if len(self.comment_content) > 10:
            return self.comment_content[:10] + '...'
        else:
            return self.comment_content

    def summary(self):
        if len(self.comment_content) > 10:
            return self.comment_content[:10] + '...'
        else:
            return self.comment_content

    summary.short_description = "评论内容"


class DownloadHistory(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="下载用户")
    download_history = models.ForeignKey("Tool", on_delete=models.CASCADE, verbose_name="下载内容")
    download_time = models.DateTimeField(auto_now_add=True, verbose_name="下载时间")

    class Meta:
        db_table = "download_history"
        verbose_name = '下载历史'
        verbose_name_plural = '下载历史'

    def __str__(self):
        return self.download_history.tool_name


class SupportMe(models.Model):
    user = models.ForeignKey("User", blank=True, null=True, on_delete=models.CASCADE, verbose_name="打赏用户")
    pay_amount = models.FloatField(default=0.0, verbose_name="支付金额")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="下单时间")
    order_id = models.CharField(max_length=100, null=False, blank=False, verbose_name="订单号")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")
    pay_finish = models.BooleanField(default=False, verbose_name="是否完成交易")
    ip_addr = models.CharField(max_length=25, verbose_name="IP地址")

    class Meta:
        db_table = "support_me"
        verbose_name = '支付历史'
        verbose_name_plural = '支付历史'

    def __str__(self):
        return self.order_id
