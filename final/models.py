from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pro_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    bio = models.TextField(blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()
    media = models.FileField(upload_to="post_media/", blank=True, null=True)

    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

