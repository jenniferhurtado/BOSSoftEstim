from datetime import datetime

from django.core.management.base import BaseCommand

from core.models import Setting


class Command(BaseCommand):
    help = 'Prints the titles of all Posts'

    def handle(self, *args, **options):
        setting = Setting.objects.get(name='model_last_update')
        setting.timestamp = datetime.now()
        setting.save()
