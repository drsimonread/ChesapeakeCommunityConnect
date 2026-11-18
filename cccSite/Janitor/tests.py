from django.test import TestCase
from django.urls import reverse

from mapViewer.models import MapPost


class PendingPostReviewTests(TestCase):
    def setUp(self):
        self.post = MapPost.objects.create(
            title="Guest submission",
            content="A pending guest post",
            description="A pending guest post",
            geoCode={"geometry": {"location": {"lat": 38.98, "lng": -76.49}}},
            guest_email="guest@example.com",
            visibility=0,
        )
        self.pending_url = reverse("Janitor:pending_posts")

    def sign_in_as_moderator(self):
        session = self.client.session
        session["rank"] = 98
        session.save()

    def test_guest_email_is_only_shown_to_moderators(self):
        response = self.client.get(self.pending_url)
        self.assertRedirects(
            response,
            reverse("mapViewer:default"),
            fetch_redirect_response=False,
        )

        self.sign_in_as_moderator()
        response = self.client.get(self.pending_url)
        self.assertContains(response, "guest@example.com")
        self.assertContains(response, "Posts awaiting review")

    def test_moderator_can_approve_guest_post(self):
        self.sign_in_as_moderator()

        response = self.client.post(self.pending_url, {
            "pk": self.post.pk,
            "action": "approve",
        })

        self.assertRedirects(
            response,
            self.pending_url + "?updated=approve",
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.visibility, 1)

    def test_moderator_can_reject_guest_post(self):
        self.sign_in_as_moderator()

        response = self.client.post(self.pending_url, {
            "pk": self.post.pk,
            "action": "reject",
        })

        self.assertRedirects(
            response,
            self.pending_url + "?updated=reject",
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.visibility, -1)
