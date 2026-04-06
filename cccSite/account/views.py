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
from django.core.paginator import Paginator
from urllib.parse import urlencode
import json
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from PIL import Image
from .models import Member, GLogIn

# YOUR SPECIFIC CLIENT ID
GOOGLE_CLIENT_ID = "909497695712-h9smcju9klvlqk70celohtne9o438htn.apps.googleusercontent.com"

def google_signin(request):
    if request.method == "POST":
        token = request.POST.get("credential", "")

        try:
            # 1. Verify the Google token
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                GOOGLE_CLIENT_ID
            )

            google_id = idinfo["sub"]  # Google's unique user ID
            email = idinfo.get("email", "")
            first_name = idinfo.get("given_name", "")
            last_name = idinfo.get("family_name", "")

            # 2. Check if this GoogleID already exists
            try:
                glog = GLogIn.objects.get(googleID=google_id)
                member = glog.referTo
                user = member.user

            except GLogIn.DoesNotExist:
                # 3. Create or get Django User based on email
                user, created = User.objects.get_or_create(
                    username=email,
                    defaults={
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name,
                    }
                )

                # 4. Create Member if not exists
                member, created_member = Member.objects.get_or_create(
                    user=user,
                    defaults={"ranking": 1}
                )

                # 5. Store mapping GoogleID → Member
                GLogIn.objects.create(
                    googleID=google_id,
                    referTo=member
                )

            # 6. Log them in using Django
            login(request, user)

            # 7. Set your custom session keys
            request.session["rank"] = member.ranking
            request.session["user"] = member.pk
            request.session["name"] = user.username

            return JsonResponse({"success": True})

        except ValueError:
            return JsonResponse({"success": False, "message": "Invalid token"}, status=400)

    return JsonResponse({"success": False}, status=405)
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
    nameQ = (request.GET.get("q") or "").strip()
    sortQ = request.GET.get("s") or "0"
    users = Member.objects.filter(forums__visibility__gt=0).distinct().annotate(
        num_forums=Count("forums", filter=Q(forums__visibility=1)),
    )
    if nameQ:
        users = users.filter(user__username__icontains=nameQ)
    match sortQ:
        case "0":
            users = users.order_by("user__username")
        case "1":
            users = users.order_by("-user__username")
        case "2":
            users = users.order_by("num_forums")
        case "3":
            users = users.order_by("-num_forums")
        case _:
            users = users.order_by("user__username")
    paginator = Paginator(users, 18)
    page_obj = paginator.get_page(request.GET.get("page"))
    search = SearchAccountForm(request.GET)

    def qs(**params):
        data = {}
        if nameQ:
            data["q"] = nameQ
        data["s"] = params.get("s", sortQ)
        if "page" in params:
            data["page"] = params["page"]
        return "?" + urlencode(data)

    ctx = {
        "page_obj": page_obj,
        "search": search,
        "search_query": nameQ,
        "sort_value": sortQ,
        "qs_sort_az": qs(s="0", page=1),
        "qs_sort_za": qs(s="1", page=1),
        "qs_sort_forums_hi": qs(s="2", page=1),
        "qs_sort_forums_lo": qs(s="3", page=1),
        "qs_clear_search": "?" + urlencode({"s": sortQ, "page": 1}),
        "qs_reset": "?",
    }
    if page_obj.has_next():
        ctx["qs_next"] = qs(page=page_obj.next_page_number())
    if page_obj.has_previous():
        ctx["qs_prev"] = qs(page=page_obj.previous_page_number())
    return render(request, "account/account_list.html", ctx)

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
        #Admin View, includes all forums, posts, and comments from a user
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
        #Not Signed in only contains forums and posts/comments made on public forums
        elif(request.session.get('rank',0)==0):
            accountInz=Member.objects.get(pk=want)
            userForums=Forum.objects.filter(author=accountInz).filter(visibility=1)
            form = UserRepForm(initial={'account':accountInz})
            publicPosts= Post.objects.filter(author=accountInz, forum__private_public="public")
            publicComments = Comment.objects.filter(author=accountInz, post__forum__private_public="public")
            return render(request, 'account/single_account.html', {'user' : accountInz,
                                                           'forums' : userForums,
                                                           'form' : form,
                                                           'posts' : publicPosts,
                                                           'comments' : publicComments,
                                                           'msg' : msg,
                                                            })
        #Default member view contains forums as well as posts/comments made on public forums AND forums-
        #-the user is a contributor on
        userInz = Member.objects.get(pk=request.session.get('user'))
        accountInz=Member.objects.get(pk=want)
        userForums=Forum.objects.filter(author=accountInz).filter(visibility=1)
        form = UserRepForm(initial={'account':accountInz})
        privatePosts= Post.objects.filter(author=accountInz, forum__contributors=userInz)
        publicPosts= Post.objects.filter(author=accountInz, forum__private_public="public")
        allPosts= (privatePosts|publicPosts).distinct
        privateComments = Comment.objects.filter(author=accountInz, post__forum__contributors=userInz)
        publicComments = Comment.objects.filter(author=accountInz, post__forum__private_public="public")
        allComments = (privateComments|publicComments).distinct
        return render(request, 'account/single_account.html', {'user' : accountInz,
                                                           'forums' : userForums,
                                                           'form' : form,
                                                           'msg' : msg,
                                                           'posts' : allPosts,
                                                            'comments' : allComments
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
                                   first_name=contentForm.cleaned_data['firstName'],
                                   last_name=contentForm.cleaned_data['lastName'],
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