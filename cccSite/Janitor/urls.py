from django.urls import path
from . import views

app_name = "Janitor"
urlpatterns = [
    path("", views.default, name="default"),
    path("messages/", views.contactList, name="messageList"),
    path("member/", views.memberList, name="memberList"),
    path("member/<int:want>", views.member_manage, name="manage_user"),
    path("post/", views.pendingPostList, name='postList'),
    path('post/<int:want>', views.rev_post, name='postReview'),
    path('reports/', views.reportList, name="reportList"),
    path('tags/', views.tagList, name = "tagList"),
]