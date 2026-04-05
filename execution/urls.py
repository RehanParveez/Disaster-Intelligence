from django.urls import path, include
from rest_framework.routers import DefaultRouter
from execution.views import ExecutionViewset

router = DefaultRouter()
router.register(r'execution', ExecutionViewset, basename = 'execution')

urlpatterns = [
  path('', include(router.urls))
]