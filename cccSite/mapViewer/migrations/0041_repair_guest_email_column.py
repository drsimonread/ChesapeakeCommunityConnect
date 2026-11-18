from django.db import migrations
from django.db import models


def add_guest_email_if_missing(apps, schema_editor):
    table = "mapViewer_mappost"
    with schema_editor.connection.cursor() as cursor:
        cursor.execute('PRAGMA table_info("mapViewer_mappost")')
        columns = {row[1] for row in cursor.fetchall()}

    if "guest_email" not in columns:
        MapPost = apps.get_model("mapViewer", "MapPost")
        field = models.EmailField(blank=True, null=True, max_length=254)
        field.set_attributes_from_name("guest_email")
        schema_editor.add_field(MapPost, field)


class Migration(migrations.Migration):
    dependencies = [
        ("mapViewer", "0040_merge_20261118_2124"),
    ]

    operations = [
        migrations.RunPython(add_guest_email_if_missing, migrations.RunPython.noop),
    ]
