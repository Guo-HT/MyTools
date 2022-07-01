from django.contrib import admin
from Resume.models import *


# Register your models here.
class ResumeAdmin(admin.ModelAdmin):
    """工具模型管理"""
    list_per_page = 20
    list_display = ['id', 'user_belong', 'file_name', 'resume_img', 'resume_show', 'resume_show2',  'watch_num', 'is_public','upload_time', 'change_time']
    list_filter = ['is_public']
    search_fields = ['id', 'user_belong', 'file_name']
    list_display_links = ['id', 'user_belong', 'file_name',]



admin.site.register(UserResume, ResumeAdmin)