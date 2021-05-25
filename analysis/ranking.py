"""
    SCRIPTS DO ZÉ PARA REALIZAR A CESTA
"""

from django_pandas.io import read_frame
from core.models import MapaDeCampo, Produto, Produtor
from datetime import datetime as dt

# Para ler a tabela MapaDeCampo toda:
qs = MapaDeCampo.objects.all()

# Para ler a tabela MapaDeCampo entre duas datas:
date_start = dt(2021,5,1)
date_end = dt(2021,5,10)
qs = MapaDeCampo.objects.filter(data__gte=date_start, data__lte=date_end)

# Para ler a tabela MapaDeCampo só com urgente:
qs = MapaDeCampo.objects.filter(urgente=True)

# Para ler a tabela MapaDeCampo só para um produtor:
qs = MapaDeCampo.objects.filter(produtor__nome="Varanda do campo (Renato)")

# Para converter um django queryset para uma pandas dataframe:
df = read_frame(qs)


 # Podemos só assumir que terás uma função que recebe uma dataframe e que devolve uma dataframe também:
def main(df):
    # Do some stuff
    return df