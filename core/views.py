from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

from core.models import User
from core.serializers import UserRegistrationSerializer, UserLoginSerializer, UserRetrieveUpdateSerializer, \
    UserUpdatePasswordSerializer


class UserRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserRetrieveUpdateSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class RegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        response: Response = super(RegistrationView, self).create(request, *args, **kwargs)
        user = authenticate(request, username=request.data.get('username'), password=request.data.get('password'))
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return Response(response.data, status=status.HTTP_201_CREATED)


class LoginView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, username=serializer.data['username'], password=serializer.data['password'])
        if user is None:
            raise ValidationError({
                'password': ['Password or username do not fit'],
                'username': ['Password or username do not fit'],
            })
        login(request, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdatePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdatePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
