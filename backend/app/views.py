from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet

from app.serializers import MessageCreateSerializer
from app.utils import create_message


class MessagesAPI(ViewSet):
    serializer_class = MessageCreateSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_message(**serializer.validated_data)
        return HttpResponse(200)
