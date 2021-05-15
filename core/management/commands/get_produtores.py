from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from gsheets.connect import ConnectGS
import pandas as pd
import numpy as np
from core.models import *
from core.utils import get_estado


class Command(BaseCommand):
    help = "Reads produtores sheet"

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
            print("reading sheet 'Produtores' from google sheets")
            gs = ConnectGS()
            data = gs.read_sheet(
                sheet_id=self.spreadsheet,
                worksheet="Produtores",
                range="A:G",
            )
            df = pd.DataFrame().from_dict(data["values"])
            df.columns = df.iloc[0]
            df = df[1:]
        else:
            print("Reading local 'produtores.csv' file")
            try:
                df = pd.read_csv("produtores.csv")
            except FileNotFoundError:
                print("-cant find file...")
                return
        # df.to_csv("produtores.csv")
        df.columns = [c.lower() for c in df.columns]

        df.rename(columns={"estado do produtor": "estado"}, inplace=True)

        print("Updating 'Produtores' Table\n")
        for i, row in df.iterrows():
            print(row.produtor)
            provider, created = Produtor.objects.update_or_create(
                nome=row.produtor,
                defaults={
                    "email": row.email,
                    "estado": get_estado(row.estado),
                    "morada": row.morada,
                    "concelho": row.concelho,
                },
            )

            if isinstance(row.produtos, str):

                products = row.produtos.split(",")
                products = [p.strip() for p in products]
                for product in products:
                    try:
                        product_obj = Produto.objects.get(nome=product)
                    except Produto.DoesNotExist:
                        continue
                    provider.produtos.add(product_obj)
        print("\n\nDone!")
        print(len(df), Produtor.objects.all().count())
