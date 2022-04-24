from django.contrib import admin
from .models import BlogType, Blog
# Register your models here.

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):  # 后台管理界面显示博文类型列表
    list_display = ('id', 'type_name')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):  # 后台管理界面显示博文列表
    list_display = ('id', 'title', 'blog_type', 'author', 'summary', 'get_read_num', 'created_time', 'last_updated_time')
