from django.core import serializers
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from Filterer.views import TextSearch, FilterSearch
from account.models import Member
from .forms import *
from django.db.models import Q
import googlemaps
from datetime import datetime

def save_widget(request):
    if request.method == "POST":
        MapWidget.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            latitude=request.POST.get('latitude'),
            longitude=request.POST.get('longitude')
        )
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)


def viewMap(request):
    posts = MapPost.objects.filter(isVisible=True) #begin by fetching visible posts from database
    madePostSuccess = False #assume the user did not just post
    if(request.method=="POST"): #if the request was a post, it is an attempt to create a post
        postingForm= MakePostForm(request.POST) #create the posting form instance and populate it with the data in the POST request
        madePostSuccess = postingForm.is_valid() #if the data is valid (more info on this in mapViewer/forms.py)
        if madePostSuccess: #if the post is good to go
            userInz=Member.objects.get(pk=request.session['user']) #get user's member instance from session
            latLong=postingForm.cleaned_data['geoResult'][0]['geometry']['location'] #get the latitude/longitude from the form
            if len(postingForm.cleaned_data['content']) > 25: #if content overflows the preview length
                disc = postingForm.cleaned_data['content'][slice(0,25)] + "..." #create description to act as a preview
            else:
                disc = postingForm.cleaned_data['content'] #otherwise just use content to describe
            postInz=MapPost.objects.create(title=postingForm.cleaned_data['title'], #actually create the post instance in the database
                                   content=postingForm.cleaned_data['content'],
                                   author=userInz,
                                   description=disc,
                                   latitude=latLong['lat'],
                                   longitude=latLong['lng'],
                                   isVisible=request.session['rank']>1
                                   )
            if postingForm.cleaned_data['tags']:
                postInz.tags.set(postingForm.cleaned_data['tags']) #set the post's tags according to selected tags
    else: #if not POST, create a post form with no initial data
        postingForm = MakePostForm()
    contQuery = request.GET.get("q") #get content and tag query from url
    tagQuery = request.GET.getlist("t")
    searchForm = SearchPostsForm(request.GET) #create a search form from url
    if contQuery: #filter the posts according to search queries if the search queries are nonempty
        posts = posts.filter(Q(title__icontains=contQuery) | Q(content__icontains=contQuery) )
    if tagQuery:
        for tag in tagQuery:
            posts=posts.filter(tags__pk=tag)
    widgets = serializers.serialize('json', posts) #serialize posts as JSON for google maps
    #print(widgets)  # Temporary print statement to check the output
    return render(request, 'mapViewer/mapPage.html', {'widgets': widgets,
                                                      'postForm' : postingForm,
                                                      'searchForm' : searchForm,
                                                      'hasPosted': madePostSuccess}) #render template

def search_widgets(request):
    if (request.GET.get('searchBtn')):
        searchText = request.GET.get('search-text')
        return JsonResponse({"status":"success"})
    return JsonResponse({"status": "error"}, status = 400)


def post_list(request):
    contQuery = request.GET.get("q")
    tagQuery = request.GET.getlist("t")
    form = SearchPostsForm(request.GET)
    posts = MapPost.objects.filter(isVisible=True)
    if contQuery:
        posts = posts.filter(Q(title__icontains=contQuery) | Q(content__icontains=contQuery) )
    if tagQuery:
        for tag in tagQuery:
            posts=posts.filter(tags__pk=tag)
    posts = posts.order_by("id")
    return render(request, "mapViewer/listPosts.html", {"postList" : posts,
                                                        "form" : form})


#this is practice of using url args and absolute URLs of a model. see models.py and urls.py to see how its working
def post_detail(request, want):
    if MapPost.objects.filter(pk=want).exists():
        lookAt= MapPost.objects.get(pk=want)
        if lookAt.isVisible or request.session.get('rank',0)>1:
            return render(request, "mapViewer/viewPost.html", {"post" : lookAt,})
    return redirect(reverse("mapViewer:default"))