from django.core import serializers
from django.shortcuts import render, redirect
from account import views
from django.urls import reverse
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from account.models import Member
from .forms import *
from django.db.models import Q
import googlemaps
from datetime import datetime
from Janitor.forms import PostRepForm


def make_post(request):
    if(request.session.get('rank',0) == 0):
        return redirect(reverse("account:signin"))
    if(request.method=="POST"): #if the request was a post, it is an attempt to create a post
        form= MakePostForm(request.POST, request.FILES) #create the posting form instance and populate it with the data in the POST request
        if form.is_valid(): #if the post is good to go
            userInz=Member.objects.get(pk=request.session['user']) #get user's member instance from session\
            if len(form.cleaned_data['content']) > 35: #if content overflows the preview length
                disc = form.cleaned_data['content'][slice(0,35)] + "..." #create description to act as a preview
            else:
                disc = form.cleaned_data['content'] #otherwise just use content to describe
            vis=0
            if request.session['rank'] > 1:
                vis=1
            postInz=MapPost.objects.create(title=form.cleaned_data['title'], #actually create the post instance in the database
                                   content=form.cleaned_data['content'],
                                   author=userInz,
                                   description=disc,
                                   geoCode=form.cleaned_data['geoResult'][0],
                                   visibility=vis
                                   )
            if form.cleaned_data['tags']:
                postInz.tags.set(form.cleaned_data['tags']) #set the post's tags according to selected tags
            if form.cleaned_data['files']:
                for f in form.cleaned_data['files']:
                    fileInz = PostFile.objects.create(post=postInz, file=f)
    else:
        form = MakePostForm()
    
    return render(request, 'mapViewer/create_post.html', {'form': form})

def viewMap(request):
    posts = MapPost.objects.filter(visibility=1) #begin by fetching visible posts from database
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
                                                      'searchForm' : searchForm,}) #render template



def post_list(request):
    contQuery = request.GET.get("q")
    tagQuery = request.GET.getlist("t")
    form = SearchPostsForm(request.GET)
    posts = MapPost.objects.filter(visibility=1)
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
    hasReported=False
    if MapPost.objects.filter(pk=want).exists():
        lookAt= MapPost.objects.get(pk=want)
        if request.method == 'POST':
            reporter = PostRepForm(request.POST)
            hasReported = reporter.is_valid()
            if hasReported:
                reporter.save()
        else:
            reporter = PostRepForm(initial={'post':lookAt})
        if lookAt.visibility>0 or request.session.get('rank',0)>1 or lookAt.author.pk==request.session.get('user',-1):
            return render(request, "mapViewer/viewPost.html", {"post" : lookAt,
                                                               "form" : reporter,
                                                               "hasReported" : hasReported})
    return redirect(reverse("mapViewer:default"))