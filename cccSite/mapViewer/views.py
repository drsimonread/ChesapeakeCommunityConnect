from django.core import serializers
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from Filterer.views import TextSearch, FilterSearch
from .forms import SearchPostsForm
from django.db.models import Q

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
    widgets = serializers.serialize('json', MapWidget.objects.all())
    print(widgets)  # Temporary print statement to check the output
    return render(request, 'mapViewer/mapPage.html', {'widgets': widgets})

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
    return HttpResponse("hi")

#this is practice of using url args and absolute URLs of a model. see models.py and urls.py to see how its working
def post_detail(request, want):
    if MapPost.objects.filter(pk=want).exists():
        lookAt= MapPost.objects.get(pk=want)
        if lookAt.isVisible or request.session.get('rank',0)>1:
            return render(request, "mapViewer/viewPost.html", {"post" : lookAt,})
    return redirect(reverse("mapViewer:post_list"))