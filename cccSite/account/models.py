
from django import forms
from django.db import models
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, Textarea
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .storage import OverwriteStorage


def user_directory_profile(instance, filename):
    """Store profile images under users/<member-id>/profile.<extension>."""
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "png"
    return f"users/{instance.pk}/profile.{ext}"


class Member(models.Model):
    RANKING_CHOICES = (
        (-1, "banned"),
        (1, "member"),
        (2, "trusted member"),
        (98, "moderator"),
        (99, "admin"),
    )

    name = models.CharField(max_length=35)
    ranking = models.SmallIntegerField(
        default=1,
        choices=RANKING_CHOICES,
    )
    pic = models.ImageField(
        upload_to=user_directory_profile,
        storage=OverwriteStorage(),
        default="default/blankprof.png",
    )
    about = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("account:account_view", args=[str(self.pk)])

    def get_admin_url(self):
        return reverse("Janitor:manage_user", args=[str(self.pk)])


class GLogIn(models.Model):
    googleID = models.CharField(max_length=255, unique=True)
    referTo = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.googleID}|{self.referTo}"


class ManageForm(ModelForm):
    class Meta:
        model = Member
        fields = ["pic", "name", "about"]
        widgets = {
            "name": TextInput(attrs={"class": "nameField"}),
            "about": Textarea(attrs={"class": "aboutField"}),
        }


class UPLogIn(models.Model):
    referTo = models.ForeignKey(Member, on_delete=models.CASCADE)
    username = models.CharField(max_length=35, unique=True)
    salt = models.CharField(max_length=22)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username} | {self.referTo.name}"


class AccountCreation(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=75)
    displayname = models.CharField(max_length=75)
    password = models.CharField(max_length=50)
    confirmpassword = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.email} | {self.username} | {self.displayname}"


class MessageForm(ModelForm):
    class Meta:
        model = AccountCreation
        fields = [
            "email",
            "username",
            "displayname",
            "password",
            "confirmpassword",
        ]
        labels = {
            "email": _("Email"),
            "username": _("Username"),
            "displayname": _("Display name"),
        }
        widgets = {
            "email": EmailInput(attrs={
                "placeholder": "Email address",
                "class": "input-text",
            }),
            "username": TextInput(attrs={
                "placeholder": "Username",
                "class": "input-text",
            }),
            "displayname": TextInput(attrs={
                "placeholder": "Display name",
                "class": "input-text",
            }),
            "password": PasswordInput(attrs={
                "placeholder": "Password",
                "class": "input-text",
                "autocomplete": "new-password",
            }),
            "confirmpassword": PasswordInput(attrs={
                "placeholder": "Confirm password",
                "class": "input-text",
                "autocomplete": "new-password",
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirmpassword")

        if password and confirm and password != confirm:
            self.add_error(
                "confirmpassword",
                _("Passwords do not match."),
            )

        return cleaned_data