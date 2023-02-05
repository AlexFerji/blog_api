from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_delete
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.dispatch.dispatcher import receiver
from django.core.mail import send_mail
from datetime import datetime

from .managers import CustomUserManager


def user_images(instance, filename):
    date_time = datetime.now().strftime("%Y_%m_%d,%H:%M:%S")
    saved_file_name = instance.user.username + "-" + date_time + ".jpg"
    return 'profile/{0}/{1}'.format(instance.user.username, saved_file_name, filename)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('Nickname'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    tos = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    class Meta:
        verbose_name = 'Список Пользователей'
        verbose_name_plural = 'Список Пользователей'

    def __str__(self):
        return self.email

    def email_user(self, *args, **kwargs):
        send_mail(
            '{}'.format(args[0]),
            '{}'.format(args[1]),
            '{}'.format(args[2]),
            [self.email],
            fail_silently=False,
        )


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to=user_images, default='profile/default/default.png')
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last_name'), max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{0} -- {1}'.format(
            self.user.email,
            self.image.url,
        )


@receiver(post_delete, sender=Profile)
def profile_image_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(True)