from django.http import HttpResponse, StreamingHttpResponse
from drf_yasg.utils import swagger_auto_schema
from knox.models import AuthToken
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action
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
from backend import settings


class MessagesAPI(ViewSet):
    serializer_class = MessageSerializer
    permission_classes = (AllowAny,)
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    @swagger_auto_schema(request_body=MessageCreateSerializer, responses={200: "OK"})
    def create(self, request):
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_message(**serializer.validated_data)
        response = HttpResponse(200)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    def list(self, request):
        if request.user.is_authenticated:
            messages = get_messages(language=request.user.language)
        else:
            messages = get_messages(language="en")
        serializer = self.serializer_class(messages, many=True)
        response = Response(serializer.data)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    @action(detail=True, methods=["post"])
    def delete(self, request, pk):
        msg = Message.objects.get(id=pk)
        msg.deleted = True
        msg.save()
        response = HttpResponse(200)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    @action(detail=True, methods=["post"])
    def resolve(self, request, pk):
        msg = Message.objects.get(id=pk)
        msg.resolved = True
        msg.save()
        response = HttpResponse(200)
        response['Access-Control-Allow-Origin'] = '*'
        return response


class RegistrationAPI(ViewSet):
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=CreateUserSerializer, responses={200: "OK"})
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = Response(
            {
                "user": UserSerializer(user, context=self.serializer_class()).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )
        response['Access-Control-Allow-Origin'] = '*'
        return response


class LoginAPI(ViewSet):
    serializer_class = LoginUserSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=LoginUserSerializer, responses={200: "OK"})
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        response = Response(
            {
                "user": UserSerializer(user, context=self.serializer_class()).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )
        response['Access-Control-Allow-Origin'] = '*'
        return response


def files(request, file_):
    response = StreamingHttpResponse(open(settings.BASE_DIR + "/files/" + file_, "rb"))
    response["Content-Type"] = ""
    response['Access-Control-Allow-Origin'] = '*'
    return response
