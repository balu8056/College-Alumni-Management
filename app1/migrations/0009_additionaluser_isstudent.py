# Generated by Django 2.2.7 on 2020-02-22 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_auto_20200209_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionaluser',
            name='isStudent',
            field=models.BooleanField(default=True),
        ),
    ]
