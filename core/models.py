from django.db import models
from googleapiclient import model
from pandas.core.algorithms import quantile
from core.enum import TIPO_PRODUTO_CHOICES, ESTADO_CHOICES, MEDIDA_CHOICES

# Create your models here.


class FamiliaProduto(models.Model):
    nome = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Família de Produto"
        verbose_name_plural = "Famílias de Produtos"

    def __str__(self):
        return str(self.nome)


class Produto(models.Model):
    """Possible products"""

    nome = models.CharField(max_length=255)
    familia = models.ForeignKey("FamiliaProduto", on_delete=models.CASCADE)
    tipo = models.PositiveSmallIntegerField(
        choices=TIPO_PRODUTO_CHOICES, blank=True, null=True
    )

    @property
    def tipo_name(self):
        return dict(TIPO_PRODUTO_CHOICES).get(self.tipo)

    def __str__(self):
        return f"{self.nome} - {self.tipo_name}"


class Produtor(models.Model):
    """Produts providers"""

    nome = models.CharField(max_length=255)
    produtos = models.ManyToManyField("Produto")
    estado = models.PositiveSmallIntegerField(choices=ESTADO_CHOICES)
    email = models.EmailField(max_length=255, null=True, blank=True)
    morada = models.CharField(max_length=255, null=True, blank=True)
    concelho = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Produtores"

    @property
    def estado_name(self):
        return dict(ESTADO_CHOICES).get(self.estado)

    def __str__(self):
        return self.nome


class Disponibilidade(models.Model):
    data = models.DateField()
    produto = models.ForeignKey("Produto", on_delete=models.CASCADE)
    produtor = models.ForeignKey("Produtor", on_delete=models.CASCADE)
    quantidade = models.FloatField()
    medida = models.PositiveSmallIntegerField(choices=MEDIDA_CHOICES)
    preco = models.FloatField()
    urgente = models.BooleanField()

    @property
    def medida_name(self):
        return dict(MEDIDA_CHOICES).get(self.medida)
    
    def __str__(self):
        return f"{self.data} : {self.produtor} : {self.produto}"


class MapaDeCampo(models.Model):
    data = models.DateField()
    produto = models.ForeignKey("Produto", on_delete=models.CASCADE)
    produtor = models.ForeignKey("Produtor", on_delete=models.CASCADE)
    quantidade = models.FloatField()
    medida = models.PositiveSmallIntegerField(choices=MEDIDA_CHOICES)
    preco = models.FloatField()
    urgente = models.BooleanField()

    @property
    def medida_name(self):
        return dict(MEDIDA_CHOICES).get(self.medida)
    
    def __str__(self):
        return f"{self.data} : {self.produtor} : {self.produto}"

class Ranking(models.Model):
    data = models.DateField()
    produto = models.ForeignKey("Produto", on_delete=models.CASCADE)
    produtor = models.ForeignKey("Produtor", on_delete=models.CASCADE)
    pontuacao = models.FloatField()


# TODO - Model(s) para a sugestão de cestas