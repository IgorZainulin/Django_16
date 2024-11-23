from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

class PostsAdmin(admin.ModelAdmin):
    list_display = ('author', 'header', 'create_time', 'rating')

    list_filter = ('author__user__username', 'create_time', 'rating')



admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostsAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)

