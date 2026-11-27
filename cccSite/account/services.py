from django.db import IntegrityError, transaction

from .models import AccountCreation, Member


def approve_signup(account):
    if account.status != "pending" or not account.email_verified:
        return False

    try:
        with transaction.atomic():
            account = AccountCreation.objects.select_for_update().get(pk=account.pk)
            if account.status != "pending" or not account.email_verified:
                return False
            if Member.objects.filter(email__iexact=account.email).exists():
                return False

            member = Member.objects.create(
                name=account.displayname,
                email=account.email,
                ranking=1,
            )
            account.member = member
            account.status = "accepted"
            account.save(update_fields=("member", "status"))
    except IntegrityError:
        return False

    return True
