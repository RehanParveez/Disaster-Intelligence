from django.urls import path, include
from incidents.views import IncidentViewset, IncidentReportViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'incident', IncidentViewset, basename = 'incident')
router.register(r'incidentreport', IncidentReportViewset, basename = 'incidentreport')

urlpatterns = [
  path('', include(router.urls)),
]

