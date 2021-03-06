# Generated by Django 2.2.7 on 2020-03-10 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='chat_room_messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ma', models.TextField(max_length=10000)),
                ('M1', models.TextField(blank=True, null=True)),
                ('M2', models.TextField(blank=True, null=True)),
                ('M3', models.TextField(blank=True, null=True)),
                ('M4', models.TextField(blank=True, null=True)),
                ('M5', models.TextField(blank=True, null=True)),
                ('M6', models.TextField(blank=True, null=True)),
                ('M7', models.TextField(blank=True, null=True)),
                ('M8', models.TextField(blank=True, null=True)),
                ('M9', models.TextField(blank=True, max_length=256, null=True)),
                ('M10', models.TextField(blank=True, max_length=256, null=True)),
                ('M11', models.TextField(blank=True, max_length=256, null=True)),
                ('M12', models.TextField(blank=True, max_length=256, null=True)),
                ('M13', models.TextField(blank=True, max_length=256, null=True)),
                ('M14', models.TextField(blank=True, max_length=256, null=True)),
                ('M15', models.TextField(blank=True, max_length=256, null=True)),
                ('M16', models.TextField(blank=True, max_length=256, null=True)),
                ('M17', models.TextField(blank=True, max_length=256, null=True)),
                ('M18', models.TextField(blank=True, max_length=256, null=True)),
                ('M19', models.TextField(blank=True, max_length=256, null=True)),
                ('M20', models.TextField(blank=True, max_length=256, null=True)),
                ('chat_room_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='chat_room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_room_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
