from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.exceptions import EmailNotVerified
from user.models import Permission
from user.tasks import send_email_task

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    permission = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'permission')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        permission = validated_data.pop('permission', None)
        if not permission:
            permission = Permission.objects.get(level=1)
        user = User.objects.create_user(permission=permission, **validated_data)
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['permission_level'] = user.permission.level if user.permission else None
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_email_verified:
            send_email_task.delay(self.user.pk)
            raise EmailNotVerified

        data.update({'user_id': self.user.id, 'username': self.user.username, 'email': self.user.email})
        return data


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
