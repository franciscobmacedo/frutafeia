from enum import Enum


class TipoProduto(Enum):
    VERDE = 1
    FRUTA = 2
    LEGUME = 3
    OUTRO = 4


TIPO_PRODUTO_CHOICES = (
    (TipoProduto.VERDE.value, "Verde"),
    (TipoProduto.FRUTA.value, "Fruta"),
    (TipoProduto.LEGUME.value, "Legume"),
    (TipoProduto.OUTRO.value, "Outro"),
)


class Estado(Enum):
    FINAL = 1
    POTENCIAL = 2
    ANTIGO = 3
    LISTA_NEGRA = 4


ESTADO_CHOICES = (
    (Estado.FINAL.value, "Final"),
    (Estado.POTENCIAL.value, "Potencial"),
    (Estado.ANTIGO.value, "Antigo"),
    (Estado.LISTA_NEGRA.value, "Lista Negra"),
)


class Medida(Enum):
    UNIDADE = 1
    KG = 2


MEDIDA_CHOICES = (
    (Medida.UNIDADE.value, "Unidade"),
    (Medida.KG.value, "Kg"),
)
