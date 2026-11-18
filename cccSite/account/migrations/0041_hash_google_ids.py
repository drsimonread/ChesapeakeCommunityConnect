import re

from django.db import migrations

from account.hashing import hash_google_id

_ALREADY_HASHED = re.compile(r"^[0-9a-f]{64}$")


def hash_existing_google_ids(apps, schema_editor):
    GLogIn = apps.get_model("account", "GLogIn")
    for glog in GLogIn.objects.all():
        if not _ALREADY_HASHED.match(glog.googleID):
            glog.googleID = hash_google_id(glog.googleID)
            glog.save(update_fields=["googleID"])


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0040_alter_member_ranking"),
    ]
    operations = [
        migrations.RunPython(hash_existing_google_ids),
    ]