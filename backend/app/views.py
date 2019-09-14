from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from knox.models import AuthToken
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet

from app.models import Message, User
from app.serializers import (
    MessageCreateSerializer,
    MessageSerializer,
    CreateUserSerializer,
    UserSerializer,
    LoginUserSerializer,
)
from app.utils import create_message, get_messages


class MessagesAPI(ViewSet):
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(request_body=MessageCreateSerializer, responses={200: "OK"})
    def create(self, request):
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_message(**serializer.validated_data)
        return HttpResponse(200)

    def list(self, request):
        if request.user.is_authenticated:
            messages = get_messages(language=request.user.language)
        else:
            messages = []
        serializer = self.serializer_class(messages, many=True)
        return Response(serializer.data)


class RegistrationAPI(ViewSet):
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=CreateUserSerializer, responses={200: "OK"})
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(user, context=self.serializer_class()).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LoginAPI(ViewSet):
    serializer_class = LoginUserSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=LoginUserSerializer, responses={200: "OK"})
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(user, context=self.serializer_class()).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )
