from django.urls import path
from . import views

app_name = "Janitor"
urlpatterns = [
    path("", views.default, name="default"),
    path("messages/", views.contactList, name="messageList"),
    path("member/", views.memberList, name="memberList"),
    path("member/<int:want>/", views.member_manage, name="manage_user"),
    path("forum/", views.pendingForumList, name='forumList'),
    path('forum/<int:want>/', views.rev_forum, name='forumReview'),
    path('reports/', views.reportList, name="reportList"),
    path('tags/', views.tagList, name = "tagList"),
]