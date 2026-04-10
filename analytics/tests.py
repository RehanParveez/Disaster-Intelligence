from accounts.tests import ParentTest
from resources.models import Resource, Unit
from django.utils import timezone
from datetime import timedelta
from incidents.models import AllocationDecision
from analytics.models import ResponseRecord
from django.urls import reverse

class AnalyticsTest(ParentTest):
  def setUp(self):
    super().setUp()
    self.resource = Resource.objects.create(name = 'Ambulance')
    self.unit = Unit.objects.create(kind=self.resource, identifier = 'AMB-01')
    self.incident.created_at = timezone.now() - timedelta(hours=1)
    self.incident.save()
    self.alloc = AllocationDecision.objects.create(incident=self.incident, unit=self.unit, allocated_by=self.admin)
    desired_time = self.incident.created_at + timedelta(minutes=10)
    AllocationDecision.objects.filter(id=self.alloc.id).update(created_at=desired_time)
    self.alloc.refresh_from_db()
  
  def test_analy_gen(self):
    self.incident.status = 'resolved'
    self.incident.save()
    record = ResponseRecord.objects.get(incident=self.incident)
    self.assertEqual(record.disp_time_sec, 600)
    self.assertGreaterEqual(record.total_reso_time, 3600)
    self.assertEqual(record.primary_auth, self.admin)
  
  def test_resp_time(self):
    ResponseRecord.objects.create(incident=self.incident, disp_time_sec=200, total_reso_time=1000,
      primary_auth=self.admin)
    self.auth_user(self.admin)
    url = reverse('analytics-resp-time')
    resp = self.client.get(url)
    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.data['total_incidents_analyzed'], 1)
    self.assertEqual(resp.data['average_dispatch_seconds'], 200)
 
  def test_system_recal(self):
    self.auth_user(self.admin)
    url = reverse('system-recal-all')
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.data['status'], 'success')