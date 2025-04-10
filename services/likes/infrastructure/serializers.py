from rest_framework import serializers
from services.likes.domain.models import Like

class LikeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    post_id = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Like(**validated_data)

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.post_id = validated_data.get('post_id', instance.post_id)
        return instance