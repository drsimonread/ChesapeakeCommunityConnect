from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "mapViewer"

urlpatterns = [
    path("", views.viewMap, name="default"),
    path("search/", views.forum_list, name="forum_list"),
    path("forum/<int:want>/", views.forum_detail, name="forum_detail"),
    path("forum/<int:want>/post/<int:wants>/", views.post_detail, name="post_detail"),
    # Add other URL patterns here
]
