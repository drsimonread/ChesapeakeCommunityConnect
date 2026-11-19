from google.oauth2 import id_token
from google.auth.transport import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import CreateAccountForm, SearchAccountForm, CreateForumForm
from django.db.models import Count
from django.db.models import Q
from django.core.mail import send_mail
from django.core import signing
from django.conf import settings
from django.utils.http import (
    url_has_allowed_host_and_scheme,
    urlsafe_base64_encode,
    urlsafe_base64_decode,
)
from django.utils.encoding import force_bytes, force_str
from django.core.paginator import Paginator
import logging
import json
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from PIL import Image
from .models import Member, GLogIn, AccountCreation

logger = logging.getLogger(__name__)

# YOUR SPECIFIC CLIENT ID
GOOGLE_CLIENT_ID = getattr(settings, "GOOGLE_CLIENT_ID", "")

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

            # 2. Check if this Google ID already exists
            try:
                glog = GLogIn.objects.get(googleID=google_id)
                member = glog.referTo
            except GLogIn.DoesNotExist:
                member = Member.objects.filter(email__iexact=email).first()
                if member is None:
                    name = " ".join(part for part in (first_name, last_name) if part).strip()
                    member = Member.objects.create(
                        name=name or email,
                        email=email,
                        ranking=1,
                    )
                GLogIn.objects.create(
                    googleID=google_id,
                    referTo=member
                )

            # Set the custom session keys used throughout the site.
            request.session["rank"] = member.ranking
            request.session["user"] = member.pk
            request.session["name"] = member.name

            return JsonResponse({"success": True})

        except ValueError:
            return JsonResponse({"success": False, "message": "Invalid token"}, status=400)
        except Exception:
            logger.exception("Google sign-in token verification failed")
            return JsonResponse({"success": False, "message": "Could not verify Google token"}, status=400)

    return JsonResponse({"success": False}, status=405)
from mapViewer.models import MapPost
from .forms import CreateForumForm, SearchAccountForm
from urllib.parse import urlencode
from string import ascii_uppercase


def safe_next_url(request, candidate):
    if candidate and url_has_allowed_host_and_scheme(
        candidate,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return candidate
    return reverse("account:default")


def signin(request):
    next_url = safe_next_url(request, request.GET.get("next"))
    if request.session.get("rank", 0) != 0:
        return redirect(next_url)

    return render(request, "account/signin.html", {
        "next_url": next_url,
        "google_auth_url": request.build_absolute_uri(reverse("account:authG")),
        "google_client_id": GOOGLE_CLIENT_ID,
    })


def signin_form(request):
    next_url = safe_next_url(
        request,
        request.POST.get("next") or request.GET.get("next"),
    )
    if request.session.get("rank", 0) != 0:
        return redirect(next_url)

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        account = AccountCreation.objects.filter(
            username__iexact=username,
            status="accepted",
        ).first()

        if account is None:
            # Spend comparable time checking credentials for unknown users.
            AccountCreation().set_password(password)
        elif account.check_password(password):
            member = Member.objects.filter(email__iexact=account.email).first()
            if member is None:
                member = Member.objects.create(
                    name=account.displayname,
                    email=account.email,
                    ranking=1,
                )
            request.session["rank"] = member.ranking
            request.session["user"] = member.pk
            request.session["name"] = member.name
            return redirect(next_url)

        return render(request, "account/signin_form.html", {
            "error": "The username or password is incorrect.",
            "next_url": next_url,
        })

    return render(request, "account/signin_form.html", {
        "next_url": next_url,
        "reset_done": request.GET.get("reset") == "done",
    })

def signup(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        username = request.POST.get("username", "").strip()
        displayname = request.POST.get("displayname", "").strip()
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirmpassword", "")

        if not all((email, username, displayname, password, confirm)):
            error = "Fill in all account fields."
        elif password != confirm:
            error = "The passwords do not match."
        elif len(password) < 8:
            error = "Your password must be at least 8 characters long."
        elif len(password) > AccountCreation.MAX_PASSWORD_LENGTH:
            error = "Your password is too long."
        elif AccountCreation.objects.filter(email__iexact=email).exists():
            error = "An account with that email already exists."
        elif AccountCreation.objects.filter(username__iexact=username).exists():
            error = "That username is already in use."
        else:
            account = AccountCreation(
                email=email,
                username=username,
                displayname=displayname,
                status="pending",
            )
            account.set_password(password)
            account.save()
            return render(request, "account/signup.html", {
                "error": "Your account request was submitted for review.",
            })

        return render(request, "account/signup.html", {"error": error})

    return render(request, "account/signup.html")

# if a user tries to sign out by URL, redirects to account. if there is a POST request to this url, flushes the session and sends them to confirmation
def signout(request):
    if request.method == "POST":
        request.session.flush()
    return redirect(reverse("account:default"))

@csrf_exempt
def authG(request):
    if request.method != "POST":
        return redirect(reverse("account:account_list"))

    csrf_token = request.POST.get("g_csrf_token")
    csrf_cookie = request.COOKIES.get("g_csrf_token")
    if not csrf_token:
        return render(request, "account/signedout.html", {
            "auth_error": "Something went wrong, no csrf token",
            "google_client_id": GOOGLE_CLIENT_ID,
        })
    if not csrf_cookie:
        return render(request, "account/signedout.html", {
            "auth_error": "Something went wrong, no csrf cookie",
            "google_client_id": GOOGLE_CLIENT_ID,
        })
    if csrf_token != csrf_cookie:
        return render(request, "account/signedout.html", {
            "auth_error": "Something went wrong, csrf token mismatch",
            "google_client_id": GOOGLE_CLIENT_ID,
        })

    credential = request.POST.get("credential", "")
    if not credential:
        return render(request, "account/signedout.html", {
            "auth_error": "Something went wrong, missing Google credential",
            "google_client_id": GOOGLE_CLIENT_ID,
        })

    result = google_signin(request)
    if getattr(result, "status_code", 200) == 200:
        payload = json.loads(result.content)
        if payload.get("success"):
            return redirect(safe_next_url(request, request.POST.get("state")))
    return render(request, "account/signedout.html", {
        "auth_error": "Google sign-in could not be verified.",
        "google_client_id": GOOGLE_CLIENT_ID,
    })

 
 # default account page. send to sign in if not signed in, otherwise displays user info
def default(request):
    if request.session.get('rank',0)==0:
        return redirect(reverse("account:signin"))
    else:
        userInz=Member.objects.get(pk=request.session['user']) #get user from session
        visible_posts = MapPost.objects.filter(
            author=userInz, visibility=1
        ).order_by("-created")
        return render(request, 'account/myaccount.html', {
            'name': userInz.name,
            'email' : userInz.email,
            'image' : userInz.pic,
            'about' : userInz.about,
            'visible_posts': visible_posts,
        })
    
def account_all(request):
    search = SearchAccountForm(request.GET)
    query = request.GET.get("q", "").strip()
    letter = request.GET.get("letter", "").strip().upper()
    if letter not in ascii_uppercase:
        letter = ""
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
    if letter:
        members = members.filter(name__istartswith=letter)

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
        values = {"q": query, "letter": letter, "s": sort, "page": page_obj.number}
        values.update(updates)
        return "?" + urlencode({key: value for key, value in values.items() if value not in ("", None)}
                               )

    return render(request, "account/account_list.html", {
        "is_signed_in": request.session.get("rank", 0) > 0,
        "search": search,
        "search_query": query,
        "selected_letter": letter,
        "letter_links": [
            {"letter": alphabet_letter, "url": query_string(letter=alphabet_letter, page=1)}
            for alphabet_letter in ascii_uppercase
        ],
        "sort_value": sort,
        "page_obj": page_obj,
        "users": page_obj.object_list,
        "qs_clear_search": query_string(q="", page=1),
        "qs_reset": query_string(q="", letter="", s="0", page=1),
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
    view_inz = get_object_or_404(Member, pk=want)
    return render(request, "account/profile.html", {
        "profile": view_inz,
        "visible_posts": MapPost.objects.filter(
            author=view_inz, visibility=1
        ).order_by("-created"),
    })
    

# the username/password account that belongs to a signed-in member, or None if they only sign in with Google.
# members and their password accounts are linked by email, the same way signin_form links them
def password_account_for(member):
    return AccountCreation.objects.filter(email__iexact=member.email, status="accepted").first()

# checks the change password form and returns an error message, or None if the new password can be saved
def password_change_error(account, current, new, confirm):
    if not (current and new and confirm):
        return "Fill in all three password fields."
    if not account.check_password(current):
        return "Your current password is incorrect."
    if new != confirm:
        return "The new passwords do not match."
    if new == current:
        return "Your new password must be different from your current password."
    if len(new) < 8:
        return "Your new password must be at least 8 characters long."
    max_length = AccountCreation.MAX_PASSWORD_LENGTH
    if len(new) > max_length:
        return f"Your new password must be at most {max_length} characters long."
    return None

# lets members edit their info
def manage(request):
    if request.session.get('rank',0)==0:
        return redirect('/account/signin/')
    if request.method == "POST":
        userInz=Member.objects.get(pk=request.session['user']) 
        if "change_password" in request.POST:
            account = password_account_for(userInz)
            if account is None:
                password_error = "This account does not use a password."
            else:
                password_error = password_change_error(
                    account,
                    request.POST.get("current_password", ""),
                    request.POST.get("new_password", ""),
                    request.POST.get("confirm_password", ""),
                )
                if password_error is None:
                    account.set_password(request.POST["new_password"])
                    account.save(update_fields=["password"])
                    return redirect(reverse("account:manage") + "?password=changed")
            form = ManageForm(instance=userInz)
            return render(request, "account/manage.html", {
                "form": form,
                "current_profile_image": userInz.pic,
                "has_password": account is not None,
                "password_error": password_error,
                "password_changed": False,
            })

        form = ManageForm(request.POST, request.FILES, instance=userInz)
        if form.is_valid():
            form.save()
            request.session['name']=userInz.name
            return redirect("/account/")
    else:
        userInz=Member.objects.get(pk=request.session['user'])
        form = ManageForm(instance=userInz)
    return render(request, "account/manage.html", {
        "form": form,
        "current_profile_image": userInz.pic,
        "has_password": password_account_for(userInz) is not None,
        "password_changed": request.GET.get("password") == "changed",
    })

# a lot of this code is from google btw. this view verifies google one touch log in credentials
#view for creating forums
def make_forum(request):
    if(request.session.get('rank',0) == 0): #if user is not signed in, require sign in
        return redirect(reverse("account:signin"))
    if request.method == "POST":
        content_form = CreateForumForm(request.POST, request.FILES)
        if content_form.is_valid():
            author = Member.objects.get(pk=request.session["user"])
            content = content_form.cleaned_data["content"]
            description = content[:35] + "..." if len(content) > 35 else content
            visibility = 1 if request.session["rank"] > 1 else 0
            geo_result = content_form.cleaned_data["geoResult"]
            geo_code = geo_result

            forum = MapPost.objects.create(
                title=content_form.cleaned_data["title"],
                content=content,
                author=author,
                description=description,
                geoCode=geo_code,
                visibility=visibility,
                comments_enabled=not content_form.cleaned_data["disable_comments"],
            )
            if content_form.cleaned_data.get("tags"):
                forum.tags.set(content_form.cleaned_data["tags"])
            return redirect(reverse("account:my_forums") + "?success=1")
    else:
        content_form = CreateForumForm()
    return render(request, "account/create_forum.html", {
        "form": content_form,
        "GOOGLE_API_KEY": settings.GOOGLE_API_KEY,
    })

def create_forum(request):
    return make_forum(request)

def my_forums(request):
    if request.session.get("rank", 0) == 0:
        return redirect(reverse("account:signin"))

    member = Member.objects.get(pk=request.session["user"])
    posts = MapPost.objects.filter(author=member).order_by("-created")
    return render(request, "account/myForums.html", {
        "vis": posts.filter(visibility=1),
        "pend": posts.filter(visibility=0),
        "den": posts.filter(visibility=-1),
        "forum_just_submitted": request.GET.get("success") == "1",
        "forum_just_updated": request.GET.get("updated") == "1",
    })

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        account = AccountCreation.objects.filter(
            email__iexact=email,
            status="accepted",
        ).first()
        if account is not None:
            uid = urlsafe_base64_encode(force_bytes(account.pk))
            token = signing.dumps(account.pk, salt="account.password_reset")
            reset_url = reverse(
                "account:reset_password",
                kwargs={"uidb64": uid, "token": token},
            )
            try:
                send_mail(
                    "Reset your Chesapeake Community Connect password",
                    f"Use this link to reset the password for \"{account.username}\":\n\n"
                    f"{request.build_absolute_uri(reset_url)}",
                    getattr(settings, "DEFAULT_FROM_EMAIL", "webmaster@localhost"),
                    [account.email],
                )
            except Exception:
                logger.exception("Password reset email delivery failed")
        return render(request, "account/forgot_password.html", {
            "sent": True,
            "email": email,
        })

    return render(request, "account/forgot_password.html")

def reset_password(request, uidb64, token):
    account = None
    invalid = False
    try:
        account_pk = force_str(urlsafe_base64_decode(uidb64))
        account = AccountCreation.objects.get(pk=account_pk)
        signed_pk = signing.loads(
            token,
            salt="account.password_reset",
            max_age=getattr(settings, "PASSWORD_RESET_TIMEOUT", 3600),
        )
        if str(signed_pk) != str(account.pk):
            invalid = True
    except Exception:
        invalid = True

    used_tokens = request.session.get("used_password_reset_tokens", [])
    if not invalid and token in used_tokens:
        invalid = True

    if invalid:
        return render(request, "account/reset_password.html", {"invalid": True})

    if request.method == "POST":
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("confirm_password", "")
        if new_password != confirm_password:
            error = "The passwords do not match."
        elif len(new_password) < 8:
            error = "Your password must be at least 8 characters long."
        elif len(new_password) > AccountCreation.MAX_PASSWORD_LENGTH:
            error = "Your password is too long."
        else:
            account.set_password(new_password)
            account.save(update_fields=["password"])
            used_tokens.append(token)
            request.session["used_password_reset_tokens"] = used_tokens
            return redirect(reverse("account:signin_form") + "?reset=done")

        return render(request, "account/reset_password.html", {
            "username": account.username,
            "error": error,
        })

    return render(request, "account/reset_password.html", {
        "username": account.username,
    })
