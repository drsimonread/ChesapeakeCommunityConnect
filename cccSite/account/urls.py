from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("", views.default, name="default"),
    path("signin/", views.signin, name="signin"),
    path("auth/", views.auth, name="auth"),
    path("signout/", views.signout, name="signout")
    
]