import hashlib
import hmac

from django.conf import settings
from django.db import migrations
from django.core.exceptions import ImproperlyConfigured


def hash_existing_google_ids(apps, schema_editor):
    GLogIn = apps.get_model("account", "GLogIn")
    key = getattr(settings, "GOOGLE_ID_HASH_KEY", "")

    if not key:
        raise ImproperlyConfigured(
            "GOOGLE_ID_HASH_KEY must be configured before migrating Google IDs."
        )

    for record in GLogIn.objects.all().iterator():
        hashed_id = hmac.new(
            key.encode("utf-8"),
            record.googleID.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        record.googleID = hashed_id
        record.save(update_fields=["googleID"])


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0052_alter_member_ranking"),
    ]

    operations = [
        migrations.RunPython(
            hash_existing_google_ids,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
