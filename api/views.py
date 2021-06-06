from django.http.response import JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView

from core.models import (
    FamiliaProduto,
    MapaDeCampo,
    Produtor,
    Produto,
    Disponibilidade,
    Ranking,
)
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
from datetime import datetime as dt
from datetime import timedelta

from django.conf import settings


class ProdutorViewSet(viewsets.ModelViewSet):
    """Access Providers in the database"""

    serializer_class = serializers.ProdutorSerializer
    queryset = Produtor.objects.all()


class FamiliaProdutoViewSet(viewsets.ModelViewSet):
    """Access Products in the database"""

    serializer_class = serializers.FamiliaProdutoSerializer
    queryset = FamiliaProduto.objects.all()


class ProdutoViewSet(viewsets.ModelViewSet):
    """Access Products in the database"""

    serializer_class = serializers.ProdutoSerializer
    queryset = Produto.objects.all()


class DisponibilidadeViewSet(viewsets.ModelViewSet):
    """Access Disponibilidade in the database"""

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.DisponibilidadeDetailSerializer
        return (
            serializers.DisponibilidadeSerializer
        )  # I dont' know what you want for create/destroy/update.

    queryset = Disponibilidade.objects.all()


class RankingViewSet(viewsets.ModelViewSet):
    """Access Disponibilidade in the database"""

    serializer_class = serializers.RankingSerializer
    queryset = Ranking.objects.all()


class MapasDeCampoViewSet(viewsets.ModelViewSet):
    """Access Disponibilidade in the database"""

    serializer_class = serializers.MapaDeCampoSerializer
    queryset = MapaDeCampo.objects.all()


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


# class mapaDeCampoAtualizado(APIView):
#     def get(self, request, *args, **kwargs):
#         last_map = MapaDeCampo.objects.order_by("data").last()

#         today = dt.now()
#         # offset = (today.weekday() - settings.START_WEEK_DAY) % 7
#         # last_week_day = today - timedelta(days=offset)
#         recent_map_data = False

#         if today.weekday >= settings.START_WEEK_DAY and not recent_map_data:
#             return
#         return JsonResponse(
#             [{"id": t[0], "nome": t[1]} for t in MEDIDA_CHOICES], safe=False
#         )
