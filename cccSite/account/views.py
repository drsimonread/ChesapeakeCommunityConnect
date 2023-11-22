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
@csrf_exempt
def signin(request):
    if request.session.get('rank', 'anon')=='anon':
        return render(request, 'account/signin.html')
    else:
        return redirect("/account/")

@csrf_exempt
def default(request):
    if request.session.get('rank','anon')=='anon':
        return redirect('/account/signin/')
    else:
        return HttpResponse("you are logged in")

@csrf_exempt
def auth(request):
    if request.method == "GET":
       return redirect("/account/")
    elif request.method == "POST":
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