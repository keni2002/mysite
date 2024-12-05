from django.contrib import admin
# Register your models here.
from .models import Post,Comment
#admin.site.register(Post)
#The @admin.register() decorator performs the same function as the admin.site.register() function that you replaced, registering the ModelAdmin class that it decorates


#DOESNT matter the name of class
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ["title",]}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active','created', 'updated']
    search_fields = ['name','email', 'body']

