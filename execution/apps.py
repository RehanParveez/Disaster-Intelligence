from django.apps import AppConfig

class ExecutionConfig(AppConfig):
    name = 'execution'
    
    def ready(self):
      import execution.signals
