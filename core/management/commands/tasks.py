from core.models import Disponibilidade
from django.core.management.base import BaseCommand, CommandError
from core.update_db import (
    read_update_produtos,
    read_update_produtores,
    read_update_disponibilidade,
)
from django.conf import settings

spreadsheet = settings.SPREADSHEET_ID
script_id = settings.SCRIPT_ID


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
            # locale.setlocale(locale.LC_ALL, "pt_pt.UTF-8")

            # week_start, week_end = get_start_end_week()
            # if week_start.month != week_end.month:
            #     cell_text = f"Semana de {week_start.day} de {week_start.strftime('%B')} a {week_end.day} de {week_end.strftime('%B')}"
            # else:
            #     cell_text = f"Semana de {week_start.day} a {week_end.day} de {week_end.strftime('%B')}"

            # gs = ConnectGS()
            # data = gs.write_sheet(
            #     sheet_id=spreadsheet,
            #     worksheet="Disponibilidade",
            #     range="A5:A5",
            #     values=[[cell_text]],
            # )
            # gs.run_function(script_id, "resetAvailability")
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

    # def calculate_ran
