from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from gsheets.connect import ConnectGS
import pandas as pd


class Command(BaseCommand):
    help = "Reads produtores sheet"

    spreadsheet = settings.SPREADSHEET_ID

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "model",
    #         type=str,
    #         help="name of the table in app energy (with no underscore) that you want to dump data from",
    #     )

    def handle(self, *args, **options):
        # model_string = options["model"]

        gs = ConnectGS()
        data = gs.read_sheet(
            sheet_id=self.spreadsheet,
            worksheet="Produtores",
            range="A:G",
        )
        df = pd.DataFrame().from_dict(data["values"])
        df.columns = df.iloc[0]
        df = df[1:]
        # TODO clean data and store it in the database
        # df.to_csv("produtores.csv")
