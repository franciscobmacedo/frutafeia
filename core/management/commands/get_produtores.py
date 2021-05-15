from django.core.management.base import BaseCommand, CommandError
from core.update_db import read_update_produtores


class Command(BaseCommand):
    help = "Reads produtores sheet and update DB"

    def handle(self, *args, **options):
        read_update_produtores()
