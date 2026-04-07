from django.contrib import admin
from analytics.models import ResponseRecord, ResourceEfficiency, ResponderPerformance

# Register your models here.
@admin.register(ResponseRecord)
class ResponseRecordAdmin(admin.ModelAdmin):
  list_display = ['incident', 'disp_time_sec', 'total_reso_time', 'primary_auth', 'created_at', 'updated_at']
  
@admin.register(ResourceEfficiency)
class ResourceEfficiencyAdmin(admin.ModelAdmin):
  list_display = ['reso_kind', 'unit', 'alloca_count', 'failure_count', 'active_hours', 'created_at', 'updated_at']

@admin.register(ResponderPerformance)
class ResponderPerformanceAdmin(admin.ModelAdmin):
  list_display = ['responder', 'incid_handl', 'avg_peak_load', 'succ_exec', 'created_at', 'updated_at']
