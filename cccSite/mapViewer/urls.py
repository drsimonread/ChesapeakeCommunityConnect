from django.urls import path
from . import views

app_name = "mapViewer"

urlpatterns = [
    path('save_widget/', views.save_widget, name='save_widget'),
    path('search_widgets/', views.search_widgets, name='search_widgets'),
    path("", views.viewMap, name="default"),
    # Add other URL patterns here
]
