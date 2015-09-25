from rest_framework import serializers

from portfolio.models import Security

class SecuritySerializer(serializers.ModelSerializer):
    """
    Serializing all the Authors
    """
    class Meta:
        model = Security
        fields = ('ticker', 'name', 'id')

