from django.contrib import admin
from scheduler.models import IncidentList, Cycle, DecisionRecord

# Register your models here.
@admin.register(IncidentList)
class IncidentListAdmin(admin.ModelAdmin):
  list_display = ['incident', 'prior', 'position', 'updated_at']
  
@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
  list_display = ['started_at', 'completed_at', 'total_incids', 'decis_made']
  
@admin.register(DecisionRecord)
class DecisionRecordAdmin(admin.ModelAdmin):
  list_display = ['cycle', 'incident', 'unit', 'responder', 'reason', 'created_at']
