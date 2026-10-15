
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q

from account.models import Member
from Janitor.forms import PostRepForm

from .models import MapPost, MapTag
from .forms import *


def viewMap(request):
    posts = MapPost.objects.filter(visibility=1)
    madePostSuccess = False

    if request.method == "POST":
        postingForm = MakePostForm(request.POST, request.FILES)
        madePostSuccess = postingForm.is_valid()

        if madePostSuccess:
            member_id = request.session.get("user")

            if not member_id:
                return redirect("account:signin")

            userInz = get_object_or_404(Member, pk=member_id)

            content = postingForm.cleaned_data["content"]
            disc = content[:35] + "..." if len(content) > 35 else content

            geo_result = postingForm.cleaned_data.get("geoResult")

            if not geo_result:
                postingForm.add_error(
                    "location",
                    "Please enter a valid address.",
                )
                madePostSuccess = False
            else:
                vis = 1 if request.session.get("rank", 0) > 1 else 0

                postInz = MapPost.objects.create(
                    title=postingForm.cleaned_data["title"],
                    content=content,
                    author=userInz,
                    description=disc,
                    geoCode=geo_result[0],
                    visibility=vis,
                )

                tags = postingForm.cleaned_data.get("tags")
                if tags:
                    postInz.tags.set(tags)

                return redirect(
                    reverse("mapViewer:post_detail", args=[postInz.pk])
                )

    else:
        postingForm = MakePostForm()

    contQuery = request.GET.get("q")
    tagQuery = request.GET.getlist("t")

    searchForm = SearchPostsForm(request.GET)

    if contQuery:
        posts = posts.filter(
            Q(title__icontains=contQuery)
            | Q(content__icontains=contQuery)
        )

    if tagQuery:
        for tag in tagQuery:
            posts = posts.filter(tags__pk=tag)

    widgets = serializers.serialize("json", posts)

    return render(
        request,
        "mapViewer/mapPage.html",
        {
            "widgets": widgets,
            "postForm": postingForm,
            "searchForm": searchForm,
            "hasPosted": madePostSuccess,
        },
    )


def post_list(request):
    contQuery = request.GET.get("q")
    tagQuery = request.GET.getlist("t")

    form = SearchPostsForm(request.GET)
    posts = MapPost.objects.filter(visibility=1)

    if contQuery:
        posts = posts.filter(
            Q(title__icontains=contQuery)
            | Q(content__icontains=contQuery)
        )

    if tagQuery:
        for tag in tagQuery:
            posts = posts.filter(tags__pk=tag)

    posts = posts.order_by("id")

    return render(
        request,
        "mapViewer/listPosts.html",
        {
            "postList": posts,
            "form": form,
        },
    )


def post_detail(request, want, wants=None):
    """
    Supports the existing URL with one argument.
    If a second argument is supplied by another URL, it displays that post.
    """

    # Individual post page, when a post ID is supplied.
    if wants is not None:
        lookAt = get_object_or_404(Forum, pk=want)
        lookAtPost = get_object_or_404(Post, pk=wants)
        comments = lookAtPost.comments.all()

        forumData = {
            "title": lookAt.title,
            "description": lookAt.description,
        }

        return render(
            request,
            "mapViewer/viewPost.html",
            {
                "forum": lookAt,
                "Post": lookAtPost,
                "forumData": forumData,
                "comments": comments,
            },
        )

    # Existing URL: /post/<want>
    # MapPost details are handled separately from Forum details.
    map_post = MapPost.objects.filter(pk=want).first()

    if map_post is not None:
        return render(
            request,
            "mapViewer/post_detail.html",
            {"post": map_post},
        )

    # Preserve the original forum-viewing behavior.
    lookAt = Forum.objects.filter(pk=want).first()

    if lookAt is None:
        return redirect("mapViewer:default")

    files = Media.objects.filter(forum=lookAt)

    forumData = {
        "title": lookAt.title,
        "description": lookAt.description,
    }

    if request.method == "POST":
        reporter = PostRepForm(request.POST)
        hasReported = reporter.is_valid()

        if hasReported:
            reporter.save()
    else:
        reporter = PostRepForm(initial={"post": lookAt})
        hasReported = False

    if not (
        lookAt.visibility > 0
        or request.session.get("rank", 0) > 1
        or lookAt.author.pk == request.session.get("user", -1)
    ):
        return redirect("mapViewer:default")

    if lookAt.visibility == 0:
        msg = "Your forum is currently pending approval and only visible to you."
    elif lookAt.visibility == -1:
        msg = (
            "Your forum has been denied for the following reason: "
            f"{lookAt.description}.\n"
            "To resubmit, please create a new forum."
        )
    else:
        msg = ""

    # Use the related posts if this model exposes them.
    forum_posts = []
    page_obj = Paginator(forum_posts, 10).get_page(
        request.GET.get("page", 1)
    )

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        post_html = [
            render_to_string(
                "mapViewer/postTemplate.html",
                {
                    "post": post,
                    "forum": lookAt,
                    "page_obj": page_obj.number,
                },
                request=request,
            )
            for post in page_obj.object_list
        ]

        return JsonResponse(
            {
                "posts": post_html,
                "has_next": page_obj.has_next(),
            }
        )

    return render(
        request,
        "mapViewer/viewForum.html",
        {
            "forum": lookAt,
            "form": reporter,
            "forumData": forumData,
            "hasReported": hasReported,
            "files": files,
            "msg": msg,
            "posts": page_obj,
            "page_number": page_obj.number,
        },
    )


@require_http_methods(["GET"])
def get_posts_and_tags(request):
    posts = (
        MapPost.objects
        .filter(visibility=1)
        .prefetch_related("tags")
    )

    tags = MapTag.objects.all()

    post_data = []

    for post in posts:
        if post.geoCode:
            post_data.append(
                {
                    "id": post.id,
                    "title": post.title,
                    "description": post.description,
                    "geoCode": post.geoCode,
                    "tags": [tag.name for tag in post.tags.all()],
                }
            )

    tag_data = [tag.name for tag in tags]

    return JsonResponse(
        {
            "posts": post_data,
            "tags": tag_data,
        }
    )
