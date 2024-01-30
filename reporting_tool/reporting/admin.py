from django.contrib import admin

from .models import DB_CWE, DB_OWASP, Customer, Report, Finding


models = [Finding, DB_CWE, DB_OWASP, Customer, Report]

admin.site.register(models)
