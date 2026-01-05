from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    
    path("create", views.create_post, name="create_post"),
    path("globe", views.globe, name="globe"),
    path("globe_data", views.globe_data, name="globe_data"),
    path("country/<str:country>", views.country, name="country"),
    path("profile/<str:username>", views.profile, name="profile"),
]
 