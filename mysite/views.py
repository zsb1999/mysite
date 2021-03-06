import datetime
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from blog import models
from blog.models import Blog
from read_statistics.utils import get_seven_days_read_date, get_today_hot_data,get_yesterday_hot_data


def get_seven_day_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects\
                .filter(read_details__date__lt = today, read_details__date__gte = date)\
                .values('id', 'title')\
                .annotate(read_num_sum = Sum('read_details__read_num'))\
                .order_by('-read_num_sum')
    return blogs[:7]

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_date(blog_content_type)
    # 获取七天热门博客缓存数据

    context = {}
    context['blog_types'] = models.BlogType.objects.all()
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['seven_day_hot_data'] = get_seven_day_hot_blogs()
    return render(request,'home.html', context)

def blog_list2(request):  # 该方法将博客的类型返回给base.html 因为导航栏需要使用
    # 处理方法：显示博客列表
    context = {} # 字典：存放所有博文对象
    context['blog_types'] = models.BlogType.objects.all() # 返回所有的博客类型
    return render(request,'base.html', context)  # 将context返回到 blog_list.html文件

