from rest_framework import serializers
from .models import Car
from utils.sanitizeUserInput import sanitize_user_input

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"

class CreateUpdateCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["brand", "motor", "model"]

    def validate(self, data):
        return sanitize_user_input(data)





