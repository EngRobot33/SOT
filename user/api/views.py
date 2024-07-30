from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from api.permissions import get_level_permission, IsNotAuthenticated
from user.api.serializers import UserSerializer, MyTokenObtainPairSerializer, EmailSerializer
from user.models import User
from user.tasks import send_email_task


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class EditProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [get_level_permission(1)]

    def get_object(self):
        user = self.request.user
        if user is None:
            return Response('User not found!', status=status.HTTP_404_NOT_FOUND)
        return user


class ManageUsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [get_level_permission(3)]


class VerifyEmailView(APIView):
    permission_classes = [IsNotAuthenticated]

    def get(self, request, uib64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uib64))
        except DjangoUnicodeDecodeError:
            return Response('Unable to decode URL!', status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response('User not found!', status=status.HTTP_404_NOT_FOUND)
        else:
            if not default_token_generator.check_token(user, token):
                return Response('Token is invalid or expired.', status=status.HTTP_400_BAD_REQUEST)
            user.is_email_verified = True
            user.save()
            return Response('Email successfully confirmed', status=status.HTTP_200_OK)


class ResendEmailView(GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('User with such email was not found!', status=status.HTTP_404_NOT_FOUND)
        else:
            if not user.is_email_verified:
                send_email_task.delay(user.pk)
                return Response('Verification email has been sent.', status=status.HTTP_200_OK)
            return Response('Email is already activated!', status=status.HTTP_400_BAD_REQUEST)
