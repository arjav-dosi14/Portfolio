from django.contrib import admin
from .models import ContactMessage, Experience, Education

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company_name', 'start_date', 'end_date', 'display_order', 'is_current')
    list_editable = ('display_order',)
    search_fields = ('job_title', 'company_name')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution_name', 'start_year', 'end_year', 'display_order')
    list_editable = ('display_order',)
    search_fields = ('degree', 'institution_name')
