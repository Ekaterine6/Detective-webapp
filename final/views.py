from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Post

def index(request):
    posts = Post.objects.all().order_by("-create_time")
    return render(request, "index.html", {
        "posts": posts
    })

@login_required
def create_post(request):
    if request.method == "POST":
        Post.objects.create(
            author=request.user,
            title=request.POST["title"],
            body=request.POST["body"],
            country=request.POST["country"],
            city=request.POST.get("city", ""),
            tags=request.POST.get("tags", "")
        )
        return redirect("index")
    
    return render(request, "create_post.html")


