from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.jwt_auth import get_refresh_view
from accounts.api.views import (
	RegisterUser,
	RegisterVerify,
	PasswordReset,
	PasswordResetVerify,
	EmailChange,
	EmailChangeVerify,
	PasswordChange,
	UserUpdate,
)


urlpatterns = [
 	path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),

	path('login/', LoginView.as_view(), name='rest_login'),
	path('logout/', LogoutView.as_view(), name='rest_logout'),

	path('register/', RegisterUser.as_view(), name='register'),

	path('register/verify/', RegisterVerify.as_view(), name='register_verify'),

	path('password/reset/', PasswordReset.as_view(), name='password_reset'),
	path('password/reset/verify/', PasswordResetVerify.as_view(), name='password_reset_verify'),

	path('email/change/', EmailChange.as_view(), name='email_change'),
	path('email/change/verify/', EmailChangeVerify.as_view(), name='email_change_verify'),

	path('password/change/', PasswordChange.as_view(), name='password_change'),

	path('user-update/', UserUpdate.as_view(), name='user'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
