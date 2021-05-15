from rest_framework import viewsets

from core.models import Produtor, Produto
from api import serializers


class ProdutorViewSet(viewsets.ModelViewSet):
    """Access Providers in the database"""

    serializer_class = serializers.ProdutorSerializer
    queryset = Produtor.objects.all()


class ProdutoViewSet(viewsets.ModelViewSet):
    """Access Products in the database"""

    serializer_class = serializers.ProdutoSerializer
    queryset = Produto.objects.all()
