# Generated manually

from django.db import migrations, models
from ._account_status import AddAccountStatus


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0030_alter_member_ranking'),
    ]

    operations = [
        AddAccountStatus(
            other_migration='0032_auto_20251022_2002',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
        migrations.AddField(
            model_name='accountcreation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
