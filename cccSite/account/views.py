from google.oauth2 import id_token
from google.auth.transport import requests
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from PIL import Image

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
            'name': userInz.name,
            'email' : userInz.email,
            'image' : userInz.pic,
            'about' : userInz.about,
        })
    
def account_all(request):
    return HttpResponse("insert account view list here")
    
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

# a lot of this code is from google btw
@csrf_exempt #the csrf is from google, not django, and is verified. can't get django's csrf to work tho due to origin of post
def authG(request):
    if request.method == "GET":
       return redirect("/account/")
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
        return redirect("/account/")