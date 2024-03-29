# Generated by Django 2.1.5 on 2019-08-03 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('value', models.CharField(blank=True, max_length=32, null=True)),
                ('active', models.BooleanField()),
            ],
        ),
    ]
