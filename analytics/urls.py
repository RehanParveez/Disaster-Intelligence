from django.urls import path, include
from analytics.views import AnalyticsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'analytics', AnalyticsViewSet, basename = 'analytics')

urlpatterns = [
  path('', include(router.urls))
]
