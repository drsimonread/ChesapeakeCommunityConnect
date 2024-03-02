from django.shortcuts import render, redirect
from django.http import HttpResponse
from boiler.models import Message
from account.models import Member
from .models import PostReport, UserReport
from mapViewer.models import MapPost, MapTag
from .forms import *
from django.db.models import Count

# Create your views here.
def default(request):
    return render(request, "Janitor/AdminBase.html")

def contactList(request):
    messages = Message.objects.all()
    return render(request, "Janitor/contactList.html", {'messages' : messages,})

def memberList(request):
    members = Member.objects.exclude(pk=request.session.get('user',-1))
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
                addForm = TagAdder()
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

def exportData(request):
    #https://docs.djangoproject.com/en/5.0/howto/outputting-csv/
    return HttpResponse("Not implemented yet")

def reportList(request):
    msg=""
    if request.method == "POST":
        if request.POST.get('type') == 'user':
            userInz = Member.objects.get(pk=request.POST.get('pk'))
            msg=userInz.name + "'s reports have been cleared."
            UserReport.objects.filter(account=userInz).delete()
        else:
            postInz = MapPost.objects.get(pk=request.POST.get('pk'))
            msg=postInz.title + "'s reports have been cleared."
            PostReport.objects.filter(post=postInz).delete()
    pwReports = MapPost.objects.filter(postreport__id__gt=0).distinct().annotate(num_reports=Count("postreport")).order_by('-num_reports')
    uwReports = Member.objects.filter(userreport__id__gt=0).distinct().annotate(num_reports=Count("userreport")).order_by('-num_reports')
    pList = []
    uList = []
    for item in pwReports:
        reports = PostReport.objects.filter(post=item)
        tempList = [item,reports]
        pList.append(tempList)
    for item in uwReports:
        reports = UserReport.objects.filter(account=item)
        tempList = [item,reports]
        uList.append(tempList)
    print(uList)
    return render(request, 'Janitor/reportList.html', {
        'msg' : msg,
        'pList' : pList,
        'uList' : uList,
    })

