from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0040_alter_member_ranking"),
    ]

    operations = [
        migrations.AddField(
            model_name="member",
            name="email",
            field=models.EmailField(default="", max_length=254),
        ),
        migrations.AlterField(
            model_name="member",
            name="email",
            field=models.EmailField(max_length=254),
        ),
    ]
