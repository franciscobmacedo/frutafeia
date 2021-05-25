from django.http.response import JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView

from core.models import Produtor, Produto, Disponibilidade
from api import serializers
from core.update_db import read_update_disponibilidade
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

    def create(self, request, *args, **kwargs):
        print(args)
        print(kwargs)
        data = request.data
        print(data)

        if data.get('delete') and data.get('delete').lower() == "true":
            print('deleting!')
            qs = Disponibilidade.objects.filter(data=data.get('data'), produto__nome=data.get('produto'), produtor__nome=data.get('produtor'), quantidade=float(data.get('quantidade')), medida=int(data.get('medida')), preco=float(data.get('preco')), urgente=data.get('urgente').lower()=='true')
            print(qs)
            if qs.exists:
                qs.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return super().create(request, *args, **kwargs)

class getDisponibilidades(APIView):
    def get(self, request, *args, **kwargs):
        read_update_disponibilidade()
        return JsonResponse({"success": True})
