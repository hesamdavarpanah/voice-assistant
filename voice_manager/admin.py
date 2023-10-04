from django.contrib import admin
from .models import Voice


class VoiceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Voice, VoiceAdmin)
