from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as CoreValidationError
from django.contrib.auth import password_validation
from django.conf import settings

from core.models import User


class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[password_validation.validate_password])

    class Meta:
        model = User
        fields = (
            'id',
            'old_password',
            'new_password',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        user: User = self.instance
        if not user.check_password(old_password):
            raise ValidationError({'old_password': 'wrong old pass'})
        return attrs

    def update(self, instance: User, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save(update_fields=['password'])
        return instance

class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_null=False, allow_blank=False)
    password = serializers.CharField(allow_null=False, allow_blank=False)

    class Meta:
        model = User
        fields = (
            'password',
            'username',
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password_repeat',
        )
        extra_kwargs = {
            'password': {
                'validators': [password_validation.validate_password],
            },
        }

    def validate(self, attrs):
        if 'password_repeat' not in attrs:
            raise ValidationError({
                'password_repeat': ['This field is mandatory'],
            })
        password = attrs.get('password')
        password_repeat = attrs.pop('password_repeat')
        if password_repeat != password:
            raise ValidationError({
                'password_repeat': ['Passwords do not match'],
                'password': ['Passwords do not match'],
            })
        return super(UserRegistrationSerializer, self).validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user
