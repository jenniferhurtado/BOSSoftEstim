# Generated by Django 2.1.5 on 2019-07-10 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jiracloud', '0005_auto_20190710_1658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='username',
        ),
    ]