from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


# user profiles
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pro_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    bio = models.TextField(blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

# posts/news
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()

    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    event_date = models.DateField()

    def __str__(self):
        return self.title
    

# pictures
class PostImg(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="post_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)



# creating "cases"
class Case(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cases")
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

# case "evidence"
# adding posts to cases
class CaseEvidence(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="evidence")
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.post.title} -> {self.case.title}"


# comments
class Comments(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} on {self.case.title}"


# notes for the board
class Notes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=100)
    text = models.TextField(blank=True)
    top = models.IntegerField(default=100)
    left = models.IntegerField(default=200)
    note_type = models.CharField(max_length=20, default="clue")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"
