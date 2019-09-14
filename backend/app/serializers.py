from rest_framework import serializers as s


class MessageSerializer(s.Serializer):
    content = s.CharField()
    language = s.CharField()
    tags = s.CharField()


class MessageCreateSerializer(s.Serializer):
    content = s.CharField()
