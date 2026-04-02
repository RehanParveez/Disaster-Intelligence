from django.contrib import admin
from resources.models import Resource, Unit, Availability, Inventory, Consumption

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

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
  list_display = ['name', 'location', 'created_at']
  
@admin.register(Consumption)
class ConsumptionAdmin(admin.ModelAdmin):
  list_display = ['unit', 'inventory', 'change_kind', 'prev_avail_units', 'pres_avail_units', 'reason', 'created_by', 'created_at']