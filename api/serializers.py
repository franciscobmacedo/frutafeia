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

    produto = serializers.SlugRelatedField(
        queryset=Produto.objects.all(), read_only=False, slug_field="nome"
    )

    produtor = serializers.SlugRelatedField(
        queryset=Produtor.objects.all(), read_only=False, slug_field="nome"
    )
    medida = serializers.CharField(source='get_medida_display')

    class Meta:
        model = Disponibilidade
        fields ="__all__"
