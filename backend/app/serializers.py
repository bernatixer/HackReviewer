from rest_framework import serializers as s


class MessageCreateSerializer(s.Serializer):
    title = s.CharField()
    content = s.CharField()
    language = s.CharField()
    tags = s.CharField()
