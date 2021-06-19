from rest_framework.permissions import BasePermission, SAFE_METHODS


class AccessProvider(BasePermission):
	message = 'permission denied, you are not the provider'

	def has_permission(self, request, view):
		if request.user.is_authenticated and request.user.is_provider:
			return True
		return False


class AsseccAddProductProvider(BasePermission):
	message = 'permission denied, you are not the provider'

	def has_permission(self, request, view):
		if request.user.is_provider and request.user.is_authenticated:
			return True
		return False
		

class IsOwnerOrReadOnly(BasePermission):
	message = 'permission denied, you\'re not the owner'

	def has_permission(self, request, view):
		return request.user.is_authenticated and request.user

	def has_object_permission(self, request, view, obj):
		if request.method in SAFE_METHODS:
			return True
		return obj.user == request.user
