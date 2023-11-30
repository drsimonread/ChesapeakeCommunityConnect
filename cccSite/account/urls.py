from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("", views.default, name="default"),
    path("signin/", views.signin, name="signin"),
    path("authG/", views.authG, name="authG"),
    path("signout/", views.signout, name="signout"),
    path("manage/", views.manage, name='manage')
]