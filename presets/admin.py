from django.contrib import admin
from .models import Band, Preset

admin.site.register(Band)


@admin.register(Preset)
class PresetAdmin(admin.ModelAdmin):
    list_display = ('song_name', 'band', 'amp_model', 'author', 'created_at')
