from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()

    def create(self, validated_data):
        # Logic to create a user instance
        pass

    def update(self, instance, validated_data):
        # Logic to update a user instance
        pass