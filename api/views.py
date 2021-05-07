from rest_framework import viewsets

from core.models import Produtor
from api import serializers


class ProdutorViewSet(viewsets.ModelViewSet):
    """Access Products in the database"""

    serializer_class = serializers.ProdutorSerializer
    queryset = Produtor.objects.all()
