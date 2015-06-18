# inventory/admin.py
from django.contrib import admin

# from inventory.models import Domain, Environment
from company.models import Status, Company
admin.site.register(Status)
admin.site.register(Company)
