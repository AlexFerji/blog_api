from django.contrib import admin

from .models import BlogPost, BlogComent, Like


admin.site.register(BlogPost)
admin.site.register(BlogComent)
admin.site.register(Like)