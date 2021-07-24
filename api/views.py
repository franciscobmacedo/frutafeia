from django.http.response import JsonResponse
from django_pandas.io import read_frame
from rest_framework import viewsets
from rest_framework.views import APIView

from core.models import (
    CestaResult,
    FamiliaProduto,
    MapaDeCampo,
    Produtor,
    Produto,
    Disponibilidade,
    Ranking,
    Cesta,
    noWorkLastWeek,
)
from api import serializers
from core.update_db import (
    read_update_disponibilidade,
    read_update_produtores,
    read_update_produtos,
    calculate_and_update_ranking,
    calculate_and_update_cestas,
    read_update_mapas_de_campo,
    read_update_sazonalidade
)
from core.enum import MEDIDA_CHOICES, TIPO_PRODUTO_CHOICES, ESTADO_CHOICES
from core.utils import get_start_end_this_week, get_start_end_next_week
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime as dt
from datetime import timedelta

from django.conf import settings
from analysis.ranking.adjusted_ranking import adjusted_ranking


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

    queryset = Disponibilidade.objects.all()

    def get_queryset(self):
        """Return objects for disponibilidade on hold"""
        queryset = self.queryset.filter(on_hold=True)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.DisponibilidadeDetailSerializer
        return serializers.DisponibilidadeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list)
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        calculate_and_update_cestas()

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class DisponibilidadeAntigaViewSet(viewsets.ModelViewSet):
    """Access old Disponibilidade in the database"""

    serializer_class = serializers.DisponibilidadeDetailSerializer
    queryset = Disponibilidade.objects.all()

    def get_queryset(self):
        """Return objects for disponibilidade not on hold"""
        queryset = self.queryset.filter(on_hold=False)
        return queryset


class RankingViewSet(viewsets.ModelViewSet):
    """Access Disponibilidade in the database"""

    serializer_class = serializers.RankingSerializer
    queryset = Ranking.objects.all()


class MapasDeCampoViewSet(viewsets.ModelViewSet):
    """Access Mapa de Campo in the database"""

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
        try:
            calculate_and_update_ranking()
        except:
            pass
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


class getMapasDeCampo(APIView):
    def get(self, request, *args, **kwargs):
        read_update_mapas_de_campo()
        try:
            calculate_and_update_ranking()
        except:
            pass
        return JsonResponse({"success": True})


class getSazonalidade(APIView):
    def get(self, request, *args, **kwargs):
        read_update_sazonalidade()
        try:
            calculate_and_update_ranking()
        except:
            pass
        return JsonResponse({"success": True})

class CestaNovaViewSet(viewsets.ModelViewSet):
    """Access Cesta in the database"""

    serializer_class = serializers.CestaSerializer
    queryset = Cesta.objects.all()

    def get_queryset(self):
        """Return objects for most recent cestas"""
        date_start, _ = get_start_end_next_week()
        queryset = self.queryset.filter(data__gte=date_start)
        return queryset

    # def list(self, request, pk=None):
    #     print("asdasdasdasd")
    #     if CestaResult.objects.all().exists():
    #         info = CestaResult.objects.last()
    #         if info.result == False:
    #             return JsonResponse(
    #                 {"success": False, "message": info.message, "data": []}
    #             )

    #     serializer = self.serializer_class(self.queryset, many=True)
    #     print(self.queryset.first().conteudo.first().produtor)
    #     data = serializer.data
    #     if data:
    #         if not data[0]['conteudo']:
    #             for d in data:
    #                 d['conteudo'] =

    #     return JsonResponse({"success": True, "message": "", "data": serializer.data})

    #     return Response(serializer.data)


class CestaAntigaViewSet(viewsets.ModelViewSet):
    """Access Old Cestas in the database"""

    serializer_class = serializers.CestaSerializer
    queryset = Cesta.objects.all()

    def get_queryset(self):
        """Return objects for old cestas"""
        date_start, _ = get_start_end_next_week()
        queryset = self.queryset.filter(data__lt=date_start).order_by("-data")
        return queryset


class CestaMessageViewSet(APIView):
    def get(self, request, *args, **kwargs):
        if CestaResult.objects.all().exists():
            info = CestaResult.objects.last()
            if info.result == False:
                return JsonResponse({"success": False, "message": info.message})
        return JsonResponse({"success": True, "message": ""})


class getDisponibilidades(APIView):
    def get(self, request, *args, **kwargs):
        read_update_disponibilidade()
        calculate_and_update_cestas()
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


class setNoWorkLastWeek(APIView):
    def get(self, request, *args, **kwargs):
        qs = noWorkLastWeek.objects.all()
        if qs.exists():
            return JsonResponse({"didntWork?": noWorkLastWeek.objects.first().value})
        else:
            return JsonResponse({"didntWork?": None})

    def post(self, request, *args, **kwargs):
        value = request.data.get("value")
        if value is not None:
            qs = noWorkLastWeek.objects.all().delete()
            qs = noWorkLastWeek.objects.create(value=value).save()
            result = noWorkLastWeek.objects.all().first().value
        else:
            qs = noWorkLastWeek.objects.all()
            if qs.exists():
                result = qs.first().value
            else:
                result = None
        return JsonResponse({"didntWork?": result})

    # def post(self, request, *args, **kwargs):
    #     noWorkLastWeek.objects.all().delete()
    #     noWorkLastWeek.objects.create(value=True).save()
    #     return JsonResponse({"didntWork?": noWorkLastWeek.objects.first().value})


class comMapaDeCampo(APIView):
    def get(self, request, *args, **kwargs):
        qs_work = noWorkLastWeek.objects.all()
        if qs_work.exists():
            didnt_work_last_week = qs_work.first().value
        else:
            didnt_work_last_week = True
        if didnt_work_last_week:
            return JsonResponse({"has_data": True})

        qs = MapaDeCampo.objects.all()
        if qs.exists():
            last_mapa = qs.order_by("data").last()
            start, end = get_start_end_this_week()

            if last_mapa.data >= start.date():
                return JsonResponse({"has_data": True})

        return JsonResponse({"has_data": False})


class rankingAlterado(APIView):
    def get(self, request, *args, **kwargs):
        qs = Ranking.objects.values("produtor", "produto__nome", "pontuacao")
        df = read_frame(qs)
        df.rename(columns={"produto__nome": "produto"}, inplace=True)
        data = adjusted_ranking(df)
        for d in data:
            try:
                produtor_obj = Produtor.objects.get(nome=d["produtor"]).__dict__
                produtor_obj = {
                    key: value for key, value in produtor_obj.items() if key != "_state"
                }

                d["produtor"] = produtor_obj
            except:
                continue
        # data = [
        #     {
        #         "produtor": "António Marques",
        #         "produtos": [{"produto": "morango", "pontuacao": 10.0}],
        #     },
        #     {
        #         "produtor": "João Saramago",
        #         "produtos": [
        #             {"produto": "nectarina", "pontuacao": 10.0},
        #             {"produto": "pêra", "pontuacao": 6.875},
        #             {"produto": "maçã", "pontuacao": 6.458333333333334},
        #         ],
        #     },
        #     {
        #         "produtor": "Francelina",
        #         "produtos": [{"produto": "morango", "pontuacao": 10.0}],
        #     },
        #     {
        #         "produtor": "Jorge Silva",
        #         "produtos": [
        #             {"produto": "damasco", "pontuacao": 9.375},
        #             {"produto": "morango", "pontuacao": 9.375},
        #         ],
        #     },
        #     {
        #         "produtor": "João Mineiro",
        #         "produtos": [{"produto": "pimento", "pontuacao": 9.375}],
        #     },
        #     {
        #         "produtor": "António Gomes",
        #         "produtos": [
        #             {"produto": "cereja", "pontuacao": 8.75},
        #             {"produto": "ameixa", "pontuacao": 6.875},
        #             {"produto": "maçã", "pontuacao": 5.208333333333332},
        #         ],
        #     },
        #     {
        #         "produtor": "Luísa Botelho/ João Botelho",
        #         "produtos": [
        #             {"produto": "cereja", "pontuacao": 8.75},
        #             {"produto": "ameixa", "pontuacao": 6.875},
        #         ],
        #     },
        # ]

        # for d in data:
        #     d["produtor"] = Produtor.objects.filter(nome=d["produtor"]).values()[0]

        return JsonResponse({"data": data})


"""
    - Mapas de campo dos ultimos 2 anos (ex de 5 Junho de 2020 a 5 Junho de 2021)
    - Passar uma dataframe com data, produtor, produto
    
    from core.utils import get_start_end_this_week
    start_week, end_week = get_start_end_this_week()
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
