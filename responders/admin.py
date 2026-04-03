from django.contrib import admin
from responders.models import Responder, Capability, Shift, Load

# Register your models here.
@admin.register(Responder)
class ResponderAdmin(admin.ModelAdmin):
  list_display = ['user', 'max_load']

@admin.register(Capability)
class CapabilityAdmin(admin.ModelAdmin):
  list_display = ['name', 'description']
  
@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
  list_display = ['responder', 'start_time', 'end_time']
  
@admin.register(Load)
class LoadAdmin(admin.ModelAdmin):
  list_display = ['responder', 'incident', 'load_count']