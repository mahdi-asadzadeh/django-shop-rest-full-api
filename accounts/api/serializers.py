from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterUserSerializer(serializers.Serializer):
	email = serializers.EmailField(max_length=60, required=True)
	username = serializers.CharField(max_length=10, required=True)
	password = serializers.CharField(max_length=15, required=True)
	first_name = serializers.CharField(required=False)
	last_name = serializers.CharField(required=False)


class RegisterVerifiedSerializer(serializers.Serializer):
	token = serializers.CharField(max_length=100)
	email = serializers.EmailField(max_length=60)


class ChangeEmailVerifiedSerializer(serializers.Serializer):
	token = serializers.CharField(max_length=100)
	email = serializers.EmailField(max_length=60)


class UserUpdateSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username']
		read_only_fields = [
			'email',
		]


class PasswordResetSerializer(serializers.Serializer):
	email = serializers.EmailField(max_length=60)


class PasswordResetVerifiedSerializer(serializers.Serializer):
	token = serializers.CharField(max_length=100)
	email = serializers.EmailField(max_length=60)
	new_password = serializers.CharField(max_length=128)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)


class EmailChangeSerializer(serializers.Serializer):
	email = serializers.EmailField(max_length=60)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128)
