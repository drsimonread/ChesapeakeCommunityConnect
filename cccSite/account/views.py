from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction

from .models import (
    Member,
    GLogIn,
    ManageForm,
    MessageForm,
    UPLogIn,
)

from mapViewer.forms import MakePostForm
from mapViewer.models import MapPost


GOOGLE_CLIENT_ID = (
    "909497695712-h9smcju9klvlqk70celohtne9o438htn.apps.googleusercontent.com"
)


# ---------------------------------------------------------
# GOOGLE SIGN-IN
# ---------------------------------------------------------

@require_http_methods(["GET", "POST"])
def google_signin(request):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "POST required"},
            status=405,
        )

    token = request.POST.get("credential", "")

    if not token:
        return JsonResponse(
            {"success": False, "message": "Missing Google credential"},
            status=400,
        )

    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )
    except ValueError:
        return JsonResponse(
            {"success": False, "message": "Invalid Google token"},
            status=400,
        )

    google_id = idinfo.get("sub")
    email = idinfo.get("email", "").strip().lower()

    if (
        not google_id
        or not email
        or not idinfo.get("email_verified", False)
    ):
        return JsonResponse(
            {"success": False, "message": "Verified Google email required"},
            status=400,
        )

    display_name = (
        f"{idinfo.get('given_name', '')} "
        f"{idinfo.get('family_name', '')}"
    ).strip() or email.split("@")[0]

    try:
        with transaction.atomic():
            mapping = (
                GLogIn.objects
                .select_related("referTo")
                .filter(googleID=google_id)
                .first()
            )

            if mapping:
                member = mapping.referTo
                user = User.objects.filter(username=email).first()

                if user is None:
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                    )
            else:
                # Do not automatically link an existing account
                # just because its email matches Google's email.
                user = User.objects.filter(username=email).first()

                if user is None:
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                    )

                member = Member.objects.create(
                    name=display_name[:35],
                    ranking=1,
                )

                GLogIn.objects.create(
                    googleID=google_id,
                    referTo=member,
                )

            if member.ranking == -1:
                return JsonResponse(
                    {"success": False, "message": "This account is banned"},
                    status=403,
                )

            login(request, user)

            request.session["rank"] = member.ranking
            request.session["user"] = member.pk
            request.session["name"] = member.name

    except Exception:
        # Log the exception server-side when deploying.
        return JsonResponse(
            {"success": False, "message": "Unable to complete sign-in"},
            status=500,
        )

    return JsonResponse({"success": True})


# ---------------------------------------------------------
# SIGNUP
# ---------------------------------------------------------

@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"].strip()
            displayname = form.cleaned_data["displayname"].strip()
            password = form.cleaned_data["password"]

            if len(username) > 35:
                form.add_error(
                    "username",
                    "Username must be 35 characters or fewer.",
                )

            elif UPLogIn.objects.filter(username=username).exists():
                form.add_error(
                    "username",
                    "That username is already taken.",
                )

            else:
                with transaction.atomic():
                    member = Member.objects.create(
                        name=displayname[:35],
                        ranking=1,
                    )

                    UPLogIn.objects.create(
                        referTo=member,
                        username=username,
                        salt="",
                        password=make_password(password),
                    )

                messages.success(
                    request,
                    "Account created successfully. You can now sign in.",
                )

                return redirect("account:signin")

    else:
        form = MessageForm()

    return render(
        request,
        "account/signup.html",
        {"form": form},
    )


# ---------------------------------------------------------
# SIGNIN
# ---------------------------------------------------------

@require_http_methods(["GET", "POST"])
def signin(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        login_record = (
            UPLogIn.objects
            .select_related("referTo")
            .filter(username=username)
            .first()
        )

        if (
            login_record
            and check_password(password, login_record.password)
            and login_record.referTo.ranking != -1
        ):
            member = login_record.referTo

            request.session["rank"] = member.ranking
            request.session["user"] = member.pk
            request.session["name"] = member.name

            messages.success(request, "You are now signed in.")
            return redirect("account:default")

        messages.error(request, "Invalid username or password.")

    return render(request, "account/signin.html")


# ---------------------------------------------------------
# SIGNOUT
# ---------------------------------------------------------

@require_http_methods(["GET", "POST"])
def signout(request):
    if request.method == "POST":
        request.session.flush()
        return redirect("account:signin")

    return redirect("account:default")


# ---------------------------------------------------------
# DEFAULT ACCOUNT PAGE
# ---------------------------------------------------------

def default(request):
    if request.session.get("rank", 0) == 0:
        return redirect("account:signin")

    member_id = request.session.get("user")

    if not member_id:
        request.session.flush()
        return redirect("account:signin")

    member = get_object_or_404(Member, pk=member_id)

    return render(
        request,
        "account/myaccount.html",
        {
            "name": member.name,
            "image": member.pic,
            "about": member.about,
        },
    )


# ---------------------------------------------------------
# LIST ACCOUNTS
# ---------------------------------------------------------

def account_list(request):
    members = Member.objects.all().order_by("name")

    return render(
        request,
        "account/account_all.html",
        {"members": members},
    )



# ---------------------------------------------------------
# VIEW ONE ACCOUNT
# ---------------------------------------------------------

def account_view(request, want):
    member = get_object_or_404(Member, pk=want)

    return render(
        request,
        "account/account_view.html",
        {
            "member": member,
            "name": member.name,
            "image": member.pic,
            "about": member.about,
        },
    )


# ---------------------------------------------------------
# MANAGE OWN PROFILE
# ---------------------------------------------------------

@require_http_methods(["GET", "POST"])
def manage(request):
    if request.session.get("rank", 0) == 0:
        return redirect("account:signin")

    member_id = request.session.get("user")

    if not member_id:
        request.session.flush()
        return redirect("account:signin")

    member = get_object_or_404(Member, pk=member_id)

    if request.method == "POST":
        form = ManageForm(
            request.POST,
            request.FILES,
            instance=member,
        )

        if form.is_valid():
            form.save()
            request.session["name"] = member.name

            messages.success(request, "Your profile was updated.")
            return redirect("account:default")

    else:
        form = ManageForm(instance=member)

    return render(
        request,
        "account/manage.html",
        {"form": form},
    )


# ---------------------------------------------------------
# CREATE POST
# ---------------------------------------------------------

@require_http_methods(["GET", "POST"])
def make_forum(request):
    if request.session.get("rank", 0) == 0:
        return redirect("account:signin")

    member_id = request.session.get("user")

    if not member_id:
        request.session.flush()
        return redirect("account:signin")

    member = get_object_or_404(Member, pk=member_id)

    if request.method == "POST":
        content_form = MakePostForm(request.POST, request.FILES)

        if content_form.is_valid():
            content = content_form.cleaned_data["content"]

            description = (
                content[:35] + "..."
                if len(content) > 35
                else content
            )

            geo_result = content_form.cleaned_data.get("geoResult")

            if not geo_result:
                content_form.add_error(
                    "location",
                    "Please enter a valid address.",
                )
            else:
                visibility = (
                    1 if request.session.get("rank", 0) > 1 else 0
                )

                post = MapPost.objects.create(
                    title=content_form.cleaned_data["title"],
                    content=content,
                    author=member,
                    description=description,
                    geoCode=geo_result[0],
                    visibility=visibility,
                )

                tags = content_form.cleaned_data.get("tags")

                if tags:
                    post.tags.set(tags)

                return redirect(
                    reverse(
                        "mapViewer:post_detail",
                        args=[post.pk],
                    )
                )

    else:
        content_form = MakePostForm()

    return render(
        request,
        "account/create_forum.html",
        {"form": content_form},
    )