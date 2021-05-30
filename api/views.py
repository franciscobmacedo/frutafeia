from django.http.response import JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView

from core.models import Produtor, Produto, Disponibilidade, Ranking
from api import serializers
from core.update_db import (
    read_update_disponibilidade,
    read_update_produtores,
    read_update_produtos,
)
from core.enum import MEDIDA_CHOICES, TIPO_PRODUTO_CHOICES, ESTADO_CHOICES
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


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


class RankingViewSet(viewsets.ModelViewSet):
    """Access Disponibilidade in the database"""

    serializer_class = serializers.RankingSerializer
    queryset = Ranking.objects.all()


class getDisponibilidades(APIView):
    def get(self, request, *args, **kwargs):
        read_update_disponibilidade()
        return JsonResponse({"success": True})


class getProdutores(APIView):
    def get(self, request, *args, **kwargs):
        read_update_produtores()
        return JsonResponse({"success": True})


class getProdutos(APIView):
    def get(self, request, *args, **kwargs):
        read_update_produtos()
        return JsonResponse({"success": True})


class tipoProdutos(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            [{"id": t[0], "nome": t[1]} for t in TIPO_PRODUTO_CHOICES], safe=False
        )


class estadoProdutor(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            [{"id": t[0], "nome": t[1]} for t in ESTADO_CHOICES], safe=False
        )


class medida(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            [{"id": t[0], "nome": t[1]} for t in MEDIDA_CHOICES], safe=False
        )
