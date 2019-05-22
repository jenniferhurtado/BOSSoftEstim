from django import forms
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    jira_url = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    last_name = models.CharField(max_length=200, blank=False, null=False)
    username = models.CharField(max_length=30, blank=False, null=False)
    jira_username = models.CharField(max_length=254, blank=False, null=False)
    email = models.EmailField(max_length=254, blank=False, null=False)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    jira_password = models.CharField(max_length=32)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return '{} - {} {}'.format(self.client.name, self.name, self.last_name)
