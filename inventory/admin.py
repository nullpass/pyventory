from django.contrib import admin

from . import models
admin.site.register(models.Application)
admin.site.register(models.Server)
admin.site.register(models.Domain)
admin.site.register(models.Company)
admin.site.register(models.Department)
