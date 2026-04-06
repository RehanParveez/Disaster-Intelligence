from django.urls import path, include
from notifications.views import NotificationViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'notification', NotificationViewset, basename = 'notification')

urlpatterns = [
  path('', include(router.urls))
]
