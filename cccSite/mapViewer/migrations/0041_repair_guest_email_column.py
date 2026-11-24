from django.db import migrations


def add_guest_email_if_missing(apps, schema_editor):
    MapPost = apps.get_model("mapViewer", "MapPost")
    field = MapPost._meta.get_field("guest_email")
    table = MapPost._meta.db_table
    with schema_editor.connection.cursor() as cursor:
        columns = {
            column.name
            for column in schema_editor.connection.introspection.get_table_description(
                cursor, table
            )
        }

    if field.column not in columns:
        schema_editor.add_field(MapPost, field)


class Migration(migrations.Migration):
    dependencies = [
        ("mapViewer", "0040_merge_20261118_2124"),
    ]

    operations = [
        migrations.RunPython(
            add_guest_email_if_missing, migrations.RunPython.noop, atomic=False
        ),
    ]
