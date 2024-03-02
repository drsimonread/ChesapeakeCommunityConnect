from django.shortcuts import render, redirect
from django.http import HttpResponse
from boiler.models import Message
from account.models import Member
from .models import PostReport, UserReport
from mapViewer.models import MapPost, MapTag
from .forms import *

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

def pendingPostList(request):
    pending_posts= MapPost.objects.filter(isVisible=False)
    return HttpResponse("hey")

def tagList(request):
    msg = ""
    if request.method == "POST":
        if 'addTag' in request.POST:
            addForm = TagAdder(request.POST)
            delForm = TagRemover()
            if addForm.is_valid():
                addForm.save()
                msg = addForm.cleaned_data['name'] + " has been successfully added."
        elif 'delTag' in request.POST:
            addForm = TagAdder()
            delForm = TagRemover(request.POST)
            if delForm.is_valid():
                for tag in delForm.cleaned_data['tags']:
                    tag.delete()
                msg = "Tag(s) successfully deleted."
    else:
        addForm = TagAdder()
        delForm = TagRemover()
    return render(request, "Janitor/tagList.html", {
        'msg' : msg,
        'addForm' : addForm,
        'delForm' : delForm,
    })



def reportList(request):
    pReports = PostReport.objects.all().order_by("post")
    uReports = UserReport.objects.all().order_by("account")
    currentPK = -1
    pReportSorted = []
    tempList = []
    for report in pReports:
        if report.post.pk != currentPK:
            currentPK = report.post.pk
            if len(tempList) != 0:
                pReportSorted.append(tempList)
            tempList = [report.post]
        tempList.append(report)
    currentPK = -1
    uReportSorted = []
    tempList = []
    for report in uReports:
        if report.account.pk != currentPK:
            currentPK = report.account.pk
            if len(tempList) != 0:
                uReportSorted.append(tempList)
            tempList = [report.account]
        tempList.append(report)
    pReportSorted.sort(key = len, reverse=True)
    uReportSorted.sort(key = len, reverse=True)
    print(pReportSorted)
    print(uReportSorted)
    return HttpResponse("hi")