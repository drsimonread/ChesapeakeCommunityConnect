from django.test import TestCase, Client
from django.urls import reverse
from .models import Member, GLogIn
from mapViewer.models import MapPost

class AccountViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Member.objects.create(name="Test User", email="test@example.com", ranking=1)
        self.glogin = GLogIn.objects.create(googleID="1234567890", referTo=self.user)
        self.session = self.client.session
        self.session['user'] = self.user.pk
        self.session['rank'] = self.user.ranking
        self.session.save()

    def test_default_view_redirects_if_not_signed_in(self):
        self.session.flush()
        response = self.client.get(reverse("account:default"))
        self.assertRedirects(response, reverse("account:signin"))

    def test_default_view_shows_account_info(self):
        response = self.client.get(reverse("account:default"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test User")
        self.assertContains(response, reverse("account:create_forum"))

    def test_signed_out_contributor_page_has_only_menu_sign_in(self):
        self.session.flush()
        response = self.client.get(reverse("account:signin"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "nav-auth__link")
        self.assertNotContains(response, 'id="Signin"')

    def test_account_search_lists_visible_forum_authors(self):
        MapPost.objects.create(
            title="Visible forum",
            content="A visible forum",
            author=self.user,
            description="A visible forum",
            geoCode={"lat": 38.98, "lng": -76.49},
            visibility=1,
        )

        response = self.client.get(reverse("account:account_list"), {"q": "Test"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test User")
        self.assertContains(response, "1 forum")

    def test_create_forum_page_uses_existing_template(self):
        response = self.client.get(reverse("account:create_forum"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create a forum")

    def test_create_forum_submission_creates_pending_post(self):
        response = self.client.post(reverse("account:create_forum"), {
            "title": "Community forum",
            "firstName": "Test",
            "lastName": "User",
            "location": "123 Main Street",
            "content": "A community forum description",
            "associated": "yes",
            "private_public": "public",
            "geoResult": '{"lat": 38.98, "lng": -76.49}',
        })
        self.assertRedirects(response, reverse("account:my_forums") + "?success=1")
        self.assertTrue(MapPost.objects.filter(
            author=self.user, title="Community forum", visibility=0,
        ).exists())

    def test_my_forums_shows_member_posts(self):
        MapPost.objects.create(
            title="Pending forum",
            content="A forum awaiting review",
            author=self.user,
            description="A forum awaiting review",
            geoCode={"lat": 38.98, "lng": -76.49},
            visibility=0,
        )

        response = self.client.get(reverse("account:my_forums"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pending forum")
        self.assertContains(response, "Pending review")

    def test_my_forums_redirects_if_not_signed_in(self):
        self.session.flush()
        response = self.client.get(reverse("account:my_forums"))
        self.assertRedirects(response, reverse("account:signin"))

    def test_manage_view_redirects_if_not_signed_in(self):
        self.session.flush()
        response = self.client.get(reverse("account:manage"))
        self.assertRedirects(response, "/account/signin/")

    def test_manage_view_updates_user_info(self):
        response = self.client.post(reverse("account:manage"), {'name': "Updated User", 'email': "updated@example.com"})
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "Updated User")
        self.assertRedirects(response, "/account/")

    def test_authG_view_invalid_request(self):
        response = self.client.get(reverse("account:authG"))
        self.assertRedirects(response, "/account/")

    def test_authG_view_invalid_csrf(self):
        response = self.client.post(reverse("account:authG"), {'g_csrf_token': 'invalid'})
        self.assertContains(response, "Something went wrong, no csrf cookie", status_code=200)
