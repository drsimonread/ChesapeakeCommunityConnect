from google.oauth2 import id_token
from google.auth.transport import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from PIL import Image


# if user not signed in, sends them to log in

def signin(request):
    if request.session.get('rank', 0) == 0:
        return render(request, 'account/signin.html')
    else:
        return redirect('/account/')


# if a user tries to sign out by URL, redirects to account. if there is a POST request to this url, flushes the session and sends them to confirmation

def signout(request):
    if request.method == "POST":
        request.session.flush()
    return redirect(reverse("account:default"))


# default account page. send to sign in if not signed in, otherwise displays user info

def default(request):
    if request.session.get('rank', 0) == 0:
        return redirect(reverse("account:signin"))
    else:
        userInz = Member.objects.get(pk=request.session['user'])
        return render(request, 'account/myaccount.html', {
            'name': userInz.name,
            'email': userInz.email,
            'image': userInz.pic,
            'about': userInz.about,
        })


def account_all(request):
    return HttpResponse("insert account view list here")


def account_view(request, want):
    if not want:
        return HttpResponse("Insert list view here")
    if not Member.objects.get(pk=want):
        return redirect(reverse("account:default"))
    viewInz = Member.objects.get(pk=want)
    if request.session.get('rank', 0) != 0:
        userInz = Member.objects.get(request.session['user'])
    else:
        userInz = Member.objects.none()


# lets members edit their info

def manage(request):
    if request.session.get('rank', 0) == 0:
        return redirect('/account/signin/')
    if request.method == "POST":
        userInz = Member.objects.get(pk=request.session['user'])
        form = ManageForm(request.POST, request.FILES, instance=userInz)
        if form.is_valid():
            form.save()
            request.session['name'] = userInz.name
            return redirect('/account/')
    else:
        userInz = Member.objects.get(pk=request.session['user'])
        form = ManageForm(instance=userInz)
    return render(request, "account/manage.html", {'form': form})


# a lot of this code is from google btw
@csrf_exempt

def authG(request):
    if request.method == "GET":
        return redirect('/account/')
    elif request.method == "POST":
        csrf_tok_cookie = request.COOKIES.get('g_csrf_token')
        if not csrf_tok_cookie:
            return HttpResponse("Something went wrong, no csrf cookie")
        csrf_tok_body = request.POST.get('g_csrf_token')
        if not csrf_tok_body:
            return HttpResponse("Something went wrong, no csrf cookie from google")
        if csrf_tok_cookie != csrf_tok_body:
            return HttpResponse("Could not verify csrf")

        tok = request.POST.get('credential')
        try:
            idinfo = id_token.verify_oauth2_token(
                tok,
                requests.Request(),
                "316865720473-94ccs1oka6ev4kmlv5ii261dirvjkja0.apps.googleusercontent.com"
            )
            if not GLogIn.objects.filter(googleID=idinfo['sub']).exists():
                userInz = Member.objects.create(name=idinfo['given_name'], email=idinfo['email'])
                GLogIn.objects.create(googleID=idinfo['sub'], referTo=userInz)
            else:
                gLogInz = GLogIn.objects.get(googleID=idinfo['sub'])
                userInz = gLogInz.referTo

            request.session['rank'] = userInz.ranking
            request.session['user'] = userInz.pk
            request.session['name'] = userInz.name
        except ValueError:
            return HttpResponse("Something went wrong, invalid credentials from Google (somehow)")

        return redirect('/account/')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password1', '')

        if username and email and password:
            member = Member.objects.create(name=username, email=email)
            request.session['rank'] = member.ranking
            request.session['user'] = member.pk
            request.session['name'] = username
            return redirect('/account/')

    return render(request, 'account/signedout.html')


def username_validation(request):
    username = request.GET.get('username', '').strip()
    is_taken = bool(Member.objects.filter(name=username).exists())
    return JsonResponse({'is_taken': is_taken})


def email_validation(request):
    email = request.GET.get('email', '').strip()
    is_taken = bool(Member.objects.filter(email=email).exists())
    return JsonResponse({'is_taken': is_taken})
