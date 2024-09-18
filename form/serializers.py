from rest_framework import serializers
from .models import Registration


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        exclude = [
            'id',
            'created',
        ]

        
class EmailSerializer(serializers.Serializer):
    emails = serializers.ListField(
        child=serializers.EmailField(),
        allow_empty=False
    )

class SingleEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()