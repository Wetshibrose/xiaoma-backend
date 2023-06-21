from django.contrib import admin

from .models import Gender


class GendersAdmin(admin.ModelAdmin):
    pass


admin.site.register(Gender, GendersAdmin)
