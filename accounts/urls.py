from django.urls import path, include
from accounts.views import UserViewset, ProfileViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', UserViewset, basename = 'user')
router.register(r'profile', ProfileViewset, basename = 'profile')

urlpatterns = [
  path('', include(router.urls)),
]
