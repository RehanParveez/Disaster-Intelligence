from django.contrib import admin
from incidents.models import Incident, IncidentReport, IncidentGroup, IncidentPriorRecord, AllocationDecision

# Register your models here.
@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
  list_display = ['title', 'location', 'description', 'severity', 'prior', 'group', 'status', 'created_by', 'created_at']
  
@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
  list_display = ['incident', 'reported_by', 'description', 'location', 'created_at']
  
@admin.register(IncidentGroup)
class IncidentGroupAdmin(admin.ModelAdmin):
  list_display = ['location', 'group_size']
  
@admin.register(IncidentPriorRecord)
class IncidentPriorRecordAdmin(admin.ModelAdmin):
  list_display = ['incident', 'prev_prior', 'new_prior', 'reason', 'created_at']

@admin.register(AllocationDecision)
class AllocationDecisionAdmin(admin.ModelAdmin):
  list_display = ['unit', 'incident', 'allocated_by', 'inventory', 'reason', 'created_at']