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
from django.shortcuts import get_object_or_404, render
from .models import MapPost

def slideshow_popup(request, post_id):
    post = get_object_or_404(MapPost, pk=post_id)
    files = post.postfile_set.all()
    return render(request, 'mapViewer/slideshow_popup.html', {'post': post, 'files': files})

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
        files = PostFile.objects.filter(post=lookAt)
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
                                                               "hasReported" : hasReported,
                                                               "files" : files})
    return redirect(reverse("mapViewer:default"))