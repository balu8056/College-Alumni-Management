# Generated by Django 2.2.7 on 2020-04-21 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_additionaluser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionaluser',
            name='phone',
            field=models.CharField(blank=True, default='None', max_length=10),
        ),
    ]