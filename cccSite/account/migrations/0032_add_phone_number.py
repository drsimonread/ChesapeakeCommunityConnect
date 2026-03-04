# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0031_add_account_creation_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
