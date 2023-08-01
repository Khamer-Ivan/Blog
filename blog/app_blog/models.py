from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    name = models.TextField(default='', verbose_name='Name')
    email = models.EmailField(verbose_name='Your email')


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=100, blank=True)
    body = models.TextField(default='', verbose_name='Post text')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

