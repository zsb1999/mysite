from django.urls import path
from . import views
# 这里是blog app的路由 是分路由  需要在总路由文件中include

urlpatterns = [
    # 博文地址 http://localhost:8000/blog/1
    path('', views.blog_list, name = 'blog_list'),
    path('<int:blog_pk>', views.blog_detail, name = "blog_detail"),
    path('type/<int:blog_type_pk>', views.blogs_with_type, name = "blogs_with_type"),
    path('date/<int:year>/<int:month>', views.blogs_with_date, name = "blogs_with_date")
]


# 博客列表地址 http://localhost:8000/blog/


# 博文地址 http://localhost:8000/blog/1

# 首页地址 http://localhost:8000/  在总路由中设置