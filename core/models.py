from django.db import models


class Setting(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    timestamp = models.DateTimeField(blank=True, null=True)
    value = models.CharField(max_length=32, blank=True, null=True)
    active = models.BooleanField(blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.name)
