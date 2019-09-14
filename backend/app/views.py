from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet

from app.models import Message
from app.serializers import MessageCreateSerializer
from app.utils import create_message


class MessagesAPI(ViewSet):
    serializer_class = MessageCreateSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=MessageCreateSerializer,
        responses={
            200: "OK"
        },
    )
    def create(self, request):
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_message(**serializer.validated_data)
        return HttpResponse(200)

    def list(self, request):
        messages = Message.objects.all()
        serializer = self.serializer_class(messages, many=True)
        return Response(serializer.data)
