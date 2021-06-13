from core.enum import ESTADO_CHOICES, MEDIDA_CHOICES, TIPO_PRODUTO_CHOICES
from datetime import datetime as dt, time
from datetime import timedelta


def get_choice_value(choice_str, choices):
    choice_nr = [
        t[0] for t in choices if t[1].lower().strip() == choice_str.lower().strip()
    ]
    if not choice_nr:
        return None
    return choice_nr[0]


def get_estado(estado_str):
    return get_choice_value(estado_str, ESTADO_CHOICES)


def get_tipo_produto(tipo_str):
    return get_choice_value(tipo_str, TIPO_PRODUTO_CHOICES)


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
