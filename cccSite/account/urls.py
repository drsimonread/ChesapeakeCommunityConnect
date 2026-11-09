from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("", views.default, name="default"),
    path("signin/", views.signin, name="signin"),
    path("signin-form/", views.signin_form, name="signin_form"),
    path("signup/", views.signup, name="signup"),
    path("authG/", views.authG, name="authG"),
    path("signout/", views.signout, name="signout"),
    path("manage/", views.manage, name='manage'),
    path("my-forums/", views.my_forums, name="my_forums"),
    path("create-forum/", views.create_forum, name="create_forum"),
    path("view/", views.account_all, name="account_list"),
    path("view/<want>", views.account_view, name='account_view'),
]
