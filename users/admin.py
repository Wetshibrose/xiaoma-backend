from django.contrib import admin

from .models import CustomUser, Gender, Country


class CustomUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(CustomUser, CustomUserAdmin)
