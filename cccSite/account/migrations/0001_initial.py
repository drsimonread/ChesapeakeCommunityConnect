from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ranking', models.SmallIntegerField(default=1, choices=[(-1, 'banned'), (1, 'member'), (2, 'trusted member'), (98, 'moderator'), (99, 'admin')])),
                ('pic', models.ImageField(upload_to='users', default='default/blankprof.png')),
                ('about', models.TextField(blank=True, default='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='AccountCreation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=75)),
                ('displayname', models.CharField(max_length=75)),
                ('password', models.CharField(max_length=50)),
                ('confirmpassword', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'User Request',
                'verbose_name_plural': 'User Requests',
            },
        ),
        migrations.CreateModel(
            name='GLogIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('googleID', models.CharField(max_length=255, unique=True)),
                ('referTo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.member')),
            ],
        ),
        migrations.CreateModel(
            name='UPLogIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=35, unique=True)),
                ('salt', models.CharField(max_length=22)),
                ('password', models.CharField(max_length=50)),
                ('referTo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.member')),
            ],
        ),
    ]

