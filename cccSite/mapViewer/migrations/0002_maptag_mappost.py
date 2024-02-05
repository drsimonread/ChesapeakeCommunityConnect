# Generated by Django 4.2.6 on 2024-02-04 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_member_ranking'),
        ('mapViewer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagName', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='MapPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('description', models.TextField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('isVisible', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.member')),
                ('tags', models.ManyToManyField(related_name='posts', to='mapViewer.maptag')),
            ],
        ),
    ]
