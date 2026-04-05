from django.core import serializers
from django.shortcuts import render, redirect
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
from .models import MapPost, MapTag



def viewMap(request):
    posts = MapPost.objects.filter(visibility=1) #begin by fetching visible posts from database
    madePostSuccess = False #assume the user did not just post
    if(request.method=="POST"): #if the request was a post, it is an attempt to create a post
        postingForm= MakePostForm(request.POST) #create the posting form instance and populate it with the data in the POST request
        madePostSuccess = postingForm.is_valid() #if the data is valid (more info on this in mapViewer/forms.py)
        if madePostSuccess: #if the post is good to go
            userInz=Member.objects.get(pk=request.session['user']) #get user's member instance from session\
            if len(postingForm.cleaned_data['content']) > 35: #if content overflows the preview length
                disc = postingForm.cleaned_data['content'][slice(0,35)] + "..." #create description to act as a preview
            else:
                disc = postingForm.cleaned_data['content'] #otherwise just use content to describe
            vis=0
            if request.session['rank'] > 1:
                vis=1
            postInz=MapPost.objects.create(title=postingForm.cleaned_data['title'], #actually create the post instance in the database
                                   content=postingForm.cleaned_data['content'],
                                   author=userInz,
                                   description=disc,
                                   geoCode=postingForm.cleaned_data['geoResult'][0],
                                   visibility=vis
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
    if Forum.objects.filter(pk=want).exists():
        lookAt= Forum.objects.get(pk=want)
        files = Media.objects.filter(forum=lookAt)
        forumData = {
            "title": lookAt.title,
            "description": lookAt.description,
        }

        if request.method == 'POST':
            reporter = PostRepForm(request.POST)
            hasReported = reporter.is_valid()
            if hasReported:
                reporter.save()
        else:
            reporter = PostRepForm(initial={'post':lookAt})
        if lookAt.visibility>0 or request.session.get('rank',0)>1 or lookAt.author.pk==request.session.get('user',-1):
            
            if lookAt.visibility==0:
                msg="Your forum is currently pending approval and only visible to you."
            elif lookAt.visibility == -1:
                msg="Your forum has been denied for the following reason: {0}.\nTo resubmit, please create a new forum.".format(lookAt.description)
            else:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
                    # Render each post using the postTemplate
                    post_html = [
                        render_to_string('mapViewer/postTemplate.html', {'post': post, 'forum': lookAt, 'page_obj': page_obj.number})
                        for post in page_obj.object_list
                    ]
                    return JsonResponse({
                        'posts': post_html,
                        'has_next': page_obj.has_next()
                    })
                
                # Initial render for the HTML template
                return render(request, "mapViewer/viewForum.html", {"forum" : lookAt,
                                                                "form" : reporter,
                                                                "forumData": forumData,
                                                                "hasReported" : hasReported,
                                                                "files" : files,
                                                                "msg" : msg,
                                                                "posts" : page_obj, 
                                                                "page_number" : page_obj.number
                                                                })                
    return redirect(reverse("mapViewer:default"))


    #view for creating forums
def make_post(request):
    if(request.session.get('rank',0) == 0): #if user is not signed in, require sign in
        return redirect(reverse("account:signin"))
    if(request.method=="POST"): #if the request was a post, it is an attempt to create a forum
        contentForm= MakeForumForm(request.POST, request.FILES) #create the posting form instance and populate it with the data in the POST request
        if contentForm.is_valid(): #if the forum is good to go, calls the clean method and validators from MakeForumForm in mapViewer/forms.py
            # MEMBER_DELETE
            userInz=Member.objects.get(pk=request.session['user']) #get user's member instance from session
            if len(contentForm.cleaned_data['content']) > 35: #if content overflows the preview length
                disc = contentForm.cleaned_data['content'][slice(0,35)] + "..." #create description to act as a preview
            else:
                disc = contentForm.cleaned_data['content'] #otherwise just use content to describe #? Why does description exist at all?
            vis=0 #default visibility set to pending
            if request.session['rank'] > 1: #if user is trusted, set visibility to visible
                vis=1
            forumInz=Forum.objects.create(title=contentForm.cleaned_data['title'], #actually create the forum instance in the database
                                   content=contentForm.cleaned_data['content'],
                                   author=userInz,
                                   description=disc,
                                   geoCode=contentForm.cleaned_data['geoResult'][0],
                                   visibility=vis,
                                   associated=contentForm.cleaned_data['associated'],
                                   private_public=contentForm.cleaned_data['private_public']
                                   )
            if contentForm.cleaned_data['tags']: #if there are any tags
                forumInz.tags.set(contentForm.cleaned_data['tags']) #set the forum's tags according to selected tags
            
            if contentForm.cleaned_data['files']: #if there are files uploaded
                for item in contentForm.cleaned_data['files']: #iterates through file upload fields
                    if item != None: #if item is none, then nothing was uploaded
                        fileInz = Media.objects.create(forum=forumInz, file=item) #create a forumfile instance
                        fileInz.format = fileInz.get_format() #get the format and set the format
                        fileInz.save() #save the updated format
            return redirect(reverse('mapViewer:forum_detail', args=[forumInz.pk])) #redirect to the forum view of the just posted forum
            
    else:
        contentForm = MakeForumForm()
    return render(request, 'account/create_forum.html', {'form': contentForm,})

def post_detail(request, want, wants):
    if Forum.objects.filter(pk=want).exists():
        lookAt= Forum.objects.get(pk=want)
        lookAtPost= Post.objects.get(pk=wants)
        comments = lookAtPost.comments.all()
        forumData = {
            "title": lookAt.title,
            "description": lookAt.description,
        }

        return render(request, "mapViewer/viewPost.html", {"forum" : lookAt,
                                                            "Post" : lookAtPost,
                                                            "forumData": forumData,
                                                            "comments" : comments,})

def create_comment(request, want, wants):
    if(request.session.get('rank',0) == 0): #if user is not signed in, require sign in
        return redirect(reverse("account:signin"))
    if(request.method=="POST"): #if the request was a post, it is an attempt to create a forum
        if Forum.objects.filter(pk=want).exists():
            # lookAt= Forum.objects.get(pk=want)
            #TODO Make sure the post exists
            lookAtPost= Post.objects.get(pk=wants)
            contentComment= MakeCommentsForm(request.POST) #create the posting form instance and populate it with the data in the POST request
            if contentComment.is_valid(): #if the forum is good to go, calls the clean method and validators from MakeForumForm in mapViewer/forms.py
                # MEMBER_DELETE
                userInz=Member.objects.get(pk=request.session['user']) #get user's member instance from session
                commenntInz=Comment.objects.create(content=contentComment.cleaned_data['content'],
                                    author=userInz,
                                    post=lookAtPost
                                    )
                commenntInz.save()
    return redirect(reverse('mapViewer:post_detail', args=[want, wants])) #redirect to the forum view of the just posted forum
            
    # else:
    #     contentComment = MakeForumForm()
    # return render(request, 'account/.html', {'form': contentComment,})
