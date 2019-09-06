from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    remote_host_name = models.CharField(max_length=254, blank=False, null=False)
    jira_username = models.CharField(max_length=254, blank=False, null=False)
    jira_password = models.CharField(max_length=32, blank=False, null=False)
    storypoint_name_field = models.CharField(max_length=32, blank=False, null=False)

    def __str__(self):
        return 'Profile of {}'.format(self.user)
