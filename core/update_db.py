from django.conf import settings
from django.core.checks import messages
from gsheets.connect import ConnectGS
import pandas as pd
import numpy as np
from core.models import *
from core.utils import (
    get_estado,
    get_tipo_produto,
    get_medida,
    get_produtor_by_name,
    get_produto_by_name,
    get_start_end_next_week,
    get_tipo_produto_str,
    months
)
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from django_pandas.io import read_frame
from core.enum import TIPO_PRODUTO_CHOICES
from analysis.ranking.ranking import ranking
from analysis import cesta_feia

spreadsheet = settings.SPREADSHEET_ID


def rename_produtores_columns(cols):
    clean_cols = []
    for c_ in cols:
        c = c_.lower()
        if "estado" in c:
            clean_cols.append("estado")
        else:
            clean_cols.append(c)
    return clean_cols


def read_update_produtores(replace=False):
    """Reads produtores data from google sheets and updates database"""

    print("\nReading sheet 'Produtores' from google sheets")
    gs = ConnectGS()
    data = gs.read_sheet(
        sheet_id=spreadsheet,
        worksheet="Produtores",
        range="A:H",
    )
    df = pd.DataFrame().from_dict(data["values"])
    df.columns = df.iloc[0]
    df = df[1:]

    # df.to_csv("produtores.csv")
    df.columns = [c.lower() for c in df.columns]
    df.columns = rename_produtores_columns(df.columns)
    df.remover = df.remover.apply(lambda x: x.lower() == "true")

    if not df.empty and replace:
        Produtor.objects.all().delete()

    df = df.loc[~df.produtor.isnull()]
    print("Updating 'Produtores' Table\n")
    for i, row in df.iterrows():
        if row.remover:
            try:
                Produtor.objects.get(nome=row.produtor).delete()
            except:
                pass
            continue

        provider, created = Produtor.objects.update_or_create(
            nome=row.produtor,
            defaults={
                "email": row.email,
                "estado": get_estado(row.estado),
                "morada": row.morada,
                "concelho": row.concelho,
                "telefone": row.telefone,
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


def rename_produtos_columns(cols):
    clean_cols = []
    for c_ in cols:
        c = c_.lower()
        if "família" in c:
            clean_cols.append("familia")
        elif "quantidade" in c and "pequena" in c:
            clean_cols.append("quantidade_cesta_pequena")
        elif "quantidade" in c and "grande" in c:
            clean_cols.append("quantidade_cesta_grande")
        else:
            clean_cols.append(c)
    return clean_cols


def read_update_produtos(replace=False):
    """Reads produtos data from google sheets and updates database"""

    print("\nReading sheet 'Produtos' from google sheets")
    gs = ConnectGS()
    data = gs.read_sheet(
        sheet_id=spreadsheet,
        worksheet="Produtos",
        range="A:F",
    )
    df = pd.DataFrame().from_dict(data["values"])
    df.columns = df.iloc[0]
    df = df[1:]

    # df.to_csv("produtos.csv")
    df.columns = rename_produtos_columns(df.columns)
    if not df.empty and replace:
        Produto.objects.all().delete()
    print("Updating 'Produto' Table\n")
    for i, row in df.iterrows():
        try:
            family_obj, created = FamiliaProduto.objects.get_or_create(nome=row.familia)
        except:
            pass
        if isinstance(row.quantidade_cesta_pequena, str):
            try:
                row.quantidade_cesta_pequena = float(row.quantidade_cesta_pequena)
            except:
                row.quantidade_cesta_pequena = None

        if isinstance(row.quantidade_cesta_grande, str):
            try:
                row.quantidade_cesta_grande = float(row.quantidade_cesta_grande)
            except:
                row.quantidade_cesta_grande = None

        product_obj, created = Produto.objects.get_or_create(
            familia=family_obj,
            nome=row.produto,
            tipo=get_tipo_produto(row.tipo),
            medida=get_medida(row.medida),
            quantidade_cesta_pequena=row.quantidade_cesta_pequena,
            quantidade_cesta_grande=row.quantidade_cesta_grande,
        )

    print("\n\nDone!")
    print(len(df), Produto.objects.all().count())
    print(len(df.familia.unique()), FamiliaProduto.objects.all().count())


def rename_disponibilidade_columns(cols):
    clean_cols = []
    for c in cols:
        if "data" in c.lower():
            clean_cols.append("data")
        elif "preço" in c.lower():
            clean_cols.append("preco")
        elif "quantidade" in c.lower():
            clean_cols.append("quantidade")
        elif "urgente" in c.lower():
            clean_cols.append("urgente")
        else:
            clean_cols.append(c.lower())
    return clean_cols


def check_bool(u):
    if u:
        if u.lower() == "sim":
            return True
        elif u.lower() == "true":
            return True
    return False


def try_float(x):
    if not x:
        return None
    else:
        try:
            return float(x)
        except:
            if "," in x and "." in x:  # '.' is decimal and ',' is thousands
                return float(x.replace(",", ""))
            elif "," in x:
                return float(x.replace(",", "."))
            else:
                return None


def read_update_disponibilidade():
    """Reads isponibilidades data from google sheets and updates database"""

    print("\nReading sheet 'Cesta Feita' from google sheets")
    gs = ConnectGS()
    data = gs.read_sheet(
        sheet_id=spreadsheet,
        worksheet="Cesta Feita",
        range="A:H",
    )
    df = pd.DataFrame().from_dict(data["values"])
    df = df.iloc[7:]
    df.columns = df.iloc[0]
    df = df[1:]
    # df.to_csv("disponibilidade.csv")

    df.columns = rename_disponibilidade_columns(df.columns)
    df = df.loc[~df.produtor.isnull()]
    df.data = pd.to_datetime(df.data)
    df.medida = df.medida.map(get_medida)
    df.quantidade = df.quantidade.map(try_float)
    df.preco = df.preco.map(try_float)
    df.remover = df.remover.map(check_bool)
    df.urgente = df.urgente.map(check_bool)

    if df.empty:
        print("No 'disponibilidade' available (all done). Setting on_hold to False\n")
        qs = Disponibilidade.objects.filter(on_hold=True)
        qs.update(on_hold=False)
        return

    # Delete everything first, so we make sure we dont have any duplicates
    Disponibilidade.objects.filter(on_hold=True).delete()
    print("Updating 'Disponibilidade' Table\n")
    for i, row in df.iterrows():
        print("getting", row.data, row.produtor, row.produto)
        if row.remover:
            continue
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

        Disponibilidade.objects.create(
            data=row.data,
            produto=produto_obj,
            produtor=produtor_obj,
            quantidade=row.quantidade,
            medida=row.medida,
            preco=row.preco,
            urgente=row.urgente,
            on_hold=True,
        ).save()
    print("\n\nDone!")


def calculate_and_update_ranking():
    print("calculating Ranking")
    today = dt.now()
    two_years_ago = today - relativedelta(years=2)
    qs = MapaDeCampo.objects.filter(data__gte=two_years_ago).values(
        "data", "produto__nome", "produtor"
    )
    df = read_frame(qs)
    df.rename(columns={"produto__nome": "produto"}, inplace=True)
    df.data = pd.to_datetime(df.data)
    result = ranking(df)
    if not result:
        print("No data estimated..")
        return False
    Ranking.objects.all().delete()
    for rank in result:
        # rank = result[0]
        produtor = Produtor.objects.get(nome=rank.get("produtor"))
        produto = Produto.objects.get(nome=rank.get("produto"))
        pontuacao = rank.get("pontuacao")
        Ranking.objects.create(produtor=produtor, produto=produto, pontuacao=pontuacao)
    print("Done")
    return True


def calculate_and_update_cestas():
    print("calculating cestas")
    CestaResult.objects.all().delete()

    qs = Disponibilidade.objects.filter(on_hold=True).values(
        "produto__nome",
        "produto__id",
        "produto__familia__nome",
        "produto__tipo",
        "produto__quantidade_cesta_pequena",
        "produto__quantidade_cesta_grande",
        "produtor__nome",
        "produtor__id",
        "quantidade",
        "medida",
        "preco",
        "urgente",
    )
    df = read_frame(qs)
    df.reset_index(inplace=True, drop=True)
    df.produto__tipo = df.produto__tipo.map(get_tipo_produto_str)
    
    df["ranking"] = 10
    for i, row in df.iterrows():
        try:
            r = Ranking.objects.get(
                produtor__nome=row.produtor__nome, produto__nome=row.produto__nome
            )
            df.iloc[i, "ranking"] = r
            print("success")
        except:
            continue
    df.rename(
        columns={
            "produto__id": "ID_PRODUTO",
            "produto__nome": "produto",
            "produto__familia__nome": "familia",
            "produto__tipo": "tipo",
            "produto__quantidade_cesta_pequena": "quantidade_cesta_pequena",
            "produto__quantidade_cesta_grande": "quantidade_cesta_grande",
            "produtor__nome": "produtor",
            "produtor__id": "ID_PRODUTOR",
        },
        inplace=True,
    )

    success, result = cesta_feia.main(df)
    if not success:
        CestaResult.objects.create(result=False, message=result).save()
        return False

    # delete the ones that where calculated before if they exist
    date_start, _ = get_start_end_next_week()
    Cesta.objects.filter(data__gte=date_start).delete()

    print(f"Updating {len(result)} cestas..")
    for i, res in enumerate(result):
        print(f"cesta {i + 1}")
        df = res["df"]
        df = df[
            [
                "produto",
                "produtor",
                "quantidade_cesta_pequena",
                "quantidade_cesta_grande",
                "medida",
                "preco",
                "yij",
            ]
        ]
        df.produtor = df.produtor.map(get_produtor_by_name)
        df.produto = df.produto.map(get_produto_by_name)
        df.medida = df.medida.map(get_medida)
        cesta, _ = Cesta.objects.get_or_create(
            data=date_start,
            preco_pequena=res["stats"]["pequena"]["preco"],
            peso_pequena=res["stats"]["pequena"]["peso"],
            preco_grande=res["stats"]["grande"]["preco"],
            peso_grande=res["stats"]["grande"]["peso"],
        )
        for i, row in df.iterrows():
            obj, created = ConteudoCesta.objects.get_or_create(
                produto=row.produto,
                produtor=row.produtor,
                quantidade_pequena=row.quantidade_cesta_pequena,
                quantidade_grande=row.quantidade_cesta_grande,
                medida=row.medida,
                preco_unitario=row.preco,
                produto_extra=int(row.yij) == 1,
            )
            cesta.conteudo.add(obj)

    CestaResult.objects.create(result=True, message="success").save()
    return True

def read_update_sazonalidade():
    """Reads sazonalidade data from google sheets and updates database"""

    print("\nReading sheet 'Sazonalidade' from google sheets")
    gs = ConnectGS()
    data = gs.read_sheet(
        sheet_id=spreadsheet,
        worksheet="Sazonalidade",
        range="A:M",
    )
    df = pd.DataFrame().from_dict(data["values"])
    df.columns = df.iloc[0]
    df = df[1:]
    df = df.loc[~df.Produto.isnull()]

    # df.columns = [c.lower() for c in df.columns]
    if df.empty:
        return
    df.columns = [c.lower() for c in df.columns]
    df.rename(columns={
        'março': 'marco'
    }, inplace=True)
    Sazonalidade.objects.all().delete()
    # df = df.melt(id_vars="Produto")
    # df.columns = ["produto", "mes", "sazonalidade"]
    # update mes

    # df.mes = df.mes.map(months)
    for c in df.columns:
        if c == 'produo':
            continue
        df[c] = df[c].map(try_float)
    
    print("Updating 'Sazonalidade' Table\n")
    for i, row in df.iterrows():
        try:
            produto = Produto.objects.get(nome=row.produto)
        except:
            continue
        Sazonalidade.objects.create(
            produto=produto,
            janeiro=row.janeiro,
            fevereiro=row.fevereiro,
            marco=row.marco,
            abril=row.abril,
            maio=row.maio,
            junho=row.junho,
            julho=row.julho,
            agosto=row.agosto,
            setembro=row.setembro,
            outubro=row.outubro,
            novembro=row.novembro,
            dezembro=row.dezembro,
        ).save()

    print("\n\nDone!")
    print(len(df), Sazonalidade.objects.all().count())


def map_from_avai():
    for d in Disponibilidade.objects.all():
        MapaDeCampo.objects.create(
            data=d.data,
            produto=d.produto,
            produtor=d.produtor,
            quantidade=d.quantidade,
            medida=d.medida,
            preco=d.preco,
        ).save()



    

def read_update_mapas_de_campo():
    """Reads Histórico data from google sheets and updates database"""

    print("\nReading sheet 'Histórico' from google sheets")
    gs = ConnectGS()
    data = gs.read_sheet(
        sheet_id=spreadsheet,
        worksheet="Histórico",
        range="A:D",
    )
    df = pd.DataFrame().from_dict(data["values"])
    df.columns = df.iloc[0]
    df = df[1:]
    # df.to_csv("disponibilidade.csv")
    df.columns = [c.lower() for c in df.columns]
    df = df.loc[~df.produtor.isnull()]
    df.data = pd.to_datetime(df.data)
    # df = df.loc[df.cesta == 'cesta grande']
    df = df.drop_duplicates()
    for idx, row in df.iterrows():
        produtor = Produtor.objects.get(nome=row.produtor)
        produto = Produto.objects.get(nome=row.produto)
        res = MapaDeCampo.objects.get_or_create(
            data=row.data,
            produto=produto,
            produtor=produtor
        )

# df.head(10)

# # df.produto
# df.data = df.data.dt.strftime('%Y-%m-%d')

# df.to_excel('clean_cesta_3.xlsx')
    # row.produto = row.produto.lower().replace(' - ', '-')
    # if 'feijão' in row.produto or 'alho' in row.produto:
    #     row.produto = row.produto.replace(' ', '-')



# c = 0
# dates_complete= ['07 junho 2021', '31 maio 2021', '24 maio 2021', '17 maio 2021', '10 maio 2021', '3 maio 2021', '26 abril 2021', '19 abril 2021', '12 abril 2021', '5 abril 2021', '29 março 2021', '22 março 2021', '15 março 2021', '08 março 2021', '1 março 2021', '22 fevereiro 2021', '15 fevereiro 2021', '8 fevereiro 2021', '01 fevereiro 2021', '25 janeiro 2021', '18 janeiro 2021', '11 janeiro 2021', '04 janeiro 2021', '14zembro 2020', '7zembro 2020', '30 novembro 2020', '23 novembro 2020', '16 novembro 2020', '9 novembro 2020', '2 novembro 2020', '26 outubro 2020', '19 outubro 2020', '12 outubro 2020', '28 setembro 2020', '21 setembro 2020', '14 setembro 2020', '7 setembro 2020', '31 agosto 2020', '27 julho 2020', '20 julho 2020', '13 julho 2020', '6 julho 2020', '29 junho 2020', '22 junho 2020', '15 junho 2020', '8 junho 2020', '01 junho 2020', '25 maio 2020', '18 maio 2020', '11 maio 2020', '4 maio 2020', '27 abril 2020', '20 abril 2020', '13 abril 2020', '06 abril 2020', '09 março 2020', '2 março 2020', '24 fevereiro 2020', '17 fevereiro 2020', '10 fevereiro 2020', '03 fevereiro 2020', '27 janeiro 2020', '20 janeiro 2020', '13 janeiro 2020', '6 janeiro 2020', '16zembro 2019', '9zembro 2019', '2zembro 2019', '25 novembro 2019', '18 novembro 2019', '11 novembro 2019', '4 novembro 2019', '28 outubro 2019', '21 outubro 2019', '14 outubro 2019', '07 outubro 2019', '30 setembro 2019', '23 setembro 2019', '16 setembro 2019', '9 setembro 2019', '2 setembro 2019', '22 julho 2019', '15 julho 2019', '8 julho 2019', '01 julho 2019', '17 junho 2019', '03 junho 2019', '27 maio 2019', '20 maio 2019', '13 maio 2019', '6 maio 2019', '29 abril 2019', '22 abril 2019', '15 abril 2019', '8 abril 2019', '1 abril 2019', '25 março 2019', '18 março 2019', '11 março 2019', '4 março 2019', '25 fevereiro 2019', '18 fevereiro 2019', '11 fevereiro 2019', '4 fevereiro 2019', '28 janeiro 2019', '21 janeiro 2019', '14 janeiro 2019', '7 janeiro 2019', '17zembro 2018', '10zembro 2018', '3zembro 2018', '26 novembro 2018', '19 novembro 2018', '12 novembro 2018', '5 novembro 2018', '29 outubro 2018', '22 outubro 2018', '15 outubro 2018', '4 outubro 2018', '27 setembro 2018', 'do dia 20 setembro 2018', '13 setembro 2018', '6 setembro 2018', '26 julho 2018', '19 julho 2018', '12 julho 2018', '5 julho 2018', '28 junho 2018', '21 junho 2018']

# datas = df.data.unique()
# for idx, row in df.iterrows():
#     data = row.data
#     d_ = [d_ for d_ in dates_complete if data in d_][0]        
#     produtor = Produtor.objects.get(nome=row.produtor)
#     try:
#         row.data = toCustomMonth(d_)
#     except:
#         c+=1
# df.data = df.data.dt.strftime('%Y-%m-%d')

# for idx, row in df.iterrows():
#     produtor = Produtor.objects.get(nome=row.produtor)



# def toCustomMonth(date):
#     date = date.lower()
#     months = {
#         'janeiro':1,
#         'fevereiro':2,
#         'março':3,
#         'abril':4,
#         'maio':5,
#         'junho':6,
#         'julho':7,
#         'agosto':8,
#         'setembro':9,
#         'outubro':10,
#         'novembro':11,
#         'dezembro':12,
#     }
#     date = date.replace('do dia ', '')
#     if date == '22 março':
#         return dt(2021, 3, 22)
#     if date == '11 janeiro':
#         return dt(2021, 1, 11)
#     if date == '26 outubro':
#         return dt(2020, 10, 26)
#     if date == '6 julho':
#         return dt(2020, 7, 6)
#     if date == '15 julho':
#         return dt(2019, 7, 15)
#     if date == '15 junho':
#         return dt(2020, 6, 15)
#     if date == '20 abril':
#         return dt(2020, 4, 20)
#     if date == '13 abril':
#         return dt(2020, 4, 13)
#     if date == '10 fevereiro':
#         return dt(2020, 2, 10)
#     date_month = None
#     if "zembro" in date:
#         date_month = 12
#         date_day = date.split('zembro')[0]
#     else:
#         for m, m_nr in months.items():
#             if m in date:
#                 date_month =  m_nr
#                 break
#         date_day = date.split(' ')[0]
#     date_year = date.split(' ')[-1]
#     return dt(int(date_year), int(date_month), int(date_day))         
