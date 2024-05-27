from django.contrib import admin
from .models import Registration


@admin.register(Registration)
class Registration(admin.ModelAdmin):
    list_display = ('name','section', 'email', 'phone_number')
    list_filter = ('section', 'email', 'year', 'branch')
    search_fields = ('section', 'email', 'year', 'branch')

    