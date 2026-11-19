from django.test import TestCase, Client
from django.urls import reverse
from django.test import override_settings
from unittest.mock import patch

from account.models import Member
from Janitor.models import CommentReport
from .models import MapPost, PostComment


class MapPostCreationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Member.objects.create(
            name="Post Author", email="author@example.com", ranking=1
        )
        session = self.client.session
        session["user"] = self.author.pk
        session["rank"] = self.author.ranking
        session.save()

    def test_map_post_submission_saves_geo_result(self):
        response = self.client.post(
            reverse("mapViewer:default"),
            {
                "title": "Community location",
                "description": "A useful community location",
                "location": "123 Main Street",
                "content": "A useful community location",
                "geoResult": (
                    '{"geometry": {"location": {"lat": 38.98, "lng": -76.49}}}'
                ),
            },
        )

        self.assertEqual(response.status_code, 200)
        post = MapPost.objects.get(title="Community location")
        self.assertEqual(
            post.geoCode,
            {"geometry": {"location": {"lat": 38.98, "lng": -76.49}}},
        )


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

    def test_comment_author_link_opens_commenter_profile(self):
        comment = PostComment.objects.create(
            post=self.post,
            author=self.commenter,
            content="A comment with a profile link",
        )

        response = self.client.get(
            reverse("mapViewer:post_detail", args=[self.post.pk])
        )

        self.assertContains(
            response,
            f'href="{reverse("account:account_view", args=[self.commenter.pk])}"',
        )
        profile_response = self.client.get(
            reverse("account:account_view", args=[comment.author.pk])
        )
        self.assertEqual(profile_response.status_code, 200)
        self.assertContains(profile_response, self.commenter.name)

    def test_user_can_report_a_comment(self):
        comment = PostComment.objects.create(
            post=self.post,
            author=self.commenter,
            content="A comment to report",
        )

        response = self.client.post(
            reverse("mapViewer:post_detail", args=[self.post.pk]),
            {
                "action": "report_comment",
                "comment": comment.pk,
                "reason": "This comment is inappropriate.",
            },
        )

        self.assertEqual(response.status_code, 200)
        report = CommentReport.objects.get()
        self.assertEqual(report.comment, comment)
        self.assertContains(response, "Your report has been received.")

    def test_comment_report_must_belong_to_current_post(self):
        other_comment = PostComment.objects.create(
            post=self.other_post,
            author=self.commenter,
            content="Unrelated comment",
        )

        response = self.client.post(
            reverse("mapViewer:post_detail", args=[self.post.pk]),
            {
                "action": "report_comment",
                "comment": other_comment.pk,
                "reason": "Invalid report.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(CommentReport.objects.exists())


class GuestPostTests(TestCase):
    def setUp(self):
        self.post_url = reverse("mapViewer:default")
        self.post_data = {
            "action": "guest_post",
            "email": "guest@example.com",
            "title": "Community garden",
            "description": "A neighborhood garden",
            "address": "123 Main Street",
            "city": "Anytown",
            "state": "MD",
            "zipcode": "20601",
        }

    def test_map_page_offers_login_and_guest_paths(self):
        response = self.client.get(self.post_url)

        self.assertContains(response, "Continue as guest")
        self.assertContains(
            response,
            reverse("account:signin") + "?next=/account/create-forum/",
        )
        self.assertContains(response, 'id="post-form" hidden')

    def test_guest_choice_opens_form_and_email_note_is_above_input(self):
        response = self.client.get(self.post_url, {"guest_post": "open"})
        page = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["guest_post_open"])
        self.assertNotContains(response, 'id="post-form" hidden')
        self.assertContains(response, 'name="guest_post" value="open"')
        self.assertContains(response, f'action="{self.post_url}#post-form"')
        self.assertLess(
            page.index("We will use this to contact you about your post."),
            page.index('id="email"'),
        )

    @override_settings(GOOGLE_API_KEY="test-google-key")
    @patch("mapViewer.views.googlemaps.Client")
    def test_guest_submission_is_saved_pending_and_email_is_private(self, client_factory):
        client_factory.return_value.geocode.return_value = [{
            "geometry": {
                "location": {
                    "lat": 38.98,
                    "lng": -76.49,
                },
            },
        }]

        response = self.client.post(self.post_url, self.post_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"],
            self.post_url + "?guest_post=submitted#post-form",
        )
        post = MapPost.objects.get(title="Community garden")
        self.assertIsNone(post.author)
        self.assertEqual(post.guest_email, "guest@example.com")
        self.assertEqual(post.visibility, 0)
        client_factory.return_value.geocode.assert_called_once_with(
            "123 Main Street, Anytown, MD, 20601"
        )

        post.visibility = 1
        post.save(update_fields=["visibility"])
        map_response = self.client.get(self.post_url)
        detail_response = self.client.get(
            reverse("mapViewer:post_detail", args=[post.pk])
        )
        self.assertContains(map_response, "Community garden")
        self.assertNotContains(map_response, "guest@example.com")
        self.assertContains(detail_response, "Guest contributor")
        self.assertNotContains(detail_response, "guest@example.com")

    def test_invalid_guest_email_keeps_form_open_without_creating_a_post(self):
        self.post_data["email"] = "not-an-email"

        response = self.client.post(self.post_url, self.post_data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["guest_post_open"])
        self.assertContains(response, "Enter a valid email address.")
        self.assertFalse(MapPost.objects.exists())

    @override_settings(GOOGLE_API_KEY="test-google-key")
    @patch("mapViewer.views.googlemaps.Client")
    def test_guest_submission_requires_a_geocodable_address(self, client_factory):
        client_factory.return_value.geocode.return_value = []

        response = self.client.post(self.post_url, self.post_data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["guest_post_open"])
        self.assertContains(response, "We couldn&#x27;t find that address.")
        self.assertFalse(MapPost.objects.exists())

    def test_comments_are_disabled_for_pending_and_denied_posts(self):
        self.sign_in_as_commenter()

        for visibility in (0, -1):
            with self.subTest(visibility=visibility):
                self.post.visibility = visibility
                self.post.save(update_fields=("visibility",))
                post_url = reverse("mapViewer:post_detail", args=[self.post.pk])

                response = self.client.get(post_url)
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, 'id="comment-button"')
                self.assertNotContains(response, "Reply")

                response = self.client.post(post_url, {
                    "action": "comment",
                    "content": "This comment must not be created.",
                })
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Comments are disabled for this post.")
                self.assertFalse(
                    PostComment.objects.filter(
                        content="This comment must not be created."
                    ).exists()
                )

    def test_comments_can_be_disabled_on_a_visible_post(self):
        self.post.comments_enabled = False
        self.post.save(update_fields=("comments_enabled",))
        self.sign_in_as_commenter()
        post_url = reverse("mapViewer:post_detail", args=[self.post.pk])

        response = self.client.get(post_url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'id="comment-button"')
        self.assertContains(response, "Comments are disabled for this post.")

        response = self.client.post(post_url, {
            "action": "comment",
            "content": "This comment must not be created.",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            PostComment.objects.filter(
                content="This comment must not be created."
            ).exists()
        )
