from django.urls import path, include
from events.views import EventViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'event', EventViewset, basename = 'event')

urlpatterns = [
  path('', include(router.urls))
]
