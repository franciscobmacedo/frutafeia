from pandas.core import series
from rest_framework import serializers
from core.models import (
    Cesta,
    ConteudoCesta,
    Disponibilidade,
    FamiliaProduto,
    MapaDeCampo,
    Produtor,
    Produto,
    Ranking,
)


class ConteudoCestaSerializer(serializers.ModelSerializer):
    """Serializer for cesta content objects"""

    produto = serializers.SlugRelatedField(
        queryset=Produto.objects.all(), read_only=False, slug_field="nome"
    )
    produtor = serializers.SlugRelatedField(
        queryset=Produtor.objects.all(), read_only=False, slug_field="nome"
    )

    class Meta:
        model = ConteudoCesta
        fields = (
            "produto",
            "produtor",
            "quantidade_pequena",
            "quantidade_grande",
            "medida_name",
            "preco_unitario",
            "produto_extra",
        )


class CestaSerializer(serializers.ModelSerializer):
    """Serializer for cesta objects"""

    conteudo = ConteudoCestaSerializer(many=True, read_only=True)

    class Meta:
        model = Cesta
        fields = "__all__"


class ProdutoSerializer(serializers.ModelSerializer):
    """Serializer for produto objects"""

    class Meta:
        model = Produto
        fields = "__all__"


class FamiliaProdutoSerializer(serializers.ModelSerializer):
    """Serializer for familia produto objects"""

    class Meta:
        model = FamiliaProduto
        fields = "__all__"


class ProdutoSimpleSerializer(serializers.ModelSerializer):
    """Serializer for produto objects"""

    id = serializers.IntegerField()

    class Meta:
        model = Produto
        fields = "__all__"


class ProdutoNameSerializer(serializers.ModelSerializer):
    """Serializer for produto objects"""

    class Meta:
        model = Produto
        fields = ("nome",)


class ProdutorSerializer(serializers.ModelSerializer):
    """Serializer for produtor objects"""

    produtos = ProdutoSerializer(many=True, read_only=True)
    produtos_ids = serializers.PrimaryKeyRelatedField(
        many=True, read_only=False, queryset=Produto.objects.all(), source="produtos"
    )

    class Meta:
        model = Produtor
        fields = (
            "id",
            "nome",
            "produtos",
            "estado",
            "estado_name",
            "telefone",
            "email",
            "morada",
            "concelho",
            "produtos_ids",
        )


class DisponibilidadeSerializer(serializers.ModelSerializer):
    """Serializer for disponibilidade objects"""

    produto = serializers.SlugRelatedField(
        queryset=Produto.objects.all(), read_only=False, slug_field="nome"
    )

    produtor = serializers.SlugRelatedField(
        queryset=Produtor.objects.all(), read_only=False, slug_field="nome"
    )

    class Meta:
        model = Disponibilidade
        fields = "__all__"


class DisponibilidadeDetailSerializer(serializers.ModelSerializer):
    """Serializer for disponibilidade objects"""

    produtor = ProdutorSerializer(many=False, read_only=False)
    produto = ProdutoSerializer(many=False, read_only=False)

    class Meta:
        model = Disponibilidade
        # fields = "__all__"
        fields = (
            "id",
            "data",
            "produto",
            "produtor",
            "quantidade",
            "preco",
            "medida_dict",
            "medida",
            "on_hold",
            "urgente",
        )


class RankingSerializer(serializers.ModelSerializer):
    """Serializer for ranking objects"""

    produto = serializers.SlugRelatedField(
        queryset=Produto.objects.all(), read_only=False, slug_field="nome"
    )

    produtor = serializers.SlugRelatedField(
        queryset=Produtor.objects.all(), read_only=False, slug_field="nome"
    )

    class Meta:
        model = Ranking
        fields = "__all__"


class MapaDeCampoSerializer(serializers.ModelSerializer):
    """Serializer for mapa de campo"""

    # def __init__(self, *args, **kwargs):
    #     many = kwargs.pop("many", True)
    #     super(MapaDeCampoSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = MapaDeCampo
        fields = "__all__"
