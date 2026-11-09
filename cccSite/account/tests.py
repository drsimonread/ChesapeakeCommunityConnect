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

    def test_manage_view_shows_current_profile_image(self):
        response = self.client.get(reverse("account:manage"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Current profile image:")
        self.assertContains(response, self.user.pic.url)

    def test_signin_redirects_signed_in_user_to_account_page(self):
        response = self.client.get(reverse("account:signin"))
        self.assertRedirects(response, reverse("account:default"))

    def test_signed_out_contributor_page_has_only_menu_sign_in(self):
        self.session.flush()
        response = self.client.get(reverse("account:signin"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "nav-auth__link")
        self.assertNotContains(response, ">Account<")
        self.assertNotContains(response, 'id="Signin"')

    def test_contributors_link_is_directory_for_signed_in_users(self):
        response = self.client.get(reverse("account:account_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'href="' + reverse("account:account_list") + '" style="background-color: #f3c10d; color: #00205c;"',
        )
        self.assertContains(response, reverse("account:account_list"))
        self.assertContains(response, "Contributors")
        self.assertContains(response, reverse("account:default"))
        self.assertContains(response, "My Account")

    def test_contributors_link_is_directory_for_signed_out_users(self):
        self.session.flush()
        response = self.client.get(reverse("account:account_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'href="' + reverse("account:account_list") + '" style="background-color: #f3c10d; color: #00205c;"',
        )
        self.assertContains(response, reverse("account:account_list"))
        self.assertContains(response, "Contributors")
        self.assertNotContains(response, ">Account<")

    def test_signed_out_contributors_page_prompts_for_sign_in(self):
        self.session.flush()
        response = self.client.get(reverse("account:account_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign in to view contributors")
        self.assertContains(response, "⚠️")
        self.assertContains(response, "You need to sign in to view the contributors page.")
        self.assertContains(response, "contributors-signin-link")
        self.assertContains(response, "What it means to be a Contributor")
        self.assertNotContains(response, "Search by username")

    def test_signed_in_pages_include_account_in_main_menu(self):
        response = self.client.get(reverse("account:default"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '>Account<')
        self.assertContains(response, 'class="nav-account-dropdown"')
        self.assertContains(response, 'class="nav-auth nav-account-menu"')
        for url_name in (
            "default",
            "create_forum",
            "my_forums",
        ):
            self.assertContains(response, reverse("account:" + url_name))
        self.assertContains(response, reverse("account:manage"))
        self.assertContains(response, "Sign Out")
        self.assertNotContains(
            response,
            'href="' + reverse("account:account_list") + '" style="background-color: #f3c10d; color: #00205c;"',
        )
        self.assertNotContains(response, 'position:fixed;width: 15%')

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
        self.assertRedirects(response, reverse("account:account_list"))

    def test_authG_view_invalid_csrf(self):
        response = self.client.post(reverse("account:authG"), {'g_csrf_token': 'invalid'})
        self.assertContains(response, "Something went wrong, no csrf cookie", status_code=200)


# issue #72: changing your password from the edit account page
class PasswordChangeTest(TestCase):
    def setUp(self):
        from .models import AccountCreation
        self.member = Member.objects.create(name="Pat", email="pat@example.com", ranking=1)
        self.account = AccountCreation.objects.create(
            email="pat@example.com", username="pat", displayname="Pat",
            password="oldpassword", confirmpassword="oldpassword", status="accepted",
        )
        session = self.client.session
        session["user"] = self.member.pk
        session["rank"] = self.member.ranking
        session.save()

    def change(self, current, new, confirm):
        return self.client.post(reverse("account:manage"), {
            "change_password": "Change password",
            "current_password": current,
            "new_password": new,
            "confirm_password": confirm,
        })

    def test_form_shows_for_password_accounts(self):
        response = self.client.get(reverse("account:manage"))
        self.assertContains(response, 'id="password-form"')

    def test_change_password(self):
        response = self.change("oldpassword", "newpassword1", "newpassword1")
        self.assertRedirects(response, reverse("account:manage") + "?password=changed")
        self.account.refresh_from_db()
        self.assertEqual(self.account.password, "newpassword1")
        self.assertContains(self.client.get(response.url), "Your password has been changed.")

    def test_can_sign_in_with_new_password(self):
        self.change("oldpassword", "newpassword1", "newpassword1")
        self.client.session.flush()
        response = self.client.post(reverse("account:signin_form"), {"username": "pat", "password": "newpassword1"})
        self.assertRedirects(response, reverse("account:default"), fetch_redirect_response=False)

    def assert_rejected(self, response, message):
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, message)
        self.account.refresh_from_db()
        self.assertEqual(self.account.password, "oldpassword")

    def test_wrong_current_password(self):
        self.assert_rejected(self.change("wrong", "newpassword1", "newpassword1"), "Your current password is incorrect.")

    def test_new_passwords_do_not_match(self):
        self.assert_rejected(self.change("oldpassword", "newpassword1", "newpassword2"), "The new passwords do not match.")

    def test_new_password_too_short(self):
        self.assert_rejected(self.change("oldpassword", "short", "short"), "at least 8 characters")

    def test_new_password_same_as_old(self):
        self.assert_rejected(self.change("oldpassword", "oldpassword", "oldpassword"), "must be different")

    def test_profile_form_still_works(self):
        response = self.client.post(reverse("account:manage"), {"name": "Patricia", "email": "pat@example.com", "about": ""})
        self.assertRedirects(response, "/account/", fetch_redirect_response=False)
        self.member.refresh_from_db()
        self.assertEqual(self.member.name, "Patricia")

    def test_google_only_account_has_no_password_form(self):
        self.account.delete()
        response = self.client.get(reverse("account:manage"))
        self.assertNotContains(response, 'id="password-form"')
        self.assertContains(response, "You sign in with Google")

    def test_signed_out_user_is_sent_to_sign_in(self):
        self.client.session.flush()
        self.client.cookies.clear()
        response = self.client.post(reverse("account:manage"), {"change_password": "1"})
        self.assertRedirects(response, "/account/signin/", fetch_redirect_response=False)
