from django.db import models
from  django.contrib.auth.models import User  # 这时Django自带的用户模型
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from read_statistics.models import ReadNumExpandMethod,ReadDetail
# Create your models here.

class BlogType(models.Model): # 博文类型的模型，对博文分类
	type_name = models.CharField(max_length = 15)	# 分类名字段

	def __str__(self):  # 显示类型的名称
		return self.type_name

class Blog(models.Model, ReadNumExpandMethod):	# 创建博文模型，添加博文字段
	title = models.CharField(max_length = 50)  # 文章标题字段
	blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
	summary = models.TextField()  # 文章摘要字段
	#readed_num = models.IntegerField(default=0)
	content = RichTextField()				# 文章内容字段
	author = models.ForeignKey(User, on_delete=models.CASCADE) # 文章作者字段
	read_details= GenericRelation(ReadDetail)
	created_time = models.DateTimeField(auto_now_add = True)	# 创建时间字段
	last_updated_time = models.DateTimeField(auto_now = True)	# 最新更新时间字段

	def __str__(self):
		return "<Blog: %s>" % self.title

	class Meta:
		ordering = ['-created_time']