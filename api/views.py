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
from core.utils import get_start_end_this_week, get_start_end_last_week
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

    # serializer_class = serializers.MapaDeCampoSerializer
    # queryset = MapaDeCampo.objects.all()
    queryset = MapaDeCampo.objects.all()
    serializer_class = serializers.MapaDeCampoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list)
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        """
            today = dt.now()
            start_date = today - timedelta(years=2)
            qs_mapas_de_campo = MapaDeCampo.objects.filter(data__gte=start_date)
            df_mapas_de_campo = read_frame(qs_mapas_de_campo)
            ranking = get_ranking(df_mapas_de_campo)
            Ranking.objects.all().delete()
            obj_list = [Ranking(**r) for r in ranking]
            objs = Ranking.objects.bulk_create(obj_list)
        """
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


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


class comMapaDeCampo(APIView):
    def get(self, request, *args, **kwargs):
        qs = MapaDeCampo.objects.all()
        if qs.exists:
            last_mapa = qs.order_by("data").last()
        start, end = get_start_end_this_week()
        if last_mapa.data >= start.date():
            return JsonResponse({"has_data": True})
        else:
            return JsonResponse({"has_data": False})


class rankingAlterado(APIView):
    def get(self, request, *args, **kwargs):
        """
        ranking = Ranking.objects.all()
        data = clean_ranking(ranking)
        """
        data = [
            {
                "produtor": "António Marques",
                "produtos": [{"produto": "morango", "pontuacao": 10.0}],
            },
            {
                "produtor": "João Saramago",
                "produtos": [
                    {"produto": "nectarina", "pontuacao": 10.0},
                    {"produto": "pêra", "pontuacao": 6.875},
                    {"produto": "maçã", "pontuacao": 6.458333333333334},
                ],
            },
            {
                "produtor": "Francelina",
                "produtos": [{"produto": "morango", "pontuacao": 10.0}],
            },
            {
                "produtor": "Jorge Silva",
                "produtos": [
                    {"produto": "damasco", "pontuacao": 9.375},
                    {"produto": "morango", "pontuacao": 9.375},
                ],
            },
            {
                "produtor": "João Mineiro",
                "produtos": [{"produto": "pimento", "pontuacao": 9.375}],
            },
            {
                "produtor": "António Gomes",
                "produtos": [
                    {"produto": "cereja", "pontuacao": 8.75},
                    {"produto": "ameixa", "pontuacao": 6.875},
                    {"produto": "maçã", "pontuacao": 5.208333333333332},
                ],
            },
            {
                "produtor": "Luísa Botelho/ João Botelho",
                "produtos": [
                    {"produto": "cereja", "pontuacao": 8.75},
                    {"produto": "ameixa", "pontuacao": 6.875},
                ],
            },
        ]

        for d in data:
            d["produtor"] = Produtor.objects.filter(nome=d["produtor"]).values()[0]

        print(d)
        return JsonResponse({"data": data})


"""
    - Mapas de campo dos ultimos 2 anos (ex de 5 Junho de 2020 a 5 Junho de 2021)
    - Passar uma dataframe com data, produtor, produto
    
    from core.utils import get_start_end_week
    start_week, end_week = get_start_end_week()
    ranking = Ranking.objects.filter(data__gte=start_week, data__lte=end_week).values('produtor', 'produto', 'pontuacao')

    # daqui sai isto
    ls = [
        {'produtor': 'Natália Dias', 'produto': 'laranja', 'pontuação': 64.58333333333334},
        {'produtor': 'Adelino', 'produto': 'limão', 'pontuação': 81.25},
        {'produtor': 'Francelina', 'produto': 'morango', 'pontuação': 100.0},
        {'produtor': 'David Oliveira', 'produto': 'alface', 'pontuação': 68.75},
        {'produtor': 'PAM', 'produto': 'couve coração', 'pontuação': 68.75}
    ]
    # df = read_frame(ls)

    # .... Código a fazer ....
    # daqui sai isto
    ranking_ajustado = 
                [
                    {  
                        'produtor': 'PAM',
                        'produtos' : [
                                        {'produto': 'couve coração', 'pontuação': 68.75},
                                        {'produto': 'alho-francês', 'pontuação': 33.33333333333333}
                                        {'produto': 'espargos', 'pontuação': 33.33333333333333}
                                    ]
                    },
                    {
                        'produtor': 'Natália Dias', 
                        'produtos' : [
                                        {'produto': 'laranja', 'pontuação': 34.5}
                                    ]
                    },
                ]
"""
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
