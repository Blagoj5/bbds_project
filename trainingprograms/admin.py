from django.contrib import admin
from .models import Programs, Program

class ProgramsAdmin(admin.ModelAdmin):
    list_display = ('athleteName', 'programName', 'programCategory','is_published')
    list_display_links = ('athleteName', 'programName')
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    list_per_page= 25
    search_fields = ('athleteName', 'programName', 'programCategory')

admin.site.register(Programs, ProgramsAdmin)

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('day_title', 'program_id')
    list_display_links = ('day_title', 'program_id')
    list_per_page = 25
    search_fields = ('day_title', 'program_id')



admin.site.register(Program, ProgramAdmin)
