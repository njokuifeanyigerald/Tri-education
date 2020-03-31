from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor.fields import RichTextField

User = get_user_model()

class PostView(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Signup(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField()

    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = 'authors'

class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'categories'

class Post(models.Model):
    title = models.CharField(max_length=70)
    overview = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    content = RichTextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    prev_post = models.ForeignKey('self', related_name='prev',on_delete=models.SET_NULL, null=True, blank=True)
    next_post = models.ForeignKey('self', related_name='next',on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        verbose_name_plural = 'posts'
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('post', kwargs={'id': self.id})

    def get_update_url(self):
        return reverse('post-update', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('post-delete', kwargs={'id': self.id})

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

class Comments(models.Model):
    name = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'comments'


