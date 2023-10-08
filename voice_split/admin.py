from django.contrib import admin
from .models import LowDenoiseResult, HighDenoiseResult


class LowDenoiseResultAdmin(admin.ModelAdmin):
    pass


class HighDenoiseResultAdmin(admin.ModelAdmin):
    pass


admin.site.register(LowDenoiseResult, LowDenoiseResultAdmin)
admin.site.register(HighDenoiseResult, HighDenoiseResultAdmin)
