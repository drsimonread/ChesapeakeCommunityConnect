from google.oauth2 import id_token
from google.auth.transport import requests
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from PIL import Image
from mapViewer.models import MapPost
from .forms import CreateForumForm, SearchAccountForm
from urllib.parse import urlencode

# if user not signed in, sends them to log in 
def signin(request):
    if request.session.get('rank', 0)==0:
        return render(request, 'account/signin.html')
    else:
        return redirect(reverse("account:default"))

def signin_form(request):
    if request.method == "GET":
        return render(request, "account/signin_form.html")

    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "")
    account = AccountCreation.objects.filter(
        username__iexact=username, status="accepted"
    ).first()
    if account is None or account.password != password:
        return render(request, "account/signin_form.html", {
            "error": "The username or password is incorrect.",
        })

    member, _ = Member.objects.get_or_create(
        email=account.email,
        defaults={"name": account.displayname},
    )
    request.session["rank"] = member.ranking
    request.session["user"] = member.pk
    request.session["name"] = member.name
    return redirect(reverse("account:default"))

def signup(request):
    if request.method == "GET":
        return render(request, "account/signup.html")

    values = {
        field: request.POST.get(field, "").strip()
        for field in ("email", "username", "displayname", "password", "confirmpassword")
    }
    if not all(values.values()):
        return render(request, "account/signup.html", {
            "error": "All fields are required.",
        })
    if values["password"] != values["confirmpassword"]:
        return render(request, "account/signup.html", {
            "error": "The passwords do not match.",
        })
    if AccountCreation.objects.filter(
        email__iexact=values["email"], status="pending"
    ).exists() or AccountCreation.objects.filter(
        username__iexact=values["username"], status="pending"
    ).exists():
        return render(request, "account/signup.html", {
            "error": "An account request with that email or username is already pending.",
        })

    AccountCreation.objects.create(**values)
    return redirect(reverse("account:signin"))

# if a user tries to sign out by URL, redirects to account. if there is a POST request to this url, flushes the session and sends them to confirmation
def signout(request):
    if request.method == "POST":
        request.session.flush()
    return redirect(reverse("account:default"))

 
 # default account page. send to sign in if not signed in, otherwise displays user info
def default(request):
    if request.session.get('rank',0)==0:
        return redirect(reverse("account:signin"))
    else:
        userInz=Member.objects.get(pk=request.session['user']) #get user from session
        return render(request, 'account/myaccount.html', {
            'name': userInz.name,
            'email' : userInz.email,
            'image' : userInz.pic,
            'about' : userInz.about,
        })
    
def account_all(request):
    search = SearchAccountForm(request.GET)
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("s", "0")
    page_number = request.GET.get("page", "1")

    members = Member.objects.annotate(
        num_forums=Count(
            "mappost",
            filter=Q(mappost__visibility=1),
        ),
    ).filter(num_forums__gt=0)
    if query:
        members = members.filter(name__icontains=query)

    sort_fields = {
        "0": ("name",),
        "1": ("-name",),
        "2": ("-num_forums", "name"),
        "3": ("num_forums", "name"),
    }
    sort = sort if sort in sort_fields else "0"
    members = members.order_by(*sort_fields[sort])
    page_obj = Paginator(members, 20).get_page(page_number)

    def query_string(**updates):
        values = {"q": query, "s": sort, "page": page_obj.number}
        values.update(updates)
        return "?" + urlencode({key: value for key, value in values.items() if value not in ("", None)}
                               )

    return render(request, "account/account_list.html", {
        "is_signed_in": request.session.get("rank", 0) > 0,
        "search": search,
        "search_query": query,
        "sort_value": sort,
        "page_obj": page_obj,
        "qs_clear_search": query_string(q="", page=1),
        "qs_reset": query_string(q="", s="0", page=1),
        "qs_sort_az": query_string(s="0", page=1),
        "qs_sort_za": query_string(s="1", page=1),
        "qs_sort_forums_hi": query_string(s="2", page=1),
        "qs_sort_forums_lo": query_string(s="3", page=1),
        "qs_prev": query_string(page=page_obj.previous_page_number() if page_obj.has_previous() else 1),
        "qs_next": query_string(page=page_obj.next_page_number() if page_obj.has_next() else page_obj.number),
    })
    
def account_view(request, want):
    if not want:
        return HttpResponse("Insert list view here")
    if not Member.objects.get(pk=want):
        return redirect(reverse("account:default"))
    viewInz=Member.objects.get(pk=want)
    if request.session.get('rank',0) != 0:
        userInz=Member.objects.get(request.session['user'])
    else:
        userInz= Member.objects.none()
    

# lets members edit their info
def manage(request):
    if request.session.get('rank',0)==0:
        return redirect('/account/signin/')
    if request.method == "POST":
        userInz=Member.objects.get(pk=request.session['user']) 
        form = ManageForm(request.POST, request.FILES, instance=userInz)
        if form.is_valid():
            form.save()
            request.session['name']=userInz.name
            return redirect("/account/")
    else:
        userInz=Member.objects.get(pk=request.session['user'])
        form = ManageForm(instance=userInz)
    return render(request, "account/manage.html", {
        'form': form,
        'current_profile_image': userInz.pic,
    })


def my_forums(request):
    if request.session.get("rank", 0) == 0:
        return redirect(reverse("account:signin"))

    posts = MapPost.objects.filter(
        author_id=request.session["user"],
    ).order_by("-created")
    return render(request, "account/myForums.html", {
        "vis": posts.filter(visibility=1),
        "pend": posts.filter(visibility=0),
        "den": posts.filter(visibility=-1),
    })


def create_forum(request):
    if request.session.get("rank", 0) == 0:
        return redirect(reverse("account:signin"))

    form = CreateForumForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        content = form.cleaned_data["content"]
        MapPost.objects.create(
            title=form.cleaned_data["title"],
            content=content,
            author_id=request.session["user"],
            description=content[:35] + ("..." if len(content) > 35 else ""),
            geoCode=form.cleaned_data["geoResult"] or {},
            visibility=0,
        ).tags.set(form.cleaned_data["tags"])
        return redirect(f"{reverse('account:my_forums')}?success=1")

    return render(request, "account/create_forum.html", {"form": form})

# a lot of this code is from google btw
@csrf_exempt #the csrf is from google, not django, and is verified. can't get django's csrf to work tho due to origin of post
def authG(request):
    if request.method == "GET":
       return redirect(reverse("account:account_list"))
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
                
                userInz = Member.objects.create(name=idinfo['given_name'], email = idinfo['email']) #stores the user's info, scraped from google, in the member model
                gLogInz = GLogIn.objects.create(googleID=idinfo['sub'], referTo=userInz) # stores the google ID and the member it is associated with
            else: #if the user has logged in with google before
                gLogInz=GLogIn.objects.get(googleID=idinfo['sub']) #get the object in the google log in table identified by the google ID
                userInz=gLogInz.referTo #get the object that the google ID is associated with

            #store information about the user in the session
            request.session['rank']=userInz.ranking
            request.session['user']=userInz.pk 
            request.session['name']=userInz.name
        except ValueError:
            return HttpResponse("Something went wrong, invalid credentials from Google (somehow)")
            pass
        return redirect(reverse("account:default"))