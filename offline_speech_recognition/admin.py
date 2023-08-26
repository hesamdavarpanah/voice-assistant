from django.contrib import admin
from .models import Voice, VoiceDetail, VoiceResult


class VoiceAdmin(admin.ModelAdmin):
    pass


class VoiceDetailAdmin(admin.ModelAdmin):
    pass


class VoiceResultAdmin(admin.ModelAdmin):
    pass


admin.site.register(Voice, VoiceAdmin)
admin.site.register(VoiceDetail, VoiceDetailAdmin)
admin.site.register(VoiceResult, VoiceResultAdmin)
