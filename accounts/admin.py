from django.contrib import admin
from accounts.models import User


@admin.register(User)
class AccountAdmin(admin.ModelAdmin):
	class Meta:
		model = User
