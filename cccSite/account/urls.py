from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("", views.default, name="default"),
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("signout/", views.signout, name="signout"),
    path("manage/", views.manage, name='manage'),
    path("view/", views.account_list, name='account_list'),
    path("view/<want>/", views.account_view, name='account_view'),
    path("create/", views.make_forum, name="create_forum"),
    path("edit/<int:forum_id>/", views.edit_forum, name="edit_forum"),
    path("myforums/", views.my_forums, name='my_forums'),
    path("ajax/username_validation/", views.username_validation, name='username_validation'),
    path("ajax/email_validation/", views.email_validation, name='email_validation'),
    path("google-signin/", views.google_signin, name="google_signin"),
]
