from django.conf import settings
from gsheets.connect import ConnectGS
import pandas as pd
import numpy as np
from core.models import *
from core.utils import get_estado, get_tipo_produto

spreadsheet = settings.SPREADSHEET_ID


def read_update_produtores():
    """Reads produtores data from google sheets and updates database"""

    print("reading sheet 'Produtores' from google sheets")
    gs = ConnectGS()
    data = gs.read_sheet(
        sheet_id=spreadsheet,
        worksheet="Produtores",
        range="A:G",
    )
    df = pd.DataFrame().from_dict(data["values"])
    df.columns = df.iloc[0]
    df = df[1:]

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


def read_update_produtos():
    """Reads produtos data from google sheets and updates database"""

    print("reading sheet 'Produtos' from google sheets")
    gs = ConnectGS()
    data = gs.read_sheet(
        sheet_id=spreadsheet,
        worksheet="Produtos",
        range="A:C",
    )
    df = pd.DataFrame().from_dict(data["values"])
    df.columns = df.iloc[0]
    df = df[1:]

    # df.to_csv("produtos.csv")
    cols = [c.lower() for c in df.columns]
    df.columns = cols

    df.rename(columns={"família": "familia"}, inplace=True)
    print("Updating 'Produto' Table\n")
    for i, row in df.iterrows():
        print(row.produto)
        family_obj, created = FamiliaProduto.objects.get_or_create(nome=row.familia)

        product_obj, created = Produto.objects.get_or_create(
            familia=family_obj, nome=row.produto, tipo=get_tipo_produto(row.tipo)
        )

    print("\n\nDone!")
    print(len(df), Produto.objects.all().count())
    print(len(df.familia.unique()), FamiliaProduto.objects.all().count())


def read_update_disponibilidade():
    """Reads isponibilidades data from google sheets and updates database"""

    print("reading sheet 'Disponibilidade' from google sheets")
    gs = ConnectGS()
    data = gs.read_sheet(
        sheet_id=spreadsheet,
        worksheet="Disponibilidade",
        range="A:E",
    )
    df = pd.DataFrame().from_dict(data["values"])
    df.columns = df.iloc[0]
    df = df[1:]
    # df.to_csv("disponibilidade.csv")

    df.columns = [c.lower() for c in df.columns]
    df.rename(
        columns={"delegação": "delegacao", "quantidade total": "quantidade"},
        inplace=True,
    )
    df.data = pd.to_datetime(df.data)

    print("Updating 'Disponobilidade' Table\n")
    for i, row in df.iterrows():
        print(row.data, row.produtor, row.produto)
        try:
            produto_obj = Produto.objects.get(nome=row.produto)
        except Produto.DoesNotExist:
            print(f"cant find product {row.producto}")
            continue
        try:
            produtor_obj = Produtor.objects.get(nome=row.produtor)
        except Produtor.DoesNotExist:
            print(f"cant find produtor {row.produtor}")
            continue
        disponibilidade_obj, created = Disponibilidade.objects.get_or_create(
            data=row.data,
            delegacao=row.delegacao,
            quantidade=row.quantidade,
            produto=produto_obj,
            produtor=produtor_obj,
        )
    print("\n\nDone!")
