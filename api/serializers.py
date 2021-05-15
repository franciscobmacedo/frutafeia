from rest_framework import serializers
from core.models import Disponibilidade, Produtor, Produto


class ProdutorSerializer(serializers.ModelSerializer):
    """Serializer for produtor objects"""

    class Meta:
        model = Produtor
        fields = "__all__"


class ProdutoSerializer(serializers.ModelSerializer):
    """Serializer for produto objects"""

    class Meta:
        model = Produto
        fields = "__all__"


class DisponibilidadeSerializer(serializers.ModelSerializer):
    """Serializer for disponibilidade objects"""

    class Meta:
        model = Disponibilidade
        fields = "__all__"
