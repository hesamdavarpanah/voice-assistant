from django.contrib import admin
from .models import VoiceDetail, VoiceResult


class VoiceDetailAdmin(admin.ModelAdmin):
    pass


class VoiceResultAdmin(admin.ModelAdmin):
    pass


admin.site.register(VoiceDetail, VoiceDetailAdmin)
admin.site.register(VoiceResult, VoiceResultAdmin)
