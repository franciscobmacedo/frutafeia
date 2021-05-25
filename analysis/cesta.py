"""
    SCRIPTS DA ANA PARA REALIZAR A CESTA
"""

from django_pandas.io import read_frame
from core.models import Disponibilidade
from datetime import datetime as dt

# Para ler a tabela Disponibilidade toda:
qs = Disponibilidade.objects.all()

# Para ler a tabela Disponibilidade entre duas datas:
date_start = dt(2021,5,1)
date_end = dt(2021,5,10)
qs = Disponibilidade.objects.filter(data__gte=date_start, data__lte=date_end)

# Para ler a tabela Disponibilidade só com urgente:
qs = Disponibilidade.objects.filter(urgente=True)

# Para ler a tabela Disponibilidade só para um produtor:
qs = Disponibilidade.objects.filter(produtor__nome="Varanda do campo (Renato)")

# Para converter um django queryset para uma pandas dataframe:
df = read_frame(qs)


 # Podemos só assumir que terás uma função que recebe uma dataframe e que devolve uma dataframe também:
def main(df):
    # Do some stuff
    return df