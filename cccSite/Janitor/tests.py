from django.test import TestCase
from django.urls import reverse

from account.models import Member
from mapViewer.models import MapPost
from .models import PostReport, UserReport


class MemberManagementTests(TestCase):
    def setUp(self):
        self.member = Member.objects.create(name="Community member", email="member@example.com")
        session = self.client.session
        session["rank"] = 98
        session.save()

    def test_member_list_counts_visible_posts_and_reports(self):
        visible = MapPost.objects.create(
            author=self.member, title="Published post", geoCode={}, visibility=1
        )
        MapPost.objects.create(
            author=self.member, title="Pending post", geoCode={}, visibility=0
        )
        PostReport.objects.create(post=visible, reason="Placeholder post report")
        UserReport.objects.create(account=self.member, reason="Placeholder member report")

        response = self.client.get(reverse("Janitor:memberList"))

        self.assertContains(response, "Visible Posts: 1")
        self.assertContains(response, "Reports: 2")

    def test_member_manager_updates_existing_member(self):
        response = self.client.post(reverse("Janitor:manage_user", args=[self.member.pk]), {
            "name": "Updated member",
            "email": self.member.email,
            "ranking": 2,
            "about": "Updated biography",
        })

        self.assertEqual(response.status_code, 200)
        self.member.refresh_from_db()
        self.assertEqual(self.member.name, "Updated member")
        self.assertEqual(self.member.ranking, 2)
        self.assertEqual(Member.objects.count(), 1)


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
