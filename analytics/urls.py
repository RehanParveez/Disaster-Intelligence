from django.urls import path, include
from analytics.views import AnalyticsViewSet, SystemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'analytics', AnalyticsViewSet, basename = 'analytics')
router.register(r'system', SystemViewSet, basename = 'system')

urlpatterns = [
  path('', include(router.urls))
]
