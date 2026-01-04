from django.db.models import Count
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Post

def index(request):
    posts = Post.objects.all().order_by("-create_time")

    country_data = (
        Post.objects
        .values("country")
        .annotate(count=Count("id"))
    )

    return render(request, "index.html", {
        "posts": posts,
        "country_data": country_data
    })

@login_required
def create_post(request):
    if request.method == "POST":
        print("post data:", request.POST)
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

# The globe 
@login_required
def globe(request):
    return render(request, "globe.html")

@login_required
def globe_data(request):
    data = Post.objects.values("country").annotate(count=Count("id"))
    return JsonResponse(list(data), safe=False)


def country(request, country):
    # filtering post by the selected country 
    posts = Post.objects.filter(country=country).order_by("-create_time")

    # i want the small globe to be on every page so will paste this code couple of times
    country_data = (
        Post.objects
        .values("country")
        .annotate(count=Count("id"))
    )

    return render(request, "index.html", {
        "posts": posts,
        "country_data": country_data
    })