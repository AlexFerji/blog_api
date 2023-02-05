from django.contrib import admin

from .models import BlogPost, BlogComent


admin.site.register(BlogPost)
admin.site.register(BlogComent)
