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
    PrecisaMapaDeCampo,
)
from api import serializers
from core.update_db import (
    read_update_disponibilidade,
    read_update_produtores,
    read_update_produtos,
    calculate_and_update_ranking,
    calculate_and_update_cestas,
    read_update_mapas_de_campo,
    read_update_sazonalidade,
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
    
    def get_serializer_class(self):
        print(self.action)
        if self.action == "update" or self.action == "create":
            return serializers.ProdutorSerializer

        return serializers.ProdutorDetailSerializer

class FamiliaProdutoViewSet(viewsets.ModelViewSet):
    """Access Products in the database"""

    serializer_class = serializers.FamiliaProdutoSerializer
    queryset = FamiliaProduto.objects.all()


class ProdutoViewSet(viewsets.ModelViewSet):
    """Access Products in the database"""

    serializer_class = serializers.ProdutoDetailSerializer
    queryset = Produto.objects.all()
    def get_serializer_class(self):
        print(self.action)
        if self.action == "update" or self.action == "create":
            return serializers.ProdutoSerializer

        return serializers.ProdutoDetailSerializer


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

        # Does not need mapa de campo for next week anymore
        needs = PrecisaMapaDeCampo.objects.first()
        needs.value = False
        needs.date = dt.now() + timedelta(days=7)
        needs.save()
        try:
            calculate_and_update_ranking()
        except:
            pass

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


class needsMapaDeCampo(APIView):
    def get(self, request, *args, **kwargs):
        from core.utils import get_start_end_this_week

        needs = PrecisaMapaDeCampo.objects.first()
        start, end = get_start_end_this_week()
        # print("start", start.date())
        # print("dte", needs.date.date())
        # if it was set for this week or later the value is what it is
        if needs.date.date() >= start.date():
            return JsonResponse({"needs_mapadecampo": needs.value, "date": needs.date})

        # if it was set in last or older week the value is wrong
        else:
            return JsonResponse({"needs_mapadecampo": True, "date": needs.date})

    def post(self, request, *args, **kwargs):
        value = request.data.get("value")
        if value is not None:
            needs = PrecisaMapaDeCampo.objects.all().first()
            needs.value = value
            needs.date = dt.now()
            needs.save()

        else:
            needs = PrecisaMapaDeCampo.objects.all().first()
            value = needs.value

        return JsonResponse({"needs_mapadecampo": value, "date": needs.date})


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
