from django.contrib import admin
from ToolsBox.models import User, Tool, EmailVerify, History, ToolComment, DownloadHistory, SupportMe


# Register your models here.
class ToolsAdmin(admin.ModelAdmin):
    """工具模型管理"""
    list_per_page = 20
    list_display = ['id', "tool_name", 'summary', 'tool_upload_user', 'tool_watch', 'tool_download', 'tool_img', 'tool_create_time', 'tool_upload_time','is_checked']
    list_filter = ['tool_is_checked']
    search_fields = ['tool_name', 'tool_describe', 'tool_upload_user__user_name']
    list_display_links = ['id', "tool_name", 'summary']

    def set_tools_passed(self, request, queryset):
        rows_updated = queryset.update(tool_is_checked=True)
        self.message_user(request, f"{rows_updated}个工具成功通过审核")

    set_tools_passed.short_description = "设置为”通过审核”"

    def set_tools_failed(self, request, queryset):
        rows_updated = queryset.update(tool_is_checked=False)
        self.message_user(request, f"{rows_updated}个工具被拒绝通过审核")

    set_tools_failed.short_description = "设置为“不通过审核”"

    def set_watch_zero(self, request, queryset):
        row_update = queryset.update(tool_watch=0)
        self.message_user(request, f"{row_update}个工具的浏览量置0")

    set_watch_zero.short_description = "浏览量 置0"

    def set_download_zero(self, request, queryset):
        row_update = queryset.update(tool_download=0)
        self.message_user(request, f"{row_update}个工具的浏览量置0")

    set_download_zero.short_description = "下载量 置0"

    actions = [set_tools_passed, set_tools_failed, set_watch_zero, set_download_zero]


class UserAdmin(admin.ModelAdmin):
    """用户信息管理"""
    list_per_page = 30
    list_display = ['id', 'user_name', 'user_email', 'user_reg_time']
    search_fields = ['id', 'user_name', 'user_email']
    list_display_links = ['id', 'user_name', 'user_email']

    def delete(self, request, queryset):
        rows_delete = queryset.delete()
        self.message_user(request, f"{rows_delete[0]}条数据被删除。")

    delete.short_description = "删除选中的 用户信息"
    actions = [delete]


class HistoryAdmin(admin.ModelAdmin):
    """历史记录管理"""
    list_per_page = 50
    list_display = ['user', 'browse_history', 'browse_time', 'ip_addr']
    search_fields = ['user__user_name', 'browse_history__tool_name', 'ip_addr']
    list_display_links = ['user', 'browse_history']

    def delete(self, request, queryset):
        rows_delete = queryset.delete()
        self.message_user(request, f"{rows_delete[0]}条数据被删除。")

    delete.short_description = "删除选中的 浏览历史"
    actions = [delete]


class EmailVerifyAdmin(admin.ModelAdmin):
    """邮箱验证管理"""
    list_per_page = 30
    list_display = ['email_addr', 'verify_code', 'send_time']
    search_fields = ['email_addr', 'verify_code']
    list_display_links = ['email_addr', 'verify_code']
    actions_on_top = True

    def delete(self, request, queryset):
        rows_delete = queryset.delete()
        self.message_user(request, f"{rows_delete[0]}条数据被删除。")

    delete.short_description = "删除选中的 验证信息"
    actions = [delete]


class ToolCommentAdmin(admin.ModelAdmin):
    """评论信息管理"""
    list_per_page = 30
    list_display = ['user', 'tool', "summary", "good", "comment_time"]
    search_fields = ['user__user_name', 'tool__tool_name', "comment_content"]
    list_display_links = ['user', 'tool', "summary", "good"]

    def delete(self, request, queryset):
        rows_delete = queryset.delete()
        self.message_user(request, f"{rows_delete[0]}条数据被删除。")

    delete.short_description = "删除选中的 评论"
    actions = [delete]


class DownloadHistoryAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ['user', "download_history", "download_time"]
    search_fields = ["user", "download_history"]
    list_display_links = ["user", "download_history"]

    def delete(self, request, queryset):
        rows_delete = queryset.delete()
        self.message_user(request, f"{rows_delete[0]}条数据被删除。")

    delete.short_description = "删除选中的 下载记录"
    actions = [delete]


class SupportMeAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ["id", "user", "pay_amount", "order_id", "create_time", "pay_time", "pay_finish", "ip_addr"]
    search_fields = ["user", "pay_amount", "order_id"]
    list_display_links = ["user", "pay_amount", "order_id"]
    list_filter = ['pay_finish']

admin.site.register(User, UserAdmin)
admin.site.register(Tool, ToolsAdmin)
admin.site.register(EmailVerify, EmailVerifyAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(ToolComment, ToolCommentAdmin)
admin.site.register(DownloadHistory, DownloadHistoryAdmin)
admin.site.register(SupportMe, SupportMeAdmin)

admin.site.site_title = "ToolsBox后台管理"
admin.site.site_header = "ToolsBox后台管理"
admin.site.disable_action('delete_selected')
