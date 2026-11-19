from django.core import serializers
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from account.models import Member
from .forms import *
from django.db.models import Q
import googlemaps
from googlemaps.exceptions import ApiError, Timeout, TransportError
from datetime import datetime
from Janitor.forms import CommentRepForm, PostRepForm
from .models import MapPost, MapTag, PostComment
import logging


logger = logging.getLogger(__name__)

def viewMap(request):
    posts = MapPost.objects.filter(visibility=1) #begin by fetching visible posts from database
    madePostSuccess = False #assume the user did not just post
    guest_post_form = GuestPostForm()
    guest_post_open = request.GET.get("guest_post") == "open"
    guest_post_submitted = request.GET.get("guest_post") == "submitted"
    if request.method == "POST" and request.POST.get("action") == "guest_post":
        guest_post_open = True
        guest_post_form = GuestPostForm(request.POST)
        if guest_post_form.is_valid():
            if not settings.GOOGLE_API_KEY:
                logger.error("Google Maps API key is not configured for guest post geocoding.")
                guest_post_form.add_error(
                    "address",
                    "Guest submissions are temporarily unavailable because address lookup is not configured.",
                )
            else:
                cleaned_data = guest_post_form.cleaned_data
                address_parts = (
                    cleaned_data["address"],
                    cleaned_data["city"],
                    cleaned_data["state"],
                    cleaned_data["zipcode"],
                )
                full_address = ", ".join(part for part in address_parts if part)
                try:
                    geocode_results = googlemaps.Client(
                        key=settings.GOOGLE_API_KEY
                    ).geocode(full_address)
                except (ApiError, Timeout, TransportError):
                    logger.exception("Could not geocode guest map post address.")
                    guest_post_form.add_error(
                        "address",
                        "We couldn't verify the address right now. Please try again.",
                    )
                else:
                    if not geocode_results:
                        guest_post_form.add_error(
                            "address",
                            "We couldn't find that address. Please check it and try again.",
                        )
                    else:
                        MapPost.objects.create(
                            title=cleaned_data["title"],
                            content=cleaned_data["description"],
                            author=None,
                            guest_email=cleaned_data["email"],
                            description=cleaned_data["description"],
                            geoCode=geocode_results[0],
                            visibility=0,
                        )
                        return redirect(
                            f"{reverse('mapViewer:default')}?guest_post=submitted#post-form"
                        )
    elif request.method == "POST": #a post from the existing contributor form
        postingForm= MakePostForm(request.POST) #create the posting form instance and populate it with the data in the POST request
        madePostSuccess = postingForm.is_valid() #if the data is valid (more info on this in mapViewer/forms.py)
        if madePostSuccess: #if the post is good to go
            userInz=Member.objects.get(pk=request.session['user']) #get user's member instance from session\
            vis=0
            if request.session['rank'] > 1:
                vis=1
            geo_result = postingForm.cleaned_data['geoResult']
            if isinstance(geo_result, list):
                geo_result = geo_result[0]
            postInz=MapPost.objects.create(title=postingForm.cleaned_data['title'], #actually create the post instance in the database
                                   content=postingForm.cleaned_data['content'],
                                   author=userInz,
                                   description=postingForm.cleaned_data['description'],
                                   geoCode=geo_result,
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
    widgets = serializers.serialize(
        "json",
        posts,
        fields=("title", "description", "geoCode"),
    )
    #print(widgets)  # Temporary print statement to check the output
    return render(request, 'mapViewer/mapPage.html', {'widgets': widgets,
                                                      'searchForm' : searchForm,
                                                      'posts': posts,
                                                      'GOOGLE_API_KEY': settings.GOOGLE_API_KEY,
                                                      'guest_post_form': guest_post_form,
                                                      'guest_post_open': guest_post_open,
                                                      'guest_post_submitted': guest_post_submitted,}) #render template



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
                                                        "form" : form,
                                                        "GOOGLE_API_KEY": settings.GOOGLE_API_KEY})


#this is practice of using url args and absolute URLs of a model. see models.py and urls.py to see how its working
def post_detail(request, want):
    hasReported=False
    reported_comment_id = None
    comment_report_form = None
    comment_report_comment_id = None
    if MapPost.objects.filter(pk=want).exists():
        lookAt= MapPost.objects.get(pk=want)
        reporter = PostRepForm(initial={'post':lookAt})
        comment_form = PostCommentForm()
        if request.method == 'POST' and request.POST.get("action") == "report":
            reporter = PostRepForm(request.POST)
            hasReported = reporter.is_valid()
            if hasReported:
                reporter.save()
        elif request.method == 'POST' and request.POST.get("action") == "report_comment":
            comment_report_comment_id = request.POST.get("comment")
            comment_report_form = CommentRepForm(request.POST)
            reported_comment = PostComment.objects.filter(
                pk=comment_report_comment_id, post=lookAt
            ).first()
            if reported_comment is None:
                comment_report_form.add_error(
                    "comment", "That comment is no longer available."
                )
            elif comment_report_form.is_valid():
                comment_report_form.save()
                reported_comment_id = reported_comment.pk
                comment_report_form = None
        elif request.method == "POST" and request.POST.get("action") == "comment":
            if not request.session.get("user"):
                return redirect(f"{reverse('account:signin')}?next={request.path}")
            comment_form = PostCommentForm(request.POST)
            if lookAt.visibility != 1 or not lookAt.comments_enabled:
                comment_form.add_error(
                    None, "Comments are disabled for this post."
                )
            elif comment_form.is_valid():
                parent_id = request.POST.get("parent")
                parent = None
                if parent_id:
                    parent = PostComment.objects.filter(
                        pk=parent_id, post=lookAt
                    ).first()
                    if parent is None:
                        comment_form.add_error(None, "That comment is no longer available.")
                if comment_form.is_valid():
                    PostComment.objects.create(
                        post=lookAt,
                        author_id=request.session["user"],
                        parent=parent,
                        content=comment_form.cleaned_data["content"],
                    )
                    return redirect(
                        f"{reverse('mapViewer:post_detail', args=[want])}#comments"
                    )
        is_author = lookAt.author_id == request.session.get("user", -1)
        if lookAt.visibility > 0 or request.session.get('rank', 0) > 1 or is_author:
            comments = list(
                PostComment.objects.filter(post=lookAt).select_related("author")
            )
            comments_by_parent = {}
            for comment in comments:
                comments_by_parent.setdefault(comment.parent_id, []).append(comment)
            for comment in comments:
                comment.thread_replies = comments_by_parent.get(comment.pk, [])
                if comment.pk == reported_comment_id:
                    comment.reported = True
                else:
                    comment.reported = False
                if (
                    str(comment.pk) == str(comment_report_comment_id)
                    and comment_report_form
                ):
                    comment.report_form = comment_report_form
                else:
                    comment.report_form = CommentRepForm(
                        initial={"comment": comment}
                    )
            return render(request, "mapViewer/viewPost.html", {"post" : lookAt,
                                                               "form" : reporter,
                                                               "hasReported" : hasReported,
                                                               "comment_form": comment_form,
                                                               "can_comment": (
                                                                   lookAt.visibility == 1
                                                                   and lookAt.comments_enabled
                                                               ),
                                                               "comments": comments_by_parent.get(None, []),
                                                               "comment_count": len(comments)})
    return redirect(reverse("mapViewer:default"))



def get_posts_and_tags(request):
    posts = MapPost.objects.filter(visiblity=1)
    tags = MapTag.objects.all()

    post_data = []
    for post in posts:
        if post.geoCode:
            post_data.append({
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "geoCode": post.geoCode,
                "tags": [tag.name for tag in post.tags.all()]
            })
    
    tag_data = [tag.name for tag in tags]

    return JsonResponse({"posts": post_data, "tags": tag_data})
