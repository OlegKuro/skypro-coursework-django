from rest_framework import generics, permissions
from core.serializers import UserRegistrationSerializer


class RegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)
