from django.shortcuts import  get_object_or_404,render
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from read_statistics.utils  import read_statistics_one_read
from .models import Blog, BlogType
#from user.forms import LoginForm

# 控制前端页面的显示
# Create your views here.

def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 每十篇博客作为一页
    page_num = request.GET.get('page', 1)  # 获取url的页面参数 ?page = page_num
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number  # 获取当前页码
    # page_range = [current_page_num - 2, current_page_num - 1, current_page_num,current_page_num + 1,current_page_num+2]
    # 第14个视频 19分处
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 加上省略
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取日期归档对应博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order= "DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year = blog_date.year,
                            created_time__month = blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}  # 字典：存放所有博文对象
    context['blogs'] = page_of_blogs.object_list  # 获取所有的博文，并赋值给字典
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count = Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return context

def blog_list(request):  # 该方法将博文列表显示到前端页面
    # 处理方法：显示博客列表
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request,'blog/blog_list.html', context)  # 将context返回到 blog_list.html文件

def blogs_with_type(request, blog_type_pk):   # 该方法按类型分类博文，同一类型的博文展现在同一界面

    blog_type = get_object_or_404(BlogType, pk = blog_type_pk) # 获取BlogType模型中的 类型名
    blogs_all_list = Blog.objects.filter(blog_type = blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type

    return render(request,'blog/blogs_with_type.html', context)

def blogs_with_date(request, year, month):

    blogs_all_list = Blog.objects.filter(created_time__year = year, created_time__month = month)
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request,'blog/blogs_with_date.html', context)

def blog_detail(request, blog_pk):  # 该方法显示博文细节内容
    # blog_pk是博文的id，是唯一标识
    blog = get_object_or_404(Blog, id=blog_pk)  # 根据传递进来的id，获取对应的博文对象，
    read_cookie_key  = read_statistics_one_read(request, blog)
    #blog_content_type = ContentType.objects.get_for_model(blog)
    #comments = Comment.objects.filter(content_type = blog_content_type, object_id = blog_pk, parent = None)
    context = {}
    context['blog'] = blog
    context['blog_types'] = BlogType.objects.all()
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    #context['login_form'] = LoginForm()
    #context['comment_count'] = Comment.objects.filter(content_type = blog_content_type, object_id = blog_pk).count()
    #context['comment_form'] = CommentForm(initial={'content_type':blog_content_type.model,'object_id':blog_pk, 'reply_comment_id':'0'})

    response = render(request,'blog/blog_detail.html', context) # 将对应的博文对象返回到前端页面中
    response.set_cookie(read_cookie_key, 'true') # 已阅读cookie标记
    return response