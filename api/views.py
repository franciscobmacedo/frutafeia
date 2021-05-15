from django.http.response import JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView

from core.models import Produtor, Produto, Disponibilidade
from api import serializers
from core.update_db import read_update_disponibilidade


class ProdutorViewSet(viewsets.ModelViewSet):
    """Access Providers in the database"""

    serializer_class = serializers.ProdutorSerializer
    queryset = Produtor.objects.all()


class ProdutoViewSet(viewsets.ModelViewSet):
    """Access Products in the database"""

    serializer_class = serializers.ProdutoSerializer
    queryset = Produto.objects.all()


class DisponibilidadeViewSet(viewsets.ModelViewSet):
    """Access Disponibilidade in the database"""

    serializer_class = serializers.DisponibilidadeSerializer
    queryset = Disponibilidade.objects.all()


class getDisponibilidades(APIView):
    def get(self, request, *args, **kwargs):
        read_update_disponibilidade()
        return JsonResponse({"success": True})
