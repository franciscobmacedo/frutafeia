from django.db import models
from core.enum import TIPO_PRODUTO_CHOICES, ESTADO_CHOICES

# Create your models here.
"""
Produtor	Produtos	Estado do Produtor	Email	Telefone	Morada	Concelho	Origem do Contacto	Visita	Reactivação contacto	Descrição (site: texto + foto)	Acordo Entregue	Ultimo Contacto / Comentários

"""


class Produto(models.Model):
    """Possible products"""

    nome = models.CharField(max_length=255)
    tipo = models.PositiveSmallIntegerField(
        choices=TIPO_PRODUTO_CHOICES, blank=True, null=True
    )

    @property
    def tipo_name(self):
        return dict(TIPO_PRODUTO_CHOICES).get(self.tipo)

    def __str__(self):
        return f"{self.nome} - {self.tipo_name}"


class Telefone(models.Model):
    """Phone numbers"""

    numero = models.BigIntegerField()

    def __str__(self):
        return str(self.numero)


class Produtor(models.Model):
    """Produts providers"""

    nome = models.CharField(max_length=255)
    produto = models.ManyToManyField("Produto")
    estado = models.PositiveSmallIntegerField(choices=ESTADO_CHOICES)
    email = models.EmailField(max_length=255)
    telefone = models.ManyToManyField("Telefone")
    morada = models.CharField(max_length=255, null=True, blank=True)
    concelho = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Produtores"

    @property
    def estado_name(self):
        return dict(ESTADO_CHOICES).get(self.estado)

    def __str__(self):
        return self.nome
