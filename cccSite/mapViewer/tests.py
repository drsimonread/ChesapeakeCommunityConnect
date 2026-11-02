from django.test import TestCase, Client
from django.urls import reverse

from account.models import Member
from .models import MapPost, PostComment


class PostCommentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Member.objects.create(
            name="Post Author", email="author@example.com", ranking=1
        )
        self.commenter = Member.objects.create(
            name="Commenter", email="commenter@example.com", ranking=1
        )
        self.post = MapPost.objects.create(
            title="Community discussion",
            content="A discussion post",
            author=self.author,
            description="A discussion post",
            geoCode={"lat": 38.98, "lng": -76.49},
            visibility=1,
        )
        self.other_post = MapPost.objects.create(
            title="Another discussion",
            content="Another discussion post",
            author=self.author,
            description="Another discussion post",
            geoCode={"lat": 38.98, "lng": -76.49},
            visibility=1,
        )

    def sign_in_as_commenter(self):
        session = self.client.session
        session["user"] = self.commenter.pk
        session["rank"] = self.commenter.ranking
        session.save()

    def test_post_detail_shows_comment_section_to_signed_out_visitor(self):
        response = self.client.get(
            reverse("mapViewer:post_detail", args=[self.post.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Comments (0)")
        self.assertContains(response, "Sign in")

    def test_signed_in_user_can_create_nested_comments(self):
        self.sign_in_as_commenter()
        post_url = reverse("mapViewer:post_detail", args=[self.post.pk])

        response = self.client.post(post_url, {
            "action": "comment",
            "content": "This is a top-level comment.",
        })
        self.assertRedirects(response, post_url + "#comments")
        comment = PostComment.objects.get()
        self.assertIsNone(comment.parent)

        response = self.client.post(post_url, {
            "action": "comment",
            "content": "This is a reply.",
            "parent": comment.pk,
        })
        self.assertRedirects(response, post_url + "#comments")
        reply = PostComment.objects.get(content="This is a reply.")
        self.assertEqual(reply.parent, comment)

        response = self.client.get(post_url)
        self.assertContains(response, "Comments (2)")
        self.assertContains(response, "This is a reply.")

    def test_reply_parent_must_belong_to_current_post(self):
        self.sign_in_as_commenter()
        other_comment = PostComment.objects.create(
            post=self.other_post,
            author=self.commenter,
            content="Unrelated comment",
        )

        response = self.client.post(
            reverse("mapViewer:post_detail", args=[self.post.pk]),
            {
                "action": "comment",
                "content": "Invalid reply",
                "parent": other_comment.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(PostComment.objects.filter(content="Invalid reply").exists())
