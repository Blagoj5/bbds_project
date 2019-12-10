from django.contrib import admin
from .models import Programs, Program

class ProgramsAdmin(admin.ModelAdmin):
    list_display = ('athleteName', 'programName', 'programCategory', 'is_published')
    list_display_links = ('athleteName', 'programName')
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    list_per_page= 25
    search_fields = ('athleteName', 'programName', 'programCategory')

admin.site.register(Programs, ProgramsAdmin)

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('program_id', 'day_title', 'for_day')
    list_display_links = ('day_title', 'for_day', 'program_id')
    list_per_page = 25
    search_fields = ('for_day', 'day_title', 'program_id__athleteName')


admin.site.register(Program, ProgramAdmin)