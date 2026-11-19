from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Janitor", "0002_remove_userreport_user_userreport_account"),
        ("mapViewer", "0042_merge_20261119_1506"),
    ]

    operations = [
        migrations.CreateModel(
            name="CommentReport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("reason", models.TextField()),
                (
                    "comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mapViewer.postcomment",
                    ),
                ),
            ],
        ),
    ]
