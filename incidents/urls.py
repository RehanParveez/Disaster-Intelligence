from django.urls import path, include
from incidents.views import IncidentViewset, IncidentReportViewset, IncidentGroupViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'incident', IncidentViewset, basename = 'incident')
router.register(r'incidentreport', IncidentReportViewset, basename = 'incidentreport')
router.register(r'incidentgroup', IncidentGroupViewset, basename = 'incidentgroup')

urlpatterns = [
  path('', include(router.urls))
]

