from django.contrib.auth import views as auth_views
from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    
    path("create", views.create_post, name="create_post"),
    path("country/<str:country>", views.country, name="country"),
    path("post/<int:post_id>", views.view_post, name="view_post"),
    path("profile/<str:username>", views.profile, name="profile"),
]
 