# services\posts\infrastructure\serializers.py

from rest_framework import serializers


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
