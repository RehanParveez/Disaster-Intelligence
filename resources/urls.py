from django.urls import path, include
from resources.views import ResourceViewset, UnitViewset, AvailabilityViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'resource', ResourceViewset, basename = 'resource')
router.register(r'unit', UnitViewset, basename = 'unit')
router.register(r'availability', AvailabilityViewset, basename = 'availability')

urlpatterns = [
  path('', include(router.urls))
]                              