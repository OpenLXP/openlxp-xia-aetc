import logging

from django.core.management.base import BaseCommand

logger = logging.getLogger('dict_config_logger')


class Command(BaseCommand):
    """Django command to extract raw metadata and process to further
    extraction in EVTVL process"""

    def handle(self, *args, **options):
        """ Extracting raw metadata and process to further
        extraction in EVTVL process"""