from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Finding, DB_CWE, DB_OWASP, Customer, Report, Finding_Template, UserProfile


models = [Finding, DB_CWE, DB_OWASP, Customer, Report, Finding_Template, UserProfile]

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(models)
