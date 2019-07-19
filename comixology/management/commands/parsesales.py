from django.core.management.base import BaseCommand

from comixology import tasks


class Command(BaseCommand):
    help = "Parse the current comixology sales"

    def handle(self, *args, **options):
        tasks.parse_sales()
