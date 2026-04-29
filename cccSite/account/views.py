from django.forms import formset_factory
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
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
        try:
            # Lazy import so management commands can run without google auth crypto deps.
            from google.oauth2 import id_token
            from google.auth.transport import requests as google_requests
        except Exception:
            return JsonResponse(
                {"success": False, "message": "Google sign-in dependencies are unavailable"},
                status=503,
            )

        token = request.POST.get("credential", "")

        try:
            # 1. Verify the Google token
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
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
    if request.session.get('rank', 0)==0:
        return render(request, 'account/signin.html')
    else:
        return redirect("/account/")

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
    return render(request, "account/manage.html", {'form' : form})

# a lot of this code is from google btw. this view verifies google one touch log in credentials
#view for creating forums
def make_forum(request):
    if request.session.get("rank", 0) == 0:
        return redirect(reverse("account:signin"))
    if request.method == "POST":
        contentForm = MakeForumForm(request.POST, request.FILES)
        if contentForm.is_valid():
            userInz = Member.objects.get(pk=request.session["user"])
            content = contentForm.cleaned_data["content"]
            if len(content) > 35:
                disc = content[0:35] + "..."
            else:
                disc = content
            geo = _geocode_for_forum_storage(contentForm.cleaned_data["geoResult"])
            if geo is None:
                messages.error(
                    request,
                    "We could not save the map location. Please choose a full address from the suggestions and try again.",
                )
            else:
                forumInz = Forum.objects.create(
                    title=contentForm.cleaned_data["title"],
                    content=content,
                    first_name=contentForm.cleaned_data["firstName"],
                    last_name=contentForm.cleaned_data["lastName"],
                    author=userInz,
                    description=disc,
                    geoCode=geo,
                    visibility=0,
                    associated=contentForm.cleaned_data["associated"],
                    private_public=contentForm.cleaned_data["private_public"],
                )
                tags = contentForm.cleaned_data.get("tags")
                if tags:
                    forumInz.tags.set(tags)
                for item in contentForm.cleaned_data.get("files") or []:
                    if item is not None:
                        fileInz = Media.objects.create(forum=forumInz, file=item)
                        fileInz.format = fileInz.get_format()
                        fileInz.save()
                messages.success(
                    request,
                    "Forum successfully submitted! It will appear under Pending review until an administrator approves it.",
                )
                return redirect(
                    reverse("account:my_forums") + "?success=1&cleardraft=1"
                )
        else:
            messages.error(
                request,
                "Your forum was not saved. Please fix the errors highlighted below and try again.",
            )
    else:
        contentForm = MakeForumForm()
    return render(request, 'account/create_forum.html', {'form': contentForm,})