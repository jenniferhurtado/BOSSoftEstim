# Generated by Django 2.1.5 on 2019-07-10 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jiracloud', '0006_auto_20190710_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='remote_host_name',
            field=models.CharField(default='', max_length=254),
            preserve_default=False,
        ),
    ]
