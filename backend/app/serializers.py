from django.contrib.auth import authenticate
from rest_framework import serializers as s

from app.models import User


class MessageSerializer(s.Serializer):
    content = s.CharField()
    language = s.CharField()
    tags = s.CharField()


class MessageCreateSerializer(s.Serializer):
    content = s.CharField()


class CreateUserSerializer(s.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "name", "surname", "password", "language")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data["name"],
            surname=validated_data["surname"],
            language=validated_data["language"],
        )
        user.save()
        return user


class UserSerializer(s.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "language")


class LoginUserSerializer(s.Serializer):
    email = s.CharField()
    password = s.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise s.ValidationError("Unable to login with the provided credentials.")
