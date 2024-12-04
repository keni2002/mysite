from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

#model manager good
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
        .filter(status=Post.Status.PUBLISHED)



class Post(models.Model):
    #inherit enum?
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED  = 'PB', 'Published'
        #names     values   labels

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    #go to model User, and ask User likrd=>blog_post do yo have?

    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status  = models.CharField(max_length=2,choices=Status.choices, default=Status.DRAFT)

    #model manager
    objects = models.Manager() #default
    published = PublishedManager() #my custome manager


    class Meta:
        ordering = ['-publish']
        #provide index, improve performance for queries filtering
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title