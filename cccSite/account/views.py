from google.oauth2 import id_token
from google.auth.transport import requests
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import member
from google.oauth2 import id_token
from google.auth.transport import requests

# Create your views here.
def signin(request):
    if request.session.get('rank', 'anon')=='anon':
        return render(request, 'account/signin.html')
    else:
        return redirect("/account/")

def signout(request):
    if request.method == "GET":
        return redirect("/account/")
    else:
        request.session.flush()
        return render(request, "account/signout.html")


def default(request):
    if request.session.get('rank','anon')=='anon':
        return redirect('/account/signin/')
    else:
        userInz=member.objects.get(userID=request.session['user'])
        return render(request, 'account/myaccount.html', {
            "first_name": userInz.first,
            'last_name' : userInz.last,
            'email' : userInz.email,
            'rank' : userInz.ranking,
        })

@csrf_exempt #the csrf is from google, not django, and is verified. can't get django's csrf to work tho due to origin of post
def auth(request):
    if request.method == "GET":
       return redirect("/account/")
    elif request.method == "POST":

        csrf_tok_cookie = request.COOKIES.get('g_csrf_token')
        
        if not csrf_tok_cookie:
            return HttpResponse("Something went wrong, no csrf cookie")
        csrf_tok_body = request.POST.get('g_csrf_token')
        if not csrf_tok_body:
            return HttpResponse("Something went wrong, no csrf cookie from google")
        if csrf_tok_cookie != csrf_tok_body:
            return HttpResponse("Could not verify csrf")

        tok = request.POST.get("credential")  
        try:
            idinfo = id_token.verify_oauth2_token(tok, requests.Request(), "316865720473-94ccs1oka6ev4kmlv5ii261dirvjkja0.apps.googleusercontent.com")
            if not(member.objects.filter(userID=idinfo['sub']).exists()):
                userInz = member.objects.create(userID=idinfo['sub'], first=idinfo['given_name'], last=idinfo['family_name'], email = idinfo['email'])
            else:
                userInz=member.objects.get(userID=idinfo['sub'])
            request.session['rank']=userInz.ranking
            request.session['user']=userInz.userID
            request.session['name']=userInz.first
        except ValueError:
            return HttpResponse("Something went wrong, invalid credentials from Google (somehow)")
            pass
        return redirect("/account/")