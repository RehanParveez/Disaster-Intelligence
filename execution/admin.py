from django.contrib import admin
from execution.models import Execution, ExecutionRecord, FailureRecord

# Register your models here.
@admin.register(Execution)
class ExecutionAdmin(admin.ModelAdmin):
  list_display = ['incident', 'unit', 'inventory', 'status', 'created_by', 'created_at', 'updated_at']
  
@admin.register(ExecutionRecord)
class ExecutionRecordAdmin(admin.ModelAdmin):
  list_display = ['execution', 'message', 'updated_at']
  
@admin.register(FailureRecord)
class FailureRecordAdmin(admin.ModelAdmin):
  list_display = ['execution', 'reason', 'updated_at']