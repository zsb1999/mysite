from django.contrib import admin
from  .models import ReadNum, ReadDetail
# Register your models here.

@admin.register(ReadNum)
class BlogTypeAdmin(admin.ModelAdmin):  # 后台管理界面显示博文类型列表
    list_display = ('read_num', 'content_object')

@admin.register(ReadDetail)
class BlogTypeAdmin(admin.ModelAdmin):  # 后台管理界面显示博文类型列表
    list_display = ('date', 'read_num', 'content_object')