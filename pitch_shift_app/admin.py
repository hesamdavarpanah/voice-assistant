from django.contrib import admin
from .models import PitchShiftResult


class PitchShiftResultAdmin(admin.ModelAdmin):
    pass


admin.site.register(PitchShiftResult, PitchShiftResultAdmin)
