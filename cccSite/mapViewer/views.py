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
    posts = MapPost.objects.filter(isVisible=True)
    madePostSuccess = False
    if(request.method=="POST"):
        gmaps = googlemaps.Client(key='AIzaSyAH_5F4XRcZh8_OZib8cUD-DoE7ust60lc')
        postingForm= MakePostForm(request.POST)
        madePostSuccess = postingForm.is_valid()
        if madePostSuccess:
            userInz=Member.objects.get(pk=request.session['user'])
            latLong=postingForm.cleaned_data['geoResult'][0]['geometry']['location']
            if len(postingForm.cleaned_data['content']) > 25:
                disc = postingForm.cleaned_data['content'][slice(0,25)] + "..."
            else:
                disc = postingForm.cleaned_data['content']
            postInz=MapPost.objects.create(title=postingForm.cleaned_data['title'],
                                   content=postingForm.cleaned_data['content'],
                                   author=userInz,
                                   description=disc,
                                   latitude=latLong['lat'],
                                   longitude=latLong['lng'],
                                   isVisible=request.session['rank']>1
                                   )
            if postingForm.cleaned_data['tags']:
                postInz.tags.set(postingForm.cleaned_data['tags'])
    else:
        postingForm = MakePostForm()
    contQuery = request.GET.get("q")
    tagQuery = request.GET.getlist("t")
    searchForm = SearchPostsForm(request.GET)
    if contQuery:
        posts = posts.filter(Q(title__icontains=contQuery) | Q(content__icontains=contQuery) )
    if tagQuery:
        for tag in tagQuery:
            posts=posts.filter(tags__pk=tag)
    widgets = serializers.serialize('json', posts)
    print(widgets)  # Temporary print statement to check the output
    return render(request, 'mapViewer/mapPage.html', {'widgets': widgets,
                                                      'postForm' : postingForm,
                                                      'searchForm' : searchForm,
                                                      'hasPosted': madePostSuccess})

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


def makePost(request):
    if request.method == "POST":
        gmaps = googlemaps.Client(key='AIzaSyAH_5F4XRcZh8_OZib8cUD-DoE7ust60lc')
        postingForm= MakePostForm(request.POST)
        if postingForm.is_valid():
            loc = gmaps.geocode(address=request.POST.get('location'), components={'administrative_area': 'MD','country': 'US'})
            print(loc)
    else:
        if request.session.get('rank',0)!=0:
            postingForm = MakePostForm()
        
    return render(request, 'mapViewer/makePost.html', {'form':postingForm})

#this is practice of using url args and absolute URLs of a model. see models.py and urls.py to see how its working
def post_detail(request, want):
    if MapPost.objects.filter(pk=want).exists():
        lookAt= MapPost.objects.get(pk=want)
        if lookAt.isVisible or request.session.get('rank',0)>1:
            return render(request, "mapViewer/viewPost.html", {"post" : lookAt,})
    return redirect(reverse("mapViewer:post_list"))