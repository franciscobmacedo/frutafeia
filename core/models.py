from django.db import models
from core.enum import TIPO_PRODUTO_CHOICES, ESTADO_CHOICES

# Create your models here.


class FamiliaProduto(models.Model):
    nome = models.CharField(max_length=255)

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


class Telefone(models.Model):
    """Phone numbers"""

    numero = models.BigIntegerField()

    def __str__(self):
        return str(self.numero)


class Produtor(models.Model):
    """Produts providers"""

    nome = models.CharField(max_length=255)
    produtos = models.ManyToManyField("Produto")
    estado = models.PositiveSmallIntegerField(choices=ESTADO_CHOICES)
    email = models.EmailField(max_length=255, null=True, blank=True)
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
