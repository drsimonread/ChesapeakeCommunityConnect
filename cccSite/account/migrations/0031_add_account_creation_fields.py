# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0030_alter_member_ranking'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountcreation',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
        migrations.AddField(
            model_name='accountcreation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
