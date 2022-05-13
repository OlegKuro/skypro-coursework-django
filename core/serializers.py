from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as CoreValidationError
from django.contrib.auth import password_validation
from django.conf import settings

from core.models import User


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
        password_validators = password_validation.get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
        try:
            password_validation.validate_password(
                password=validated_data['password'],
                user=user,
                password_validators=password_validators,
            )
        except CoreValidationError as e:
            raise ValidationError({'password': [error.messages[0] for error in e.error_list]})
        user.set_password(validated_data['password'])
        user.save()

        return user
