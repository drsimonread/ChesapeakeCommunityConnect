from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "mapViewer"

urlpatterns = [
    path('slideshow/<int:post_id>/', views.slideshow_popup, name='slideshow_popup'),
    path("", views.viewMap, name="default"),
    path("search/", views.post_list, name="post_list"),
   
    # Add other URL patterns here
]
