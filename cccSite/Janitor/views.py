from django.shortcuts import render, redirect
from django.http import HttpResponse
from boiler.models import Message
from account.models import Member
from .models import ForumReport, UserReport
from mapViewer.models import Forum, Tag, Media
from .forms import *
from django.db.models import Count

# Create your views here.
def default(request):
    databaseRank = Member.objects.get(pk=request.session.get('user',-1)).ranking
    if request.session.get('rank',0) != databaseRank:
        request.session['rank']=databaseRank
    return render(request, "Janitor/AdminBase.html")

#displays a list of accordion elements that show contact instances from the contact us form.
def contactList(request):
    messages = Message.objects.all() #fetch messages
    return render(request, "Janitor/contactList.html", {'messages' : messages,})#pass messages to template

#display a list of users, not including the currently logged in account. needs to be remade using querysets to allow searching/sorting
def memberList(request):
    if request.session.get('rank',0) != 99: #if user isn't an admin, they aren't allowed to edit ranks
        redirect(default)
    members = Member.objects.exclude(pk=request.session.get('user',-1)) #exclude the actively logged in user, so admins can't edit their own rank
    memberStats = [] #list for storing a dictionary that associates a user object with their stats
    for user in members:
        visibleforums = Forum.objects.filter(author=user, visibility__gt=0).count() #number of forums that the user has made that were approved
        reports = ForumReport.objects.filter(forum__author=user).count()+UserReport.objects.filter(account=user).count() #number of reports against a user and their forums
        memberStats.append({'user' : user, 'goodforums': visibleforums, 'reports':reports}) #add to the stats list
    
    return render(request, "Janitor/memberList.html", {'members' : memberStats,}) #pass the list to the template

def member_manage(request, want): #view for adjusting user ranks and information
    if request.session.get('rank',0) != 99: #if the session isn't an admin
        redirect(default)
    if Member.objects.filter(pk=want).exists(): #confirm that the url corresponds to a user
        userInz=Member.objects.get(pk=want) #if so, get the relevant user object
    else:
        return redirect(memberList)
    if request.method == 'POST': #if method is post, a form has been submitted to edit the user's info
        form = MemberManager(request.POST, instance=userInz) 
        if form.is_valid:
            form.save()
    else:
        form = MemberManager(instance=userInz) #initalize form if request method was GET
    return render(request, 'Janitor/memberManager.html', {'form' : form,
                                                          })

def pendingForumList(request): #show a list of forums pending approval
    msg = ""
    forums= Forum.objects.filter(visibility=0) #fetch all forums with pending visibility
    if not forums:
        msg = "No pending forums!"
    return render(request, 'Janitor/forumList.html', {'forums' : forums,
                                                     'msg' : msg})

#view that allows the viewing of a forum with a form that allows admin/moderator to change visibility. 
def rev_forum(request, want): 
    msg="" #default value for msg is None, allows us to check if msg in template to decide whether to render msg or not
    if Forum.objects.filter(pk=want).exists(): #confirm forum object exists
        forumInz = Forum.objects.get(pk=want) #get forum and associated files form the database
        files = Media.objects.filter(forum=forumInz)
        if request.method == "POST": #if the method was POST, visibility has been updated
            form = ForumManager(request.POST, instance=forumInz) #forum manager is a modelform with custom form validation, see forms.py
            if form.is_valid(): #if form input is OK
                form.save()
                if form.cleaned_data['visibility'] == 1: #change msg so admin can confirm their change has been made
                    msg="Forum Approved!"
                elif form.cleaned_data['visibility'] == 0:
                    msg="No changes made."
                else:
                    msg="Forum Denied!"
        else:
            form = ForumManager(instance=forumInz)
        return render(request, 'Janitor/forumManager.html', {'form' : form,
                                                            'forum' : forumInz,
                                                            'files' : files,
                                                            'msg' : msg})
    return redirect(pendingForumList) #if the url doesn't correspond to a forum, redirect to the pending forum list

def tagList(request): #view allowing mod/admin to add/remove tags to the forum tagging system
    msg = ""
    if request.method == "POST":
        if 'addTag' in request.POST: #if a form has been posted, a tag is being added or deleted this checks which one, indicated by a hidden field
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

def exportData(request): #low priority
    #https://docs.djangoproject.com/en/5.0/howto/outputting-csv/
    return HttpResponse("Not implemented yet")

def reportList(request): #view for seeing reported forums/users and the reports associated with them
    msg=""
    if request.method == "POST": #if POST, there was an attempt to clear reports
        if request.POST.get('type') == 'user': #if the clear was from a user reports section
            userInz = Member.objects.get(pk=request.POST.get('pk')) #get user object
            msg=userInz.name + "'s reports have been cleared." #set the message
            UserReport.objects.filter(account=userInz).delete() #delete reports associated with user
        else: #same flow, but for forums
            forumInz = Forum.objects.get(pk=request.POST.get('pk'))
            msg=forumInz.title + "'s reports have been cleared."
            ForumReport.objects.filter(forum=forumInz).delete()
    #annotations essentially add a temporary field to model objects. in this case, we are adding the number of associated reports and sorting by it
    pwReports = Forum.objects.filter(forumreport__id__gt=0).distinct().annotate(num_reports=Count("forumreport")).order_by('-num_reports')
    uwReports = Member.objects.filter(userreport__id__gt=0).distinct().annotate(num_reports=Count("userreport")).order_by('-num_reports')
    #we create pList for forums, uList for users. each entry is a list, index 0= user/forum object and index 1= query set of reports associated with object
    pList = []
    uList = []
    for item in pwReports:
        reports = ForumReport.objects.filter(forum=item)
        tempList = [item,reports]
        pList.append(tempList)
    for item in uwReports:
        reports = UserReport.objects.filter(account=item)
        tempList = [item,reports]
        uList.append(tempList)
    #print(uList)
    return render(request, 'Janitor/reportList.html', {
        'msg' : msg,
        'pList' : pList,
        'uList' : uList,
    })

