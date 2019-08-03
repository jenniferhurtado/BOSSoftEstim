from datetime import datetime

from django.core.management.base import BaseCommand

from core.models import Setting
from deeplearning.main import fit
from jiracloud.jira_connector import get_training_dataframe
from jiracloud.models import Profile


class Command(BaseCommand):
    help = 'Updates the model training already estimated tasks'

    def handle(self, *args, **options):
        for profile in Profile.objects.all():
            user = profile.user
            df_train = get_training_dataframe(user)
            fit(df_train)

        setting = Setting.objects.get(name='model_last_update')
        setting.timestamp = datetime.now()
        setting.save()
