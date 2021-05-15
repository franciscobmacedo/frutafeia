from core.models import Disponibilidade
from django.core.management.base import BaseCommand, CommandError
from core.update_db import (
    read_update_produtos,
    read_update_produtores,
    read_update_disponibilidade,
)


class Command(BaseCommand):
    help = "Reads data from googlesheets and updates DB"

    def add_arguments(self, parser):

        parser.add_argument(
            "-produto",
            "--produto",
            action="store_true",
            help="Read and update produtos",
        )
        parser.add_argument(
            "-produtor",
            "--produtor",
            action="store_true",
            help="Read and update produtores",
        )

        parser.add_argument(
            "-disponibilidade",
            "--disponibilidade",
            action="store_true",
            help="Read and update disponibilidade",
        )

    def handle(self, *args, **options):
        produto = options["produto"]
        produtor = options["produtor"]
        disponibilidade = options["disponibilidade"]

        if not any([produto, produtor, disponibilidade]):
            read_update_produtos()
            read_update_produtores()
            read_update_disponibilidade()
        else:
            if produto:
                read_update_produtos()
            if produtor:
                read_update_produtores()
            if disponibilidade:
                read_update_disponibilidade()
