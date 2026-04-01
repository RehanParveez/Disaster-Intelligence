from django.contrib import admin
from resources.models import Resource, Unit, Availability

# Register your models here.
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
  list_display = ['name', 'description']
  
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
  list_display = ['kind', 'identifier', 'location', 'created_by']

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
  list_display = ['res_kind', 'total_units', 'avail_units', 'location', 'last_updated']
