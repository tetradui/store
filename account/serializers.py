from rest_framework import serializers
from django.contrib.auth import get_user_model

from .utils import send_activation_code

User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    password_comfirm = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('email','password', 'password_confirm')

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.get('password_confirm')
        if p1 != p2:
            raise serializers.ValidationError('Passwords do not match')
        return attrs
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code(user.email, user.activation_code)
        return user
