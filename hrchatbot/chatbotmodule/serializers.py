from rest_framework import serializers

class ChatbotSerializer(serializers.Serializer):
    personId=serializers.CharField(max_length=150)
    query=serializers.CharField(max_length=1000)
    status=serializers.CharField()