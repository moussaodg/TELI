from django.contrib import admin

from .models import role, Administrator

admin.site.register(role)
admin.site.register(Administrator)