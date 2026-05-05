from django.test import TestCase, Client
from django.urls import reverse
from .models import Member, GLogIn

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
