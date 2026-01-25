from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    
    path("create", views.create_post, name="create_post"),
    path("cases/create/", views.create_case, name="create_case"),
    path("country/<str:country>", views.country, name="country"),
    path("post/<int:post_id>", views.view_post, name="view_post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("cases/<int:case_id>/", views.case_details, name="case_detail"),
    path("post/<int:post_id>/add_to_case/", views.add_to_case, name="add_to_case"),
    path("board/", views.board, name="board"),
    path("delete-note/<int:note_id>/", views.delete_note, name="delete_note"),
    path("post/<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path("post/<int:post_id>/delete/", views.delete_post, name="delete_post"),
    path("post/<int:post_id>/", views.view_post, name="view_post"),

]
