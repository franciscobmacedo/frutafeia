from rest_framework import serializers
from core.models import Produtor, Produto


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
