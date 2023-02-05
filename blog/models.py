from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from datetime import datetime
from user.models import CustomUser


# Create your models here.
def blog_user_files(instance, filename):
    date_time = datetime.now().strftime("%Y_%m_%d,%H:%M:%S")
    saved_file_name = instance.author.username + "-" + date_time + ".jpg"
    return 'profile/blog/{0}/{1}'.format(instance.author.username, saved_file_name, filename)


def coment_user_files(instance, filename):
    date_time = datetime.now().strftime("%Y_%m_%d,%H:%M:%S")
    saved_file_name = instance.author.username + "-" + date_time + ".jpg"
    return 'profile/coment/{0}/{1}'.format(instance.author.username, saved_file_name, filename)


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class BlogPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='posts',
                               null=True, on_delete=models.SET_NULL)
    title = models.CharField(_('Post title'), max_length=100)
    body = models.TextField(_('Post body'), max_length=1000)
    files = models.FileField(upload_to=blog_user_files)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = GenericRelation(Like)

    # class Meta:
    #     ordering = ("-created_at",)

    @property
    def total_likes(self):
        return self.likes.count()


    def __str__(self):
        return f"{self.title} by {self.author.username}"




class BlogComent(models.Model):
    post = models.ForeignKey(BlogPost, related_name='blog_comment', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='author_comment',
                               on_delete=models.CASCADE)
    body = models.TextField(max_length=150)
    file = models.FileField(upload_to=coment_user_files)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = GenericRelation(Like)

    # class Meta:
    #     ordering = ("-created_at",)

    @property
    def total_likes(self):
        return self.likes.count()


    def __str__(self):
        return f"{self.body[:20]} by {self.author}"



