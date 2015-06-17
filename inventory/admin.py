# inventory/admin.py
from django.contrib import admin

from inventory.models import Domain, Environment
admin.site.register(Domain)
admin.site.register(Environment)
