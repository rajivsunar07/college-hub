# Generated by Django 3.0.8 on 2020-07-29 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200719_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='college_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
