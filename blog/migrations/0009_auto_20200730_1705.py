# Generated by Django 3.0.8 on 2020-07-30 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20200730_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(null=True, upload_to='post_pics'),
        ),
    ]