from rest_framework import serializers
from .models import Favourite


class UserSerializer(serializers.Serializer):
    login = serializers.CharField(max_length=20)
    # password = serializers.CharField(max_length=64)
    name = serializers.CharField(max_length=64)
    email = serializers.EmailField(max_length=64)
    registration_date = serializers.IntegerField(read_only=True)
    last_signin_date = serializers.IntegerField(read_only=True)


class ColorSerializer(serializers.Serializer):
    color = serializers.RegexField(regex=r'[\dA-F]{6}', required=True, max_length=6, min_length=6)
    n = serializers.IntegerField(min_value=1, required=True)


class CarIDSerializer(serializers.Serializer):
    car_id = serializers.IntegerField(min_value=1, required=True)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ['user', 'car', 'date']



