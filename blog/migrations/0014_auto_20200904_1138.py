# Generated by Django 3.0.8 on 2020-09-04 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20200904_1058'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='clickedpost',
            table='ClickedPost',
        ),
        migrations.AlterModelTable(
            name='postoption',
            table='PostOption',
        ),
    ]
