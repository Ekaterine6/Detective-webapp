from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create_post, name="create_post"),
    path("globe", views.globe, name="globe"),
    path("globe_data", views.globe_data, name="globe_data"),
    path("country/<str:country>", views.country, name="country"),
]
 