import getpass

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email
from django.db import transaction
from django.db.models import Q

from account.models import AccountCreation, Member


class Command(BaseCommand):
    help = "Create an administrator for the website's username and password login."

    def handle(self, *args, **options):
        try:
            username = input("Username: ").strip()
            email = input("Email: ").strip()
            displayname = input("Display name: ").strip()
            password = getpass.getpass("Password: ")
            confirmation = getpass.getpass("Password (again): ")
        except (EOFError, KeyboardInterrupt) as exc:
            raise CommandError("Account creation cancelled.") from exc

        if not all((username, email, displayname, password)):
            raise CommandError("All fields are required.")
        try:
            validate_email(email)
        except ValidationError as exc:
            raise CommandError("Enter a valid email address.") from exc
        if len(username) > 75 or len(displayname) > 35 or len(email) > 254:
            raise CommandError("Username, display name, or email is too long.")
        if not 8 <= len(password) <= 50:
            raise CommandError("Password must be between 8 and 50 characters.")
        if password != confirmation:
            raise CommandError("Passwords do not match.")

        with transaction.atomic():
            if AccountCreation.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=email)
            ).exists() or Member.objects.filter(email__iexact=email).exists():
                raise CommandError("An account or member already uses that username or email.")
            Member.objects.create(name=displayname, email=email, ranking=99)
            AccountCreation.objects.create(
                username=username, email=email, displayname=displayname,
                password=password, confirmpassword=password, status="accepted",
            )
        self.stdout.write(self.style.SUCCESS("Website administrator created successfully."))
