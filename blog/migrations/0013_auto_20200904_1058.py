# Generated by Django 3.0.8 on 2020-09-04 10:58

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0012_remove_comments_parent'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Clicked_Post',
            new_name='ClickedPost',
        ),
    ]
