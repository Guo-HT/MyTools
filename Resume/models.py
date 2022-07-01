from django.db import models
from django.utils.html import format_html
from ToolsBox.models import *

# Create your models here.
class UserResume(models.Model):
    user_belong = models.ForeignKey(User, blank=False, null=False, on_delete=models.DO_NOTHING, verbose_name="所属用户")
    is_public = models.BooleanField(default=True, verbose_name="是否公开")
    file_name = models.TextField(max_length=20, verbose_name="文件名")
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")
    change_time = models.DateTimeField(auto_now=True, verbose_name="更改时间")
    watch_num = models.IntegerField(default=0, verbose_name="浏览量")
    first_page_img = models.ImageField(upload_to="Resume/", blank=True, null=True, verbose_name="简历封面")

    class Meta:
        db_table = "user_resume"
        verbose_name = '用户简历'
        verbose_name_plural = '用户简历'

    def __str__(self):
        return self.file_name
    
    def resume_img(self):
        return format_html('<img src="{}{}" alt="" width="24"/>', settings.MEDIA_URL, self.first_page_img)  # 在后台管理列表显示图标
    resume_img.short_description = "图标"

    def resume_show(self):
        return format_html('<a href="/resume/show/{}" title="简历链接" target="_blank">简历链接1</a>', self.file_name)  # 在后台管理列表显示简历链接
    resume_show.short_description = "简历链接1"

    def resume_show2(self):
        return format_html('<a href="/resume/show2/{}" title="简历链接" target="_blank">简历链接2</a>', self.file_name)  # 在后台管理列表显示简历链接
    resume_show2.short_description = "简历链接2"
