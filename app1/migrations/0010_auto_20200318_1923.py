# Generated by Django 2.2.7 on 2020-03-18 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_additionaluser_isstudent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionaluser',
            name='college',
            field=models.CharField(choices=[('Government college of engineering, salem', 'Government college of engineering, salem')], max_length=256),
        ),
    ]
