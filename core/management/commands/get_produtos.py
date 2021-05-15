from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from gsheets.connect import ConnectGS
import pandas as pd
import numpy as np
from core.models import *
from core.utils import get_tipo_produto


class Command(BaseCommand):
    help = "Reads produtos sheet and store it in the database"

    spreadsheet = settings.SPREADSHEET_ID

    def add_arguments(self, parser):
        parser.add_argument(
            "-g",
            "--get",
            action="store_true",
            help="Get data from google sheets",
        )

    def handle(self, *args, **options):

        g = options["get"]
        if g:
            print("reading sheet 'Produtos' from google sheets")
            gs = ConnectGS()
            data = gs.read_sheet(
                sheet_id=self.spreadsheet,
                worksheet="Produtos",
                range="A:C",
            )
            df = pd.DataFrame().from_dict(data["values"])
            df.columns = df.iloc[0]
            df = df[1:]
        else:
            print("Reading local produtos.csv file")
            try:
                df = pd.read_csv("produtos.csv", index_col=0)
            except FileNotFoundError:
                print("-cant find file...")
                return
        # df.to_csv("produtos.csv")
        cols = [c.lower() for c in df.columns]
        df.columns = cols

        df.rename(columns={"família": "familia"}, inplace=True)
        print("Updating 'Produtos' Table\n")
        for i, row in df.iterrows():
            print(row.produto)
            family_obj, created = FamiliaProduto.objects.get_or_create(nome=row.familia)

            product_obj, created = Produto.objects.get_or_create(
                familia=family_obj, nome=row.produto, tipo=get_tipo_produto(row.tipo)
            )

        print("\n\nDone!")
        print(len(df), Produto.objects.all().count())
        print(len(df.familia.unique()), FamiliaProduto.objects.all().count())
