from core.models import Disponibilidade
from django.core.management.base import BaseCommand, CommandError
from core.update_db import (
    calculate_and_update_cestas,
    read_update_produtos,
    read_update_produtores,
    read_update_disponibilidade,
    calculate_and_update_ranking,
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

        parser.add_argument(
            "-ranking",
            "--ranking",
            action="store_true",
            help="Calculate Ranking",
        )

        parser.add_argument(
            "-cesta",
            "--cesta",
            action="store_true",
            help="Calculate Cesta",
        )

        parser.add_argument(
            "-r",
            "--replace",
            action="store_true",
            help="Read and update disponibilidade",
        )

    def handle(self, *args, **options):
        produto = options["produto"]
        produtor = options["produtor"]
        disponibilidade = options["disponibilidade"]
        ranking = options["ranking"]
        cesta = options["cesta"]
        replace = options["replace"]

        if not any([produto, produtor, disponibilidade, ranking, cesta]):
            # locale.setlocale(locale.LC_ALL, "pt_pt.UTF-8")

            # week_start, week_end = get_start_end_week()
            # if week_start.month != week_end.month:
            #     cell_text = f"Semana de {week_start.day} de {week_start.strftime('%B')} a {week_end.day} de {week_end.strftime('%B')}"
            # else:
            #     cell_text = f"Semana de {week_start.day} a {week_end.day} de {week_end.strftime('%B')}"

            # gs = ConnectGS()
            # data = gs.write_sheet(
            #     sheet_id=spreadsheet,
            #     worksheet="Cesta Feita",
            #     range="A5:A5",
            #     values=[[cell_text]],
            # )
            # gs.run_function(script_id, "resetAvailability")
            read_update_produtos(replace)
            read_update_produtores(replace)
            read_update_disponibilidade()
            calculate_and_update_ranking()
            calculate_and_update_cestas()

        else:
            if produto:
                read_update_produtos(replace)
            if produtor:
                read_update_produtores(replace)
            if disponibilidade:
                read_update_disponibilidade()
            if ranking:
                calculate_and_update_ranking()
            if cesta:
                calculate_and_update_cestas()

    # def calculate_ran
