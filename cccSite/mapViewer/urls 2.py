from django.urls import path
from . import views

app_name = "mapViewer"
urlpatterns = [
    path("", views.viewMap, name="default"),
]