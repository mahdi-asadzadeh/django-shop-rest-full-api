from datetime import date
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import serializers, status, generics

from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from accounts.utils import get_from_redis, token_delete_to_redis
from accounts.tasks import task_send_register_email, task_send_change_email, task_send_reset_password_email
from .serializers import (
	UserUpdateSerializer,
	RegisterUserSerializer,
	PasswordResetSerializer,
	PasswordResetVerifiedSerializer,
	PasswordChangeSerializer,
	EmailChangeSerializer,
	LoginSerializer,
	RegisterVerifiedSerializer,
	ChangeEmailVerifiedSerializer
	)


User = get_user_model()


class RegisterUser(generics.GenericAPIView):
	permission_classes = [AllowAny, ]
	serializer_class = RegisterUserSerializer

	def post(self, request, format=None):
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			email = serializer.data.get('email')
			username = serializer.data.get('username')
			password = serializer.data.get('password')
			first_name = serializer.data.get('first_name')
			last_name = serializer.data.get('last_name')
			user=None
			try: 
				user_exists = User.objects.get(email=email)
				if user_exists.is_active:
					content = {'error': 'Duplicate user.'}
					return Response(content, status=status.HTTP_400_BAD_REQUEST)
				else:
					user = user_exists

			except User.DoesNotExist:
				user = User.objects.create_user(
					username=username, 
					email=email, 
					password=password, 
					is_active=False,
					first_name=first_name,
					last_name=last_name
					)

			task_send_register_email.delay(
				id=user.id , 
				email=user.email, 
				username=user.username, 
				first_name=user.first_name, 
				last_name=user.last_name)
			content = {'success': 'create user.'}
			return Response(content, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterVerify(generics.GenericAPIView):
	permission_classes = [AllowAny, ]
	serializer_class = RegisterVerifiedSerializer

	def post(self, request):
		serilizer = self.serializer_class(data=request.data)
		if serilizer.is_valid():
			token = serilizer.data.get('token')
			email = serilizer.data.get('email')
			try:
				user = User.objects.get(email=email)
			except User.DoesNotExist:
				content = {'error': 'Wrong/Expired Token!.'}
				return Response(content, status=status.HTTP_400_BAD_REQUEST)
				
			token_from_redis = get_from_redis(user.id, 'register')
			if not token_from_redis:
				content = {'error': 'Wrong/Expired Token!.'}
				return Response(content, status=status.HTTP_400_BAD_REQUEST)

			if token != token_from_redis.decode('UTF-8'):
				content = {'error': 'Wrong/Expired Token!.'}
				return Response(content, status=status.HTTP_400_BAD_REQUEST)

			user.is_active = True
			user.save()
			token_delete_to_redis(user.id, 'register')
			content = {'success': 'active account.'}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdate(generics.GenericAPIView):
	permission_classes = [IsAuthenticated, ]
	serializer_class = UserUpdateSerializer

	def get_queryset(self, request):
		serializer = self.serializer_class(request.user)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def put(self, request):
		serializer = self.serializer_class(data=request.data, instance=request.user, partial=True)
		if serializer.is_valid():
			serializer.save()
			content = {'success': 'update account.'}
			return Response(content, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordReset(generics.GenericAPIView):
	permission_classes = [AllowAny, ]
	serializer_class = PasswordResetSerializer

	def post(self, request):
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			email = serializer.data['email']

			try:
				user = User.objects.get(email=email)
				task_send_reset_password_email.delay(
					id=user.id , 
					email=user.email, 
					username=user.username, 
					first_name=user.first_name, 
					last_name=user.last_name
				)
				content = {'success': 'send email.'}
				return Response(content, status=status.HTTP_200_OK)

			except User.DoesNotExist:
				content = {'error': 'Email dose not exists..'}
				return Response(content, status=status.HTTP_400_BAD_REQUEST)
			
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerify(generics.GenericAPIView):
	permission_classes = [AllowAny, ]
	serializer_class = PasswordResetVerifiedSerializer

	def post(self, request):
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			token = serializer.data['token']
			email = serializer.data['email']
			new_password = serializer.data['new_password']

			try:
				user = User.objects.get(email=email)
				token_from_redis = get_from_redis(user.id, 'reset_password')
				if token_from_redis == None:
					content = {'error': 'Wrong/Expired Token!.'}
					return Response(content, status=status.HTTP_400_BAD_REQUEST)

				if token != token_from_redis.decode('UTF-8'):
					content = {'error': 'Wrong/Expired Token!.'}
					return Response(content, status=status.HTTP_400_BAD_REQUEST)

				user.set_password(new_password)
				user.save()
				token_delete_to_redis(user.id, 'reset_password')
				content = {'success': 'verify password.'}
				return Response(content, status=status.HTTP_200_OK)
	
			except User.DoesNotExist:
				content = {'error': 'Wrong/Expired Token!.'}
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailChange(generics.GenericAPIView):
	permission_classes = [IsAuthenticated, ]
	serializer_class = EmailChangeSerializer

	def post(self, request):
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			user = request.user
			email = serializer.data['email']
			try:
				User.objects.get(email=email)
				content = {'error': 'Email address already taken.'}
				return Response(content, status=status.HTTP_400_BAD_REQUEST)

			except User.DoesNotExist:
				user.email = email
				user.is_active = False
				user.save()
				task_send_change_email.delay(      
					id=user.id , 
					email=user.email, 
					username=user.username, 
					first_name=user.first_name, 
					last_name=user.last_name
					)
				content = {'success': 'send email.'}
				return Response(content, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailChangeVerify(generics.GenericAPIView):
	permission_classes = [AllowAny, ]
	serializer_class = ChangeEmailVerifiedSerializer

	def post(self, request):
		serilizer = self.serializer_class(data=request.data)
		if serilizer.is_valid():
			token = serilizer.data.get('token')
			email = serilizer.data.get('email')
			try:
				user = User.objects.get(email=email)
				token_from_redis = get_from_redis(user.id, 'change_email')

				if not token_from_redis:
					content = {'error': 'Wrong/Expired Token!'}
					return Response(content, status=status.HTTP_400_BAD_REQUEST)

				if token != token_from_redis.decode('UTF-8'):
					content = {'error': 'Wrong/Expired Token!'}
					return Response(content, status=status.HTTP_400_BAD_REQUEST)

				user.is_active = True
				user.save()
				token_delete_to_redis(user.id, 'change_email')
				content = {'success': 'verify email.'}
				return Response(content, status=status.HTTP_200_OK)

			except User.DoesNotExist:
				content = {'error': 'Wrong/Expired Token!'}
				return Response(content, status=status.HTTP_400_BAD_REQUEST)
		return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChange(generics.GenericAPIView):
	permission_classes = [IsAuthenticated, ]
	serializer_class = PasswordChangeSerializer

	def post(self, request):
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			new_password = serializer.data['new_password']
			old_password = serializer.data['old_password']
			
			if request.user.check_password(old_password):
				request.user.set_password(new_password)
				request.user.save()
				return Response(serializer.data, status=status.HTTP_200_OK)

			content = {'detail': 'your old password is not valid'}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class Login(APIView):
#     permission_classes = [AllowAny, ]
#     serializer_class = LoginSerializer
#
#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=request.data)
#
#         if serializer.is_valid():
#             email = serializer.data['email']
#             password = serializer.data['password']
#             user = authenticate(email=email, password=password)
#
#             if user:
#                 if user.is_active:
#                     token, created = Token.objects.get_or_create(user=user)
#                     return Response({'token': token.key}, status=status.HTTP_200_OK)
#                 else:
#                     content = {'detail': 'User account not active.'}
#                     return Response(content, status=status.HTTP_401_UNAUTHORIZED)
#             else:
#                 content = {'detail': 'Unable to login with provided credentials.'}
#                 return Response(content, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class Logout(APIView):
#     permission_classes = [IsAuthenticated, ]
#
#     def get(self, request, format=None):
#         """
#         Remove all auth tokens owned by request.user.
#         """
#         tokens = Token.objects.filter(user=request.user)
#         for token in tokens:
#             token.delete()
#         content = {'success': 'User logged out.'}
#         return Response(content, status=status.HTTP_200_OK)
