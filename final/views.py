from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Profile, PostImg, Case, Comments, Notes
import json


# register
def register(request):
    #registration form
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
 
        # no repeating of usernames
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "username already exists"
            })
        
        # creating the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # note the new user sees in board only once 
        Notes.objects.create(
            user=user,
            title="Example Note - Hi Detective",
            text="You can create and add notes to this board,use it to brainstorm, or maybe u just want to visualize your thoughts."
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


    return render(request, "index.html", {
        "posts": posts,
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

    return render(request, "index.html", {
        "posts": posts,
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

    # private logic / if private only author can see
    if not case.is_public and case.author != request.user:
        return HttpResponse("""
            <script>
                alert('this case is private');
                window.location.href = '/';    
            </script>
        """)

    # users can add "posts" to their "cases" as evidence
    evidence_posts = case.evidence.all().select_related('post', 'post__author')

    #comments
    # letting users comment on cases and reply to each other 
    if request.method == "POST":
        body = request.POST.get("comment_body")
        parent_id = request.POST.get("parent_id")
        parent_comment = None
        if parent_id:
            parent_comment = Comments.objects.filter(id=parent_id).first()

        Comments.objects.create(
            case=case,
            author=request.user,
            body=body,
            parent=parent_comment
        )
        return redirect("case_detail", case_id=case.id)
    
    comments = case.comments.filter(parent=None).order_by("-created_at")

    return render(request, "case_details.html", {
        "case":case,
        "evidence_posts": evidence_posts,
        "comments": comments
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

#notes logic
@login_required
def board(request):
    # --- Instant adding via JS fetch ---
    if request.method == "POST" and request.headers.get("Content-Type") == "application/json":
        data = json.loads(request.body)
        note = Notes.objects.create(
            user=request.user,
            title=data.get("noteTitle"),
            text=data.get("noteText", ""),
            note_type=data.get("noteType", "clue"),
            top=100,
            left=100
        )
        return JsonResponse({"success": True, "id": note.id})

    # --- Saving positions via hidden form ---
    if request.method == "POST":
        positions = request.POST.get("positions")
        if positions:
            data = json.loads(positions)
            for item in data:
                note = Notes.objects.get(id=item["id"], user=request.user)
                note.top = item["top"]
                note.left = item["left"]
                note.save()
            return redirect("board")

        # --- Adding notes via normal form submit ---
        title = request.POST.get("noteTitle")
        text = request.POST.get("noteText", "")
        note_type = request.POST.get("noteType", "clue")
        if title:
            Notes.objects.create(
                user=request.user,
                title=title,
                text=text,
                note_type=note_type
            )
            return redirect("board")

    notes = Notes.objects.filter(user=request.user)
    return render(request, "board.html", {"notes": notes})

# deleting notes from board
@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Notes, id=note_id, user=request.user)
    note.delete()
    return HttpResponse("deleted")


# letting the auhor delete their own post
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.author != request.user:
        return HttpResponse("You are not allowed to delete this post", status=403)
    
    if request.method == "POST":
        post.delete()
        return redirect("index")
    
    # optional: show a confirmation page
    return render(request, "confirm_delete_post.html", {"post": post})



# letting the user edit their post
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # only author can edit
    if post.author != request.user:
        return HttpResponse("You are not allowed to edit this post", status=403)

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.body = request.POST.get("body")
        post.event_date = request.POST.get("event_date")
        post.country = request.POST.get("country")
        post.city = request.POST.get("city", "")
        post.tags = request.POST.get("tags", "")
        post.save()

        # handle images if needed
        images = request.FILES.getlist("images")
        for img in images:
            PostImg.objects.create(post=post, image=img)

        return redirect("view_post", post_id=post.id)

    return render(request, "edit_post.html", {"post": post})
