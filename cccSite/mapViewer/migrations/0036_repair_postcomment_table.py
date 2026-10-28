from django.db import migrations


def create_postcomment_table_if_missing(apps, schema_editor):
    PostComment = apps.get_model("mapViewer", "PostComment")
    table_name = PostComment._meta.db_table
    existing_tables = schema_editor.connection.introspection.table_names()

    if table_name not in existing_tables:
        schema_editor.create_model(PostComment)


class Migration(migrations.Migration):

    dependencies = [
        ("mapViewer", "0035_postcomment"),
    ]

    operations = [
        migrations.RunPython(
            create_postcomment_table_if_missing,
            migrations.RunPython.noop,
        ),
    ]
