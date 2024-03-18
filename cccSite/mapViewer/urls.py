from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "mapViewer"

urlpatterns = [
    path("", views.viewMap, name="default"),
    path("search/", views.post_list, name="post_list"),
    path("post/<int:want>", views.post_detail, name="post_detail"),
    path("post/create",views.make_post, name="post_create"),
    # Add other URL patterns here
]
