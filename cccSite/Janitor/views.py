from django.shortcuts import render, redirect
from django.http import HttpResponse
from boiler.models import Message
from account.models import Member
from .models import PostReport, UserReport
from mapViewer.models import MapPost, MapTag, PostFile
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
        visibleposts = MapPost.objects.filter(author=user, visibility__gt=0).count()
        reports = PostReport.objects.filter(post__author=user).count()+UserReport.objects.filter(account=user).count()
        memberStats.append({'user' : user, 'goodposts': visibleposts, 'reports':reports})
    
    return render(request, "Janitor/memberList.html", {'members' : memberStats,})

def member_manage(request, want):
    if Member.objects.filter(pk=want).exists():
        userInz=Member.objects.get(pk=want)
    else:
        return redirect(memberList)
    if request.method == 'POST':
        form = MemberManager(request.POST)
        if form.is_valid:
            form.save()
    else:
        form = MemberManager(instance=userInz)
    return render(request, 'Janitor/memberManager.html', {'form' : form,
                                                          })

def pendingPostList(request):
    posts= MapPost.objects.filter(visibility=0)
    return render(request, 'Janitor/postList.html', {'posts' : posts})

def rev_post(request, want):
    msg=None
    if MapPost.objects.filter(pk=want).exists():
        postInz = MapPost.objects.get(pk=want)
        files = PostFile.objects.filter(post=postInz)
        if request.method == "POST":
            form = PostManager(request.POST, instance=postInz)
            if form.is_valid():
                form.save()
                if form.cleaned_data['visibility'] == 1:
                    msg="Post Approved!"
                elif form.cleaned_data['visibility'] == 0:
                    msg="No changes made."
                else:
                    msg="Post Denied!"
        else:
            form = PostManager(instance=postInz)
        return render(request, 'Janitor/postManager.html', {'form' : form,
                                                            'post' : postInz,
                                                            'files' : files,
                                                            'msg' : msg})
    return redirect(pendingPostList)

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

