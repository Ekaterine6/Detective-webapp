from django.db.models import Count, Q
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Profile, PostImg, Case


# register
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "username already exists"
            })
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect("index")
    
    return render(request, "register.html")



def index(request):
    # search br 
    query = request.GET.get("q", "").strip()

    # posts display
    posts = Post.objects.all().order_by("-create_time")

    # search bar logic - using Q making sure it is case insensetive
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(tags__icontains=query) |
            Q(country__icontains=query) |
            Q(city__icontains=query)
        )

    country_data = (
        Post.objects
        .values("country")
        .annotate(count=Count("id"))
    )

    return render(request, "index.html", {
        "posts": posts,
        "country_data": country_data,
        "query" : query 
    })


@login_required
def create_post(request):
    if request.method == "POST":
        print("post data:", request.POST)
        post = Post.objects.create(
            author=request.user,
            title=request.POST["title"],
            event_date=request.POST["event_date"],
            body=request.POST["body"],
            country=request.POST["country"],
            city=request.POST.get("city", ""),
            tags=request.POST.get("tags", "")
        )
        images = request.FILES.getlist("images")
        for img in images:
            PostImg.objects.create(post=post, image=img)

        return redirect("index")
    
    return render(request, "create_post.html")



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


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)

    # letting the user write their bio
    # getting theri profile
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == "POST" and request.user == user:
        profile.bio = request.POST.get("bioo", "")
        profile.save()
        return redirect("profile", username=username)

    posts = Post.objects.filter(author=user).order_by("-create_time")

    # showing cases on profile page created by the user
    cases = Case.objects.filter(author=user)


    return render(request, "profile.html", {
        "profile_user": user,
        "profile": profile,
        "posts": posts,
        "cases": cases,
    })


# view individual posts

def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "view_post.html", {
        "post": post
    })


# letting the user create a case making them feel like they are sharing their tehories with people
@login_required
def create_case(request):
    if request.method == "POST":
        title = request.POST.get("title")
        notes = request.POST.get("notes")
        #they can have this case private so only they see it or public so others can see their "case"
        is_public = request.POST.get("is_public") == "on"

        Case.objects.create(
            author=request.user,
            title=title,
            notes=notes,
            is_public=is_public
        )

        return redirect("profile", request.user.username)
    
    return render(request, "create_case.html")


# like (view post) this is for cases users can click and see the full information/full case adn comment on it 
@login_required
def case_details(request, case_id):
    case=get_object_or_404(Case, id=case_id)

    # users can add "posts" to their "cases" as evidence
    evidence_posts = case.evidence.all().select_related('post', 'post__author')

    #comments on the  cases
    return render(request, "case_details.html", {
        "case":case,
        "evidence_posts": evidence_posts
    })


# letting users add posts to their "cases" as "evidence"
@login_required
def add_to_case(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user_cases = Case.objects.filter(author=request.user)

    if request.method == "POST":
        case_id = request.POST.get("case_id")
        case = get_object_or_404(Case, id=case_id)

        #adding posts to cases
        from .models import CaseEvidence
        CaseEvidence.objects.create(case=case, post=post)

        return redirect("case_detail", case_id=case.id)
    return render(request, "add_to_case.html", {
        "post":post,
        "user_cases":user_cases
    })