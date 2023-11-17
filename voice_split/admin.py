from django.contrib import admin
from .models import DenoiseResult


class DenoiseResultAdmin(admin.ModelAdmin):
    pass


admin.site.register(DenoiseResult, DenoiseResultAdmin)
