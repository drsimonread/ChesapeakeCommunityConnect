from django.urls import path
from . import views

app_name = "mapViewer"

urlpatterns = [
    path("", views.viewMap, name="default"),
    path("search/", views.post_list, name="post_list"),
    path("post/<int:want>", views.post_detail, name="post_detail"),
    # Add other URL patterns here
]
