from django.urls import path
from . import views
#from mapViewer.views import viewMap

app_name = "boiler"
urlpatterns = [
   # path("", viewMap, name="viewMap"),
    path("about/", views.about, name="about"),
    path('help/', views.help, name='help'),
]