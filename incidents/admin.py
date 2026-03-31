from django.contrib import admin
from incidents.models import Incident, IncidentReport

# Register your models here.
@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
  list_display = ['title', 'location', 'description', 'severity', 'status', 'created_by', 'created_at']
  
@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
  list_display = ['incident', 'reported_by', 'description', 'location', 'created_at']
