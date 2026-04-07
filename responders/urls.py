from django.urls import path, include
from responders.views import ResponderViewSet, CapabilityViewSet, LoadViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'responder', ResponderViewSet, basename = 'responder')
router.register(r'capabilities', CapabilityViewSet, basename = 'capabilities')
router.register(r'load', LoadViewSet, basename = 'load')

urlpatterns = [
  path('', include(router.urls))
]
