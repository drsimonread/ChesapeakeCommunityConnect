from google.oauth2 import id_token
from google.auth.transport import requests
from django.forms import formset_factory
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from mapViewer.forms import MakeForumForm
from mapViewer.models import Forum, Media, Tag, Post, Comment
from Janitor.forms import UserRepForm
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import CreateAccountForm, SearchAccountForm
from django.db.models import Count
from django.db.models import Q
# from .forms import NameForm
from PIL import Image

# if user not signed in, sends them to log in 
def signin(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['rank']=user.member.ranking
            request.session['user']=user.member.pk
            request.session['name']=user.username
            data = {"is_password": True}
        else:
            print("TEST")
            data = {"is_password": False}
        return JsonResponse(data)
    return redirect(reverse("account:default"))



def signup(request):

    if request.method == "POST":
        username = request.POST.get("username", None)
        email = request.POST.get("email", None)
        if User.objects.filter(username__iexact=username).exists() or User.objects.filter(email__iexact=email).exists():
            print("You can't reuse an email and/or username, you silly goose!") #? This should be changed to a proper log file or something.
        else:
            createUserForm = CreateAccountForm(request.POST)
            if createUserForm.is_valid():
                user, member = createUserForm.save()
                user = authenticate(request, username=user.username, password=request.POST["password1"])
                if user is not None:
                    login(request, user)
                    request.session['rank']=member.ranking
                    request.session['user']=member.pk
                    request.session['name']=user.username

    return redirect(reverse("account:default"))

def username_validation(request):
    username = request.GET.get("username", None)
    print(username)
    data = {
        "is_taken": User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def email_validation(request):
    email = request.GET.get("email", None)
    data = {
        "is_taken": User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)
    

# if a user tries to sign out by GET URL, redirects to account. if there is a POST request to this url, flushes the session and sends them to default account page
def signout(request):
    if request.method == "POST":
        request.session.flush()
    return redirect(reverse("account:default"))

 
 # default account page. send to sign in if not signed in, otherwise displays user info
def default(request):
    if request.session.get('rank',0)!=0:
        userInz=Member.objects.get(pk=request.session['user'])
        databaseRank = userInz.ranking
        if request.session.get('rank',0) != databaseRank:
            request.session['rank']=databaseRank
         #get user from session
        return render(request, 'account/myaccount.html', {
            'self': userInz,
        })
    else:
        return render(request, 'account/signedout.html')

        
        
    
def account_list(request):
    nameQ= request.GET.get("q")
    sortQ=request.GET.get("s")
    users = Member.objects.filter(forums__visibility__gt=0).distinct().annotate(num_forums=Count("forums"), filter=Q(forums__visibility=1))
    search = SearchAccountForm(request.GET)
    if nameQ:
        users=users.filter(user__username__icontains=nameQ)
    if not sortQ:
        users=users.order_by("user__username")
    else:
        match sortQ:
            case "0":
                users=users.order_by("user__username")
            case "1":
                users=users.order_by("-user__username")
            case "2":
                users=users.order_by("num_forums")
            case "3":
                users=users.order_by("-num_forums")
            case _:
                users=users.order_by("user__username")
    return render(request, 'account/account_list.html', {'users' : users,
                                                         'search' : search,
                                                         })

def my_forums(request):
    if request.session.get('rank',0)==0:
        return redirect(reverse(default))
    else:
        userInz = Member.objects.get(pk=request.session.get('user'))
        userForums=Forum.objects.filter(author=userInz)
        vis = userForums.filter(visibility=1)
        pend = userForums.filter(visibility=0)
        den = userForums.filter(visibility=-1)
        return render(request, 'account/myForums.html', {'vis' : vis,
                                    'pend' : pend,
                                    'den' : den})
    
def account_view(request, want):
    msg = ""
    
    if not Member.objects.get(pk=want): # MEMBER_DELETE
        return redirect(reverse("account:default"))
    
    if request.method == "POST":
        form = UserRepForm(request.POST)
        if form.is_valid():
            form.save()
            msg="Your report has been sent."
    else:
        #Admin View
        if(request.session.get('rank',0)==98 or request.session.get('rank',0)==99):
            accountInz=Member.objects.get(pk=want)
            userForums=Forum.objects.filter(author=accountInz).filter(visibility=1)
            form = UserRepForm(initial={'account':accountInz})
            comments = Comment.objects.filter(author=accountInz)
            post = Post.objects.filter(author=accountInz)
            return render(request, 'account/single_account.html', {'user' : accountInz,
                                                           'forums' : userForums,
                                                           'form' : form,
                                                           'msg' : msg,
                                                            'comments' : comments,
                                                            'posts' : post})
        #Not Signed in
        elif(request.session.get('rank',0)==0):
            accountInz=Member.objects.get(pk=want)
            userForums=Forum.objects.filter(author=accountInz).filter(visibility=1)
            form = UserRepForm(initial={'account':accountInz})
            return render(request, 'account/single_account.html', {'user' : accountInz,
                                                           'forums' : userForums,
                                                           'form' : form,
                                                           'msg' : msg,
                                                            })
        #Default member view
        userInz = Member.objects.get(pk=request.session.get('user'))
        accountInz=Member.objects.get(pk=want)
        userForums=Forum.objects.filter(author=accountInz).filter(visibility=1)
        form = UserRepForm(initial={'account':accountInz})
        post = Post.objects.filter(author=accountInz, forum__contributors=userInz)
        comments = Comment.objects.filter(author=accountInz, post__forum__contributors=userInz)
    return render(request, 'account/single_account.html', {'user' : accountInz,
                                                           'forums' : userForums,
                                                           'form' : form,
                                                           'msg' : msg,
                                                           'posts' : post,
                                                            'comments' : comments
                                                            })
    

# lets members edit their info
def manage(request):
    if request.session.get('rank',0)==0: #if rank is anonymous, redirect to sign in
        return redirect(reverse("account:signin"))
    if request.method == "POST":
        userInz=Member.objects.get(pk=request.session['user']) 
        form = ManageForm(request.POST, request.FILES, instance=userInz)
        if form.is_valid():
            form.save()
            request.session['name']=userInz.user.username
            #! request.session['name']=userInz.name
            return redirect(reverse("account:default"))
    else:
        userInz=Member.objects.get(pk=request.session['user'])
        form = ManageForm(instance=userInz)
    return render(request, "account/manage.html", {'form' : form})

# a lot of this code is from google btw. this view verifies google one touch log in credentials
@csrf_exempt #the csrf is from google, not django, and is verified. can't get django's csrf to work tho due to origin of post
def authG(request):
    if request.method == "GET":
       return redirect(reverse("account:default"))
    elif request.method == "POST":

        csrf_tok_cookie = request.COOKIES.get('g_csrf_token')
        # check valid csrf token
        if not csrf_tok_cookie:
            return HttpResponse("Something went wrong, no csrf cookie")
        csrf_tok_body = request.POST.get('g_csrf_token')
        if not csrf_tok_body:
            return HttpResponse("Something went wrong, no csrf cookie from google")
        if csrf_tok_cookie != csrf_tok_body:
            return HttpResponse("Could not verify csrf")
        #get token from google
        tok = request.POST.get("credential")  
        try:
            # logs user in via their google ID, or makes an entry in member if they do not have an account yet.
            idinfo = id_token.verify_oauth2_token(tok, requests.Request(), "316865720473-94ccs1oka6ev4kmlv5ii261dirvjkja0.apps.googleusercontent.com")
            if not(GLogIn.objects.filter(googleID=idinfo['sub']).exists()): #checks if there is a stored google log in yet with this user's google ID
                #when we implement other sign in methods, we will need to ask the user if they already have an account
                #if so, have user sign in via user/pass or other method and then get that member entry so gLogInz points to it 
                
                DJuserInz = User.objects.create_user(username=idinfo['given_name'], email=idinfo['email'])
                userInz = Member.objects.create(user=DJuserInz)
                #! userInz = Member.objects.create(name=idinfo['given_name'], email = idinfo['email']) #stores the user's info, scraped from google, in the member model
                gLogInz = GLogIn.objects.create(googleID=idinfo['sub'], referTo=userInz) # stores the google ID and the member it is associated with
            else: #if the user has logged in with google before
                gLogInz=GLogIn.objects.get(googleID=idinfo['sub']) #get the object in the google log in table identified by the google ID
                userInz=gLogInz.referTo #get the object that the google ID is associated with

            #store information about the user in the session
            request.session['rank']=userInz.ranking
            request.session['user']=userInz.pk
            request.session['name']=userInz.user.username
            #! request.session['name']=userInz.name
        except ValueError:
            return HttpResponse("Something went wrong, invalid credentials from Google (somehow)")
            pass
        return redirect(reverse("account:default"))
    

#view for creating forums
def make_forum(request):
    if(request.session.get('rank',0) == 0): #if user is not signed in, require sign in
        return redirect(reverse("account:signin"))
    if(request.method=="POST"): #if the request was a post, it is an attempt to create a forum
        contentForm= MakeForumForm(request.POST, request.FILES) #create the posting form instance and populate it with the data in the POST request
        if contentForm.is_valid(): #if the forum is good to go, calls the clean method and validators from MakeForumForm in mapViewer/forms.py
            # MEMBER_DELETE
            userInz=Member.objects.get(pk=request.session['user']) #get user's member instance from session
            if len(contentForm.cleaned_data['content']) > 35: #if content overflows the preview length
                disc = contentForm.cleaned_data['content'][slice(0,35)] + "..." #create description to act as a preview
            else:
                disc = contentForm.cleaned_data['content'] #otherwise just use content to describe #? Why does description exist at all?
            vis=0 #default visibility set to pending
            if request.session['rank'] > 1: #if user is trusted, set visibility to visible
                vis=1
            forumInz=Forum.objects.create(title=contentForm.cleaned_data['title'], #actually create the forum instance in the database
                                   content=contentForm.cleaned_data['content'],
                                   author=userInz,
                                   description=disc,
                                   geoCode=contentForm.cleaned_data['geoResult'][0],
                                   visibility=vis,
                                   associated=contentForm.cleaned_data['associated'],
                                   private_public=contentForm.cleaned_data['private_public']
                                   )
            if contentForm.cleaned_data['tags']: #if there are any tags
                forumInz.tags.set(contentForm.cleaned_data['tags']) #set the forum's tags according to selected tags
            
            if contentForm.cleaned_data['files']: #if there are files uploaded
                for item in contentForm.cleaned_data['files']: #iterates through file upload fields
                    if item != None: #if item is none, then nothing was uploaded
                        fileInz = Media.objects.create(forum=forumInz, file=item) #create a forumfile instance
                        fileInz.format = fileInz.get_format() #get the format and set the format
                        fileInz.save() #save the updated format
            return redirect(reverse('mapViewer:forum_detail', args=[forumInz.pk])) #redirect to the forum view of the just posted forum
            
    else:
        contentForm = MakeForumForm()
    return render(request, 'account/create_forum.html', {'form': contentForm,})