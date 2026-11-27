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
import smtplib
import time
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from PIL import Image
from .models import Member, GLogIn, AccountCreation

logger = logging.getLogger(__name__)

# YOUR SPECIFIC CLIENT ID
GOOGLE_CLIENT_ID = getattr(settings, "GOOGLE_CLIENT_ID", "")

def google_signin(request):
    if request.method != "POST":
        return JsonResponse({"success": False}, status=405)

    token = request.POST.get("credential", "")
    try:
        claims = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID,
        )
    except ValueError:
        return JsonResponse(
            {"success": False, "message": "Google sign-in could not be verified."},
            status=400,
        )

    google_id = claims.get("sub")
    email_claim = claims.get("email")
    email = email_claim.strip().lower() if isinstance(email_claim, str) else ""
    if not google_id or not email or claims.get("email_verified") is not True:
        return JsonResponse(
            {"success": False, "message": "Google must confirm this email address."},
            status=400,
        )

    session_member_id = request.session.get("user") if request.session.get("rank", 0) > 0 else None
    session_member = Member.objects.filter(pk=session_member_id).first()
    google_login = GLogIn.objects.filter(googleID=google_id).select_related("referTo").first()

    if session_member_id and session_member is None:
        return JsonResponse(
            {"success": False, "message": "Sign in again before linking Google."},
            status=401,
        )

    if google_login is not None:
        if session_member and google_login.referTo_id != session_member.pk:
            return JsonResponse(
                {"success": False, "message": "This Google account is linked to another member."},
                status=409,
            )
        member = google_login.referTo
    elif session_member is not None:
        authenticated_at = request.session.get("password_authenticated_at")
        try:
            recent_password_signin = 0 <= time.time() - float(authenticated_at) <= 300
        except (TypeError, ValueError):
            recent_password_signin = False

        if (
            not recent_password_signin
            or session_member.email.casefold() != email.casefold()
            or not AccountCreation.objects.filter(
                member=session_member,
                status="accepted",
                email_verified=True,
            ).exists()
        ):
            return JsonResponse(
                {
                    "success": False,
                    "message": "Sign in with your password before linking this Google account.",
                },
                status=403,
            )

        try:
            GLogIn.objects.create(googleID=google_id, referTo=session_member)
        except IntegrityError:
            google_login = GLogIn.objects.filter(
                googleID=google_id
            ).select_related("referTo").first()
            if google_login is None or google_login.referTo_id != session_member.pk:
                return JsonResponse(
                    {"success": False, "message": "This Google account is already linked."},
                    status=409,
                )
        member = session_member
    else:
        if Member.objects.filter(email__iexact=email).exists():
            return JsonResponse(
                {
                    "success": False,
                    "message": "Sign in with your password before linking Google to an existing account.",
                },
                status=409,
            )

        name = " ".join(
            part for part in (claims.get("given_name", ""), claims.get("family_name", ""))
            if part
        ).strip()
        try:
            with transaction.atomic():
                member = Member.objects.create(
                    name=name or email,
                    email=email,
                    ranking=1,
                )
                GLogIn.objects.create(googleID=google_id, referTo=member)
        except IntegrityError:
            google_login = GLogIn.objects.filter(
                googleID=google_id
            ).select_related("referTo").first()
            if google_login is None:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "An account with this email already exists. Sign in with your password.",
                    },
                    status=409,
                )
            member = google_login.referTo

    request.session["rank"] = member.ranking
    request.session["user"] = member.pk
    request.session["name"] = member.name
    if session_member is None:
        request.session.pop("password_authenticated_at", None)
    return JsonResponse({"success": True})
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
            email_verified=True,
        ).first()

        if account is None:
            # Spend comparable time checking credentials for unknown users.
            AccountCreation().set_password(password)
        elif account.check_password(password):
            member = account.member
            if member is None or not account.email_verified:
                return render(request, "account/signin_form.html", {
                    "error": "This account is not ready to sign in. Contact an administrator for help.",
                    "next_url": next_url,
                })
            request.session["rank"] = member.ranking
            request.session["user"] = member.pk
            request.session["name"] = member.name
            request.session["password_authenticated_at"] = time.time()
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
        email = request.POST.get("email", "").strip().lower()
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
        else:
            existing_email_account = AccountCreation.objects.filter(
                email__iexact=email
            ).first()
            if existing_email_account is not None:
                can_resend = (
                    existing_email_account.status in {"pending", "accepted"}
                    and not existing_email_account.email_verified
                    and existing_email_account.member_id is None
                    and existing_email_account.username.casefold() == username.casefold()
                    and existing_email_account.check_password(password)
                )
                if can_resend and _send_verification_email(request, existing_email_account):
                    return render(request, "account/signup.html", {
                        "message": "Check your email for a new confirmation link.",
                    })
                error = (
                    "We could not send a confirmation email. Please try again later."
                    if can_resend
                    else "An account with that email already exists."
                )
            elif AccountCreation.objects.filter(username__iexact=username).exists():
                error = "That username is already in use."
            elif Member.objects.filter(email__iexact=email).exists():
                error = "An account with that email already exists."
            else:
                account = AccountCreation(
                    email=email,
                    username=username,
                    displayname=displayname,
                    status="pending",
                )
                account.set_password(password)
                try:
                    account.save()
                except IntegrityError:
                    return render(request, "account/signup.html", {
                        "error": "That username or email is already in use.",
                    })
                if _send_verification_email(request, account):
                    return render(request, "account/signup.html", {
                        "message": "Check your email to confirm the address before your account request can be reviewed.",
                    })
                account.delete()
                error = "We could not send a confirmation email. Please try again later."

        return render(request, "account/signup.html", {"error": error})

    return render(request, "account/signup.html")


def _send_verification_email(request, account):
    token = signing.dumps(
        {"account_id": account.pk, "email": account.email},
        salt="account.email_verification",
    )
    confirmation_url = request.build_absolute_uri(
        reverse("account:verify_email", kwargs={"token": token})
    )
    try:
        sent = send_mail(
            "Confirm your Chesapeake Community Connect email",
            f"Confirm your email address by opening this link:\n\n{confirmation_url}\n\n"
            "This link expires in 24 hours.",
            getattr(settings, "DEFAULT_FROM_EMAIL", "webmaster@localhost"),
            [account.email],
            fail_silently=False,
        )
    except (OSError, smtplib.SMTPException):
        logger.exception("Account email-verification message could not be sent")
        return False
    return sent == 1


def verify_email(request, token):
    try:
        payload = signing.loads(
            token,
            salt="account.email_verification",
            max_age=24 * 60 * 60,
        )
    except (signing.BadSignature, signing.SignatureExpired):
        return render(request, "account/signup.html", {
            "error": "This confirmation link is invalid or has expired. Submit your sign-up again for a new link.",
        })

    account = AccountCreation.objects.filter(
        pk=payload.get("account_id"),
        email=payload.get("email"),
        status__in=("pending", "accepted"),
    ).first()
    if account is None:
        return render(request, "account/signup.html", {
            "error": "This confirmation link is invalid or has expired.",
        })
    if not account.email_verified:
        account.email_verified = True
        update_fields = ["email_verified"]
        if account.status == "accepted" and account.member_id is None:
            account.status = "pending"
            update_fields.append("status")
        account.save(update_fields=update_fields)

    return render(request, "account/signup.html", {
        "message": "Your email is confirmed. Your account request can now be reviewed by a moderator.",
    })

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
        auth_error = payload.get("message", "Google sign-in could not be verified.")
    else:
        auth_error = "Google sign-in could not be verified."
    return render(request, "account/signedout.html", {
        "auth_error": auth_error,
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
    return AccountCreation.objects.filter(
        member=member,
        status="accepted",
        email_verified=True,
    ).first()

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
    password_authenticated_at = request.session.get("password_authenticated_at")
    try:
        recent_password_signin = 0 <= time.time() - float(password_authenticated_at) <= 300
    except (TypeError, ValueError):
        recent_password_signin = False
    return render(request, "account/manage.html", {
        "form": form,
        "current_profile_image": userInz.pic,
        "has_password": password_account_for(userInz) is not None,
        "has_google_login": GLogIn.objects.filter(referTo=userInz).exists(),
        "can_link_google": (
            password_account_for(userInz) is not None
            and recent_password_signin
            and not GLogIn.objects.filter(referTo=userInz).exists()
        ),
        "google_client_id": GOOGLE_CLIENT_ID,
        "google_auth_url": request.build_absolute_uri(reverse("account:authG")),
        "google_link_return": request.build_absolute_uri(reverse("account:manage") + "?google=linked"),
        "google_linked": request.GET.get("google") == "linked",
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
