# Generated by Django 2.1.5 on 2019-05-22 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jira', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='jira_password',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
    ]
