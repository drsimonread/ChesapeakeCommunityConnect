from django.shortcuts import render, redirect
from django.http import HttpResponse
from boiler.models import Message
from account.models import Member
from .models import PostReport, UserReport
from mapViewer.models import MapPost, MapTag

# Create your views here.
def default(request):
    return render(request, "Janitor/AdminBase.html")

def contactList(request):
    messages = Message.objects.all()
    return render(request, "Janitor/contactList.html", {'messages' : messages,})

def memberList(request):
    members = Member.objects.all()
    memberStats = []
    for user in members:
        visibleposts = MapPost.objects.filter(author=user, isVisible=True).count()
        reports = PostReport.objects.filter(post__author=user).count()+UserReport.objects.filter(account=user).count()
        memberStats.append({'user' : user, 'goodposts': visibleposts, 'reports':reports})
    
    return render(request, "Janitor/memberList.html", {'members' : memberStats,})
