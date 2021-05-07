from rest_framework import serializers
from core.models import Produtor


class ProdutorSerializer(serializers.ModelSerializer):
    """Serializer for produtor objects"""

    class Meta:
        model = Produtor
        fields = "__all__"
