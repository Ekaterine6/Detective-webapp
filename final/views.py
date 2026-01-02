from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Post

def index(request):
    posts = Post.objects.all().order_by("-create_time")
    return render(request, "news/index.html", {
        "posts": posts
    })

@login_required
def create_post(request):
    return redirect("index")


