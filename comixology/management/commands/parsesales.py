from django.core.management.base import BaseCommand

from comixology.tasks import parse_sales


class Command(BaseCommand):
    help = 'Parse the current comixology sales'

    def handle(self, *args, **options):
        parse_sales()
