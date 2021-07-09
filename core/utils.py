from pandas.core.algorithms import isin
from core.enum import ESTADO_CHOICES, MEDIDA_CHOICES, TIPO_PRODUTO_CHOICES
from datetime import datetime as dt, time
from datetime import timedelta
from core.models import Produtor, Produto


def get_produtor_by_name(produtor_str):
    try:
        return Produtor.objects.get(nome=produtor_str)
    except:
        return None


def get_produto_by_name(produto_str):
    try:
        return Produto.objects.get(nome=produto_str)
    except:
        return None


def get_choice_value(choice_str, choices):
    if isinstance(choice_str, str):
        choice_nr = [
            t[0] for t in choices if t[1].lower().strip() == choice_str.lower().strip()
        ]
        if choice_nr:
            return choice_nr[0]
    return None


def get_estado(estado_str):
    return get_choice_value(estado_str, ESTADO_CHOICES)


def get_tipo_produto(tipo_str):
    return get_choice_value(tipo_str, TIPO_PRODUTO_CHOICES)

def get_tipo_produto_str(tipo_id):
    tipo_str = dict(TIPO_PRODUTO_CHOICES).get(tipo_id).lower()
    if tipo_str == 'legume':
        return 'verde'
    return tipo_str

def get_medida(medida_str):
    if isinstance(medida_str, str):
        medida_str = medida_str.lower().capitalize()
        return get_choice_value(medida_str, MEDIDA_CHOICES)
    else:
        return None


def get_start_end_this_week():
    now = dt.now()
    start = now - timedelta(days=now.weekday())
    end = start + timedelta(days=6)
    return start, end


def get_start_end_last_week():
    now = dt.now()

    start = now - timedelta(days=now.weekday() + 7)
    end = start + timedelta(days=6)
    return start, end


def get_start_end_next_week():
    now = dt.now()

    start = now - timedelta(days=now.weekday() - 7)
    end = start + timedelta(days=6)
    return start, end


def check():
    from core.models import Produtor
    import pandas as pd
    import numpy as np

    produtores = Produtor.objects.values_list("nome", flat=True)
    produtores = [p.lower().strip() for p in produtores if p is not np.nan]

    # df = pd.read_clipboard()
    # df.to_csv('mapa_de_campo.csv')
    df = pd.read_csv("mapa_de_campo.csv", index_col=0)


# count = 0
# mismatch = []
# for p in df.Produtor.unique():
#     if p is np.nan:
#         continue
#     if p.lower().strip() not in produtores:
#         produtos = df.loc[df.Produtor == p, "Produto"].unique().tolist()
#         produtos = [p.lower().strip() for p in produtos]
#         mismatch.append({"produtor": p, "produtos": produtos})
#         count += 1
# df_falta = pd.DataFrame(mismatch)
# df_falta.produtos = df_falta.produtos.apply(lambda x: ", ".join(x))
# df_falta.to_excel("produtores_em_falta.xlsx")

def months(m):
    m = m.lower()
    return {
        'janeiro':1,
        'fevereiro':2,
        'março':3,
        'abril':4,
        'maio':5,
        'junho':6,
        'julho':7,
        'agosto':8,
        'setembro':9,
        'outubro':10,
        'novembro':11,
        'dezembro':12,
    }[m]

def text_months(m):
    return {
        1: 'janeiro',
        2: 'fevereiro',
        3: 'marco',
        4: 'abril',
        5: 'maio',
        6: 'junho',
        7: 'julho',
        8: 'agosto',
        9: 'setembro',
        10: 'outubro',
        11: 'novembro',
        12: 'dezembro',
    }[m]
