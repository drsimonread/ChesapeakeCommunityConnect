from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("", views.default, name="default"),
    path("signin/", views.signin, name="signin"),
    path("authG/", views.authG, name="authG"),
    path("signout/", views.signout, name="signout"),
    path("manage/", views.manage, name='manage'),
    path("view/", views.account_all, name='all_account'),
    path("view/<want>", views.account_view, name='account_view'),
    path("create/", views.make_post, name="create_post"),
    path("myposts/", views.my_posts, name='my_posts'),
]