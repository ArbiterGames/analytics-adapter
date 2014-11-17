from django.core.management.base import BaseCommand
from input.mixpanel import Scraper
from adapter.utils import Logger
logger = Logger()


class Command(BaseCommand):
    """ python manage.py getmixpaneldata
        makes all the calls to trigger a daily update of mixpanel data
    """
    def handle(self, *args, **kwargs):
        logger.info('Running getmixpaneldata...')
        Scraper()
        logger.info('Done running getmixpaneldata.')
