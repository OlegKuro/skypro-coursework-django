from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import ValidationError

from core.models import User


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
        user.set_password(validated_data['password'])
        user.save()

        return user
